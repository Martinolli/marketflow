"""Strict artifact contracts for MarketFlow operational workflows."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


WORKFLOW_MANUAL_SCENARIO_ANALYSIS = "MANUAL_SCENARIO_ANALYSIS"
WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT = "CANONICAL_STRATEGY_DECISION_SUPPORT"
SCENARIO_ORIGIN_MANUAL = "MANUAL_SCENARIO"
MANIFEST_SCHEMA_VERSION = "marketflow.artifact_manifest.v1"
DEFAULT_RUN_ROOT = Path(".marketflow") / "reports" / "runs"
STAGE_BATCH_ANALYSIS = "batch_analysis"
STAGE_STRATEGY_RANKING = "strategy_ranking"
STAGE_MONTE_CARLO = "monte_carlo"
STAGE_ANNOTATED_PLOT = "annotated_plot"
STAGE_BATCH_ANALYSIS_V1 = "BATCH_ANALYSIS"
STAGE_STRATEGY_CANDIDATE_V1 = "STRATEGY_CANDIDATE"
STAGE_MANUAL_SCENARIO_V1 = "MANUAL_SCENARIO"
STAGE_MONTE_CARLO_V1 = "MONTE_CARLO"
STAGE_PLOT_V1 = "PLOT"
ARTIFACT_TYPE_ANNOTATED_DATASET = "ANNOTATED_DATASET"
ARTIFACT_TYPE_CANDIDATE_CORE = "CANDIDATE_CORE"
ARTIFACT_TYPE_MANUAL_SCENARIO_DEFINITION = "MANUAL_SCENARIO_DEFINITION"
ARTIFACT_TYPE_MONTE_CARLO_SUMMARY = "MONTE_CARLO_SUMMARY"
ARTIFACT_TYPE_ANNOTATED_PLOT = "ANNOTATED_PLOT"
PAYLOAD_TYPE_CSV = "CSV"
PAYLOAD_TYPE_JSON = "JSON"
PAYLOAD_TYPE_HTML = "HTML"
PAYLOAD_TYPE_TEXT = "TEXT"
PROFILE_SWING = "SWING"
PROFILE_POSITION_SWING = "POSITION_SWING"
PROFILE_MANUAL_SCENARIO = "MANUAL_SCENARIO"
VALID_WORKFLOW_TYPES = {
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
}
VALID_STAGES = {
    STAGE_BATCH_ANALYSIS,
    STAGE_STRATEGY_RANKING,
    STAGE_MONTE_CARLO,
    STAGE_ANNOTATED_PLOT,
    STAGE_BATCH_ANALYSIS_V1,
    STAGE_STRATEGY_CANDIDATE_V1,
    STAGE_MANUAL_SCENARIO_V1,
    STAGE_MONTE_CARLO_V1,
    STAGE_PLOT_V1,
}
VALID_ARTIFACT_TYPES = {
    ARTIFACT_TYPE_ANNOTATED_DATASET,
    ARTIFACT_TYPE_CANDIDATE_CORE,
    ARTIFACT_TYPE_MANUAL_SCENARIO_DEFINITION,
    ARTIFACT_TYPE_MONTE_CARLO_SUMMARY,
    ARTIFACT_TYPE_ANNOTATED_PLOT,
}
VALID_PAYLOAD_TYPES = {
    PAYLOAD_TYPE_CSV,
    PAYLOAD_TYPE_JSON,
    PAYLOAD_TYPE_HTML,
    PAYLOAD_TYPE_TEXT,
}
VALID_ANALYSIS_PROFILES = {
    PROFILE_SWING,
    PROFILE_POSITION_SWING,
    PROFILE_MANUAL_SCENARIO,
}
ALLOWED_TRANSITIONS = {
    WORKFLOW_MANUAL_SCENARIO_ANALYSIS: {
        (STAGE_BATCH_ANALYSIS_V1, STAGE_MANUAL_SCENARIO_V1),
        (STAGE_MANUAL_SCENARIO_V1, STAGE_MONTE_CARLO_V1),
        (STAGE_MONTE_CARLO_V1, STAGE_PLOT_V1),
    },
    WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT: {
        (STAGE_BATCH_ANALYSIS_V1, STAGE_STRATEGY_CANDIDATE_V1),
        (STAGE_STRATEGY_CANDIDATE_V1, STAGE_MONTE_CARLO_V1),
        (STAGE_MONTE_CARLO_V1, STAGE_PLOT_V1),
    },
}
STAGE_DIRECTORY = {
    STAGE_BATCH_ANALYSIS_V1: "batch_analysis",
    STAGE_STRATEGY_CANDIDATE_V1: "strategy_candidate",
    STAGE_MANUAL_SCENARIO_V1: "manual_scenario",
    STAGE_MONTE_CARLO_V1: "monte_carlo",
    STAGE_PLOT_V1: "plot",
}
STAGE_ARTIFACT_TYPE = {
    STAGE_BATCH_ANALYSIS_V1: ARTIFACT_TYPE_ANNOTATED_DATASET,
    STAGE_STRATEGY_CANDIDATE_V1: ARTIFACT_TYPE_CANDIDATE_CORE,
    STAGE_MANUAL_SCENARIO_V1: ARTIFACT_TYPE_MANUAL_SCENARIO_DEFINITION,
    STAGE_MONTE_CARLO_V1: ARTIFACT_TYPE_MONTE_CARLO_SUMMARY,
    STAGE_PLOT_V1: ARTIFACT_TYPE_ANNOTATED_PLOT,
}
MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_id",
        "run_id",
        "stage",
        "artifact_type",
        "workflow_type",
        "ticker",
        "analysis_profile",
        "timeframe",
        "source_dataset_identity",
        "source_dataset_digest",
        "source_ref",
        "code_commit",
        "strategy_config_digest",
        "candidate_core_digest",
        "manual_scenario_digest",
        "parent_artifact_id",
        "input_artifact_ids",
        "lineage_artifact_ids",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_type",
        "created_at",
    }
)
WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


class ArtifactContractError(ValueError):
    """Raised when an operational artifact handoff is missing or ambiguous."""


def stable_digest(value: Any) -> str:
    """Return a deterministic sha256 digest for JSON-compatible data."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON payloads deterministically for canonical artifacts."""
    try:
        return (
            json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False, default=str)
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ArtifactContractError("JSON artifact payload must be deterministic and finite.") from exc


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def _safe_relative_path(path: str | Path, root: str | Path) -> str:
    path_obj = Path(path)
    root_obj = Path(root)
    try:
        relative = path_obj.resolve(strict=False).relative_to(root_obj.resolve(strict=False))
    except ValueError:
        raise ArtifactContractError("Artifact path must stay within artifact_root.") from None
    if relative.is_absolute() or ".." in relative.parts:
        raise ArtifactContractError("Artifact reference must be a safe relative path.")
    return relative.as_posix()


