"""Strict artifact contracts for MarketFlow operational workflows."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


WORKFLOW_MANUAL_SCENARIO_ANALYSIS = "MANUAL_SCENARIO_ANALYSIS"
WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT = "CANONICAL_STRATEGY_DECISION_SUPPORT"
SCENARIO_ORIGIN_MANUAL = "MANUAL_SCENARIO"
STAGE_BATCH_ANALYSIS = "batch_analysis"
STAGE_STRATEGY_RANKING = "strategy_ranking"
STAGE_MONTE_CARLO = "monte_carlo"
STAGE_ANNOTATED_PLOT = "annotated_plot"
VALID_WORKFLOW_TYPES = {
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
}
VALID_STAGES = {
    STAGE_BATCH_ANALYSIS,
    STAGE_STRATEGY_RANKING,
    STAGE_MONTE_CARLO,
    STAGE_ANNOTATED_PLOT,
}


class ArtifactContractError(ValueError):
    """Raised when an operational artifact handoff is missing or ambiguous."""


def stable_digest(value: Any) -> str:
    """Return a deterministic sha256 digest for JSON-compatible data."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _safe_relative_reference(path: str | Path | None, root: str | Path | None = None) -> str | None:
    if path is None:
        return None
    path_obj = Path(path)
    if path_obj.is_absolute() and root is None:
        return path_obj.name
    if root is not None:
        try:
            return path_obj.resolve(strict=False).relative_to(Path(root).resolve(strict=False)).as_posix()
        except ValueError:
            raise ArtifactContractError("Artifact path must stay within artifact_root.") from None
    if ".." in path_obj.parts:
        raise ArtifactContractError("Artifact reference must be a safe relative path.")
    return path_obj.as_posix()


def _identity_from(item: dict[str, Any]) -> dict[str, Any]:
    identity = item.get("artifact_identity")
    if isinstance(identity, dict):
        merged = dict(item)
        merged.update(identity)
        return merged
    return item


