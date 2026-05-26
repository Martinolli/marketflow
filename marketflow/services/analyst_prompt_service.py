"""Prompt builders for future Wyckoff Volume Analyst workflows."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any


PROMPT_STYLES = ("balanced", "strict", "educational")


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _get(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != []


def _fmt(value: Any) -> str:
    if value is None or value == "":
        return "not available"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _fmt_pct(value: Any) -> str:
    if value is None or value == "":
        return "not available"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _line(label: str, value: Any) -> str:
    return f"- {label}: {_fmt(value)}"


def _section(title: str, lines: list[str]) -> str:
    clean_lines = [line for line in lines if line]
    if not clean_lines:
        clean_lines = ["- No data available."]
    return f"## {title}\n\n" + "\n".join(clean_lines)


def _event_lines(events: Any, limit: int = 8) -> list[str]:
    rows: list[str] = []
    for event in _as_list(events)[-limit:]:
        if isinstance(event, dict):
            parts = [
                _fmt(event.get("timestamp")),
                _fmt(event.get("event") or event.get("event_name")),
                _fmt(event.get("price")),
            ]
            rows.append(f"- {' | '.join(part for part in parts if part != 'not available')}")
        elif _present(event):
            rows.append(f"- {_fmt(event)}")
    return rows or ["- No recent events available."]


def _level_lines(levels: Any, limit: int = 6) -> list[str]:
    rows: list[str] = []
    for level in _as_list(levels)[:limit]:
        if isinstance(level, dict):
            rows.append(
                "- "
                + ", ".join(
                    [
                        f"timeframe={_fmt(level.get('timeframe'))}",
                        f"label={_fmt(level.get('label'))}",
                        f"price={_fmt(level.get('price'))}",
                        f"delta_pct={_fmt(level.get('delta_pct'))}",
                    ]
                )
            )
        elif _present(level):
            rows.append(f"- {_fmt(level)}")
    return rows or ["- No levels available."]


def _style_instruction(style: str) -> str:
    if style == "strict":
        return (
            "Use a strict risk-first posture. Emphasize contradictions, weak confirmation, "
            "missing data, failed gates, and clear no-go conditions."
        )
    if style == "educational":
        return (
            "Use an educational style. Explain the reasoning step by step so the reader can "
            "learn how Wyckoff, VPA, Monte Carlo, P&F, and risk constraints interact."
        )
    return "Use a balanced, practical analyst style with clear evidence and caveats."


def _safe_filename_part(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip() or fallback
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text.strip("._") or fallback


def build_prompt_filename(
    packet: dict[str, Any],
    style: str | None = None,
    include_timestamp: bool = False,
) -> str:
    """
    Return a safe markdown filename for a Wyckoff Analyst prompt.
    """
    packet = _as_dict(packet)
    summary = _as_dict(packet.get("packet_summary"))
    candidate = _as_dict(packet.get("strategy_candidate"))
    ticker = _safe_filename_part(summary.get("ticker") or packet.get("ticker") or candidate.get("ticker"), "marketflow")
    timeframe = _safe_filename_part(summary.get("selected_timeframe") or candidate.get("tf"), "selected")
    parts = [ticker, timeframe]
    if style:
        parts.append(_safe_filename_part(style, "prompt"))
    parts.append("wyckoff_analyst_prompt")
    filename = "_".join(parts)
    if include_timestamp:
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return f"{filename}.md"


def build_wyckoff_analyst_prompt(
    packet: dict[str, Any],
    style: str = "balanced",
    include_raw_json: bool = False,
) -> str:
    """
    Build a prompt for a future Wyckoff Volume Analyst from an Analyst Packet.

    This function does not call any LLM/API. It only returns text.
    """
    packet = _as_dict(packet)
    style = style if style in PROMPT_STYLES else "balanced"

    summary = _as_dict(packet.get("packet_summary"))
    profile = _as_dict(packet.get("profile"))
    market = _as_dict(packet.get("market_snapshot"))
    candidate = _as_dict(packet.get("strategy_candidate"))
    trade_plan = _as_dict(packet.get("strategy_trade_plan"))
    monte_carlo = _as_dict(packet.get("monte_carlo"))
    pnf = _as_dict(packet.get("pnf"))
    pnf_selection = _as_dict(pnf.get("selection"))
    pnf_sidecar = _as_dict(pnf.get("selected_sidecar"))
    pnf_interpretation = _as_dict(pnf.get("objective_interpretation"))
    eigen = _as_dict(packet.get("eigen"))
    eigen_latest = _as_dict(eigen.get("latest"))
    eigen_summary = _as_dict(eigen.get("summary"))
    wyckoff = _as_dict(packet.get("wyckoff_vpa"))
    selected_tf_context = _as_dict(packet.get("selected_timeframe_context") or wyckoff.get("selected_timeframe_context"))
    levels = _as_dict(packet.get("levels"))
    go_no_go = _as_dict(packet.get("go_no_go"))
    missing_data = _as_list(packet.get("missing_data"))
    warnings = _as_list(packet.get("warnings"))

    sections = [
        "# Wyckoff Volume Analyst Request",
        _section(
            "Role",
            [
                "- You are a Wyckoff Volume Analyst.",
                "- Analyze the provided market packet using Wyckoff phase/event logic, volume-price analysis, support/resistance context, strategy candidate quality, Monte Carlo probabilities, P&F objective context, Eigen diagnostic context, and risk management constraints.",
                "- If P&F objective quality is supportive_extended, treat it as a longer-range objective requiring realism/timeframe review.",
                "- Treat Eigen diagnostics as context only; do not treat them as trade signals.",
                "- Do not provide financial advice. Provide an analytical review only.",
                f"- Style directive: {_style_instruction(style)}",
            ],
        ),
        _section(
            "User Profile / Constraints",
            [
                _line("Account size", profile.get("account_size")),
                _line("Risk per trade percent", profile.get("risk_per_trade_pct")),
                _line("Risk per trade amount", profile.get("risk_per_trade_amount")),
                _line("Max total open risk", profile.get("max_total_open_risk")),
                _line("Long only", profile.get("long_only")),
                _line("Minimum POP threshold", profile.get("main_pop_threshold")),
                _line("Minimum P&F objective R", profile.get("min_pnf_objective_r")),
                _line("Minimum composite score", profile.get("min_composite_score")),
                _line("Broker", profile.get("broker")),
            ],
        ),
        _section(
            "Market Snapshot",
            [
                _line("Ticker", summary.get("ticker") or packet.get("ticker")),
                _line("Selected timeframe", summary.get("selected_timeframe")),
                _line("Current price", summary.get("current_price") or market.get("current_price")),
                _line("Signal type", market.get("signal_type")),
                _line("Signal strength", market.get("signal_strength")),
                _line("Report baseline risk", packet.get("report_baseline_risk") or market.get("report_baseline_risk") or market.get("risk")),
                _line("Data ready for analyst review", summary.get("ready_for_analyst")),
            ],
        ),
        _section(
            "Selected Setup",
            [
                _line("Candidate ticker", candidate.get("ticker")),
                _line("Candidate timeframe", candidate.get("tf")),
                _line("Candidate entry / close", candidate.get("entry") or candidate.get("close")),
                _line("Candidate stop loss", candidate.get("stop_loss")),
                _line("Candidate take profit", candidate.get("take_profit")),
                _line("Candidate RR", candidate.get("rr")),
                _line("Candidate phase", candidate.get("phase")),
                _line("Candidate event", candidate.get("event")),
                _line("Candidate trend", candidate.get("trend")),
                _line("Candidate score", candidate.get("score")),
                "",
                _line("Trade plan entry", trade_plan.get("entry")),
                _line("Trade plan stop loss", trade_plan.get("stop_loss")),
                _line("Trade plan take profit", trade_plan.get("take_profit")),
                _line("Trade plan risk/reward", trade_plan.get("risk_reward")),
                _line("Trade plan source", trade_plan.get("source")),
            ],
        ),
        _section(
            "Wyckoff / VPA Context",
            [
                _line("Selected context timeframe", selected_tf_context.get("tf")),
                _line("Phase", selected_tf_context.get("phase")),
                _line("Trading range low", selected_tf_context.get("tr_low")),
                _line("Trading range high", selected_tf_context.get("tr_high")),
                "",
                "Recent events:",
                *_event_lines(selected_tf_context.get("recent_events")),
                "",
                "Confirmed events:",
                *_event_lines(selected_tf_context.get("confirmed_events")),
            ],
        ),
        _section(
            "Support and Resistance / Levels",
            [
                "Closest support:",
                *_level_lines(levels.get("support")),
                "",
                "Closest resistance:",
                *_level_lines(levels.get("resistance")),
                "",
                "Trade levels:",
                *_level_lines(levels.get("trade_levels")),
            ],
        ),
        _section(
            "Monte Carlo Context",
            [
                _line("Model", monte_carlo.get("model") or monte_carlo.get("model_used")),
                _line("Paths", monte_carlo.get("paths")),
                _line("Horizon bars", monte_carlo.get("horizon_bars")),
                _line("TP-first probability", _fmt_pct(monte_carlo.get("pop_tp_first"))),
                _line("SL-first probability", _fmt_pct(monte_carlo.get("p_sl_first"))),
                _line("Neither probability", _fmt_pct(monte_carlo.get("p_neither"))),
                _line("Median bars to TP", monte_carlo.get("t_hit_tp_median")),
                _line("Median bars to SL", monte_carlo.get("t_hit_sl_median")),
                _line("R mean", monte_carlo.get("r_mean")),
            ],
        ),
        _section(
            "P&F Context",
            [
                _line("P&F gate", pnf.get("gate") or summary.get("pnf_gate")),
                _line("Selected sidecar", pnf_selection.get("selected_filename") or pnf_sidecar.get("filename")),
                _line("Match score", pnf_selection.get("match_score") or pnf_sidecar.get("match_score")),
                _line("Match reasons", "; ".join(pnf_selection.get("match_reasons") or pnf_sidecar.get("match_reasons") or [])),
                _line("Box size", pnf_sidecar.get("box_size")),
                _line("Reversal", pnf_sidecar.get("reversal")),
                _line("Last price", pnf_sidecar.get("last_price")),
                _line("Objective", pnf_sidecar.get("objective")),
                _line("Objective direction", pnf_interpretation.get("objective_direction") or pnf_sidecar.get("objective_direction")),
                _line("Objective supports trade", pnf_interpretation.get("objective_supports_trade") if "objective_supports_trade" in pnf_interpretation else pnf_sidecar.get("objective_supports_trade")),
                _line("Objective quality", pnf_interpretation.get("objective_quality") or pnf_sidecar.get("objective_quality")),
                _line("Objective R multiple", pnf_sidecar.get("objective_r_multiple")),
                _line("Objective notes", "; ".join(pnf_interpretation.get("notes") or pnf_sidecar.get("objective_notes") or [])),
            ],
        ),
        _section(
            "Eigen Diagnostic Context",
            [
                _line("Available", eigen.get("available") if "available" in eigen else summary.get("eigen_available")),
                _line("Matched by", eigen.get("matched_by") or summary.get("eigen_matched_by")),
                _line("Latest residual", eigen_latest.get("pv_eigen_residual") if "pv_eigen_residual" in eigen_latest else summary.get("eigen_latest_residual")),
                _line("Latest coupling", eigen_latest.get("pv_eigen_coupling") if "pv_eigen_coupling" in eigen_latest else summary.get("eigen_latest_coupling")),
                _line("Latest divergence", eigen_latest.get("pv_effort_result_divergence") if "pv_effort_result_divergence" in eigen_latest else summary.get("eigen_latest_divergence")),
                _line("Divergence count", eigen_summary.get("divergence_count") if "divergence_count" in eigen_summary else summary.get("eigen_divergence_count")),
                _line("Recent divergence count", eigen_summary.get("recent_divergence_count") if "recent_divergence_count" in eigen_summary else summary.get("eigen_recent_divergence_count")),
                _line("Observation", eigen_summary.get("observation")),
                "- Guardrail: Treat Eigen as diagnostic/confirmatory context only, not as a trade signal.",
            ],
        ),
        _section(
            "Go / No-Go Gates",
            [
                _line("POP gate", summary.get("pop_gate") or go_no_go.get("pop_gate")),
                _line("P&F gate", summary.get("pnf_gate") or go_no_go.get("pnf_gate")),
                _line("Composite score", go_no_go.get("composite_score") or candidate.get("score")),
                _line("Risk rank", summary.get("risk_rank") or go_no_go.get("risk_rank")),
                "Gate notes:",
                *[f"- {_fmt(note)}" for note in _as_list(go_no_go.get("notes"))],
            ],
        ),
        _section(
            "Warnings and Missing Data",
            [
                "Warnings:",
                *([f"- {_fmt(item)}" for item in warnings] or ["- None reported."]),
                "",
                "Missing data:",
                *([f"- {_fmt(item)}" for item in missing_data] or ["- None reported."]),
            ],
        ),
        _section(
            "Required Output Format",
            [
                "Please answer with:",
                "",
                "1. Executive summary",
                "2. Wyckoff phase interpretation",
                "3. Volume-price confirmation or contradiction",
                "4. Trade setup quality",
                "5. Monte Carlo probability review",
                "6. P&F objective review",
                "7. Key risks / invalidation",
                "8. Final posture:",
                "   - Go",
                "   - Conditional Go",
                "   - Watchlist",
                "   - No-Go",
                "9. Questions or missing data",
            ],
        ),
    ]

    if include_raw_json:
        raw_json = json.dumps(packet, indent=2, sort_keys=True, default=str)
        sections.append(f"## Raw Analyst Packet JSON\n\n```json\n{raw_json}\n```")

    return "\n\n".join(sections).strip() + "\n"