def _path_from_ref(root: str | Path, ref: str) -> Path:
    text = str(ref)
    parts = Path(text).parts
    if (
        not text
        or "\\" in text
        or ":" in text
        or "\x00" in text
        or Path(text).is_absolute()
        or text.startswith(("/", "~"))
        or ".." in parts
        or any(part in {"", ".", ".."} for part in parts)
        or any(part.rstrip(" .").upper() in WINDOWS_DEVICE_NAMES for part in parts)
        or any(part != part.rstrip(" .") for part in parts)
    ):
        raise ArtifactContractError("Artifact reference must be a safe relative path.")
    return Path(root) / Path(text)


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


def _require_opaque_id(value: object, field_name: str) -> str:
    text = _required_text(value, field_name)
    if (
        any(separator in text for separator in ("/", "\\", "..", "*", "?", "[", "]", ":"))
        or "\x00" in text
        or text.rstrip(" .") != text
        or text.upper() in WINDOWS_DEVICE_NAMES
    ):
        raise ArtifactContractError(f"{field_name} must be opaque and path-safe.")
    return text


def _require_finite_number(value: Any, field_name: str) -> Any:
    if isinstance(value, bool):
        raise ArtifactContractError(f"{field_name} must be finite numeric geometry.")
    parsed = value
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            raise ArtifactContractError(f"{field_name} must be finite numeric geometry.") from None
    if not isinstance(parsed, (int, float)) or not math.isfinite(float(parsed)):
        raise ArtifactContractError(f"{field_name} must be finite numeric geometry.")
    return value


def _safe_optional_ref(value: str | None) -> str | None:
    if value is None:
        return None
    _path_from_ref(".", value)
    return value


def _new_id(prefix: str, id_factory: Any | None = None) -> str:
    value = id_factory() if id_factory else uuid.uuid4().hex
    return _require_opaque_id(value, f"{prefix}_id")


def create_run_context(
    *,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    run_id: str | None = None,
    run_id_factory: Any | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Create one immutable run directory and return a sanitized run receipt."""
    run_id_text = _new_id("run", run_id_factory) if run_id is None else _require_opaque_id(run_id, "run_id")
    root = Path(run_root)
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / run_id_text
    try:
        run_dir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        raise ArtifactContractError("Run directory already exists.") from None
    return {
        "run_id": run_id_text,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        "run_ref": _safe_relative_path(run_dir, root),
    }


def ensure_run_context(
    *,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    run_id: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Return an existing run context without creating a hidden new run."""
    run_id_text = _require_opaque_id(run_id, "run_id")
    root = Path(run_root)
    run_dir = root / run_id_text
    if not run_dir.exists() or not run_dir.is_dir():
        raise ArtifactContractError("Run directory does not exist.")
    try:
        run_dir.resolve(strict=True).relative_to(root.resolve(strict=True))
    except ValueError:
        raise ArtifactContractError("Run directory must stay within run root.") from None
    return {
        "run_id": run_id_text,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        "run_ref": _safe_relative_path(run_dir, root),
    }


def _install_without_replace(temp_path: Path, final_path: Path) -> None:
    if final_path.exists():
        raise ArtifactContractError(f"Output artifact already exists: {final_path.name}")
    try:
        os.link(temp_path, final_path)
    except OSError:
        with final_path.open("xb") as final_handle, temp_path.open("rb") as temp_handle:
            shutil.copyfileobj(temp_handle, final_handle)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _write_temp_bytes(directory: Path, payload: bytes, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".tmp-", suffix=suffix, dir=str(directory))
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return Path(temp_name)


def _manifest_path_from_artifact_ref(run_root: str | Path, artifact_ref: str) -> Path:
    payload_path = _path_from_ref(run_root, artifact_ref)
    return payload_path.with_suffix(payload_path.suffix + ".manifest.json")


def _manifest_by_id(manifests: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["artifact_id"]): item for item in manifests if item.get("artifact_id")}


def _lineage_ids_for(parent_manifest: dict[str, Any] | None, input_manifests: list[dict[str, Any]]) -> list[str]:
    lineage_artifact_ids: list[str] = []
    if parent_manifest:
        lineage_artifact_ids.append(str(parent_manifest["artifact_id"]))
        lineage_artifact_ids.extend(str(item) for item in parent_manifest.get("lineage_artifact_ids") or [])
    for item in input_manifests:
        artifact_id_value = str(item["artifact_id"])
        if artifact_id_value not in lineage_artifact_ids:
            lineage_artifact_ids.append(artifact_id_value)
        for ancestor in item.get("lineage_artifact_ids") or []:
            if str(ancestor) not in lineage_artifact_ids:
                lineage_artifact_ids.append(str(ancestor))
    return lineage_artifact_ids


