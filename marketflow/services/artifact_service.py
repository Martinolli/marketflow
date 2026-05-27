"""Discovery and preview helpers for generated MarketFlow report artifacts."""

from __future__ import annotations

import importlib.util
import json
import traceback as traceback_module
from datetime import datetime
from pathlib import Path
from typing import Any


TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")
PREVIEWABLE_EXTENSIONS = {".html", ".json", ".txt", ".md"}


def infer_artifact_timeframe(name: str) -> str | None:
    """Infer a timeframe token from an artifact filename."""
    if not name:
        return None

    normalized = Path(str(name)).stem.lower().replace("-", "_")
    tokens = [token for token in normalized.split("_") if token]
    for token in reversed(tokens):
        if token in TIMEFRAME_TOKENS:
            return token

    for token in TIMEFRAME_TOKENS:
        if f"_{token}_" in f"_{normalized}_":
            return token
    return None


def _classify_artifact(path: Path) -> str:
    """Classify a generated report artifact from its filename."""
    name = path.name.lower()
    suffix = path.suffix.lower()

    if name.endswith("_report.html"):
        return "report_html"
    if name.endswith("_summary_report.txt"):
        return "summary_text"
    if name.endswith("_report.json"):
        return "report_json"
    if name.endswith("_llm_analysis.json"):
        return "llm_json"
    if suffix == ".csv" and name.endswith("_pv_eigen.csv"):
        return "price_volume_eigen_csv"
    if suffix == ".csv" and "_backtest_candidates" in name:
        return "backtest_candidates_csv"
    if suffix == ".csv" and "_backtest_results" in name:
        return "backtest_results_csv"
    if suffix == ".csv" and name.endswith("_wyckoff_annotated.csv"):
        return "csv_annotated"
    if suffix == ".csv":
        return "csv_raw"
    if name.endswith("_point_and_figure_plot.html"):
        return "pnf_html"
    if suffix == ".json" and (name.endswith("_pnf_meta.json") or "pnf" in name):
        return "pnf_sidecar"
    if name.endswith("_mc_summary.json"):
        return "mc_summary"
    if name.endswith("_mc_paths.html"):
        return "mc_paths_html"
    if name.endswith("_mc_hits.html"):
        return "mc_hits_html"
    if suffix == ".html" and ("price_volume" in name or "price-volume" in name):
        return "legacy_price_volume_html"
    if suffix == ".html" and "volume_profile" in name:
        return "legacy_volume_profile_html"
    if suffix == ".html" and "volume_distribution" in name:
        return "legacy_volume_distribution_html"
    if suffix == ".html" and "spread" in name:
        return "legacy_spread_html"
    if suffix == ".html" and ("feature" in name or "annotated" in name or "wyckoff" in name):
        return "legacy_features_html"
    if suffix == ".html":
        return "other_html"
    if suffix == ".json":
        return "other_json"
    if suffix == ".md" and "_wyckoff_analyst_response" in name:
        return "analyst_response_md"
    if suffix == ".md" and "_wyckoff_analyst_prompt" in name:
        return "analyst_prompt_md"
    if suffix == ".md" and "_candidate_decision_summary" in name:
        return "candidate_decision_summary_md"
    if suffix == ".md" and "_eigen_review_summary" in name:
        return "eigen_review_summary_md"
    if suffix == ".md" and "_analyst_review_notes" in name:
        return "analyst_review_notes_md"
    if suffix == ".md":
        return "markdown"
    return "other"


def _artifact_row(path: Path) -> dict[str, Any]:
    stat = path.stat()
    kind = _classify_artifact(path)
    row = {
        "kind": kind,
        "name": path.name,
        "path": str(path),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "size": stat.st_size,
        "timeframe": infer_artifact_timeframe(path.name),
        "previewable": path.suffix.lower() in PREVIEWABLE_EXTENSIONS,
        "downloadable": True,
    }
    if kind == "pnf_sidecar":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        if isinstance(data, dict):
            row["source_csv"] = data.get("source_csv") or Path(str(data.get("source_csv_path") or "")).name or None
            row["timeframe"] = data.get("inferred_timeframe") or data.get("timeframe") or row["timeframe"]
            row["box_size"] = data.get("box_size") if data.get("box_size") is not None else data.get("box")
            row["reversal"] = data.get("reversal")
    return row


