""""
Marketflow Analysis Script
This script runs a market analysis for a given ticker symbol using the MarketflowFacade.
It generates reports and saves them in the specified output directory.

Use:
    python /scripts/marketflow_analysis.py AAPL
    python /scripts/marketflow_analysis.py X:BTCUSD

    python /scripts/marketflow_analysis.py AAPL --timeframes 1d 1h 15m

"""
import argparse
import os
from pathlib import Path
import json
from datetime import datetime
from enum import Enum
from marketflow.marketflow_facade import MarketflowFacade
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_report import MarketflowReport
from marketflow.marketflow_llm_interface import MarketflowLLMInterface
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_utils import sanitize_filename
from marketflow.marketflow_utils import save_timeframe_data
from marketflow.transient_vector_memory import TransientVectorMemory
from rag.embedder import embed_text

# Ensure the logger is set up correctly
logger = get_logger("marketflow_analysis_1")
config_manager = create_app_config(logger=logger)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Enum types and other non-serializable objects."""
    
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def safe_json_dump(data: dict, file_path: str) -> bool:
    """Safely dump data to JSON file with custom encoder."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, cls=CustomJSONEncoder, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        try:
            simplified_data = {
                "error": "Original data could not be serialized",
                "error_message": str(e),
                "ticker": data.get("ticker", "unknown") if isinstance(data, dict) else "unknown",
                "timestamp": datetime.now().isoformat()
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(simplified_data, f, indent=4)
            logger.warning(f"Saved simplified error data to {file_path}")
            return False
        except Exception as fallback_error:
            logger.error(f"Failed to save even simplified data: {fallback_error}")
            return False
        
def embed_fn(text: str):
    return embed_text(text)  # 1536-dim for text-embedding-3-small

def build_narrative(output_dir: str, ticker: str, extractor=None) -> str:
    # 1) Try the summary TXT
    p_txt = Path(output_dir) / f"{sanitize_filename(ticker)}_summary.txt"
    if p_txt.exists():
        txt = p_txt.read_text(encoding="utf-8").strip()
        if isinstance(txt, str) and txt and txt.lower() not in ("true", "false", "null"):
            return txt

    # 2) Try LLM analysis JSON
    p_llm = Path(output_dir) / f"{sanitize_filename(ticker)}_llm_analysis.json"
    if p_llm.exists():
        try:
            data = json.loads(p_llm.read_text(encoding="utf-8"))
            # common keys you might have saved
            for key in ("narrative", "summary", "analysis_text", "final_text"):
                val = data.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
        except Exception:
            pass

    # 3) Try extractor (string or dict)
    if extractor is not None:
        try:
            s = extractor.get_summary_for_ticker(ticker)
            if isinstance(s, str) and s.strip():
                return s.strip()
            if isinstance(s, dict):
                parts = []
                for k in ("instrument", "timeframe", "date_range", "notes"):
                    v = s.get(k)
                    if isinstance(v, str) and v.strip():
                        parts.append(v.strip())
                # include events/signals if present
                for k in ("wyckoff_events", "signals", "highlights"):
                    v = s.get(k)
                    if isinstance(v, list) and v:
                        parts.append(" | ".join(map(str, v[:10])))
                if parts:
                    return " — ".join(parts)
        except Exception:
            pass

    # 4) Last-resort fallback to something at least textual
    return f"{ticker}: Analysis completed. See JSON/CSV reports for details."

def _compose_richer_narrative(
    ticker: str,
    llm_analysis: dict,
    extractor: MarketflowResultExtractor | None,
    results: dict | None
) -> str:
    """Build a richer narrative using extractor methods with safe fallbacks."""
    parts: list[str] = [f"{ticker} analysis"]

    if extractor:
        # Price
        try:
            cp = extractor.get_current_price(ticker)
            if isinstance(cp, (int, float)) and cp > 0:
                parts.append(f"price {cp}")
        except Exception:
            pass

        # Signal
        try:
            sig = extractor.get_signal(ticker) or {}
            stype = sig.get("type") or sig.get("signal_type")
            sstrength = sig.get("strength") or sig.get("score")
            if stype or sstrength:
                parts.append(f"signal={stype or 'NA'} strength={sstrength or 'NA'}")
        except Exception:
            pass

        # Risk assessment
        try:
            ra = extractor.get_risk_assessment(ticker) or {}
            sl = ra.get("stop_loss"); tp = ra.get("take_profit"); rr = ra.get("risk_reward_ratio")
            if any(v is not None for v in (sl, tp, rr)):
                parts.append(
                    "risk:"
                    f" SL={sl if sl is not None else 'NA'}"
                    f" TP={tp if tp is not None else 'NA'}"
                    f" RR={rr if rr is not None else 'NA'}"
                )
        except Exception:
            pass

        # Timeframes summary: trend, S/R, Wyckoff events
        tf_summary = []
        try:
            tfs = extractor.get_timeframes(ticker) or []
            preferred = ["1d", "4h", "1h", "15m"]
            ordered = [tf for tf in preferred if tf in tfs] + [tf for tf in tfs if tf not in preferred]
            for tf in ordered[:4]:
                # Trend
                trend_dir = slope = conf = None
                try:
                    trend = extractor.get_trend_analysis(ticker, tf) or {}
                    trend_dir = trend.get("trend_direction") or trend.get("direction") or trend.get("trend")
                    slope = trend.get("slope")
                    conf = trend.get("confidence") or trend.get("score")
                except Exception:
                    pass

                # Support/Resistance nearest
                s_lvl = r_lvl = None
                try:
                    sr = extractor.get_support_resistance(ticker, tf) or {}
                    s_levels = sr.get("support") or []
                    r_levels = sr.get("resistance") or []
                    if s_levels:
                        s0 = s_levels[0]
                        s_lvl = (s0.get("price") or s0.get("level") or s0.get("value")) if isinstance(s0, dict) else s0
                    if r_levels:
                        r0 = r_levels[0]
                        r_lvl = (r0.get("price") or r0.get("level") or r0.get("value")) if isinstance(r0, dict) else r0
                except Exception:
                    pass

                # Wyckoff events (top 2)
                wy_tags = []
                try:
                    wy = extractor.get_wyckoff_events(ticker, tf)
                    if isinstance(wy, list) and wy:
                        wy_tags = [e.get("label") if isinstance(e, dict) else str(e) for e in wy[:2]]
                except Exception:
                    pass

                seg = f"{tf}:trend={trend_dir or 'NA'}"
                if slope is not None:
                    seg += f" slope={slope}"
                if conf is not None:
                    seg += f" conf={conf}"
                if (s_lvl is not None) or (r_lvl is not None):
                    seg += f" S={s_lvl if s_lvl is not None else 'NA'} R={r_lvl if r_lvl is not None else 'NA'}"
                if wy_tags:
                    seg += f" wy={','.join(wy_tags)}"
                tf_summary.append(seg)
        except Exception:
            pass
        if tf_summary:
            parts.append(" | ".join(tf_summary))

        # Pattern highlights (from the most relevant TF if available)
        try:
            first_tf = ordered[0] if 'ordered' in locals() and ordered else None
            if first_tf:
                patt = extractor.get_pattern_analysis(ticker, first_tf) or {}
                active = patt.get("active") or patt.get("detected") or []
                if isinstance(active, list) and active:
                    names = []
                    for x in active[:5]:
                        if isinstance(x, dict):
                            names.append(str(x.get("name") or x.get("type") or x))
                        else:
                            names.append(str(x))
                    if names:
                        parts.append("patterns=" + ",".join(names))
        except Exception:
            pass

    # Fallback: enrich with LLM analysis if still too short
    if llm_analysis and len(" ".join(parts).split()) < 20:
        try:
            sig = llm_analysis.get("vpa_signal", {}) or {}
            stype = sig.get("type"); sstrength = sig.get("strength")
            if stype or sstrength:
                parts.append(f"llm_signal={stype or 'NA'} {sstrength or ''}".strip())
            tf = llm_analysis.get("timeframe_data", {}) or {}
            d1 = tf.get("1d", {}) or {}
            trend = (d1.get("trend") or {}).get("trend_direction")
            if trend:
                parts.append(f"llm_1d_trend={trend}")
        except Exception:
            pass

    # Timestamp and dedup
    parts.append(f"ts={datetime.now().strftime('%Y-%m-%d %H:%M')}")
    seen, ordered_parts = set(), []
    for p in parts:
        if p and p not in seen:
            ordered_parts.append(p); seen.add(p)
    return " | ".join(ordered_parts)

def run_analysis(ticker, output_dir="data", timeframes=None):
    """Run market analysis for a given ticker symbol.

    Args:
        ticker (str): Ticker symbol (e.g., AAPL or X:BTCUSD)
        output_dir (str): Directory to save the reports.
        timeframes (list, optional): List of timeframes to analyze. If None, uses default timeframes.
    """

    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Running analysis for {ticker} on {current_date}")

    facade = MarketflowFacade()
    logger.info(f"Running analysis for ticker: {ticker}")
    # Allow passing specific timeframes if needed (else use default in facade)
    if timeframes:
        results = facade.analyze_ticker(ticker, timeframes=timeframes)
        logger.info(f"Using custom timeframes: {timeframes}")
    else:
        results = facade.analyze_ticker(ticker)
        logger.info("Using default timeframes for analysis.")

    if isinstance(results, dict) and 'timeframe_analyses' in results:
        timeframe_data_to_save = results.get('timeframe_analyses', {})
        if timeframe_data_to_save:
            logger.info(f"Calling save_timeframe_data for {ticker}...")
            save_timeframe_data(ticker, timeframe_data_to_save)
            logger.info(f"Timeframe data save process for {ticker} completed.")
        else:
            logger.warning(f"Timeframe analysis data for {ticker} is empty. Skipping save.")
    else:
        logger.warning(f"Unexpected results format for {ticker} or 'timeframe_analyses' key missing.")

    extractor = MarketflowResultExtractor({ticker: results})
    logger.info("Extracting data from results...")
    config = create_app_config()
    report_root = config.REPORT_DIR
    output_dir = f"{report_root}/{current_date}/{sanitize_filename(ticker)}"
    logger.info(f"Report directory: {output_dir}")
    report = MarketflowReport(extractor, output_dir=output_dir)
    logger.info("Creating report...")
    success = report.generate_all_reports_for_ticker(ticker)
    if success:
        logger.info(f"Summary report created successfully in {report_root}")
    else:
        logger.error("Report creation failed.")
    logger.info("MarketflowFacade real data test completed successfully.")

    print(f"✅ Reports for {ticker} saved in {output_dir}")

    # Create a LLM interface for further analysis
    try:
        llm_interface = MarketflowLLMInterface()
        # Reuse the already computed 'results' to avoid a second analysis/data fetch.
        llm_interface_analysis = llm_interface.get_ticker_analysis(
            ticker,
            analysis=results,
            timeframes=timeframes
        )
        if llm_interface_analysis:
            logger.info(f"LLM analysis for {ticker} retrieved successfully.")
        else:
            logger.error(f"Failed to retrieve LLM analysis for {ticker}.")
            llm_interface_analysis = {
                "error": "No LLM analysis data returned",
                "ticker": ticker,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error creating LLM interface or getting analysis: {e}")
        llm_interface_analysis = {
            "error": f"LLM interface error: {str(e)}",
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }

    logger.info("Creating LLM interface for further analysis...")

    # Save the LLM analysis to a file with safe serialization
    llm_analysis_file = os.path.join(output_dir, f"{sanitize_filename(ticker)}_llm_analysis.json")
    
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    success = safe_json_dump(llm_interface_analysis, llm_analysis_file)
    if success:
        logger.info(f"LLM analysis saved successfully to {llm_analysis_file}")
    else:
        logger.error(f"Failed to save LLM analysis to {llm_analysis_file}")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    namespace = f"session:joao:{run_id}:{sanitize_filename(ticker)}"
    logger.info(f"Creating TVM namespace for {ticker}: {namespace}")

    ns_file = os.path.join(output_dir, ".tvm_namespace")
    with open(ns_file, "w", encoding="utf-8") as f:
        f.write(namespace)


    # Build a concise narrative from extractor or report content
    narrative = build_narrative(output_dir, ticker, extractor)
    logger.info(f"Building narrative for {ticker}...")
    # sanity check (avoid tiny/boolean-like content)
    if not isinstance(narrative, str) or len(narrative.split()) < 15:
        logger.warning("Narrative too short/invalid; constructing richer fallback.")
        narrative = _compose_richer_narrative(ticker, llm_interface_analysis, extractor, results)
        logger.info(f"Richer narrative for {ticker}: {narrative}")

    if len(narrative.split()) < 8:
        narrative = f"{ticker}: Analysis summary unavailable; minimal fallback narrative."

    # init TVM (dim must match your embedding model)
    tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536, ttl_seconds=24*3600)

    if not tvm:
        logger.error(f"Failed to create TVM for {ticker}.")
    tvm.upsert_text(
        namespace=namespace,
        report_id=f"{sanitize_filename(ticker)}_{run_id}",
        text=narrative,
        meta={"source": "marketflow_facade", "ticker": ticker}
    )

    tvm_dir = os.path.join(output_dir, ".tvm_store")
    tvm.save_namespace(namespace, tvm_dir)

    logger.info(f"Upserted narrative for {ticker} into TVM under namespace {namespace}")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Marketflow analysis for a ticker.")
    parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL or X:BTCUSD)")
    # Use a portable default; the actual report path will be resolved via config inside run_analysis
    parser.add_argument("--output", type=str, default=".marketflow/reports", help="Base output directory for reports (optional)")
    parser.add_argument("--timeframes", type=str, nargs="*", default=None,
                        help="List of timeframes (e.g., 1d 4h 1h). If not provided, uses default timeframes.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    run_analysis(args.ticker, output_dir=args.output, timeframes=args.timeframes)