def _find_manifest_by_artifact_id(
    *,
    run_root: str | Path,
    run_id: str,
    artifact_id: str,
) -> dict[str, Any]:
    run_id_text = _require_opaque_id(run_id, "run_id")
    artifact_id_text = _require_opaque_id(artifact_id, "artifact_id")
    run_dir = Path(run_root) / run_id_text
    if not run_dir.exists() or not run_dir.is_dir():
        raise ArtifactContractError("Parent run directory does not exist.")
    matches: list[dict[str, Any]] = []
    for manifest_path in run_dir.glob("*/*.manifest.json"):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("artifact_id") == artifact_id_text:
            validate_manifest(data, run_root=run_root)
            matches.append(data)
    if not matches:
        raise ArtifactContractError("Declared parent/input manifest is missing.")
    if len(matches) > 1:
        raise ArtifactContractError("Declared parent/input artifact identity is ambiguous.")
    return matches[0]


def _validate_parent_inputs(
    *,
    manifest: dict[str, Any],
    parent_manifest: dict[str, Any] | None,
    input_manifests: list[dict[str, Any]],
) -> None:
    if manifest.get("parent_artifact_id") and not parent_manifest:
        raise ArtifactContractError("Parent manifest is required.")
    ids = [item.get("artifact_id") for item in input_manifests]
    if len(ids) != len(set(ids)):
        raise ArtifactContractError("Duplicate input artifact IDs are not allowed.")
    if manifest.get("artifact_id") in ids or manifest.get("parent_artifact_id") == manifest.get("artifact_id"):
        raise ArtifactContractError("Artifact cannot be its own parent or input.")
    if parent_manifest:
        expected = (parent_manifest.get("stage"), manifest.get("stage"))
        workflow = manifest.get("workflow_type")
        if parent_manifest.get("workflow_type") != workflow:
            raise ArtifactContractError("Parent workflow does not match child workflow.")
        if expected not in ALLOWED_TRANSITIONS.get(str(workflow), set()):
            raise ArtifactContractError("Invalid artifact stage transition.")
        for key in ("run_id", "ticker", "timeframe", "analysis_profile", "source_dataset_digest"):
            if parent_manifest.get(key) != manifest.get(key):
                raise ArtifactContractError(f"Parent {key} does not match child.")
    for item in input_manifests:
        for key in ("run_id", "workflow_type", "ticker", "timeframe", "analysis_profile", "source_dataset_digest"):
            if item.get(key) != manifest.get(key):
                raise ArtifactContractError(f"Input {key} does not match child.")