def list_report_artifacts(report_dir: str) -> list[dict[str, Any]]:
    """
    Discover useful generated files in a report directory.

    Return artifacts with kind, name, path, modified, size, timeframe,
    previewable, and downloadable fields.
    """
    if not report_dir:
        return []

    directory = Path(report_dir)
    if not directory.exists() or not directory.is_dir():
        return []

    artifacts: list[dict[str, Any]] = []
    for item in directory.iterdir():
        if not item.is_file():
            continue
        kind = _classify_artifact(item)
        if kind == "other":
            continue
        try:
            artifacts.append(_artifact_row(item))
        except OSError:
            continue

    return sorted(artifacts, key=lambda artifact: (artifact["kind"], artifact["name"]))


def read_text_artifact(
    path: str,
    max_bytes: int = 8_000_000,
    report_dir: str | None = None,
) -> dict[str, Any]:
    """
    Read a generated text-like artifact defensively.

    Returns: success, text, error, too_large, and size.
    """
    result = {
        "success": False,
        "text": None,
        "error": None,
        "too_large": False,
        "size": None,
    }
    if not path:
        result["error"] = "No artifact path was provided."
        return result

    artifact_path = Path(path)
    try:
        if report_dir:
            report_path = Path(report_dir)
            if not report_path.exists() or not report_path.is_dir():
                result["error"] = "Report directory does not exist."
                return result
            try:
                artifact_path.resolve().relative_to(report_path.resolve())
            except ValueError:
                result["error"] = "Artifact is outside the selected report directory."
                return result

        if not artifact_path.exists() or not artifact_path.is_file():
            result["error"] = "Artifact file does not exist."
            return result
        if artifact_path.suffix.lower() not in PREVIEWABLE_EXTENSIONS:
            result["error"] = "This artifact type is not previewable as text."
            return result

        size = artifact_path.stat().st_size
        result["size"] = size
        if size > int(max_bytes):
            result["too_large"] = True
            result["error"] = f"Artifact is too large to preview ({size} bytes)."
            return result

        result["text"] = artifact_path.read_text(encoding="utf-8", errors="replace")
        result["success"] = True
        return result
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result


def _legacy_plotting_module() -> Any:
    """Load the existing legacy plotting script without making scripts/ a package."""
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "plot_annotated_features.py"
    spec = importlib.util.spec_from_file_location("marketflow_plot_annotated_features", script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load legacy plotting script: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_legacy_feature_plots_for_csv(
    csv_path: str,
    nrows: int | None = None,
    include_pnf: bool = True,
    include_price_volume: bool = True,
    include_volume_profile: bool = True,
    include_volume_distribution: bool = True,
    include_spread: bool = True,
) -> dict[str, Any]:
    """Run the legacy feature plotting workflow for one CSV without opening browser windows."""
    path = Path(str(csv_path))
    if not path.exists() or not path.is_file():
        return {"success": False, "csv_path": str(csv_path), "error": "CSV file does not exist.", "artifacts": []}

    try:
        module = _legacy_plotting_module()
        if not hasattr(module, "generate_feature_plot_artifacts"):
            raise AttributeError("Legacy plotting script does not expose generate_feature_plot_artifacts.")

        result = module.generate_feature_plot_artifacts(
            str(path),
            features=None,
            nrows=nrows,
            show=False,
            include_pnf=include_pnf,
            include_price_volume=include_price_volume,
            include_volume_profile=include_volume_profile,
            include_volume_distribution=include_volume_distribution,
            include_spread=include_spread,
        )
        if not isinstance(result, dict):
            result = {"success": True, "csv_path": str(path), "generated_paths": []}

        generated_paths = [str(item) for item in result.get("generated_paths") or []]
        return {
            "success": bool(result.get("success", True)),
            "csv_path": str(path),
            "output_dir": str(path.parent),
            "generated_paths": generated_paths,
            "artifacts": list_report_artifacts(str(path.parent)),
            "error": result.get("error"),
            "traceback": result.get("traceback"),
        }
    except Exception as exc:
        return {
            "success": False,
            "csv_path": str(path),
            "output_dir": str(path.parent),
            "generated_paths": [],
            "artifacts": list_report_artifacts(str(path.parent)),
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback_module.format_exc(),
        }


def parse_json_artifact_text(text: str | None) -> Any:
    """Parse JSON preview text when possible."""
    if not text:
        return None
    return json.loads(text)