def _required_text(value: object, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise ArtifactContractError(f"{field_name} is required.")
    return str(value).strip()


def build_artifact_identity(
    *,
    schema_version: str = "marketflow.operational_artifact.v1",
    artifact_id: str,
    run_id: str,
    stage: str,
    workflow_type: str,
    ticker: str,
    analysis_profile: str | None,
    timeframe: str,
    source_dataset_identity: str,
    source_dataset_digest: str | None = None,
    code_commit: str | None = None,
    strategy_config_digest: str | None = None,
    candidate_core_digest: str | None = None,
    parent_artifact_id: str | None = None,
    artifact_path: str | Path | None = None,
    artifact_root: str | Path | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build non-secret immutable identity metadata for workflow artifacts."""
    artifact_id_text = _required_text(artifact_id, "artifact_id")
    run_id_text = _required_text(run_id, "run_id")
    ticker_text = _required_text(ticker, "ticker")
    timeframe_text = _required_text(timeframe, "timeframe")
    source_identity_text = _required_text(source_dataset_identity, "source_dataset_identity")
    if parent_artifact_id == artifact_id:
        raise ArtifactContractError("Artifact cannot be its own parent.")
    if workflow_type not in VALID_WORKFLOW_TYPES:
        raise ArtifactContractError(f"Unsupported workflow_type: {workflow_type}")
    if stage not in VALID_STAGES:
        raise ArtifactContractError(f"Unsupported stage: {stage}")
    return {
        "schema_version": schema_version,
        "artifact_id": artifact_id_text,
        "run_id": run_id_text,
        "stage": stage,
        "workflow_type": workflow_type,
        "ticker": ticker_text.upper(),
        "analysis_profile": analysis_profile,
        "timeframe": timeframe_text.lower(),
        "source_dataset_identity": source_identity_text,
        "source_dataset_digest": source_dataset_digest,
        "code_commit": code_commit,
        "strategy_config_digest": strategy_config_digest,
        "candidate_core_digest": candidate_core_digest,
        "parent_artifact_id": parent_artifact_id,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "artifact_ref": _safe_relative_reference(artifact_path, artifact_root),
    }


def select_exact_artifact(
    artifacts: Iterable[dict[str, Any]],
    *,
    artifact_id: str,
    parent_artifact_id: str | None = None,
    ticker: str | None = None,
    timeframe: str | None = None,
    run_id: str | None = None,
    workflow_type: str | None = None,
    stage: str | None = None,
) -> dict[str, Any]:
    """Return the one exact artifact match or fail closed."""
    artifact_list = list(artifacts)
    matches: list[dict[str, Any]] = []
    identity_by_id = {
        str(identity["artifact_id"]): identity
        for item in artifact_list
        for identity in [_identity_from(item)]
        if identity.get("artifact_id")
    }
    for item in artifact_list:
        identity = _identity_from(item)
        if _has_parent_cycle(identity, identity_by_id):
            raise ArtifactContractError("Artifact parent cycle detected.")
        if identity.get("artifact_id") != artifact_id:
            continue
        if parent_artifact_id is not None and identity.get("parent_artifact_id") != parent_artifact_id:
            continue
        if ticker is not None and str(identity.get("ticker", "")).upper() != str(ticker).upper():
            continue
        if timeframe is not None and str(identity.get("timeframe", "")).lower() != str(timeframe).lower():
            continue
        if run_id is not None and identity.get("run_id") != run_id:
            continue
        if workflow_type is not None and identity.get("workflow_type") != workflow_type:
            continue
        if stage is not None and identity.get("stage") != stage:
            continue
        matches.append(item)

    if not matches:
        raise ArtifactContractError("No exact artifact match.")
    if len(matches) > 1:
        raise ArtifactContractError("Ambiguous artifact match.")
    return matches[0]


def _has_parent_cycle(identity: dict[str, Any], identity_by_id: dict[str, dict[str, Any]]) -> bool:
    artifact_id = identity.get("artifact_id")
    parent_id = identity.get("parent_artifact_id")
    seen = {artifact_id}
    while parent_id:
        if parent_id in seen:
            return True
        seen.add(parent_id)
        parent = identity_by_id.get(str(parent_id))
        if not parent:
            return False
        parent_id = parent.get("parent_artifact_id")
    return False


def candidate_core(candidate: dict[str, Any]) -> dict[str, Any]:
    """Extract canonical candidate geometry and source identity fields."""
    return {
        "ticker": candidate.get("ticker"),
        "timeframe": candidate.get("timeframe") or candidate.get("tf"),
        "entry": candidate.get("entry"),
        "stop_loss": candidate.get("stop_loss") if candidate.get("stop_loss") is not None else candidate.get("sl"),
        "take_profit": candidate.get("take_profit") if candidate.get("take_profit") is not None else candidate.get("tp"),
        "source_csv": candidate.get("source_csv") or candidate.get("csv"),
        "source_status": candidate.get("source_status"),
        "candidate_build_status": candidate.get("candidate_build_status"),
    }


def build_workflow_b_monte_carlo_request(
    *,
    candidate: dict[str, Any],
    strategy_artifact_id: str,
    run_id: str,
    horizon_bars: int,
    strategy_config_digest: str | None = None,
) -> dict[str, Any]:
    """Create MC request geometry from canonical Strategy candidate fields only."""
    if candidate.get("candidate_build_success") is not True or candidate.get("rank_eligible") is not True:
        raise ArtifactContractError("Strategy candidate is not actionable.")
    core = candidate_core(candidate)
    missing = [key for key in ("ticker", "timeframe", "entry", "stop_loss", "take_profit", "source_csv") if core.get(key) is None]
    if missing:
        raise ArtifactContractError(f"Strategy candidate is missing required geometry: {', '.join(missing)}")
    identity = build_artifact_identity(
        artifact_id=f"{run_id}:{core['ticker']}:{core['timeframe']}:mc",
        run_id=run_id,
        stage=STAGE_MONTE_CARLO,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker=str(core["ticker"]),
        analysis_profile=None,
        timeframe=str(core["timeframe"]),
        source_dataset_identity=str(core["source_csv"]),
        strategy_config_digest=strategy_config_digest,
        candidate_core_digest=stable_digest(core),
        parent_artifact_id=strategy_artifact_id,
    )
    return {
        "workflow_type": WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        "csv": core["source_csv"],
        "ticker": core["ticker"],
        "timeframe": core["timeframe"],
        "entry": core["entry"],
        "sl": core["stop_loss"],
        "tp": core["take_profit"],
        "horizon_bars": int(horizon_bars),
        "artifact_identity": identity,
    }


def build_workflow_a_manual_scenario_request(
    *,
    parent_analysis_artifact: dict[str, Any],
    scenario: dict[str, Any],
    run_id: str,
) -> dict[str, Any]:
    """Create MC request geometry from explicitly supplied manual scenario fields."""
    parent = _identity_from(parent_analysis_artifact)
    missing = [key for key in ("ticker", "timeframe", "source_dataset_identity") if not parent.get(key)]
    if missing:
        raise ArtifactContractError(f"Parent analysis artifact is missing identity: {', '.join(missing)}")
    required = ("entry", "stop_loss", "take_profit", "horizon_bars")
    missing_scenario = [key for key in required if scenario.get(key) is None]
    if missing_scenario:
        raise ArtifactContractError(f"Manual scenario is missing required geometry: {', '.join(missing_scenario)}")

    identity = build_artifact_identity(
        artifact_id=f"{run_id}:{parent['ticker']}:{parent['timeframe']}:manual-mc",
        run_id=run_id,
        stage=STAGE_MONTE_CARLO,
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker=str(parent["ticker"]),
        analysis_profile=parent.get("analysis_profile"),
        timeframe=str(parent["timeframe"]),
        source_dataset_identity=str(parent["source_dataset_identity"]),
        parent_artifact_id=str(parent["artifact_id"]),
    )
    return {
        "workflow_type": WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        "scenario_origin": SCENARIO_ORIGIN_MANUAL,
        "candidate_source": None,
        "csv": parent["source_dataset_identity"],
        "ticker": parent["ticker"],
        "timeframe": parent["timeframe"],
        "entry": scenario["entry"],
        "sl": scenario["stop_loss"],
        "tp": scenario["take_profit"],
        "horizon_bars": int(scenario["horizon_bars"]),
        "artifact_identity": identity,
    }


def assert_monte_carlo_geometry_matches_candidate(
    candidate: dict[str, Any],
    monte_carlo_request: dict[str, Any],
) -> None:
    """Fail if MC geometry differs from the canonical candidate geometry."""
    core = candidate_core(candidate)
    comparisons = {
        "entry": (core.get("entry"), monte_carlo_request.get("entry")),
        "stop_loss": (core.get("stop_loss"), monte_carlo_request.get("sl")),
        "take_profit": (core.get("take_profit"), monte_carlo_request.get("tp")),
        "ticker": (core.get("ticker"), monte_carlo_request.get("ticker")),
        "timeframe": (core.get("timeframe"), monte_carlo_request.get("timeframe")),
    }
    mismatches = [key for key, (left, right) in comparisons.items() if left != right]
    if mismatches:
        raise ArtifactContractError(f"MC request geometry mismatch: {', '.join(mismatches)}")
    expected_digest = stable_digest(core)
    actual_digest = None
    identity = monte_carlo_request.get("artifact_identity")
    if isinstance(identity, dict):
        actual_digest = identity.get("candidate_core_digest")
    if actual_digest is not None and actual_digest != expected_digest:
        raise ArtifactContractError("MC request candidate_core_digest mismatch.")


def run_specific_output_path(output_dir: str | Path, filename: str) -> Path:
    """Return an output path, failing if it would overwrite an existing artifact."""
    if Path(filename).is_absolute() or ".." in Path(filename).parts:
        raise ArtifactContractError("Output filename must be a safe relative filename.")
    path = Path(output_dir) / filename
    if path.exists():
        raise ArtifactContractError(f"Output artifact already exists: {filename}")
    return path