def build_artifact_manifest(
    *,
    artifact_id: str,
    run_id: str,
    stage: str,
    artifact_type: str,
    workflow_type: str,
    ticker: str,
    analysis_profile: str,
    timeframe: str,
    source_dataset_identity: str,
    source_dataset_digest: str,
    payload_ref: str,
    payload_sha256: str,
    payload_byte_size: int,
    payload_type: str,
    code_commit: str | None = None,
    strategy_config_digest: str | None = None,
    candidate_core_digest: str | None = None,
    manual_scenario_digest: str | None = None,
    parent_artifact_id: str | None = None,
    input_artifact_ids: list[str] | None = None,
    lineage_artifact_ids: list[str] | None = None,
    source_ref: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a strict Artifact Lineage v1 manifest."""
    artifact_id_text = _require_opaque_id(artifact_id, "artifact_id")
    run_id_text = _require_opaque_id(run_id, "run_id")
    if stage not in VALID_STAGES:
        raise ArtifactContractError(f"Unsupported stage: {stage}")
    if stage not in STAGE_DIRECTORY:
        raise ArtifactContractError(f"Unsupported lineage stage: {stage}")
    if artifact_type not in VALID_ARTIFACT_TYPES:
        raise ArtifactContractError(f"Unsupported artifact_type: {artifact_type}")
    if STAGE_ARTIFACT_TYPE.get(stage) != artifact_type:
        raise ArtifactContractError("Artifact type does not match stage.")
    if workflow_type not in VALID_WORKFLOW_TYPES:
        raise ArtifactContractError(f"Unsupported workflow_type: {workflow_type}")
    if analysis_profile not in VALID_ANALYSIS_PROFILES:
        raise ArtifactContractError(f"Unsupported analysis_profile: {analysis_profile}")
    if payload_type not in VALID_PAYLOAD_TYPES:
        raise ArtifactContractError(f"Unsupported payload_type: {payload_type}")
    if parent_artifact_id == artifact_id_text:
        raise ArtifactContractError("Artifact cannot be its own parent.")
    inputs = input_artifact_ids or []
    if len(inputs) != len(set(inputs)):
        raise ArtifactContractError("Duplicate input artifact IDs are not allowed.")
    if artifact_id_text in inputs:
        raise ArtifactContractError("Artifact cannot be its own input.")
    lineage_ids = lineage_artifact_ids or []
    if len(lineage_ids) != len(set(lineage_ids)):
        raise ArtifactContractError("Duplicate lineage artifact IDs are not allowed.")
    if artifact_id_text in lineage_ids:
        raise ArtifactContractError("Artifact cannot include itself in lineage.")
    safe_source_ref = _safe_optional_ref(source_ref)
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id_text,
        "run_id": run_id_text,
        "stage": stage,
        "artifact_type": artifact_type,
        "workflow_type": workflow_type,
        "ticker": _required_text(ticker, "ticker").upper(),
        "analysis_profile": analysis_profile,
        "timeframe": _required_text(timeframe, "timeframe").lower(),
        "source_dataset_identity": _required_text(source_dataset_identity, "source_dataset_identity"),
        "source_dataset_digest": _required_text(source_dataset_digest, "source_dataset_digest"),
        "source_ref": safe_source_ref,
        "code_commit": code_commit,
        "strategy_config_digest": strategy_config_digest,
        "candidate_core_digest": candidate_core_digest,
        "manual_scenario_digest": manual_scenario_digest,
        "parent_artifact_id": parent_artifact_id,
        "input_artifact_ids": inputs,
        "lineage_artifact_ids": lineage_ids,
        "payload_ref": _required_text(payload_ref, "payload_ref"),
        "payload_sha256": _required_text(payload_sha256, "payload_sha256"),
        "payload_byte_size": int(payload_byte_size),
        "payload_type": payload_type,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
    }


def commit_artifact_payload(
    *,
    payload: bytes,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    run_id: str,
    stage: str,
    artifact_type: str,
    workflow_type: str,
    ticker: str,
    analysis_profile: str,
    timeframe: str,
    source_dataset_identity: str,
    source_dataset_digest: str,
    payload_type: str,
    payload_extension: str,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
    strategy_config_digest: str | None = None,
    candidate_core_digest: str | None = None,
    manual_scenario_digest: str | None = None,
    parent_manifest: dict[str, Any] | None = None,
    input_manifests: list[dict[str, Any]] | None = None,
    source_ref: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Atomically commit a canonical payload and its v1 manifest."""
    if not isinstance(payload, bytes):
        raise ArtifactContractError("Payload must be bytes.")
    root = Path(run_root)
    run_dir = root / _required_text(run_id, "run_id")
    if not run_dir.exists() or not run_dir.is_dir():
        raise ArtifactContractError("Run directory does not exist.")
    stage_dir_name = STAGE_DIRECTORY.get(stage)
    if not stage_dir_name:
        raise ArtifactContractError(f"Unsupported lineage stage: {stage}")
    stage_dir = run_dir / stage_dir_name
    stage_dir.mkdir(parents=True, exist_ok=True)
    artifact_id_text = artifact_id or _new_id("artifact", artifact_id_factory)
    artifact_id_text = _require_opaque_id(artifact_id_text, "artifact_id")
    for existing_manifest_path in run_dir.glob("*/*.manifest.json"):
        try:
            existing_manifest = json.loads(existing_manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(existing_manifest, dict) and existing_manifest.get("artifact_id") == artifact_id_text:
            raise ArtifactContractError("Artifact output already exists.")
    extension = payload_extension if payload_extension.startswith(".") else f".{payload_extension}"
    payload_path = stage_dir / f"{artifact_id_text}{extension}"
    manifest_path = stage_dir / f"{artifact_id_text}{extension}.manifest.json"
    if payload_path.exists() or manifest_path.exists():
        raise ArtifactContractError("Artifact output already exists.")
    payload_sha = sha256_bytes(payload)
    payload_ref = _safe_relative_path(payload_path, root)
    _path_from_ref(".", payload_ref)
    parent = parent_manifest or None
    inputs = list(input_manifests or [])
    parent_artifact_id = parent.get("artifact_id") if parent else None
    input_artifact_ids = [str(item["artifact_id"]) for item in inputs]
    lineage_artifact_ids = _lineage_ids_for(parent, inputs)
    manifest = build_artifact_manifest(
        artifact_id=artifact_id_text,
        run_id=run_id,
        stage=stage,
        artifact_type=artifact_type,
        workflow_type=workflow_type,
        ticker=ticker,
        analysis_profile=analysis_profile,
        timeframe=timeframe,
        source_dataset_identity=source_dataset_identity,
        source_dataset_digest=source_dataset_digest,
        source_ref=source_ref,
        code_commit=code_commit,
        strategy_config_digest=strategy_config_digest,
        candidate_core_digest=candidate_core_digest,
        manual_scenario_digest=manual_scenario_digest,
        parent_artifact_id=parent_artifact_id,
        input_artifact_ids=input_artifact_ids,
        lineage_artifact_ids=lineage_artifact_ids,
        payload_ref=payload_ref,
        payload_sha256=payload_sha,
        payload_byte_size=len(payload),
        payload_type=payload_type,
        created_at=created_at,
    )
    _validate_parent_inputs(manifest=manifest, parent_manifest=parent, input_manifests=inputs)
    temp_payload = _write_temp_bytes(stage_dir, payload, ".payload.tmp")
    try:
        _install_without_replace(temp_payload, payload_path)
        manifest_payload = canonical_json_bytes(manifest)
        temp_manifest = _write_temp_bytes(stage_dir, manifest_payload, ".manifest.tmp")
        _install_without_replace(temp_manifest, manifest_path)
    except Exception:
        try:
            if payload_path.exists() and not manifest_path.exists():
                payload_path.unlink()
        except OSError:
            pass
        raise
    saved_manifest = load_manifest(_safe_relative_path(manifest_path, root), run_root=root)
    validate_manifest_chain(saved_manifest, run_root=root)
    receipt = {
        "run_id": saved_manifest["run_id"],
        "artifact_id": saved_manifest["artifact_id"],
        "stage": saved_manifest["stage"],
        "artifact_type": saved_manifest["artifact_type"],
        "workflow_type": saved_manifest["workflow_type"],
        "ticker": saved_manifest["ticker"],
        "analysis_profile": saved_manifest["analysis_profile"],
        "timeframe": saved_manifest["timeframe"],
        "manifest_ref": _safe_relative_path(manifest_path, root),
        "payload_ref": saved_manifest["payload_ref"],
    }
    return {"manifest": saved_manifest, "receipt": receipt, "manifest_path": manifest_path, "payload_path": payload_path}


def commit_json_artifact(*, payload: Any, **kwargs: Any) -> dict[str, Any]:
    return commit_artifact_payload(payload=canonical_json_bytes(payload), payload_type=PAYLOAD_TYPE_JSON, payload_extension=".json", **kwargs)


def commit_existing_file_artifact(*, source_path: str | Path, payload_type: str, payload_extension: str | None = None, **kwargs: Any) -> dict[str, Any]:
    path = Path(source_path)
    if not path.exists() or not path.is_file():
        raise ArtifactContractError("Source payload must be an existing regular file.")
    extension = payload_extension or path.suffix or ".bin"
    return commit_artifact_payload(payload=path.read_bytes(), payload_type=payload_type, payload_extension=extension, **kwargs)


def load_manifest(manifest_path: str | Path, *, run_root: str | Path = DEFAULT_RUN_ROOT) -> dict[str, Any]:
    path = Path(manifest_path)
    root = Path(run_root)
    if not path.exists() and not path.is_absolute():
        path = root / path
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except ValueError:
        raise ArtifactContractError("Manifest path must stay within run root.") from None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ArtifactContractError("Manifest must be a JSON object.")
    payload_ref = data.get("payload_ref")
    if not payload_ref:
        raise ArtifactContractError("Manifest payload_ref is required.")
    expected_manifest_path = _manifest_path_from_artifact_ref(root, str(payload_ref))
    if path.resolve(strict=True) != expected_manifest_path.resolve(strict=True):
        raise ArtifactContractError("Manifest path does not match manifest payload reference.")
    validate_manifest(data, run_root=root)
    return data


def validate_manifest(manifest: dict[str, Any], *, run_root: str | Path = DEFAULT_RUN_ROOT) -> None:
    extra_fields = set(manifest) - MANIFEST_FIELDS
    missing_fields = MANIFEST_FIELDS - set(manifest)
    if extra_fields or missing_fields:
        raise ArtifactContractError("Manifest fields must match Artifact Lineage v1 schema exactly.")
    if manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ArtifactContractError("Unsupported artifact manifest schema.")
    for key in (
        "artifact_id",
        "run_id",
        "stage",
        "artifact_type",
        "workflow_type",
        "ticker",
        "analysis_profile",
        "timeframe",
        "source_dataset_identity",
        "source_dataset_digest",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_type",
        "created_at",
    ):
        _required_text(manifest.get(key), key)
    _require_opaque_id(manifest.get("artifact_id"), "artifact_id")
    _require_opaque_id(manifest.get("run_id"), "run_id")
    if manifest["stage"] not in STAGE_DIRECTORY:
        raise ArtifactContractError("Unsupported artifact stage.")
    if manifest["artifact_type"] not in VALID_ARTIFACT_TYPES:
        raise ArtifactContractError("Unsupported artifact type.")
    if STAGE_ARTIFACT_TYPE.get(str(manifest["stage"])) != manifest["artifact_type"]:
        raise ArtifactContractError("Artifact type does not match stage.")
    if manifest["workflow_type"] not in VALID_WORKFLOW_TYPES:
        raise ArtifactContractError("Unsupported workflow type.")
    if manifest["analysis_profile"] not in VALID_ANALYSIS_PROFILES:
        raise ArtifactContractError("Unsupported analysis profile.")
    if manifest["payload_type"] not in VALID_PAYLOAD_TYPES:
        raise ArtifactContractError("Unsupported payload type.")
    try:
        created_at = datetime.fromisoformat(str(manifest["created_at"]).replace("Z", "+00:00"))
    except ValueError:
        raise ArtifactContractError("created_at must be an ISO timestamp.") from None
    if created_at.tzinfo is None or created_at.utcoffset() is None or created_at.utcoffset().total_seconds() != 0:
        raise ArtifactContractError("created_at must be timezone-aware UTC.")
    try:
        payload_byte_size = int(manifest["payload_byte_size"])
    except (TypeError, ValueError):
        raise ArtifactContractError("Manifest payload size must be an integer.") from None
    if payload_byte_size < 0:
        raise ArtifactContractError("Manifest payload size must be nonnegative.")
    payload_path = _path_from_ref(run_root, str(manifest["payload_ref"]))
    if not payload_path.exists() or not payload_path.is_file():
        raise ArtifactContractError("Manifest payload is missing or not a regular file.")
    expected_stage_dir = Path(run_root) / str(manifest["run_id"]) / STAGE_DIRECTORY[str(manifest["stage"])]
    try:
        payload_path.resolve(strict=True).parent.relative_to(expected_stage_dir.resolve(strict=True))
    except ValueError:
        raise ArtifactContractError("Payload path does not match manifest run/stage.") from None
    stat = payload_path.stat()
    if stat.st_size != payload_byte_size:
        raise ArtifactContractError("Manifest payload size mismatch.")
    if sha256_file(payload_path) != manifest["payload_sha256"]:
        raise ArtifactContractError("Manifest payload digest mismatch.")
    source_ref = manifest.get("source_ref")
    if source_ref is not None:
        source_path = _path_from_ref(run_root, str(source_ref))
        if not source_path.exists() or not source_path.is_file():
            raise ArtifactContractError("Manifest source_ref is missing or not a regular file.")
        try:
            source_path.resolve(strict=True).relative_to(Path(run_root).resolve(strict=True))
        except ValueError:
            raise ArtifactContractError("Manifest source_ref must stay within run root.") from None
    if manifest.get("parent_artifact_id") == manifest.get("artifact_id"):
        raise ArtifactContractError("Artifact cannot be its own parent.")
    if manifest.get("parent_artifact_id") is not None:
        _require_opaque_id(manifest.get("parent_artifact_id"), "parent_artifact_id")
    inputs = manifest.get("input_artifact_ids") or []
    if not isinstance(inputs, list):
        raise ArtifactContractError("input_artifact_ids must be a list.")
    for input_id in inputs:
        _require_opaque_id(input_id, "input_artifact_id")
    if len(inputs) != len(set(inputs)):
        raise ArtifactContractError("Duplicate input artifact IDs are not allowed.")
    if manifest.get("artifact_id") in inputs:
        raise ArtifactContractError("Artifact cannot be its own input.")
    lineage_ids = manifest.get("lineage_artifact_ids") or []
    if not isinstance(lineage_ids, list):
        raise ArtifactContractError("lineage_artifact_ids must be a list.")
    for lineage_id in lineage_ids:
        _require_opaque_id(lineage_id, "lineage_artifact_id")
    if len(lineage_ids) != len(set(lineage_ids)):
        raise ArtifactContractError("Duplicate lineage artifact IDs are not allowed.")
    if manifest.get("artifact_id") in lineage_ids:
        raise ArtifactContractError("Artifact cannot include itself in lineage.")


def validate_manifest_chain(
    manifest: dict[str, Any],
    *,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    _seen: set[str] | None = None,
) -> None:
    """Validate a manifest and reconstruct its declared ancestry from saved manifests."""
    validate_manifest(manifest, run_root=run_root)
    artifact_id = str(manifest["artifact_id"])
    seen = set(_seen or set())
    if artifact_id in seen:
        raise ArtifactContractError("Artifact lineage contains a cycle.")
    seen.add(artifact_id)
    parent_id = manifest.get("parent_artifact_id")
    input_ids = manifest.get("input_artifact_ids") or []
    if manifest.get("stage") != STAGE_BATCH_ANALYSIS_V1 and not parent_id:
        raise ArtifactContractError("Derived artifact manifest requires a parent.")
    parent_manifest = None
    if parent_id:
        parent_manifest = _find_manifest_by_artifact_id(
            run_root=run_root,
            run_id=str(manifest["run_id"]),
            artifact_id=str(parent_id),
        )
        validate_manifest_chain(parent_manifest, run_root=run_root, _seen=seen)
    input_manifests = [
        _find_manifest_by_artifact_id(
            run_root=run_root,
            run_id=str(manifest["run_id"]),
            artifact_id=str(input_id),
        )
        for input_id in input_ids
    ]
    for item in input_manifests:
        validate_manifest_chain(item, run_root=run_root, _seen=seen)
    _validate_parent_inputs(
        manifest=manifest,
        parent_manifest=parent_manifest,
        input_manifests=input_manifests,
    )
    expected_lineage_ids = _lineage_ids_for(parent_manifest, input_manifests)
    if manifest.get("lineage_artifact_ids") != expected_lineage_ids:
        raise ArtifactContractError("Declared artifact lineage does not match saved parent/input manifests.")


def validate_child_lineage(
    *,
    child_manifest: dict[str, Any],
    parent_manifest: dict[str, Any],
    input_manifests: list[dict[str, Any]] | None = None,
) -> None:
    _validate_parent_inputs(
        manifest=child_manifest,
        parent_manifest=parent_manifest,
        input_manifests=list(input_manifests or []),
    )


def artifact_receipt(manifest: dict[str, Any], *, run_root: str | Path = DEFAULT_RUN_ROOT) -> dict[str, Any]:
    payload_path = _path_from_ref(run_root, str(manifest["payload_ref"]))
    manifest_path = _manifest_path_from_artifact_ref(run_root, str(manifest["payload_ref"]))
    return {
        "run_id": manifest["run_id"],
        "artifact_id": manifest["artifact_id"],
        "stage": manifest["stage"],
        "artifact_type": manifest["artifact_type"],
        "workflow_type": manifest["workflow_type"],
        "ticker": manifest["ticker"],
        "analysis_profile": manifest["analysis_profile"],
        "timeframe": manifest["timeframe"],
        "manifest_ref": _safe_relative_path(manifest_path, run_root),
        "payload_ref": _safe_relative_path(payload_path, run_root),
    }


def annotated_dataset_artifact(
    *,
    csv_path: str | Path,
    run_root: str | Path,
    run_id: str,
    workflow_type: str,
    ticker: str,
    analysis_profile: str,
    timeframe: str,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    digest = sha256_file(csv_path)
    return commit_existing_file_artifact(
        source_path=csv_path,
        run_root=run_root,
        run_id=run_id,
        stage=STAGE_BATCH_ANALYSIS_V1,
        artifact_type=ARTIFACT_TYPE_ANNOTATED_DATASET,
        workflow_type=workflow_type,
        ticker=ticker,
        analysis_profile=analysis_profile,
        timeframe=timeframe,
        source_dataset_identity=Path(csv_path).name,
        source_dataset_digest=digest,
        source_ref=None,
        payload_type=PAYLOAD_TYPE_CSV,
        payload_extension=".csv",
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        code_commit=code_commit,
    )


def manual_scenario_contract(
    *,
    analysis_manifest: dict[str, Any],
    entry: Any,
    stop_loss: Any,
    take_profit: Any,
    horizon_bars: int,
) -> dict[str, Any]:
    _require_finite_number(entry, "entry")
    _require_finite_number(stop_loss, "stop_loss")
    _require_finite_number(take_profit, "take_profit")
    if not isinstance(horizon_bars, int) or isinstance(horizon_bars, bool) or horizon_bars < 0:
        raise ArtifactContractError("horizon_bars must be a nonnegative integer.")
    contract = {
        "workflow_type": WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        "scenario_origin": SCENARIO_ORIGIN_MANUAL,
        "ticker": analysis_manifest["ticker"],
        "timeframe": analysis_manifest["timeframe"],
        "analysis_profile": analysis_manifest["analysis_profile"],
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "horizon_bars": int(horizon_bars),
        "parent_artifact_id": analysis_manifest["artifact_id"],
        "source_dataset_digest": analysis_manifest["source_dataset_digest"],
    }
    contract["manual_scenario_digest"] = stable_digest(contract)
    return contract


def commit_manual_scenario_artifact(
    *,
    analysis_manifest: dict[str, Any],
    entry: Any,
    stop_loss: Any,
    take_profit: Any,
    horizon_bars: int,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    if analysis_manifest.get("workflow_type") != WORKFLOW_MANUAL_SCENARIO_ANALYSIS:
        raise ArtifactContractError("Manual scenario requires a manual workflow analysis artifact.")
    contract = manual_scenario_contract(
        analysis_manifest=analysis_manifest,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        horizon_bars=horizon_bars,
    )
    return commit_json_artifact(
        payload=contract,
        run_root=run_root,
        run_id=analysis_manifest["run_id"],
        stage=STAGE_MANUAL_SCENARIO_V1,
        artifact_type=ARTIFACT_TYPE_MANUAL_SCENARIO_DEFINITION,
        workflow_type=WORKFLOW_MANUAL_SCENARIO_ANALYSIS,
        ticker=analysis_manifest["ticker"],
        analysis_profile=analysis_manifest["analysis_profile"],
        timeframe=analysis_manifest["timeframe"],
        source_dataset_identity=analysis_manifest["source_dataset_identity"],
        source_dataset_digest=analysis_manifest["source_dataset_digest"],
        source_ref=analysis_manifest.get("payload_ref"),
        code_commit=code_commit,
        manual_scenario_digest=contract["manual_scenario_digest"],
        parent_manifest=analysis_manifest,
        input_manifests=[analysis_manifest],
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
    )


def commit_candidate_core_artifact(
    *,
    analysis_manifest: dict[str, Any],
    candidate: dict[str, Any],
    strategy_config_digest: str,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    if analysis_manifest.get("workflow_type") != WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT:
        raise ArtifactContractError("Candidate core requires a canonical workflow analysis artifact.")
    if candidate.get("candidate_build_success") is not True or candidate.get("rank_eligible") is not True:
        raise ArtifactContractError("Strategy candidate is not actionable.")
    core = candidate_core(candidate)
    for field in ("entry", "stop_loss", "take_profit"):
        _require_finite_number(core.get(field), field)
    digest = stable_digest(core)
    payload = {
        "candidate_core": core,
        "candidate_core_digest": digest,
        "eligibility": {
            "candidate_build_success": True,
            "rank_eligible": True,
        },
        "strategy_config_digest": strategy_config_digest,
    }
    return commit_json_artifact(
        payload=payload,
        run_root=run_root,
        run_id=analysis_manifest["run_id"],
        stage=STAGE_STRATEGY_CANDIDATE_V1,
        artifact_type=ARTIFACT_TYPE_CANDIDATE_CORE,
        workflow_type=WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT,
        ticker=analysis_manifest["ticker"],
        analysis_profile=analysis_manifest["analysis_profile"],
        timeframe=analysis_manifest["timeframe"],
        source_dataset_identity=analysis_manifest["source_dataset_identity"],
        source_dataset_digest=analysis_manifest["source_dataset_digest"],
        source_ref=analysis_manifest.get("payload_ref"),
        code_commit=code_commit,
        strategy_config_digest=strategy_config_digest,
        candidate_core_digest=digest,
        parent_manifest=analysis_manifest,
        input_manifests=[analysis_manifest],
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
    )


def commit_monte_carlo_summary_artifact(
    *,
    parent_manifest: dict[str, Any],
    summary: dict[str, Any],
    workflow_type: str,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    validate_manifest_chain(parent_manifest, run_root=run_root)
    payload = dict(summary)
    params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
    if str(payload.get("tf") or payload.get("timeframe") or "") != str(parent_manifest.get("timeframe")):
        raise ArtifactContractError("Monte Carlo summary timeframe mismatch.")
    parent_payload_ref = parent_manifest.get("payload_ref")
    if not parent_payload_ref:
        raise ArtifactContractError("Parent manifest is missing payload_ref.")
    parent_payload_path = _path_from_ref(run_root, str(parent_payload_ref))
    parent_payload = json.loads(parent_payload_path.read_text(encoding="utf-8"))
    if workflow_type == WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT:
        if parent_manifest.get("artifact_type") != ARTIFACT_TYPE_CANDIDATE_CORE:
            raise ArtifactContractError("Canonical Monte Carlo requires a candidate-core parent.")
        candidate = parent_payload.get("candidate_core") if isinstance(parent_payload, dict) else None
        if not isinstance(candidate, dict):
            raise ArtifactContractError("Candidate parent payload is missing candidate_core.")
        expected = candidate_core(candidate)
        summary_geometry = {
            "entry": params.get("entry"),
            "stop_loss": params.get("sl") if params.get("sl") is not None else params.get("stop_loss"),
            "take_profit": params.get("tp") if params.get("tp") is not None else params.get("take_profit"),
        }
        for field in ("entry", "stop_loss", "take_profit"):
            _require_finite_number(summary_geometry[field], field)
        for field in ("entry", "stop_loss", "take_profit"):
            if summary_geometry[field] != expected.get(field):
                raise ArtifactContractError(f"Monte Carlo summary {field} mismatch.")
            if parent_manifest.get("candidate_core_digest") != stable_digest(expected):
                raise ArtifactContractError("Candidate digest mismatch.")
    else:
        if parent_manifest.get("artifact_type") != ARTIFACT_TYPE_MANUAL_SCENARIO_DEFINITION:
            raise ArtifactContractError("Manual Monte Carlo requires a manual-scenario parent.")
        scenario_digest = parent_manifest.get("manual_scenario_digest")
        if not scenario_digest or parent_payload.get("manual_scenario_digest") != scenario_digest:
            raise ArtifactContractError("Manual scenario digest mismatch.")
        summary_geometry = {
            "entry": params.get("entry"),
            "stop_loss": params.get("sl") if params.get("sl") is not None else params.get("stop_loss"),
            "take_profit": params.get("tp") if params.get("tp") is not None else params.get("take_profit"),
            "horizon_bars": params.get("horizon_bars"),
        }
        for field in ("entry", "stop_loss", "take_profit"):
            _require_finite_number(summary_geometry[field], field)
        if (
            not isinstance(summary_geometry["horizon_bars"], int)
            or isinstance(summary_geometry["horizon_bars"], bool)
            or summary_geometry["horizon_bars"] < 0
        ):
            raise ArtifactContractError("horizon_bars must be a nonnegative integer.")
        for field in ("entry", "stop_loss", "take_profit", "horizon_bars"):
            if summary_geometry[field] != parent_payload.get(field):
                raise ArtifactContractError(f"Monte Carlo summary {field} mismatch.")
    payload["workflow_type"] = workflow_type
    payload["parent_artifact_id"] = parent_manifest["artifact_id"]
    if workflow_type == WORKFLOW_CANONICAL_STRATEGY_DECISION_SUPPORT:
        payload["candidate_core_digest"] = parent_manifest.get("candidate_core_digest")
        payload["strategy_config_digest"] = parent_manifest.get("strategy_config_digest")
    else:
        payload["manual_scenario_digest"] = parent_manifest.get("manual_scenario_digest")
    return commit_json_artifact(
        payload=payload,
        run_root=run_root,
        run_id=parent_manifest["run_id"],
        stage=STAGE_MONTE_CARLO_V1,
        artifact_type=ARTIFACT_TYPE_MONTE_CARLO_SUMMARY,
        workflow_type=workflow_type,
        ticker=parent_manifest["ticker"],
        analysis_profile=parent_manifest["analysis_profile"],
        timeframe=parent_manifest["timeframe"],
        source_dataset_identity=parent_manifest["source_dataset_identity"],
        source_dataset_digest=parent_manifest["source_dataset_digest"],
        source_ref=parent_manifest.get("source_ref"),
        code_commit=code_commit,
        strategy_config_digest=parent_manifest.get("strategy_config_digest"),
        candidate_core_digest=parent_manifest.get("candidate_core_digest"),
        manual_scenario_digest=parent_manifest.get("manual_scenario_digest"),
        parent_manifest=parent_manifest,
        input_manifests=[parent_manifest],
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
    )


def commit_plot_artifact(
    *,
    analysis_manifest: dict[str, Any],
    monte_carlo_manifest: dict[str, Any],
    html_payload: str | bytes,
    workflow_type: str,
    run_root: str | Path = DEFAULT_RUN_ROOT,
    artifact_id: str | None = None,
    artifact_id_factory: Any | None = None,
    code_commit: str | None = None,
) -> dict[str, Any]:
    validate_manifest_chain(analysis_manifest, run_root=run_root)
    validate_manifest_chain(monte_carlo_manifest, run_root=run_root)
    if monte_carlo_manifest["workflow_type"] != workflow_type or analysis_manifest["workflow_type"] != workflow_type:
        raise ArtifactContractError("Plot inputs must use the requested workflow.")
    if monte_carlo_manifest["run_id"] != analysis_manifest["run_id"]:
        raise ArtifactContractError("Plot inputs must use the same run.")
    for key in ("ticker", "timeframe", "analysis_profile", "source_dataset_digest"):
        if monte_carlo_manifest.get(key) != analysis_manifest.get(key):
            raise ArtifactContractError(f"Plot input {key} mismatch.")
    if monte_carlo_manifest.get("artifact_type") != ARTIFACT_TYPE_MONTE_CARLO_SUMMARY:
        raise ArtifactContractError("Plot requires a Monte Carlo summary input.")
    if analysis_manifest["artifact_id"] not in (monte_carlo_manifest.get("lineage_artifact_ids") or []):
        raise ArtifactContractError("Monte Carlo summary does not descend from the analysis artifact.")
    payload = html_payload if isinstance(html_payload, bytes) else html_payload.encode("utf-8")
    return commit_artifact_payload(
        payload=payload,
        run_root=run_root,
        run_id=analysis_manifest["run_id"],
        stage=STAGE_PLOT_V1,
        artifact_type=ARTIFACT_TYPE_ANNOTATED_PLOT,
        workflow_type=workflow_type,
        ticker=analysis_manifest["ticker"],
        analysis_profile=analysis_manifest["analysis_profile"],
        timeframe=analysis_manifest["timeframe"],
        source_dataset_identity=analysis_manifest["source_dataset_identity"],
        source_dataset_digest=analysis_manifest["source_dataset_digest"],
        source_ref=analysis_manifest.get("payload_ref"),
        payload_type=PAYLOAD_TYPE_HTML,
        payload_extension=".html",
        code_commit=code_commit,
        strategy_config_digest=monte_carlo_manifest.get("strategy_config_digest"),
        candidate_core_digest=monte_carlo_manifest.get("candidate_core_digest"),
        manual_scenario_digest=monte_carlo_manifest.get("manual_scenario_digest"),
        parent_manifest=monte_carlo_manifest,
        input_manifests=[analysis_manifest, monte_carlo_manifest],
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
    )


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
