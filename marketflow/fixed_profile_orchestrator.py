"""Normal ticker-only fixed-profile orchestration for MarketFlow."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd

from marketflow.marketflow_data_parameters import (
    FixedAnalysisProfile,
    fixed_analysis_profiles,
    fixed_profile_digest,
)
from marketflow.operational_artifacts import (
    ArtifactContractError,
    DEFAULT_RUN_ROOT,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
    annotated_dataset_artifact,
    candidate_core,
    commit_candidate_core_artifact,
    create_run_context,
    stable_digest,
)


ORCHESTRATOR_VERSION = "marketflow.fixed_profile_orchestrator.v1"
DEFAULT_NORMAL_SOURCE_ROOT = Path(__file__).resolve().parents[1] / ".marketflow" / "reports"

SOURCE_STATUS_EXACT_MATCH = "EXACT_MATCH"
PROFILE_READY_FOR_ANALYSIS = "PROFILE_READY_FOR_ANALYSIS"
DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
DATASET_IDENTITY_AMBIGUOUS = "DATASET_IDENTITY_AMBIGUOUS"
DATASET_INVALID = "DATASET_INVALID"
INSUFFICIENT_HISTORY = "INSUFFICIENT_HISTORY"
PROFILE_CONFIGURATION_INVALID = "PROFILE_CONFIGURATION_INVALID"
PROFILE_ANALYSIS_FAILED = "PROFILE_ANALYSIS_FAILED"
CANDIDATE_NOT_AVAILABLE = "CANDIDATE_NOT_AVAILABLE"
CANDIDATE_COMPLETE = "CANDIDATE_COMPLETE"
CANDIDATE_INCOMPLETE = "CANDIDATE_INCOMPLETE"
MONTE_CARLO_NOT_AUTHORIZED = "MONTE_CARLO_NOT_AUTHORIZED"
OUTCOME_EVALUATION_NOT_AUTHORIZED = "OUTCOME_EVALUATION_NOT_AUTHORIZED"

ALL_PROFILES_COMPLETED = "ALL_PROFILES_COMPLETED"
PARTIAL_PROFILE_COMPLETION = "PARTIAL_PROFILE_COMPLETION"
ALL_PROFILES_BLOCKED = "ALL_PROFILES_BLOCKED"
ORCHESTRATOR_INVALID = "ORCHESTRATOR_INVALID"

_NORMAL_TICKER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]*$")
_SOURCE_TICKER_PATTERN = re.compile(r"^[A-Z0-9._:-]+$")
_FILENAME_SUFFIX_PATTERN = re.compile(r"\.(csv|json|txt|html|md)$", re.IGNORECASE)
_TIMEFRAME_SUFFIX_PATTERN = re.compile(r"(^|[_:.-])(1mo|1w|1d|4h|2h|1h|30m|15m|5m|1m)$", re.IGNORECASE)
_SUPPORTED_TIMEFRAME_TOKENS = ("1mo", "1w", "1d", "4h", "2h", "1h", "30m", "15m", "5m", "1m")
_REQUIRED_OHLCV_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")
_GENERATED_STRATEGY_ARTIFACT_MARKERS = (
    "_pv_eigen.csv",
    "_backtest_candidates",
    "_backtest_results",
    "_eigen_review_summary",
    "_candidate_decision_summary",
    "_analyst_review_notes",
    "_walk_forward_cases_",
    "_walk_forward_results_",
    "_walk_forward_summary_",
)


class NormalTickerError(ValueError):
    """Raised when normal mode receives something other than one ticker."""


class ProfileAnalysisError(RuntimeError):
    """Carry partial profile evidence for a failed ready-profile run."""

    def __init__(self, result: dict[str, Any]) -> None:
        super().__init__("Fixed profile analysis failed.")
        self.result = result


def normalize_normal_ticker(value: object) -> str:
    """Normalize the one permitted normal-mode input or raise."""
    if value is None:
        raise NormalTickerError("Ticker is required.")
    text = str(value)
    if not text or text != text.strip():
        raise NormalTickerError("Ticker must not be empty or padded with whitespace.")
    if any(ord(char) < 32 for char in text):
        raise NormalTickerError("Ticker must not contain control characters.")
    if any(separator in text for separator in ("/", "\\", ",", ":", ";", "|")):
        raise NormalTickerError("Ticker must not contain separators or multiple symbols.")
    if _FILENAME_SUFFIX_PATTERN.search(text):
        raise NormalTickerError("Ticker must not be a filename.")
    if _TIMEFRAME_SUFFIX_PATTERN.search(text):
        raise NormalTickerError("Ticker must not include a timeframe suffix.")
    if not _NORMAL_TICKER_PATTERN.fullmatch(text):
        raise NormalTickerError("Ticker contains unsupported characters.")
    return text.upper()


def _relative_ref(path: Path, root: Path) -> str | None:
    try:
        return path.resolve(strict=True).relative_to(root.resolve(strict=True)).as_posix()
    except (OSError, ValueError):
        return None


def _source_root(source_root: str | Path | None) -> Path:
    return Path(source_root) if source_root is not None else DEFAULT_NORMAL_SOURCE_ROOT


def _path_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def _canonical_source_ticker(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    if text != text.strip() or not text or any(ord(char) < 32 for char in text):
        return None
    if "/" in text or "\\" in text:
        return None
    canonical = text.upper()
    return canonical if _SOURCE_TICKER_PATTERN.fullmatch(canonical) else None


def _canonical_source_timeframe(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    if text != text.strip() or not text:
        return None
    canonical = text.lower()
    return canonical if canonical in _SUPPORTED_TIMEFRAME_TOKENS else None


def _is_generated_strategy_artifact_csv(path: Path) -> bool:
    filename = path.name.lower()
    return filename.endswith(".csv") and any(marker in filename for marker in _GENERATED_STRATEGY_ARTIFACT_MARKERS)


def _parse_source_csv_identity(path: Path) -> dict[str, str] | None:
    if path.suffix.lower() != ".csv" or _is_generated_strategy_artifact_csv(path):
        return None
    stem = path.stem
    lowered = stem.lower()
    source_kind = "canonical" if lowered.endswith("_wyckoff_annotated") else "raw"
    core = stem[: -len("_wyckoff_annotated")] if source_kind == "canonical" else stem
    parts = core.split("_")
    if len(parts) < 2:
        return None
    for index, part in enumerate(parts[1:], start=1):
        timeframe = _canonical_source_timeframe(part)
        if timeframe is None:
            continue
        ticker = _canonical_source_ticker("_".join(parts[:index]))
        if ticker is None:
            return None
        return {"ticker": ticker, "timeframe": timeframe, "source_kind": source_kind}
    return None


def resolve_local_profile_source(
    *,
    ticker: str,
    profile: FixedAnalysisProfile,
    source_root: str | Path | None = None,
) -> dict[str, Any]:
    """Resolve exactly one local source for ticker plus profile timeframe."""
    normalized_ticker = normalize_normal_ticker(ticker)
    root = _source_root(source_root)
    try:
        root_resolved = root.resolve(strict=True)
    except OSError:
        return {"status": DATASET_NOT_FOUND, "match_count": 0, "source": None}
    if not root_resolved.is_dir():
        return {"status": DATASET_NOT_FOUND, "match_count": 0, "source": None}

    matches: list[Path] = []
    try:
        for path in root_resolved.rglob("*.csv"):
            if not path.is_file() or not _path_within_root(path, root_resolved):
                continue
            identity = _parse_source_csv_identity(path)
            if (
                identity
                and identity["ticker"] == normalized_ticker
                and identity["timeframe"] == profile.candidate_timeframe
                and identity["source_kind"] == "canonical"
            ):
                matches.append(path)
    except OSError:
        return {"status": DATASET_INVALID, "match_count": 0, "source": None}

    if not matches:
        return {"status": DATASET_NOT_FOUND, "match_count": 0, "source": None}
    if len(matches) > 1:
        return {"status": DATASET_IDENTITY_AMBIGUOUS, "match_count": len(matches), "source": None}
    return {
        "status": SOURCE_STATUS_EXACT_MATCH,
        "match_count": 1,
        "source": matches[0],
        "source_ref": _relative_ref(matches[0], root_resolved),
    }


def _finite_numeric_series(frame: pd.DataFrame, column: str) -> pd.Series:
    values = pd.to_numeric(frame[column], errors="coerce")
    return values.map(lambda value: isinstance(value, (int, float)) and math.isfinite(float(value)))


def validate_profile_dataset(
    *,
    csv_path: str | Path,
    source_root: str | Path,
    profile: FixedAnalysisProfile,
) -> dict[str, Any]:
    """Validate a resolved source read-only and return row-gate metadata."""
    path = Path(csv_path)
    root = Path(source_root)
    try:
        if not path.resolve(strict=True).relative_to(root.resolve(strict=True)):
            pass
    except (OSError, ValueError):
        return {"status": DATASET_INVALID, "actual_valid_rows": 0, "required_rows": profile.minimum_valid_rows}
    if not path.is_file() or path.suffix.lower() != ".csv":
        return {"status": DATASET_INVALID, "actual_valid_rows": 0, "required_rows": profile.minimum_valid_rows}

    try:
        frame = pd.read_csv(path)
    except Exception:
        return {"status": DATASET_INVALID, "actual_valid_rows": 0, "required_rows": profile.minimum_valid_rows}

    missing = [column for column in _REQUIRED_OHLCV_COLUMNS if column not in frame.columns]
    if missing:
        return {"status": DATASET_INVALID, "actual_valid_rows": 0, "required_rows": profile.minimum_valid_rows}

    timestamps = pd.to_datetime(frame["timestamp"], errors="coerce")
    if timestamps.isna().any() or timestamps.duplicated().any() or not timestamps.is_monotonic_increasing:
        return {"status": DATASET_INVALID, "actual_valid_rows": 0, "required_rows": profile.minimum_valid_rows}

    numeric = {column: pd.to_numeric(frame[column], errors="coerce") for column in ("open", "high", "low", "close", "volume")}
    valid = pd.Series(True, index=frame.index)
    for column in ("open", "high", "low", "close", "volume"):
        valid &= numeric[column].map(lambda value: isinstance(value, (int, float)) and math.isfinite(float(value)))
    valid &= numeric["high"] >= numeric["low"]
    valid &= numeric["volume"] >= 0
    actual_valid_rows = int(valid.sum())
    status = PROFILE_READY_FOR_ANALYSIS if actual_valid_rows >= profile.minimum_valid_rows else INSUFFICIENT_HISTORY
    return {
        "status": status,
        "actual_valid_rows": actual_valid_rows,
        "required_rows": profile.minimum_valid_rows,
    }


def _base_profile_result(profile: FixedAnalysisProfile) -> dict[str, Any]:
    return {
        "profile_id": profile.profile_id,
        "profile_timeframe": profile.candidate_timeframe,
        "profile_digest": fixed_profile_digest(profile),
        "status": PROFILE_CONFIGURATION_INVALID,
        "readiness_status": None,
        "candidate_status": CANDIDATE_NOT_AVAILABLE,
        "actual_valid_rows": None,
        "required_rows": profile.minimum_valid_rows,
        "run_id": None,
        "artifacts": [],
        "strategy_config_digest": None,
        "candidate_digest": None,
        "monte_carlo_status": MONTE_CARLO_NOT_AUTHORIZED,
        "outcome_evaluation_status": OUTCOME_EVALUATION_NOT_AUTHORIZED,
    }


def _run_ready_profile(
    *,
    ticker: str,
    profile: FixedAnalysisProfile,
    source: Path,
    source_root: Path,
    run_root: str | Path,
    run_id_factory: Any | None,
    artifact_id_factory: Any | None,
) -> dict[str, Any]:
    result = _base_profile_result(profile)
    from marketflow.marketflow_strategy import (
        CandidateBuildRequest,
        CandidateEvidenceInputs,
        SOURCE_KIND_CANONICAL_ANNOTATED,
        StrategyConfig,
        StrategyDatasetIdentity,
        build_candidate_from_prefix,
        strategy_config_digest,
    )

    try:
        run = create_run_context(run_root=run_root, run_id_factory=run_id_factory)
        result["run_id"] = run["run_id"]
        analysis = annotated_dataset_artifact(
            csv_path=source,
            run_root=run_root,
            run_id=run["run_id"],
            workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
            ticker=ticker,
            analysis_profile=profile.profile_id,
            timeframe=profile.candidate_timeframe,
            artifact_id_factory=artifact_id_factory,
        )
        result["artifacts"].append(analysis["receipt"])
        analysis_manifest = analysis["manifest"]
        payload_path = Path(run_root) / str(analysis_manifest["payload_ref"])
        frame = pd.read_csv(payload_path)
        if "timestamp" in frame.columns:
            frame["timestamp"] = pd.to_datetime(frame["timestamp"])
        cfg = StrategyConfig()
        cfg_digest = strategy_config_digest(cfg)
        candidate = build_candidate_from_prefix(
            CandidateBuildRequest(
                source_identity=StrategyDatasetIdentity(
                    ticker=ticker,
                    timeframe=profile.candidate_timeframe,
                    source=payload_path,
                    source_kind=SOURCE_KIND_CANONICAL_ANNOTATED,
                ),
                data_prefix=frame,
                config=cfg,
                evidence=CandidateEvidenceInputs(),
                report_root=run_root,
                source_report_dir=payload_path.parent,
                source_status=SOURCE_STATUS_EXACT_MATCH,
                candidate_source="fixed_profile_orchestrator_v1",
            )
        )
    except Exception as exc:
        if isinstance(exc, ArtifactContractError):
            raise
        result["status"] = PROFILE_ANALYSIS_FAILED
        result["candidate_status"] = CANDIDATE_NOT_AVAILABLE
        raise ProfileAnalysisError(result) from exc
    result["strategy_config_digest"] = cfg_digest
    if candidate.get("candidate_build_success") is not True or candidate.get("rank_eligible") is not True:
        result["status"] = CANDIDATE_INCOMPLETE
        result["candidate_status"] = CANDIDATE_INCOMPLETE
        result["candidate_reason"] = (
            candidate.get("candidate_build_reason")
            or candidate.get("score_profile_calibration")
            or candidate.get("score_reason")
            or CANDIDATE_INCOMPLETE
        )
        result["score_status"] = candidate.get("score_status")
        result["score_profile_calibration"] = candidate.get("score_profile_calibration")
        result["active_evidence_profile"] = candidate.get("active_evidence_profile")
        result["missing_components"] = list(candidate.get("missing_components") or [])
        result["disabled_components"] = list(candidate.get("disabled_components") or [])
        result["invalid_components"] = list(candidate.get("invalid_components") or [])
        return result

    candidate_artifact = commit_candidate_core_artifact(
        analysis_manifest=analysis_manifest,
        candidate=candidate,
        strategy_config_digest=cfg_digest,
        run_root=run_root,
        artifact_id_factory=artifact_id_factory,
    )
    result["artifacts"].append(candidate_artifact["receipt"])
    result["candidate_digest"] = stable_digest(candidate_core(candidate))
    result["status"] = CANDIDATE_COMPLETE
    result["candidate_status"] = CANDIDATE_COMPLETE
    return result


def run_fixed_profile_orchestrator(
    ticker: object,
    *,
    source_root: str | Path | None = None,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    run_id_factory: Any | None = None,
    artifact_id_factory: Any | None = None,
) -> dict[str, Any]:
    """Run the normal ticker-only workflow across all fixed profiles."""
    normalized_ticker = normalize_normal_ticker(ticker)
    resolved_source_root = _source_root(source_root)
    profile_results: list[dict[str, Any]] = []

    for profile in fixed_analysis_profiles():
        profile_result = _base_profile_result(profile)
        source_resolution = resolve_local_profile_source(
            ticker=normalized_ticker,
            profile=profile,
            source_root=resolved_source_root,
        )
        if source_resolution["status"] != SOURCE_STATUS_EXACT_MATCH:
            profile_result["status"] = source_resolution["status"]
            profile_result["readiness_status"] = source_resolution["status"]
            profile_result["source_status"] = source_resolution["status"]
            profile_result["source_match_count"] = source_resolution.get("match_count", 0)
            profile_results.append(profile_result)
            continue

        quality = validate_profile_dataset(
            csv_path=source_resolution["source"],
            source_root=resolved_source_root,
            profile=profile,
        )
        profile_result.update(
            {
                "status": quality["status"],
                "readiness_status": quality["status"],
                "source_status": SOURCE_STATUS_EXACT_MATCH,
                "source_match_count": 1,
                "actual_valid_rows": quality["actual_valid_rows"],
                "required_rows": quality["required_rows"],
            }
        )
        if quality["status"] != PROFILE_READY_FOR_ANALYSIS:
            profile_results.append(profile_result)
            continue

        try:
            executed = _run_ready_profile(
                ticker=normalized_ticker,
                profile=profile,
                source=source_resolution["source"],
                source_root=resolved_source_root,
                run_root=run_root,
                run_id_factory=run_id_factory,
                artifact_id_factory=artifact_id_factory,
            )
            executed.update(
                {
                    "source_status": SOURCE_STATUS_EXACT_MATCH,
                    "source_match_count": 1,
                    "readiness_status": PROFILE_READY_FOR_ANALYSIS,
                    "actual_valid_rows": quality["actual_valid_rows"],
                    "required_rows": quality["required_rows"],
                }
            )
            profile_results.append(executed)
        except ArtifactContractError:
            raise
        except ProfileAnalysisError as exc:
            profile_results.append(exc.result)
        except Exception:
            profile_result["status"] = PROFILE_ANALYSIS_FAILED
            profile_result["candidate_status"] = CANDIDATE_NOT_AVAILABLE
            profile_results.append(profile_result)

    completed = [item for item in profile_results if item["candidate_status"] == CANDIDATE_COMPLETE]
    if len(completed) == len(profile_results):
        status = ALL_PROFILES_COMPLETED
    elif completed:
        status = PARTIAL_PROFILE_COMPLETION
    else:
        status = ALL_PROFILES_BLOCKED
    return {
        "status": status,
        "ticker": normalized_ticker,
        "orchestrator_version": ORCHESTRATOR_VERSION,
        "requested_profiles": [profile.profile_id for profile in fixed_analysis_profiles()],
        "profile_results": profile_results,
    }


def receipt_to_json(receipt: dict[str, Any]) -> str:
    """Serialize a sanitized orchestration receipt deterministically."""
    return json.dumps(receipt, indent=2, sort_keys=True)
