"""Immutable offline historical-data artifact manifests and writers."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import uuid
from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Iterable

from marketflow.historical_data import analytical_segments as segments
from marketflow.historical_data import frozen_calendar as calendar_engine
from marketflow.historical_data import rth_bar_engine as rth
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


HISTORICAL_MANIFEST_SCHEMA_VERSION = "marketflow.historical_data_artifact_manifest.v1"
PROCESSING_ENGINE_VERSION = "marketflow.historical_data.processing_pipeline.v1"
DEFAULT_HISTORICAL_RUN_ROOT = Path(".marketflow") / "historical_data" / "runs"
PAYLOAD_MEDIA_TYPE_CANONICAL_JSON = "application/vnd.marketflow.canonical+json"

ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE = "CALENDAR_SCHEDULE_CANDIDATE"
ARTIFACT_TYPE_NORMALIZED_15M_OHLCV = "NORMALIZED_15M_OHLCV"
ARTIFACT_TYPE_DIVIDEND_EVENT_SET = "DIVIDEND_EVENT_SET"
ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M = "DERIVED_SWING_RTH_HALF_SESSION_195M"
ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D = "DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D"
ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP = "ANALYTICAL_SEGMENT_MAP"
ARTIFACT_TYPE_HISTORICAL_PIPELINE_RECEIPT = "HISTORICAL_PIPELINE_RECEIPT"

STAGE_CALENDAR = "calendar_schedule_candidate"
STAGE_NORMALIZED_SOURCE = "normalized_15m_ohlcv"
STAGE_DIVIDEND_EVENTS = "dividend_event_set"
STAGE_DERIVED_PROFILE = "derived_profile"
STAGE_SEGMENT_MAP = "analytical_segment_map"
STAGE_PIPELINE_RECEIPT = "historical_pipeline_receipt"

SYNTHETIC_OFFLINE_FIXTURE = "SYNTHETIC_OFFLINE_FIXTURE"

PIPELINE_COMPLETED = "PIPELINE_COMPLETED"
PIPELINE_PARTIAL = "PIPELINE_PARTIAL"
PIPELINE_BLOCKED = "PIPELINE_BLOCKED"
PIPELINE_INVALID = "PIPELINE_INVALID"

MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_id",
        "run_id",
        "artifact_type",
        "stage",
        "created_at_utc",
        "contract_v2_1_digest",
        "contract_v2_base_digest",
        "processing_engine_version",
        "profile_id",
        "canonical_bar_type",
        "requested_primary_listing_mic",
        "requested_calendar_token",
        "resolved_calendar",
        "primary_parent_artifact_id",
        "primary_parent_manifest_ref",
        "input_artifact_ids",
        "input_manifest_refs",
        "lineage_artifact_ids",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_media_type",
        "semantic_payload_digest",
    }
)

STAGE_BY_TYPE = {
    ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE: STAGE_CALENDAR,
    ARTIFACT_TYPE_NORMALIZED_15M_OHLCV: STAGE_NORMALIZED_SOURCE,
    ARTIFACT_TYPE_DIVIDEND_EVENT_SET: STAGE_DIVIDEND_EVENTS,
    ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M: STAGE_DERIVED_PROFILE,
    ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D: STAGE_DERIVED_PROFILE,
    ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP: STAGE_SEGMENT_MAP,
    ARTIFACT_TYPE_HISTORICAL_PIPELINE_RECEIPT: STAGE_PIPELINE_RECEIPT,
}

STAGE_DIRECTORY = {
    STAGE_CALENDAR: "calendar",
    STAGE_NORMALIZED_SOURCE: "source_15m",
    STAGE_DIVIDEND_EVENTS: "dividends",
    STAGE_DERIVED_PROFILE: "derived",
    STAGE_SEGMENT_MAP: "segments",
    STAGE_PIPELINE_RECEIPT: "receipt",
}

CANONICAL_BAR_TYPE_BY_ARTIFACT = {
    ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M: rth.RTH_HALF_SESSION_195M,
    ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D: rth.RTH_FULL_SESSION_1D,
}

PROFILE_BY_DERIVED_ARTIFACT = {
    ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M: rth.PROFILE_SWING,
    ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D: rth.PROFILE_POSITION_SWING,
}

WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


class HistoricalArtifactError(ValueError):
    """Raised when historical-data artifact lineage is invalid."""


@dataclass(frozen=True, slots=True)
class HistoricalRunContext:
    run_id: str
    created_at_utc: str
    run_ref: str


@dataclass(frozen=True, slots=True)
class DividendEventRecord:
    event_id: str
    ex_dividend_date: str


def _contract_v2_digest() -> str:
    return contract_v2.contract_digest(contract_v2.default_contract())


def _contract_v21_digest() -> str:
    contract = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(contract)
    return contract_v21.contract_digest(contract)


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise HistoricalArtifactError("timestamp must be timezone-aware")
    if value.utcoffset() != UTC.utcoffset(value):
        raise HistoricalArtifactError("timestamp must be UTC")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _canonicalize(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _canonicalize(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _canonicalize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_canonicalize(item) for item in value]
    if isinstance(value, datetime):
        return _utc_iso(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        if value.is_nan() or value.is_infinite():
            raise HistoricalArtifactError("Decimal values must be finite")
        return rth._decimal_text(value)
    if isinstance(value, float):
        raise HistoricalArtifactError("canonical historical payloads must not contain binary floats")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 canonical JSON payload bytes."""
    try:
        return (
            json.dumps(
                _canonicalize(value),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise HistoricalArtifactError("historical payload must be deterministic finite JSON") from exc


def semantic_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_text(value: object, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise HistoricalArtifactError(f"{field_name} is required")
    return str(value).strip()


def _require_opaque_id(value: object, field_name: str) -> str:
    text = _required_text(value, field_name)
    if (
        any(separator in text for separator in ("/", "\\", "..", "*", "?", "[", "]", ":"))
        or "\x00" in text
        or text.rstrip(" .") != text
        or text.upper() in WINDOWS_DEVICE_NAMES
    ):
        raise HistoricalArtifactError(f"{field_name} must be opaque and path-safe")
    return text


def _safe_ref_to_path(root: str | Path, ref: str) -> Path:
    text = str(ref)
    parts = Path(text).parts
    if (
        not text
        or text.startswith(("/", "\\", "~"))
        or text.startswith("//")
        or text.startswith("\\\\")
        or "\\" in text
        or ":" in text
        or "\x00" in text
        or Path(text).is_absolute()
        or ".." in parts
        or any(part in {"", ".", ".."} for part in parts)
        or any(part.rstrip(" .").upper() in WINDOWS_DEVICE_NAMES for part in parts)
        or any(part != part.rstrip(" .") for part in parts)
    ):
        raise HistoricalArtifactError("artifact reference must be a safe relative path")
    return Path(root) / Path(text)


def _safe_relative_path(path: str | Path, root: str | Path) -> str:
    root_path = Path(root).resolve(strict=False)
    path_obj = Path(path)
    if path_obj.is_symlink():
        raise HistoricalArtifactError("artifact path must be a regular file")
    try:
        relative = path_obj.resolve(strict=False).relative_to(root_path)
    except ValueError:
        raise HistoricalArtifactError("artifact path must stay within historical run root") from None
    return _safe_ref_to_path(".", relative.as_posix()).as_posix()


def _created_at_utc(value: str | None = None) -> str:
    if value is None:
        return datetime.now(UTC).isoformat().replace("+00:00", "Z")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise HistoricalArtifactError("created_at_utc must be timezone-aware UTC")
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _lineage_ids(
    primary_parent_manifest: dict[str, Any] | None,
    input_manifests: Iterable[dict[str, Any]],
) -> list[str]:
    ids: list[str] = []
    for manifest in (primary_parent_manifest, *tuple(input_manifests)):
        if not manifest:
            continue
        artifact_id = str(manifest["artifact_id"])
        if artifact_id not in ids:
            ids.append(artifact_id)
        for ancestor in manifest.get("lineage_artifact_ids") or []:
            if str(ancestor) not in ids:
                ids.append(str(ancestor))
    return ids


def create_historical_run(
    *,
    run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT,
    run_id: str | None = None,
    run_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> HistoricalRunContext:
    """Create one immutable offline historical processing run directory."""
    run_id_text = _require_opaque_id(run_id if run_id is not None else (run_id_factory() if run_id_factory else f"hist-{uuid.uuid4().hex}"), "run_id")
    root = Path(run_root)
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / run_id_text
    try:
        run_dir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        raise HistoricalArtifactError("historical run directory already exists") from None
    return HistoricalRunContext(
        run_id=run_id_text,
        created_at_utc=_created_at_utc(created_at_utc),
        run_ref=_safe_relative_path(run_dir, root),
    )


def _write_temp_bytes(directory: Path, payload: bytes, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".tmp-", suffix=suffix, dir=str(directory))
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return Path(temp_name)


def _install_without_replace(temp_path: Path, final_path: Path) -> None:
    if final_path.exists():
        raise HistoricalArtifactError("artifact output already exists")
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


def _manifest_path_from_payload_ref(root: str | Path, payload_ref: str) -> Path:
    payload_path = _safe_ref_to_path(root, payload_ref)
    return payload_path.with_suffix(payload_path.suffix + ".manifest.json")


def _build_manifest(
    *,
    artifact_id: str,
    run_id: str,
    artifact_type: str,
    created_at_utc: str | None,
    payload_ref: str,
    payload_sha256: str,
    payload_byte_size: int,
    semantic_payload_digest: str,
    profile_id: str | None = None,
    canonical_bar_type: str | None = None,
    requested_primary_listing_mic: str | None = None,
    requested_calendar_token: str | None = None,
    resolved_calendar: str | None = None,
    primary_parent_manifest: dict[str, Any] | None = None,
    primary_parent_manifest_ref: str | None = None,
    input_manifests: tuple[dict[str, Any], ...] = (),
    input_manifest_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    artifact_id_text = _require_opaque_id(artifact_id, "artifact_id")
    run_id_text = _require_opaque_id(run_id, "run_id")
    if artifact_type not in STAGE_BY_TYPE:
        raise HistoricalArtifactError("unsupported historical artifact type")
    if len(input_manifests) != len(input_manifest_refs):
        raise HistoricalArtifactError("input manifest references must match input manifests")
    input_ids = [str(item["artifact_id"]) for item in input_manifests]
    if len(input_ids) != len(set(input_ids)):
        raise HistoricalArtifactError("duplicate input artifact IDs are not allowed")
    primary_parent_id = str(primary_parent_manifest["artifact_id"]) if primary_parent_manifest else None
    if artifact_id_text == primary_parent_id or artifact_id_text in input_ids:
        raise HistoricalArtifactError("artifact cannot be its own parent or input")
    if primary_parent_id and primary_parent_id in input_ids:
        raise HistoricalArtifactError("primary parent must not be repeated as an additional input")
    for manifest in (primary_parent_manifest, *input_manifests):
        if manifest and manifest.get("run_id") != run_id_text:
            raise HistoricalArtifactError("cross-run parentage is not allowed")
        if manifest and manifest.get("contract_v2_1_digest") != _contract_v21_digest():
            raise HistoricalArtifactError("input Contract v2.1 digest mismatch")
    return {
        "schema_version": HISTORICAL_MANIFEST_SCHEMA_VERSION,
        "artifact_id": artifact_id_text,
        "run_id": run_id_text,
        "artifact_type": artifact_type,
        "stage": STAGE_BY_TYPE[artifact_type],
        "created_at_utc": _created_at_utc(created_at_utc),
        "contract_v2_1_digest": _contract_v21_digest(),
        "contract_v2_base_digest": _contract_v2_digest(),
        "processing_engine_version": PROCESSING_ENGINE_VERSION,
        "profile_id": profile_id,
        "canonical_bar_type": canonical_bar_type,
        "requested_primary_listing_mic": requested_primary_listing_mic,
        "requested_calendar_token": requested_calendar_token,
        "resolved_calendar": resolved_calendar,
        "primary_parent_artifact_id": primary_parent_id,
        "primary_parent_manifest_ref": primary_parent_manifest_ref,
        "input_artifact_ids": input_ids,
        "input_manifest_refs": list(input_manifest_refs),
        "lineage_artifact_ids": _lineage_ids(primary_parent_manifest, input_manifests),
        "payload_ref": payload_ref,
        "payload_sha256": payload_sha256,
        "payload_byte_size": int(payload_byte_size),
        "payload_media_type": PAYLOAD_MEDIA_TYPE_CANONICAL_JSON,
        "semantic_payload_digest": semantic_payload_digest,
    }


def _validate_manifest_shape(manifest: dict[str, Any]) -> None:
    extra = set(manifest) - MANIFEST_FIELDS
    missing = MANIFEST_FIELDS - set(manifest)
    if extra or missing:
        raise HistoricalArtifactError("historical manifest fields must match schema exactly")
    if manifest["schema_version"] != HISTORICAL_MANIFEST_SCHEMA_VERSION:
        raise HistoricalArtifactError("unsupported historical manifest schema")
    _require_opaque_id(manifest["artifact_id"], "artifact_id")
    _require_opaque_id(manifest["run_id"], "run_id")
    artifact_type = str(manifest["artifact_type"])
    if artifact_type not in STAGE_BY_TYPE:
        raise HistoricalArtifactError("unsupported historical artifact type")
    if manifest["stage"] != STAGE_BY_TYPE[artifact_type]:
        raise HistoricalArtifactError("historical artifact type does not match stage")
    _created_at_utc(str(manifest["created_at_utc"]))
    if manifest["contract_v2_1_digest"] != _contract_v21_digest():
        raise HistoricalArtifactError("Contract v2.1 digest mismatch")
    if manifest["contract_v2_base_digest"] != _contract_v2_digest():
        raise HistoricalArtifactError("Contract v2 digest mismatch")
    if manifest["processing_engine_version"] != PROCESSING_ENGINE_VERSION:
        raise HistoricalArtifactError("processing-engine version mismatch")
    if manifest["payload_media_type"] != PAYLOAD_MEDIA_TYPE_CANONICAL_JSON:
        raise HistoricalArtifactError("unsupported historical payload media type")
    for digest_field in ("payload_sha256", "semantic_payload_digest"):
        text = _required_text(manifest[digest_field], digest_field)
        if len(text) != 64 or any(char not in "0123456789abcdef" for char in text):
            raise HistoricalArtifactError(f"{digest_field} must be a SHA-256 hex digest")
    try:
        size = int(manifest["payload_byte_size"])
    except (TypeError, ValueError):
        raise HistoricalArtifactError("payload_byte_size must be an integer") from None
    if size < 0:
        raise HistoricalArtifactError("payload_byte_size must be nonnegative")
    inputs = manifest["input_artifact_ids"]
    input_refs = manifest["input_manifest_refs"]
    if not isinstance(inputs, list) or not isinstance(input_refs, list):
        raise HistoricalArtifactError("input artifact IDs and refs must be ordered lists")
    if len(inputs) != len(input_refs):
        raise HistoricalArtifactError("input artifact IDs and refs must have the same length")
    for item in inputs:
        _require_opaque_id(item, "input_artifact_id")
    if len(inputs) != len(set(inputs)):
        raise HistoricalArtifactError("duplicate input artifact IDs are not allowed")
    if manifest["artifact_id"] in inputs or manifest["primary_parent_artifact_id"] == manifest["artifact_id"]:
        raise HistoricalArtifactError("artifact cannot be its own parent or input")
    if manifest["primary_parent_artifact_id"] is not None:
        _require_opaque_id(manifest["primary_parent_artifact_id"], "primary_parent_artifact_id")
        if not manifest["primary_parent_manifest_ref"]:
            raise HistoricalArtifactError("primary parent manifest ref is required")
    if manifest["primary_parent_manifest_ref"] is not None:
        _safe_ref_to_path(".", str(manifest["primary_parent_manifest_ref"]))
    for ref in input_refs:
        _safe_ref_to_path(".", str(ref))
    lineage = manifest["lineage_artifact_ids"]
    if not isinstance(lineage, list):
        raise HistoricalArtifactError("lineage_artifact_ids must be a list")
    for item in lineage:
        _require_opaque_id(item, "lineage_artifact_id")
    if len(lineage) != len(set(lineage)):
        raise HistoricalArtifactError("duplicate lineage artifact IDs are not allowed")
    if manifest["artifact_id"] in lineage:
        raise HistoricalArtifactError("artifact cannot include itself in lineage")


def _load_json_payload(manifest: dict[str, Any], *, run_root: str | Path) -> Any:
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    if payload_path.is_symlink() or not payload_path.exists() or not payload_path.is_file():
        raise HistoricalArtifactError("manifest payload is missing or not a regular file")
    try:
        payload_path.resolve(strict=True).relative_to(Path(run_root).resolve(strict=True))
    except ValueError:
        raise HistoricalArtifactError("payload path must stay within historical run root") from None
    if payload_path.stat().st_size != int(manifest["payload_byte_size"]):
        raise HistoricalArtifactError("manifest payload size mismatch")
    if sha256_file(payload_path) != manifest["payload_sha256"]:
        raise HistoricalArtifactError("manifest payload digest mismatch")
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    if semantic_digest(payload) != manifest["semantic_payload_digest"]:
        raise HistoricalArtifactError("manifest semantic payload digest mismatch")
    return payload


def load_historical_manifest(manifest_ref: str | Path, *, run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT) -> dict[str, Any]:
    """Load and validate one historical artifact manifest by explicit reference."""
    ref_path = Path(manifest_ref)
    root = Path(run_root)
    path = ref_path if ref_path.is_absolute() else _safe_ref_to_path(root, str(manifest_ref))
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except FileNotFoundError:
        raise HistoricalArtifactError("manifest is missing or not a regular file") from None
    except ValueError:
        raise HistoricalArtifactError("manifest path must stay within historical run root") from None
    if path.is_symlink() or not path.exists() or not path.is_file():
        raise HistoricalArtifactError("manifest is missing or not a regular file")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise HistoricalArtifactError("historical manifest must be a JSON object")
    expected = _manifest_path_from_payload_ref(root, str(data.get("payload_ref")))
    if path.resolve(strict=True) != expected.resolve(strict=True):
        raise HistoricalArtifactError("manifest path does not match payload reference")
    validate_historical_manifest(data, run_root=root)
    return data


def validate_historical_manifest(manifest: dict[str, Any], *, run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT) -> None:
    _validate_manifest_shape(manifest)
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    if payload_path.is_symlink() or not payload_path.exists() or not payload_path.is_file():
        raise HistoricalArtifactError("manifest payload is missing or not a regular file")
    expected_stage_dir = Path(run_root) / str(manifest["run_id"]) / STAGE_DIRECTORY[str(manifest["stage"])]
    try:
        payload_path.resolve(strict=True).parent.relative_to(expected_stage_dir.resolve(strict=True))
    except ValueError:
        raise HistoricalArtifactError("payload path does not match manifest run/stage") from None
    payload = _load_json_payload(manifest, run_root=run_root)
    _validate_payload_contract(manifest, payload)


def validate_historical_manifest_chain(
    manifest: dict[str, Any],
    *,
    run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT,
    _seen: set[str] | None = None,
) -> None:
    """Validate a saved historical manifest and its declared refs from disk."""
    validate_historical_manifest(manifest, run_root=run_root)
    artifact_id = str(manifest["artifact_id"])
    seen = set(_seen or set())
    if artifact_id in seen:
        raise HistoricalArtifactError("historical artifact lineage contains a cycle")
    seen.add(artifact_id)
    parent_manifest = None
    if manifest.get("primary_parent_manifest_ref"):
        parent_manifest = load_historical_manifest(str(manifest["primary_parent_manifest_ref"]), run_root=run_root)
        if parent_manifest["artifact_id"] != manifest["primary_parent_artifact_id"]:
            raise HistoricalArtifactError("primary parent artifact ID does not match manifest ref")
        validate_historical_manifest_chain(parent_manifest, run_root=run_root, _seen=seen)
    input_manifests = tuple(load_historical_manifest(str(ref), run_root=run_root) for ref in manifest["input_manifest_refs"])
    for expected_id, input_manifest in zip(manifest["input_artifact_ids"], input_manifests, strict=True):
        if input_manifest["artifact_id"] != expected_id:
            raise HistoricalArtifactError("input artifact ID does not match manifest ref")
        validate_historical_manifest_chain(input_manifest, run_root=run_root, _seen=seen)
    _validate_lineage_transition(manifest, parent_manifest, input_manifests)
    if manifest["lineage_artifact_ids"] != _lineage_ids(parent_manifest, input_manifests):
        raise HistoricalArtifactError("declared lineage does not match saved parent/input manifests")


def _validate_lineage_transition(
    manifest: dict[str, Any],
    primary_parent: dict[str, Any] | None,
    inputs: tuple[dict[str, Any], ...],
) -> None:
    artifact_type = str(manifest["artifact_type"])
    for item in (primary_parent, *inputs):
        if item and item["run_id"] != manifest["run_id"]:
            raise HistoricalArtifactError("cross-run parentage is not allowed")
        if item and item["contract_v2_1_digest"] != manifest["contract_v2_1_digest"]:
            raise HistoricalArtifactError("input Contract v2.1 digest mismatch")
    if artifact_type in {
        ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE,
        ARTIFACT_TYPE_NORMALIZED_15M_OHLCV,
        ARTIFACT_TYPE_DIVIDEND_EVENT_SET,
    }:
        if primary_parent or inputs:
            raise HistoricalArtifactError("root historical artifacts must not declare parents")
        return
    if artifact_type in {
        ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M,
        ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D,
    }:
        if not primary_parent or primary_parent["artifact_type"] != ARTIFACT_TYPE_NORMALIZED_15M_OHLCV:
            raise HistoricalArtifactError("derived profile artifact requires normalized source parent")
        if len(inputs) != 1 or inputs[0]["artifact_type"] != ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE:
            raise HistoricalArtifactError("derived profile artifact requires calendar input")
        if manifest["profile_id"] != PROFILE_BY_DERIVED_ARTIFACT[artifact_type]:
            raise HistoricalArtifactError("derived profile does not match artifact type")
        if manifest["canonical_bar_type"] != CANONICAL_BAR_TYPE_BY_ARTIFACT[artifact_type]:
            raise HistoricalArtifactError("derived canonical bar type mismatch")
        if manifest["requested_primary_listing_mic"] != inputs[0]["requested_primary_listing_mic"]:
            raise HistoricalArtifactError("derived requested MIC mismatch")
        return
    if artifact_type == ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP:
        if not primary_parent or primary_parent["artifact_type"] not in {
            ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M,
            ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D,
        }:
            raise HistoricalArtifactError("segment map requires a derived profile parent")
        if len(inputs) != 1 or inputs[0]["artifact_type"] != ARTIFACT_TYPE_DIVIDEND_EVENT_SET:
            raise HistoricalArtifactError("segment map requires dividend-event input")
        if manifest["profile_id"] != primary_parent["profile_id"]:
            raise HistoricalArtifactError("segment map profile mismatch")
        return
    if artifact_type == ARTIFACT_TYPE_HISTORICAL_PIPELINE_RECEIPT:
        if primary_parent is not None:
            raise HistoricalArtifactError("pipeline receipt must not declare a primary parent")
        if not inputs:
            raise HistoricalArtifactError("pipeline receipt requires input artifacts")
        return
    raise HistoricalArtifactError("unsupported historical lineage transition")


def _validate_payload_contract(manifest: dict[str, Any], payload: Any) -> None:
    if not isinstance(payload, dict):
        raise HistoricalArtifactError("historical artifact payload must be a JSON object")
    artifact_type = manifest["artifact_type"]
    if payload.get("artifact_type") != artifact_type:
        raise HistoricalArtifactError("payload artifact type mismatch")
    if payload.get("contract_v2_1_digest") != manifest["contract_v2_1_digest"]:
        raise HistoricalArtifactError("payload Contract v2.1 digest mismatch")
    if artifact_type == ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE and payload.get("calendar_status") == "OPERATOR_FROZEN":
        raise HistoricalArtifactError("calendar candidate must not claim operator freeze")
    if artifact_type == ARTIFACT_TYPE_NORMALIZED_15M_OHLCV:
        if payload.get("provenance_classification") != SYNTHETIC_OFFLINE_FIXTURE:
            raise HistoricalArtifactError("synthetic source provenance classification is required")
    if artifact_type in PROFILE_BY_DERIVED_ARTIFACT:
        if payload.get("profile") != manifest["profile_id"]:
            raise HistoricalArtifactError("derived payload profile mismatch")
        if payload.get("canonical_bar_type") != manifest["canonical_bar_type"]:
            raise HistoricalArtifactError("derived payload canonical bar type mismatch")
    if artifact_type == ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP and payload.get("profile") != manifest["profile_id"]:
        raise HistoricalArtifactError("segment payload profile mismatch")


def historical_artifact_receipt(manifest: dict[str, Any], *, run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT) -> dict[str, Any]:
    payload_path = _safe_ref_to_path(run_root, str(manifest["payload_ref"]))
    manifest_path = _manifest_path_from_payload_ref(run_root, str(manifest["payload_ref"]))
    return {
        "run_id": manifest["run_id"],
        "artifact_id": manifest["artifact_id"],
        "artifact_type": manifest["artifact_type"],
        "stage": manifest["stage"],
        "profile_id": manifest["profile_id"],
        "canonical_bar_type": manifest["canonical_bar_type"],
        "manifest_ref": _safe_relative_path(manifest_path, run_root),
        "payload_ref": _safe_relative_path(payload_path, run_root),
        "semantic_payload_digest": manifest["semantic_payload_digest"],
    }


def _commit_payload(
    *,
    payload: dict[str, Any],
    run_root: str | Path,
    run_id: str,
    artifact_type: str,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
    profile_id: str | None = None,
    canonical_bar_type: str | None = None,
    requested_primary_listing_mic: str | None = None,
    requested_calendar_token: str | None = None,
    resolved_calendar: str | None = None,
    primary_parent_manifest: dict[str, Any] | None = None,
    primary_parent_manifest_ref: str | None = None,
    input_manifests: tuple[dict[str, Any], ...] = (),
    input_manifest_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    root = Path(run_root)
    run_dir = root / _require_opaque_id(run_id, "run_id")
    if not run_dir.exists() or not run_dir.is_dir():
        raise HistoricalArtifactError("historical run directory does not exist")
    stage = STAGE_BY_TYPE[artifact_type]
    stage_dir = run_dir / STAGE_DIRECTORY[stage]
    stage_dir.mkdir(parents=True, exist_ok=True)
    artifact_id_text = _require_opaque_id(artifact_id or (artifact_id_factory() if artifact_id_factory else f"hist-art-{uuid.uuid4().hex}"), "artifact_id")
    payload_path = stage_dir / f"{artifact_id_text}.json"
    manifest_path = stage_dir / f"{artifact_id_text}.json.manifest.json"
    if payload_path.exists() or manifest_path.exists():
        raise HistoricalArtifactError("artifact output already exists")
    payload_bytes = canonical_json_bytes(payload)
    payload_ref = _safe_relative_path(payload_path, root)
    manifest = _build_manifest(
        artifact_id=artifact_id_text,
        run_id=run_id,
        artifact_type=artifact_type,
        created_at_utc=created_at_utc,
        payload_ref=payload_ref,
        payload_sha256=sha256_bytes(payload_bytes),
        payload_byte_size=len(payload_bytes),
        semantic_payload_digest=semantic_digest(payload),
        profile_id=profile_id,
        canonical_bar_type=canonical_bar_type,
        requested_primary_listing_mic=requested_primary_listing_mic,
        requested_calendar_token=requested_calendar_token,
        resolved_calendar=resolved_calendar,
        primary_parent_manifest=primary_parent_manifest,
        primary_parent_manifest_ref=primary_parent_manifest_ref,
        input_manifests=input_manifests,
        input_manifest_refs=input_manifest_refs,
    )
    validate_historical_manifest_shape_without_payload(manifest)
    _validate_lineage_transition(manifest, primary_parent_manifest, input_manifests)
    temp_payload = _write_temp_bytes(stage_dir, payload_bytes, ".payload.tmp")
    try:
        _install_without_replace(temp_payload, payload_path)
        manifest_bytes = canonical_json_bytes(manifest)
        temp_manifest = _write_temp_bytes(stage_dir, manifest_bytes, ".manifest.tmp")
        _install_without_replace(temp_manifest, manifest_path)
    except Exception:
        try:
            if payload_path.exists() and not manifest_path.exists():
                payload_path.unlink()
        except OSError:
            pass
        raise
    saved_manifest = load_historical_manifest(_safe_relative_path(manifest_path, root), run_root=root)
    validate_historical_manifest_chain(saved_manifest, run_root=root)
    return {
        "manifest": saved_manifest,
        "receipt": historical_artifact_receipt(saved_manifest, run_root=root),
        "manifest_path": manifest_path,
        "payload_path": payload_path,
    }


def validate_historical_manifest_shape_without_payload(manifest: dict[str, Any]) -> None:
    _validate_manifest_shape(manifest)


def calendar_payload(calendar: calendar_engine.FrozenCalendar) -> dict[str, Any]:
    return {
        "artifact_type": ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE,
        "schema_version": "marketflow.historical_data.calendar_candidate_payload.v1",
        "contract_v2_1_digest": calendar.contract_v2_1_digest,
        "requested_primary_listing_mic": calendar.requested_primary_listing_mic,
        "requested_calendar_token": calendar.requested_calendar_token,
        "resolved_calendar": calendar.resolved_calendar,
        "calendar_alias_relationship": calendar.calendar_alias_relationship,
        "exchange_calendars_version": calendar.exchange_calendars_version,
        "tzdata_version": calendar.tzdata_version,
        "fixed_start_date": calendar.fixed_start_date,
        "fixed_end_date": calendar.fixed_end_date,
        "official_exchange_evidence_identity": calendar.official_exchange_evidence_identity,
        "official_exchange_evidence_digest": calendar.official_exchange_evidence_digest,
        "source_timezone": calendar.source_timezone,
        "canonical_timezone": calendar.canonical_timezone,
        "calendar_status": calendar.status,
        "session_schedule_digest": calendar.semantic_digest,
        "sessions": [asdict(session) for session in calendar.sessions],
    }


def commit_calendar_candidate_artifact(
    *,
    calendar: calendar_engine.FrozenCalendar,
    run_root: str | Path,
    run_id: str,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    payload = calendar_payload(calendar)
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=run_id,
        artifact_type=ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
        requested_primary_listing_mic=calendar.requested_primary_listing_mic,
        requested_calendar_token=calendar.requested_calendar_token,
        resolved_calendar=calendar.resolved_calendar,
    )


def normalized_source_payload(
    source_bars: tuple[rth.SourceBar, ...],
    *,
    provenance_classification: str = SYNTHETIC_OFFLINE_FIXTURE,
) -> dict[str, Any]:
    source_tuple = tuple(source_bars)
    starts = [bar.window_start_utc for bar in source_tuple]
    if starts != sorted(starts):
        raise HistoricalArtifactError("normalized source bars must be chronological")
    if len(starts) != len(set(starts)):
        raise HistoricalArtifactError("normalized source bars must not contain duplicate starts")
    records = [bar.semantic_payload() for bar in source_tuple]
    return {
        "artifact_type": ARTIFACT_TYPE_NORMALIZED_15M_OHLCV,
        "schema_version": "marketflow.historical_data.normalized_15m_payload.v1",
        "contract_v2_1_digest": _contract_v21_digest(),
        "source_timestamp_semantic": rth.SOURCE_TIMESTAMP_SEMANTIC,
        "source_interval": "PT15M",
        "provenance_classification": provenance_classification,
        "records": records,
        "source_bar_count": len(records),
        "source_timestamp_set_digest": calendar_engine.semantic_digest([record["window_start_utc"] for record in records]),
        "semantic_source_digest": semantic_digest(records),
    }


def commit_normalized_15m_artifact(
    *,
    source_bars: tuple[rth.SourceBar, ...],
    run_root: str | Path,
    run_id: str,
    provenance_classification: str = SYNTHETIC_OFFLINE_FIXTURE,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    payload = normalized_source_payload(source_bars, provenance_classification=provenance_classification)
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=run_id,
        artifact_type=ARTIFACT_TYPE_NORMALIZED_15M_OHLCV,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
    )


def dividend_event_set_payload(
    events: tuple[DividendEventRecord, ...],
    *,
    evidence_classification: str = SYNTHETIC_OFFLINE_FIXTURE,
) -> dict[str, Any]:
    if evidence_classification != SYNTHETIC_OFFLINE_FIXTURE:
        raise HistoricalArtifactError("only explicit synthetic offline dividend evidence is supported in this task")
    normalized = tuple(sorted(events, key=lambda item: (item.ex_dividend_date, item.event_id)))
    event_ids = [event.event_id for event in normalized]
    if len(event_ids) != len(set(event_ids)):
        raise HistoricalArtifactError("dividend event IDs must be unique")
    for event in normalized:
        _require_opaque_id(event.event_id, "dividend_event_id")
        date.fromisoformat(event.ex_dividend_date)
    records = [{"event_id": event.event_id, "ex_dividend_date": event.ex_dividend_date} for event in normalized]
    event_digest = semantic_digest(records)
    return {
        "artifact_type": ARTIFACT_TYPE_DIVIDEND_EVENT_SET,
        "schema_version": "marketflow.historical_data.dividend_event_set_payload.v1",
        "contract_v2_1_digest": _contract_v21_digest(),
        "evidence_classification": evidence_classification,
        "events": records,
        "event_count": len(records),
        "event_set_semantic_digest": event_digest,
    }


def commit_dividend_event_set_artifact(
    *,
    events: tuple[DividendEventRecord, ...],
    run_root: str | Path,
    run_id: str,
    evidence_classification: str = SYNTHETIC_OFFLINE_FIXTURE,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    payload = dividend_event_set_payload(events, evidence_classification=evidence_classification)
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=run_id,
        artifact_type=ARTIFACT_TYPE_DIVIDEND_EVENT_SET,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
    )


def load_historical_payload(manifest_or_ref: dict[str, Any] | str | Path, *, run_root: str | Path = DEFAULT_HISTORICAL_RUN_ROOT) -> Any:
    manifest = manifest_or_ref if isinstance(manifest_or_ref, dict) else load_historical_manifest(manifest_or_ref, run_root=run_root)
    validate_historical_manifest(manifest, run_root=run_root)
    return _load_json_payload(manifest, run_root=run_root)


def calendar_from_payload(payload: dict[str, Any]) -> calendar_engine.FrozenCalendar:
    sessions = tuple(calendar_engine.FrozenCalendarSession(**item) for item in payload["sessions"])
    return calendar_engine.FrozenCalendar(
        schema_version=calendar_engine.CALENDAR_SCHEMA_VERSION,
        contract_v2_1_digest=payload["contract_v2_1_digest"],
        requested_primary_listing_mic=payload["requested_primary_listing_mic"],
        requested_calendar_token=payload["requested_calendar_token"],
        resolved_calendar=payload["resolved_calendar"],
        calendar_alias_relationship=payload["calendar_alias_relationship"],
        exchange_calendars_version=payload["exchange_calendars_version"],
        tzdata_version=payload["tzdata_version"],
        fixed_start_date=payload["fixed_start_date"],
        fixed_end_date=payload["fixed_end_date"],
        source_timezone=payload["source_timezone"],
        canonical_timezone=payload["canonical_timezone"],
        official_exchange_evidence_identity=payload["official_exchange_evidence_identity"],
        official_exchange_evidence_digest=payload["official_exchange_evidence_digest"],
        status=payload["calendar_status"],
        sessions=sessions,
        semantic_digest=payload["session_schedule_digest"],
    )


def source_bars_from_payload(payload: dict[str, Any]) -> tuple[rth.SourceBar, ...]:
    return tuple(
        rth.SourceBar.build(
            window_start_utc=datetime.fromisoformat(record["window_start_utc"].replace("Z", "+00:00")),
            window_end_utc=datetime.fromisoformat(record["window_end_utc"].replace("Z", "+00:00")),
            open=record["open"],
            high=record["high"],
            low=record["low"],
            close=record["close"],
            volume=record["volume"],
        )
        for record in payload["records"]
    )


def _manifest_ref(manifest: dict[str, Any], *, run_root: str | Path) -> str:
    return _safe_relative_path(_manifest_path_from_payload_ref(run_root, str(manifest["payload_ref"])), run_root)


def commit_derived_profile_artifact(
    *,
    calendar_manifest_ref: str,
    source_manifest_ref: str,
    profile: str,
    run_root: str | Path,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    calendar_manifest = load_historical_manifest(calendar_manifest_ref, run_root=run_root)
    source_manifest = load_historical_manifest(source_manifest_ref, run_root=run_root)
    validate_historical_manifest_chain(calendar_manifest, run_root=run_root)
    validate_historical_manifest_chain(source_manifest, run_root=run_root)
    if calendar_manifest["artifact_type"] != ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE:
        raise HistoricalArtifactError("derived profile requires calendar candidate input")
    if source_manifest["artifact_type"] != ARTIFACT_TYPE_NORMALIZED_15M_OHLCV:
        raise HistoricalArtifactError("derived profile requires normalized source parent")
    if calendar_manifest["run_id"] != source_manifest["run_id"]:
        raise HistoricalArtifactError("cross-run parentage is not allowed")
    calendar_payload_data = load_historical_payload(calendar_manifest, run_root=run_root)
    source_payload_data = load_historical_payload(source_manifest, run_root=run_root)
    calendar = calendar_from_payload(calendar_payload_data)
    source_bars = source_bars_from_payload(source_payload_data)
    result = rth.derive_profile_bars(calendar, source_bars, profile)
    if profile == rth.PROFILE_SWING:
        artifact_type = ARTIFACT_TYPE_DERIVED_SWING_RTH_HALF_SESSION_195M
        canonical_bar_type = rth.RTH_HALF_SESSION_195M
    elif profile == rth.PROFILE_POSITION_SWING:
        artifact_type = ARTIFACT_TYPE_DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D
        canonical_bar_type = rth.RTH_FULL_SESSION_1D
    else:
        raise HistoricalArtifactError("unsupported historical profile")
    payload = {
        "artifact_type": artifact_type,
        "schema_version": "marketflow.historical_data.derived_profile_payload.v1",
        "contract_v2_1_digest": result.contract_v2_1_digest,
        "profile": profile,
        "profile_contract_version": result.bars[0].profile_contract_version if result.bars else None,
        "canonical_bar_type": canonical_bar_type,
        "derivation_status": result.status,
        "calendar_artifact_id": calendar_manifest["artifact_id"],
        "calendar_digest": calendar.semantic_digest,
        "normalized_source_artifact_id": source_manifest["artifact_id"],
        "normalized_source_digest": source_manifest["semantic_payload_digest"],
        "accepted_full_session_count": result.accepted_full_session_count,
        "early_close_exclusion_count": result.early_close_exclusion_count,
        "extended_hours_exclusion_count": result.extended_hours_exclusion_count,
        "invalid_or_incomplete_session_count": result.invalid_or_incomplete_session_count,
        "produced_bar_count": result.produced_bar_count,
        "findings": list(result.findings),
        "derived_dataset_semantic_digest": result.dataset_semantic_digest,
        "bars": [bar.semantic_payload() | {"bar_digest": bar.deterministic_bar_digest} for bar in result.bars],
    }
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=source_manifest["run_id"],
        artifact_type=artifact_type,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
        profile_id=profile,
        canonical_bar_type=canonical_bar_type,
        requested_primary_listing_mic=calendar_manifest["requested_primary_listing_mic"],
        requested_calendar_token=calendar_manifest["requested_calendar_token"],
        resolved_calendar=calendar_manifest["resolved_calendar"],
        primary_parent_manifest=source_manifest,
        primary_parent_manifest_ref=source_manifest_ref,
        input_manifests=(calendar_manifest,),
        input_manifest_refs=(calendar_manifest_ref,),
    )


def derived_bars_from_payload(payload: dict[str, Any]) -> tuple[rth.DerivedBar, ...]:
    bars: list[rth.DerivedBar] = []
    for record in payload["bars"]:
        bars.append(
            rth.DerivedBar(
                profile_id=record["profile_id"],
                profile_contract_version=record["profile_contract_version"],
                canonical_bar_type=record["canonical_bar_type"],
                session_date=record["session_date"],
                timestamp_utc=datetime.fromisoformat(record["timestamp_utc"].replace("Z", "+00:00")),
                local_source_window_start=record["local_source_window_start"],
                local_source_window_end=record["local_source_window_end"],
                source_bar_count=int(record["source_bar_count"]),
                source_timestamp_set_digest=record["source_timestamp_set_digest"],
                open=Decimal(record["open"]),
                high=Decimal(record["high"]),
                low=Decimal(record["low"]),
                close=Decimal(record["close"]),
                volume=Decimal(record["volume"]),
                frozen_calendar_digest=record["frozen_calendar_digest"],
                contract_v2_1_digest=record["contract_v2_1_digest"],
                deterministic_bar_digest=record["bar_digest"],
            )
        )
    return tuple(bars)


def dividend_events_from_payload(payload: dict[str, Any]) -> tuple[segments.ExDividendEvidence, ...]:
    digest = payload["event_set_semantic_digest"]
    by_date: dict[str, list[str]] = {}
    for record in payload["events"]:
        by_date.setdefault(record["ex_dividend_date"], []).append(record["event_id"])
    return tuple(
        segments.ExDividendEvidence(event_date, tuple(sorted(event_ids)), digest)
        for event_date, event_ids in sorted(by_date.items())
    )


def commit_segment_map_artifact(
    *,
    derived_manifest_ref: str,
    dividend_manifest_ref: str,
    calendar_manifest_ref: str,
    run_root: str | Path,
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    derived_manifest = load_historical_manifest(derived_manifest_ref, run_root=run_root)
    dividend_manifest = load_historical_manifest(dividend_manifest_ref, run_root=run_root)
    calendar_manifest = load_historical_manifest(calendar_manifest_ref, run_root=run_root)
    validate_historical_manifest_chain(derived_manifest, run_root=run_root)
    validate_historical_manifest_chain(dividend_manifest, run_root=run_root)
    if derived_manifest["artifact_type"] not in PROFILE_BY_DERIVED_ARTIFACT:
        raise HistoricalArtifactError("segment map requires a derived profile parent")
    if dividend_manifest["artifact_type"] != ARTIFACT_TYPE_DIVIDEND_EVENT_SET:
        raise HistoricalArtifactError("segment map requires dividend-event input")
    if calendar_manifest["artifact_type"] != ARTIFACT_TYPE_CALENDAR_SCHEDULE_CANDIDATE:
        raise HistoricalArtifactError("segment map requires calendar candidate context")
    if len({derived_manifest["run_id"], dividend_manifest["run_id"], calendar_manifest["run_id"]}) != 1:
        raise HistoricalArtifactError("cross-run parentage is not allowed")
    derived_payload = load_historical_payload(derived_manifest, run_root=run_root)
    dividend_payload = load_historical_payload(dividend_manifest, run_root=run_root)
    calendar_payload_data = load_historical_payload(calendar_manifest, run_root=run_root)
    if derived_payload.get("calendar_artifact_id") != calendar_manifest["artifact_id"]:
        raise HistoricalArtifactError("segment map calendar artifact mismatch")
    if derived_payload.get("calendar_digest") != calendar_payload_data.get("session_schedule_digest"):
        raise HistoricalArtifactError("segment map calendar digest mismatch")
    calendar = calendar_from_payload(calendar_payload_data)
    profile = str(derived_manifest["profile_id"])
    if derived_payload["profile"] != profile:
        raise HistoricalArtifactError("cross-profile segment map is not allowed")
    bars = derived_bars_from_payload(derived_payload)
    analytical, segmented = segments.assign_analytical_segments(
        bars,
        calendar=calendar,
        dividend_events=dividend_events_from_payload(dividend_payload),
        source_dataset_digest=derived_manifest["semantic_payload_digest"],
        profile=profile,
    )
    payload = {
        "artifact_type": ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP,
        "schema_version": "marketflow.historical_data.analytical_segment_map_payload.v1",
        "contract_v2_1_digest": derived_manifest["contract_v2_1_digest"],
        "profile": profile,
        "derived_artifact_id": derived_manifest["artifact_id"],
        "derived_artifact_digest": derived_manifest["semantic_payload_digest"],
        "dividend_event_set_artifact_id": dividend_manifest["artifact_id"],
        "dividend_event_set_digest": dividend_manifest["semantic_payload_digest"],
        "calendar_artifact_id": calendar_manifest["artifact_id"],
        "segment_count": len(analytical),
        "bar_assignment_count": len(segmented),
        "segments": [asdict(item) for item in analytical],
        "bar_assignments": [
            {
                "bar_digest": item.bar.deterministic_bar_digest,
                "session_date": item.bar.session_date,
                "timestamp_utc": _utc_iso(item.bar.timestamp_utc),
                "analysis_segment_id": item.analysis_segment_id,
                "readiness_status": item.readiness_status,
            }
            for item in segmented
        ],
    }
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=derived_manifest["run_id"],
        artifact_type=ARTIFACT_TYPE_ANALYTICAL_SEGMENT_MAP,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
        profile_id=profile,
        canonical_bar_type=derived_manifest["canonical_bar_type"],
        requested_primary_listing_mic=derived_manifest["requested_primary_listing_mic"],
        requested_calendar_token=derived_manifest["requested_calendar_token"],
        resolved_calendar=derived_manifest["resolved_calendar"],
        primary_parent_manifest=derived_manifest,
        primary_parent_manifest_ref=derived_manifest_ref,
        input_manifests=(dividend_manifest,),
        input_manifest_refs=(dividend_manifest_ref,),
    )


def commit_pipeline_receipt_artifact(
    *,
    run_root: str | Path,
    run_id: str,
    receipt_payload: dict[str, Any],
    input_manifest_refs: tuple[str, ...],
    artifact_id: str | None = None,
    artifact_id_factory: Callable[[], str] | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    inputs = tuple(load_historical_manifest(ref, run_root=run_root) for ref in input_manifest_refs)
    payload = {
        "artifact_type": ARTIFACT_TYPE_HISTORICAL_PIPELINE_RECEIPT,
        "schema_version": "marketflow.historical_data.pipeline_receipt_payload.v1",
        "contract_v2_1_digest": _contract_v21_digest(),
        **receipt_payload,
    }
    return _commit_payload(
        payload=payload,
        run_root=run_root,
        run_id=run_id,
        artifact_type=ARTIFACT_TYPE_HISTORICAL_PIPELINE_RECEIPT,
        artifact_id=artifact_id,
        artifact_id_factory=artifact_id_factory,
        created_at_utc=created_at_utc,
        input_manifests=inputs,
        input_manifest_refs=input_manifest_refs,
    )


def manifest_ref_from_result(result: dict[str, Any], *, run_root: str | Path) -> str:
    return _manifest_ref(result["manifest"], run_root=run_root)
