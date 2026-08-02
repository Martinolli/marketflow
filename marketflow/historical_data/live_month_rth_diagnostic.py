"""Noncanonical live-month RTH derivation diagnostic."""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
import uuid
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

from marketflow.historical_data import artifacts
from marketflow.historical_data import frozen_calendar
from marketflow.historical_data import monthly_acquisition as monthly
from marketflow.historical_data import rth_bar_engine as rth
from marketflow.historical_data.fake_transport import ScriptedExchange, ScriptedFakeTransport, http_response
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


DIAGNOSTIC_SCHEMA_VERSION = "marketflow.live_month_rth_diagnostic.v1"
DIAGNOSTIC_CLASSIFICATION = "NONCANONICAL_LIVE_MONTH_RTH_DERIVATION"
DIAGNOSTIC_RUNTIME_ROOT = Path(".marketflow/rth_derivation_smoke/runs")
SOURCE_SMOKE_ROOT = Path(".marketflow/provider_smoke/runs")
FORBIDDEN_RUN_ID_FRAGMENTS = ("AAPL", "2025", "XNAS", "OPERATOR")
MAX_DIAGNOSTIC_RUN_ID_GENERATION_ATTEMPTS = 32
DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED = "DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED"
WINDOWS_REPARSE_POINT_ATTRIBUTE = 0x400

LIVE_MONTH_RTH_PLAN_VALID = "LIVE_MONTH_RTH_PLAN_VALID"
LIVE_MONTH_SOURCE_EVIDENCE_VALID = "LIVE_MONTH_SOURCE_EVIDENCE_VALID"
LIVE_MONTH_RTH_DERIVATION_COMPLETE = "LIVE_MONTH_RTH_DERIVATION_COMPLETE"
LIVE_MONTH_RTH_DERIVATION_PARTIAL = "LIVE_MONTH_RTH_DERIVATION_PARTIAL"
LIVE_MONTH_RTH_DERIVATION_BLOCKED = "LIVE_MONTH_RTH_DERIVATION_BLOCKED"
LIVE_MONTH_SOURCE_EVIDENCE_INVALID = "LIVE_MONTH_SOURCE_EVIDENCE_INVALID"
LIVE_MONTH_CALENDAR_INVALID = "LIVE_MONTH_CALENDAR_INVALID"
REPOSITORY_ROOT_UNRESOLVED = "REPOSITORY_ROOT_UNRESOLVED"
SOURCE_EVIDENCE_PATH_INVALID = "SOURCE_EVIDENCE_PATH_INVALID"
SOURCE_EVIDENCE_PATH_OUTSIDE_ROOT = "SOURCE_EVIDENCE_PATH_OUTSIDE_ROOT"
SOURCE_EVIDENCE_REPARSE_POINT_REJECTED = "SOURCE_EVIDENCE_REPARSE_POINT_REJECTED"
SOURCE_EVIDENCE_SYMLINK_REJECTED = "SOURCE_EVIDENCE_SYMLINK_REJECTED"
SOURCE_EVIDENCE_NOT_REGULAR_FILE = "SOURCE_EVIDENCE_NOT_REGULAR_FILE"
SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED = "SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED"
SOURCE_RAW_PAGE_ANCESTRY_INVALID = "SOURCE_RAW_PAGE_ANCESTRY_INVALID"
RAW_PAGE_ARTIFACT_ID_MISMATCH = "RAW_PAGE_ARTIFACT_ID_MISMATCH"
RAW_PAGE_PAYLOAD_DIGEST_MISMATCH = "RAW_PAGE_PAYLOAD_DIGEST_MISMATCH"
RAW_PAGE_ANCESTRY_COUNT_MISMATCH = "RAW_PAGE_ANCESTRY_COUNT_MISMATCH"
RAW_PAGE_ANCESTRY_ORDER_MISMATCH = "RAW_PAGE_ANCESTRY_ORDER_MISMATCH"
RAW_PAGE_ANCESTRY_DUPLICATE = "RAW_PAGE_ANCESTRY_DUPLICATE"
RAW_PAGE_MANIFEST_MISSING = "RAW_PAGE_MANIFEST_MISSING"
RAW_PAGE_INPUT_UNDECLARED = "RAW_PAGE_INPUT_UNDECLARED"
RTH_SOURCE_ROWS_RECONCILED = "RTH_SOURCE_ROWS_RECONCILED"
RTH_SOURCE_ROWS_INCOMPLETE = "RTH_SOURCE_ROWS_INCOMPLETE"
RTH_SOURCE_ROWS_INVALID = "RTH_SOURCE_ROWS_INVALID"

OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY = "OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY"
CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN = "NOT_OPERATOR_FROZEN"
CALENDAR_FREEZE_ELIGIBLE = False
CANONICAL_ELIGIBILITY = False
REGISTRY_ELIGIBILITY = False
STRATEGY_ENABLED = False
PERFORMANCE_ENABLED = False
LOCAL_RUN_DIGEST_PREFIX_LENGTH = 12
RAW_PAGE_ANCESTRY_FINDINGS = frozenset(
    {
        RAW_PAGE_ARTIFACT_ID_MISMATCH,
        RAW_PAGE_PAYLOAD_DIGEST_MISMATCH,
        RAW_PAGE_ANCESTRY_COUNT_MISMATCH,
        RAW_PAGE_ANCESTRY_ORDER_MISMATCH,
        RAW_PAGE_ANCESTRY_DUPLICATE,
        RAW_PAGE_MANIFEST_MISSING,
        RAW_PAGE_INPUT_UNDECLARED,
    }
)


class LiveMonthRthDiagnosticError(ValueError):
    """Raised when the noncanonical live-month RTH diagnostic cannot continue."""


@dataclass(frozen=True, slots=True)
class LiveMonthRthDiagnosticSpec:
    schema_version: str
    classification: str
    source_smoke_run_id: str
    source_smoke_receipt_sha256: str
    source_ticker: str
    source_month: str
    source_normalized_row_count: int
    source_first_window_start_utc: str
    source_last_window_start_utc: str
    source_normalized_ohlcv_artifact_id: str
    source_normalized_ohlcv_semantic_digest: str
    source_normalized_audit_artifact_id: str
    source_normalized_audit_semantic_digest: str
    requested_primary_listing_mic: str
    requested_calendar_token: str
    identity_evidence_classification: str
    calendar_authority: str
    calendar_freeze_eligible: bool
    canonical_eligibility: bool
    registry_eligibility: bool
    strategy_enabled: bool
    performance_enabled: bool

    def validate(self) -> None:
        if self.schema_version != DIAGNOSTIC_SCHEMA_VERSION:
            raise LiveMonthRthDiagnosticError("diagnostic schema mismatch")
        if self.classification != DIAGNOSTIC_CLASSIFICATION:
            raise LiveMonthRthDiagnosticError("diagnostic classification mismatch")
        if self.requested_primary_listing_mic != "XNAS" or self.requested_calendar_token != "XNAS":
            raise LiveMonthRthDiagnosticError("diagnostic MIC/calendar token mismatch")
        if self.identity_evidence_classification != OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY:
            raise LiveMonthRthDiagnosticError("identity evidence classification mismatch")
        if self.calendar_authority != CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN:
            raise LiveMonthRthDiagnosticError("calendar authority mismatch")
        if any(
            (
                self.calendar_freeze_eligible,
                self.canonical_eligibility,
                self.registry_eligibility,
                self.strategy_enabled,
                self.performance_enabled,
            )
        ):
            raise LiveMonthRthDiagnosticError("diagnostic eligibility flags must remain false")
        for digest in (
            self.source_smoke_receipt_sha256,
            self.source_normalized_ohlcv_semantic_digest,
            self.source_normalized_audit_semantic_digest,
        ):
            _require_sha256(digest, "digest")


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    spec: LiveMonthRthDiagnosticSpec
    smoke_receipt: dict[str, Any]
    ohlcv_manifest: dict[str, Any]
    audit_manifest: dict[str, Any]
    completeness_manifest: dict[str, Any]
    ohlcv_payload: dict[str, Any]
    audit_payload: dict[str, Any]
    completeness_payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ValidatedSourceFile:
    path: Path
    identity: tuple[int | None, int | None, int, int]


@dataclass(frozen=True, slots=True)
class SessionView:
    calendar: frozen_calendar.FrozenCalendar
    parent_calendar_digest: str
    month_view_digest: str
    full_session_count: int
    early_close_count: int
    closed_or_absent_count: int


def default_diagnostic_spec() -> LiveMonthRthDiagnosticSpec:
    """Return the fixed, non-overridable live-month RTH diagnostic spec."""
    spec = LiveMonthRthDiagnosticSpec(
        schema_version=DIAGNOSTIC_SCHEMA_VERSION,
        classification=DIAGNOSTIC_CLASSIFICATION,
        source_smoke_run_id="smoke-c3388f68530c4131a090a895953e3d89",
        source_smoke_receipt_sha256="70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f",
        source_ticker="AAPL",
        source_month="2025-01",
        source_normalized_row_count=1277,
        source_first_window_start_utc="2025-01-02T09:00:00Z",
        source_last_window_start_utc="2025-02-01T00:45:00Z",
        source_normalized_ohlcv_artifact_id="month-art-0005-month-normalized-15m-ohlcv",
        source_normalized_ohlcv_semantic_digest="24e83b9eea95c9e7ba662123f6edac220de9fb64e9cbb4225ee76d60bcb1230e",
        source_normalized_audit_artifact_id="month-art-0006-month-normalized-aggregate-audit-fields",
        source_normalized_audit_semantic_digest="3099ffab37579b20cb3dfdcb5c1e2741ce00cbf7f05fb8a4e135e9dcb421f9cd",
        requested_primary_listing_mic="XNAS",
        requested_calendar_token="XNAS",
        identity_evidence_classification=OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY,
        calendar_authority=CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN,
        calendar_freeze_eligible=CALENDAR_FREEZE_ELIGIBLE,
        canonical_eligibility=CANONICAL_ELIGIBILITY,
        registry_eligibility=REGISTRY_ELIGIBILITY,
        strategy_enabled=STRATEGY_ENABLED,
        performance_enabled=PERFORMANCE_ENABLED,
    )
    spec.validate()
    return spec


def diagnostic_spec_digest() -> str:
    return _diagnostic_spec_digest_for_spec(default_diagnostic_spec())


def _diagnostic_spec_digest_for_spec(spec: LiveMonthRthDiagnosticSpec) -> str:
    spec.validate()
    return artifacts.semantic_digest(asdict(spec))


def diagnostic_confirmation_details() -> dict[str, str]:
    digest = diagnostic_spec_digest()
    prefix = digest[:LOCAL_RUN_DIGEST_PREFIX_LENGTH]
    return {
        "diagnostic_specification_digest": digest,
        "diagnostic_specification_digest_prefix": prefix,
        "required_confirmation_phrase": _diagnostic_confirmation_phrase_for_prefix(prefix),
    }


def diagnostic_confirmation_phrase() -> str:
    return diagnostic_confirmation_details()["required_confirmation_phrase"]


def _diagnostic_confirmation_phrase_for_prefix(prefix: str) -> str:
    return f"RUN MARKETFLOW LIVE MONTH RTH {prefix}"


def plan_receipt() -> dict[str, Any]:
    actual = default_diagnostic_spec()
    actual.validate()
    confirmation = diagnostic_confirmation_details()
    return {
        "status": LIVE_MONTH_RTH_PLAN_VALID,
        "diagnostic_specification_digest": confirmation["diagnostic_specification_digest"],
        "diagnostic_specification_digest_prefix": confirmation["diagnostic_specification_digest_prefix"],
        "schema_version": actual.schema_version,
        "classification": actual.classification,
        "source_smoke_run_id": actual.source_smoke_run_id,
        "source_smoke_receipt_sha256": actual.source_smoke_receipt_sha256,
        "source_ticker": actual.source_ticker,
        "source_month": actual.source_month,
        "source_normalized_row_count": actual.source_normalized_row_count,
        "source_normalized_ohlcv_artifact_id": actual.source_normalized_ohlcv_artifact_id,
        "source_normalized_ohlcv_semantic_digest": actual.source_normalized_ohlcv_semantic_digest,
        "source_normalized_audit_artifact_id": actual.source_normalized_audit_artifact_id,
        "source_normalized_audit_semantic_digest": actual.source_normalized_audit_semantic_digest,
        "requested_primary_listing_mic": actual.requested_primary_listing_mic,
        "requested_calendar_token": actual.requested_calendar_token,
        "identity_evidence_classification": actual.identity_evidence_classification,
        "calendar_authority": actual.calendar_authority,
        "calendar_freeze_eligible": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_enabled": False,
        "performance_enabled": False,
        "network_execution_enabled": False,
        "credential_prompted": False,
        "runtime_artifact_written": False,
        "required_confirmation_phrase": confirmation["required_confirmation_phrase"],
    }


def validate_source_evidence(
) -> SourceEvidence:
    """Validate the fixed accepted live-smoke evidence from the ignored runtime root."""
    return _validate_source_evidence_for_spec(spec=default_diagnostic_spec(), smoke_root=_production_source_smoke_root())


def _validate_source_evidence_for_spec(
    *,
    spec: LiveMonthRthDiagnosticSpec,
    smoke_root: str | Path,
) -> SourceEvidence:
    actual = spec
    actual.validate()
    root = _validated_source_smoke_root(smoke_root)
    receipt_ref = _smoke_receipt_ref(actual.source_smoke_run_id)
    receipt_file = _validate_source_evidence_file(root, receipt_ref, expected_kind="smoke_receipt")
    receipt_bytes = _read_validated_source_file(receipt_file)
    receipt_hash = artifacts.sha256_bytes(receipt_bytes)
    if receipt_hash != actual.source_smoke_receipt_sha256:
        raise LiveMonthRthDiagnosticError("source smoke receipt hash mismatch")
    receipt = _load_json_bytes(receipt_bytes)
    _validate_smoke_receipt(receipt, actual)
    by_id = {
        str(item.get("artifact_id")): item
        for item in _required_list(receipt.get("normalized_artifact_receipts"), "normalized_artifact_receipts")
        if isinstance(item, dict)
    }
    ohlcv_receipt = _required_receipt(by_id, actual.source_normalized_ohlcv_artifact_id, actual.source_normalized_ohlcv_semantic_digest)
    audit_receipt = _required_receipt(by_id, actual.source_normalized_audit_artifact_id, actual.source_normalized_audit_semantic_digest)
    ohlcv_manifest, ohlcv_payload = _load_monthly_payload(
        root,
        str(ohlcv_receipt["manifest_ref"]),
        expected_run_id=actual.source_smoke_run_id,
        expected_artifact_id=actual.source_normalized_ohlcv_artifact_id,
        expected_artifact_type=monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV,
        expected_semantic_digest=actual.source_normalized_ohlcv_semantic_digest,
    )
    audit_manifest, audit_payload = _load_monthly_payload(
        root,
        str(audit_receipt["manifest_ref"]),
        expected_run_id=actual.source_smoke_run_id,
        expected_artifact_id=actual.source_normalized_audit_artifact_id,
        expected_artifact_type=monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS,
        expected_semantic_digest=actual.source_normalized_audit_semantic_digest,
    )
    if ohlcv_manifest["primary_parent_artifact_id"] != audit_manifest["primary_parent_artifact_id"]:
        raise LiveMonthRthDiagnosticError("normalized pair completeness parent mismatch")
    if ohlcv_manifest["primary_parent_manifest_ref"] != audit_manifest["primary_parent_manifest_ref"]:
        raise LiveMonthRthDiagnosticError("normalized pair completeness manifest ref mismatch")
    completeness_manifest, completeness_payload = _load_monthly_payload(
        root,
        str(ohlcv_manifest["primary_parent_manifest_ref"]),
        expected_run_id=actual.source_smoke_run_id,
        expected_artifact_id=str(ohlcv_manifest["primary_parent_artifact_id"]),
        expected_artifact_type=monthly.ARTIFACT_MONTH_CHUNK_COMPLETENESS_MANIFEST,
    )
    _validate_monthly_parentage(root, completeness_manifest, completeness_payload, expected_raw_page_count=receipt["raw_page_count"])
    _validate_normalized_pair(actual, ohlcv_payload, audit_payload)
    return SourceEvidence(actual, receipt, ohlcv_manifest, audit_manifest, completeness_manifest, ohlcv_payload, audit_payload, completeness_payload)


def import_source_bars(evidence: SourceEvidence) -> tuple[rth.SourceBar, ...]:
    rows = _required_list(evidence.ohlcv_payload.get("rows"), "rows")
    bars: list[rth.SourceBar] = []
    starts: list[datetime] = []
    for row in rows:
        if not isinstance(row, dict):
            raise LiveMonthRthDiagnosticError("normalized OHLCV row must be an object")
        start = _parse_utc(str(row["window_start_utc"]), "window_start_utc")
        end = _parse_utc(str(row["window_end_utc"]), "window_end_utc")
        bar = rth.SourceBar.build(
            window_start_utc=start,
            window_end_utc=end,
            open=_required_decimal_text(row.get("open"), "open"),
            high=_required_decimal_text(row.get("high"), "high"),
            low=_required_decimal_text(row.get("low"), "low"),
            close=_required_decimal_text(row.get("close"), "close"),
            volume=_required_decimal_text(row.get("volume"), "volume"),
        )
        bars.append(bar)
        starts.append(start)
    if starts != sorted(starts) or len(starts) != len(set(starts)):
        raise LiveMonthRthDiagnosticError("source rows must be strictly ascending with no duplicates")
    return tuple(bars)


def build_calendar_candidate() -> frozen_calendar.FrozenCalendar:
    return _build_calendar_candidate_for_spec(default_diagnostic_spec())


def _build_calendar_candidate_for_spec(spec: LiveMonthRthDiagnosticSpec) -> frozen_calendar.FrozenCalendar:
    actual = spec
    request = frozen_calendar.default_calendar_request(
        requested_primary_listing_mic=actual.requested_primary_listing_mic,
        requested_calendar_token=actual.requested_calendar_token,
        official_exchange_evidence_identity=actual.identity_evidence_classification,
        official_exchange_evidence_digest="OFFICIAL_EVIDENCE_DIGEST_PENDING",
    )
    return frozen_calendar.generate_frozen_calendar(request)


def january_session_view(calendar: frozen_calendar.FrozenCalendar, *, month_key: str = "2025-01") -> SessionView:
    sessions = tuple(session for session in calendar.sessions if session.session_date.startswith(f"{month_key}-"))
    payload = {
        "schema_version": "marketflow.live_month_rth_session_view.v1",
        "source_month": month_key,
        "parent_calendar_candidate_digest": calendar.semantic_digest,
        "requested_primary_listing_mic": calendar.requested_primary_listing_mic,
        "requested_calendar_token": calendar.requested_calendar_token,
        "resolved_calendar": calendar.resolved_calendar,
        "calendar_alias_relationship": calendar.calendar_alias_relationship,
        "calendar_status": calendar.status,
        "sessions": [asdict(session) for session in sessions],
    }
    digest = artifacts.semantic_digest(payload)
    view_calendar = replace(calendar, sessions=sessions, semantic_digest=digest)
    return SessionView(
        calendar=view_calendar,
        parent_calendar_digest=calendar.semantic_digest,
        month_view_digest=digest,
        full_session_count=sum(1 for item in sessions if item.session_classification == frozen_calendar.NORMAL_FULL_SESSION),
        early_close_count=sum(1 for item in sessions if item.session_classification == frozen_calendar.EARLY_CLOSE_SESSION),
        closed_or_absent_count=sum(1 for item in sessions if item.session_classification == frozen_calendar.FULL_MARKET_CLOSED),
    )


def run_diagnostic(
) -> dict[str, Any]:
    """Run the fixed noncanonical diagnostic against accepted local smoke evidence."""
    return _run_diagnostic_for_spec(spec=default_diagnostic_spec(), smoke_root=_production_source_smoke_root())


def _run_diagnostic_for_spec(
    *,
    spec: LiveMonthRthDiagnosticSpec,
    smoke_root: str | Path,
) -> dict[str, Any]:
    actual = spec
    try:
        evidence = _validate_source_evidence_for_spec(spec=actual, smoke_root=smoke_root)
    except LiveMonthRthDiagnosticError as exc:
        if str(exc) in RAW_PAGE_ANCESTRY_FINDINGS:
            return _blocked_receipt(actual, LIVE_MONTH_SOURCE_EVIDENCE_INVALID, (SOURCE_RAW_PAGE_ANCESTRY_INVALID,))
        return _blocked_receipt(actual, LIVE_MONTH_SOURCE_EVIDENCE_INVALID, (str(exc),))
    except Exception:
        return _blocked_receipt(actual, LIVE_MONTH_SOURCE_EVIDENCE_INVALID, ("SOURCE_EVIDENCE_VALIDATION_FAILED",))
    try:
        source_bars = import_source_bars(evidence)
        candidate = _build_calendar_candidate_for_spec(actual)
        session_view = january_session_view(candidate, month_key=actual.source_month)
    except Exception as exc:
        return _blocked_receipt(actual, LIVE_MONTH_CALENDAR_INVALID, (str(exc),))
    validation = _session_validation_summary(session_view.calendar, source_bars)
    swing = rth.derive_profile_bars(session_view.calendar, source_bars, rth.PROFILE_SWING)
    position = rth.derive_profile_bars(session_view.calendar, source_bars, rth.PROFILE_POSITION_SWING)
    if (
        validation["incomplete_ordinary_session_count"] == 0
        and validation["rth_source_row_reconciliation_status"] == RTH_SOURCE_ROWS_RECONCILED
    ):
        status = LIVE_MONTH_RTH_DERIVATION_COMPLETE
    elif validation["complete_ordinary_session_count"] > 0:
        status = LIVE_MONTH_RTH_DERIVATION_PARTIAL
    else:
        status = LIVE_MONTH_RTH_DERIVATION_BLOCKED
    return _diagnostic_receipt(
        actual,
        evidence=evidence,
        calendar=candidate,
        session_view=session_view,
        source_bars=source_bars,
        validation=validation,
        swing=swing,
        position=position,
        status=status,
    )


def run_local_diagnostic(confirmation: str) -> dict[str, Any]:
    spec = default_diagnostic_spec()
    if confirmation != diagnostic_confirmation_phrase():
        return _blocked_receipt(spec, LIVE_MONTH_RTH_DERIVATION_BLOCKED, ("DIAGNOSTIC_AUTHORIZATION_REJECTED",))
    return _run_local_diagnostic_core(
        confirmation,
        smoke_root=_production_source_smoke_root(),
        run_root=_production_runtime_root(),
        run_id_factory=_generate_diagnostic_run_id,
    )


def _run_local_diagnostic_core(
    confirmation: str,
    *,
    smoke_root: str | Path,
    run_root: str | Path,
    run_id_factory: Callable[[], str],
) -> dict[str, Any]:
    spec = default_diagnostic_spec()
    if confirmation != diagnostic_confirmation_phrase():
        return _blocked_receipt(spec, LIVE_MONTH_RTH_DERIVATION_BLOCKED, ("DIAGNOSTIC_AUTHORIZATION_REJECTED",))
    root = _validated_runtime_root(run_root)
    source_root = _validated_source_smoke_root(smoke_root)
    run_id = _opaque_run_id(run_id_factory())
    receipt = _run_diagnostic_for_spec(spec=spec, smoke_root=source_root)
    if receipt.get("diagnostic_status") == LIVE_MONTH_SOURCE_EVIDENCE_INVALID:
        return receipt
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / run_id
    try:
        run_dir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        raise LiveMonthRthDiagnosticError("diagnostic run already exists") from None
    receipt = dict(receipt)
    receipt["diagnostic_run_id"] = run_id
    receipt_path = run_dir / "live-month-rth-diagnostic-receipt.json"
    payload = artifacts.canonical_json_bytes(receipt)
    receipt_path.write_bytes(payload)
    receipt["diagnostic_receipt_sha256"] = artifacts.sha256_bytes(payload)
    return receipt


def _repository_root() -> Path:
    root = Path(__file__).resolve().parents[2]
    module_path = root / "marketflow" / "historical_data" / "live_month_rth_diagnostic.py"
    if not module_path.is_file() or not (root / "setup.py").is_file() or not (root / "AGENTS.md").is_file():
        raise LiveMonthRthDiagnosticError(REPOSITORY_ROOT_UNRESOLVED)
    try:
        if not module_path.samefile(Path(__file__).resolve()):
            raise LiveMonthRthDiagnosticError(REPOSITORY_ROOT_UNRESOLVED)
    except OSError:
        raise LiveMonthRthDiagnosticError(REPOSITORY_ROOT_UNRESOLVED) from None
    return root


def _production_source_smoke_root() -> Path:
    repo_root = _repository_root().resolve(strict=True)
    root = repo_root / SOURCE_SMOKE_ROOT
    try:
        root.resolve(strict=True).relative_to(repo_root)
    except ValueError:
        raise LiveMonthRthDiagnosticError("source smoke root must stay inside repository") from None
    return _validated_source_smoke_root(root, repository_root=repo_root)


def _production_runtime_root() -> Path:
    repo_root = _repository_root().resolve(strict=True)
    root = (repo_root / DIAGNOSTIC_RUNTIME_ROOT).resolve(strict=False)
    try:
        root.relative_to(repo_root)
    except ValueError:
        raise LiveMonthRthDiagnosticError("diagnostic runtime root must stay inside repository") from None
    return _validated_runtime_root(root)


def _validated_source_smoke_root(smoke_root: str | Path, *, repository_root: Path | None = None) -> Path:
    try:
        root = Path(smoke_root)
        if not str(root) or "\x00" in str(root) or ".." in root.parts:
            raise LiveMonthRthDiagnosticError("source smoke root must be safe")
        root_abs = root if root.is_absolute() else root.resolve(strict=False)
        _reject_source_reparse_components(root_abs)
        resolved = root_abs.resolve(strict=True)
        _reject_source_reparse_components(resolved)
        if not resolved.is_dir():
            raise LiveMonthRthDiagnosticError("source smoke root must be a directory")
        if repository_root is not None:
            repo_root = repository_root.resolve(strict=True)
            _reject_source_reparse_components(repo_root)
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                raise LiveMonthRthDiagnosticError("source smoke root must stay inside repository") from None
        return resolved
    except FileNotFoundError:
        raise LiveMonthRthDiagnosticError("source smoke root must exist") from None
    except LiveMonthRthDiagnosticError as exc:
        message = str(exc).replace("diagnostic runtime root", "source smoke root").replace("diagnostic runtime path", "source smoke path")
        raise LiveMonthRthDiagnosticError(message) from None


def _validated_runtime_root(run_root: str | Path) -> Path:
    root = Path(run_root)
    text = str(root)
    if not text or "\x00" in text or ".." in root.parts:
        raise LiveMonthRthDiagnosticError("diagnostic runtime root must be safe")
    if root.exists() and root.is_symlink():
        raise LiveMonthRthDiagnosticError("diagnostic runtime root must not be a symlink")
    resolved = root.resolve(strict=False)
    if resolved.exists() and not resolved.is_dir():
        raise LiveMonthRthDiagnosticError("diagnostic runtime root must be a directory")
    _reject_existing_symlink_components(resolved)
    return resolved


def _validate_source_evidence_file(source_root: str | Path, relative_ref: str, *, expected_kind: str) -> ValidatedSourceFile:
    root = _validated_source_smoke_root(source_root)
    try:
        candidate = artifacts._safe_ref_to_path(root, relative_ref)
    except artifacts.HistoricalArtifactError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
    _reject_source_ref_schema(relative_ref, expected_kind=expected_kind)
    try:
        candidate.relative_to(root)
    except ValueError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_OUTSIDE_ROOT) from None
    try:
        _reject_source_reparse_components(candidate)
    except FileNotFoundError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
    try:
        resolved.relative_to(root)
    except ValueError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_OUTSIDE_ROOT) from None
    try:
        _reject_source_reparse_components(resolved)
    except FileNotFoundError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
    identity = _source_file_identity(candidate)
    return ValidatedSourceFile(path=candidate, identity=identity)


def _reject_source_ref_schema(relative_ref: str, *, expected_kind: str) -> None:
    text = str(relative_ref)
    if any(ord(char) < 32 for char in text):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID)
    if "://" in text or text.startswith(("file:", "http:", "https:")):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID)
    if expected_kind == "smoke_receipt" and not text.endswith("/smoke_receipt/smoke-receipt.json"):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID)
    if expected_kind == "manifest" and not text.endswith(".manifest.json"):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID)
    if expected_kind == "json_payload" and text.endswith(".manifest.json"):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID)


def _reject_source_reparse_components(path: Path) -> None:
    current = Path(path.anchor) if path.is_absolute() else Path()
    parts = path.parts[1:] if path.is_absolute() else path.parts
    for part in parts:
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            raise
        _reject_source_reparse_metadata(metadata)


def _reject_source_reparse_metadata(metadata: Any) -> None:
    if stat.S_ISLNK(metadata.st_mode):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_SYMLINK_REJECTED)
    if getattr(metadata, "st_file_attributes", 0) & WINDOWS_REPARSE_POINT_ATTRIBUTE:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_REPARSE_POINT_REJECTED)


def _source_file_identity(path: Path) -> tuple[int | None, int | None, int, int]:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
    _reject_source_reparse_metadata(metadata)
    if not stat.S_ISREG(metadata.st_mode):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_NOT_REGULAR_FILE)
    return _source_identity_from_metadata(metadata)


def _opened_source_file_identity(handle: Any) -> tuple[int | None, int | None, int, int]:
    metadata = os.fstat(handle.fileno())
    if not stat.S_ISREG(metadata.st_mode):
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_NOT_REGULAR_FILE)
    return _source_identity_from_metadata(metadata)


def _source_identity_from_metadata(metadata: Any) -> tuple[int | None, int | None, int, int]:
    return (
        getattr(metadata, "st_dev", None),
        getattr(metadata, "st_ino", None),
        int(metadata.st_size),
        int(getattr(metadata, "st_mtime_ns", 0)),
    )


def _read_validated_source_file(source_file: ValidatedSourceFile) -> bytes:
    before = _source_file_identity(source_file.path)
    if before != source_file.identity:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED)
    with source_file.path.open("rb") as handle:
        opened = _opened_source_file_identity(handle)
        if opened != before:
            raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED)
        try:
            _reject_source_reparse_components(source_file.path)
        except FileNotFoundError:
            raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_PATH_INVALID) from None
        before_read = _source_file_identity(source_file.path)
        if before_read != opened:
            raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED)
        data = handle.read()
        after_open = _opened_source_file_identity(handle)
        if after_open != opened:
            raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED)
    after = _source_file_identity(source_file.path)
    if after != before:
        raise LiveMonthRthDiagnosticError(SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED)
    return data


def _reject_existing_symlink_components(path: Path) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise LiveMonthRthDiagnosticError("diagnostic runtime path must not traverse a symlink")


def _generate_diagnostic_run_id(candidate_factory: Callable[[], str] | None = None) -> str:
    factory = candidate_factory or _uuid_run_id_candidate
    for _attempt in range(MAX_DIAGNOSTIC_RUN_ID_GENERATION_ATTEMPTS):
        try:
            candidate = factory()
        except Exception:
            break
        try:
            return _validated_generated_run_id(candidate)
        except LiveMonthRthDiagnosticError:
            continue
    raise LiveMonthRthDiagnosticError(DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED)


def _uuid_run_id_candidate() -> str:
    return f"rthdiag-{uuid.uuid4().hex}"


def self_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="marketflow-live-month-rth-self-check-") as temp_root:
        root = Path(temp_root)
        complete_spec = _build_synthetic_smoke_source(root / "complete", complete=True)
        partial_spec = _build_synthetic_smoke_source(root / "partial", complete=False)
        complete = _run_diagnostic_for_spec(spec=complete_spec, smoke_root=root / "complete")
        partial = _run_diagnostic_for_spec(spec=partial_spec, smoke_root=root / "partial")
    return {
        "status": "LIVE_MONTH_RTH_DERIVATION_SELF_CHECK",
        "mock_source_only": True,
        "provider_execution_enabled": False,
        "network_execution_enabled": False,
        "credential_prompted": False,
        "complete_status": complete["diagnostic_status"],
        "partial_status": partial["diagnostic_status"],
        "complete_swing_bars": complete["swing_produced_bar_count"],
        "complete_position_swing_bars": complete["position_swing_produced_bar_count"],
        "partial_incomplete_ordinary_session_count": partial["incomplete_ordinary_session_count"],
        "sanitization": "NO_OHLCV_VALUES_NO_RAW_PROVIDER_BODY_NO_KEY_NO_AUTH_HEADER_NO_RAW_URL_NO_REQUEST_ID_NO_ABSOLUTE_PATHS_NO_PERFORMANCE",
    }


def _diagnostic_receipt(
    spec: LiveMonthRthDiagnosticSpec,
    *,
    evidence: SourceEvidence,
    calendar: frozen_calendar.FrozenCalendar,
    session_view: SessionView,
    source_bars: tuple[rth.SourceBar, ...],
    validation: dict[str, Any],
    swing: rth.DerivedDatasetResult,
    position: rth.DerivedDatasetResult,
    status: str,
) -> dict[str, Any]:
    return {
        "diagnostic_status": status,
        "source_evidence_status": LIVE_MONTH_SOURCE_EVIDENCE_VALID,
        "diagnostic_specification_digest": _diagnostic_spec_digest_for_spec(spec),
        "source_smoke_run_id": spec.source_smoke_run_id,
        "source_smoke_receipt_sha256": spec.source_smoke_receipt_sha256,
        "source_normalized_ohlcv_artifact_id": spec.source_normalized_ohlcv_artifact_id,
        "source_normalized_ohlcv_semantic_digest": spec.source_normalized_ohlcv_semantic_digest,
        "source_normalized_audit_artifact_id": spec.source_normalized_audit_artifact_id,
        "source_normalized_audit_semantic_digest": spec.source_normalized_audit_semantic_digest,
        "source_row_count": len(source_bars),
        "requested_primary_listing_mic": spec.requested_primary_listing_mic,
        "requested_calendar_token": spec.requested_calendar_token,
        "resolved_calendar": calendar.resolved_calendar,
        "calendar_alias_relationship": calendar.calendar_alias_relationship,
        "calendar_status": calendar.status,
        "calendar_authority": spec.calendar_authority,
        "calendar_freeze_eligible": False,
        "exchange_calendars_version": calendar.exchange_calendars_version,
        "tzdata_version": calendar.tzdata_version,
        "source_timezone": calendar.source_timezone,
        "canonical_timezone": calendar.canonical_timezone,
        "parent_calendar_candidate_digest": session_view.parent_calendar_digest,
        "january_session_view_digest": session_view.month_view_digest,
        "january_full_session_count": session_view.full_session_count,
        "early_close_exclusion_count": validation["early_close_exclusion_count"],
        "closed_or_session_absent_count": session_view.closed_or_absent_count,
        "source_rows_inspected": len(source_bars),
        "extended_hours_rows_excluded": validation["extended_hours_rows_excluded"],
        "expected_rth_source_row_count": validation["expected_rth_source_row_count"],
        "validated_rth_source_row_count": validation["validated_rth_source_row_count"],
        "rth_source_row_reconciliation_status": validation["rth_source_row_reconciliation_status"],
        "complete_ordinary_session_count": validation["complete_ordinary_session_count"],
        "incomplete_ordinary_session_count": validation["incomplete_ordinary_session_count"],
        "fixed_session_findings": validation["fixed_session_findings"],
        "swing_derivation_status": swing.status,
        "position_swing_derivation_status": position.status,
        "swing_produced_bar_count": swing.produced_bar_count,
        "position_swing_produced_bar_count": position.produced_bar_count,
        "swing_dataset_semantic_digest": swing.dataset_semantic_digest,
        "position_swing_dataset_semantic_digest": position.dataset_semantic_digest,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_enabled": False,
        "performance_enabled": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
        "sanitization": "NO_OHLCV_VALUES_NO_RAW_PROVIDER_BODY_NO_KEY_NO_AUTH_HEADER_NO_RAW_URL_NO_REQUEST_ID_NO_ABSOLUTE_PATHS_NO_PERFORMANCE",
        "normalized_pair_parent_artifact_id": evidence.ohlcv_manifest["primary_parent_artifact_id"],
    }


def _session_validation_summary(calendar: frozen_calendar.FrozenCalendar, source_bars: tuple[rth.SourceBar, ...]) -> dict[str, Any]:
    by_date = _bars_by_local_date(calendar, source_bars)
    complete = 0
    incomplete = 0
    early = 0
    extended = 0
    expected_rth = 0
    validated_rth = 0
    invalid_rth = False
    findings: list[dict[str, str]] = []
    for session in calendar.sessions:
        session_bars = by_date.get(session.session_date, ())
        validation = rth.validate_session_sources(calendar, session, session_bars)
        extended += validation.extended_hours_exclusion_count
        expected = rth.expected_source_windows(session)
        expected_rth += len(expected)
        validated_rth += _matched_expected_rth_source_row_count(expected, session_bars)
        if validation.outcome == rth.SESSION_COMPLETE:
            complete += 1
        elif validation.outcome == rth.EARLY_CLOSE_SESSION_EXCLUDED:
            early += 1
        elif validation.outcome == rth.FULL_MARKET_CLOSED_OUTCOME:
            continue
        else:
            incomplete += 1
            if validation.outcome in {rth.SESSION_SOURCE_DUPLICATE_SLOT, rth.SESSION_SOURCE_EXTRA_SLOT, rth.SESSION_SOURCE_INVALID}:
                invalid_rth = True
            findings.append({"session_date": session.session_date, "finding": validation.finding})
    if invalid_rth:
        rth_status = RTH_SOURCE_ROWS_INVALID
    elif expected_rth == validated_rth and incomplete == 0:
        rth_status = RTH_SOURCE_ROWS_RECONCILED
    else:
        rth_status = RTH_SOURCE_ROWS_INCOMPLETE
    return {
        "complete_ordinary_session_count": complete,
        "incomplete_ordinary_session_count": incomplete,
        "early_close_exclusion_count": early,
        "extended_hours_rows_excluded": extended,
        "expected_rth_source_row_count": expected_rth,
        "validated_rth_source_row_count": validated_rth,
        "rth_source_row_reconciliation_status": rth_status,
        "fixed_session_findings": findings,
    }


def _matched_expected_rth_source_row_count(expected: tuple[datetime, ...], source_bars: tuple[rth.SourceBar, ...]) -> int:
    if not expected:
        return 0
    expected_set = set(expected)
    matched = {bar.window_start_utc for bar in source_bars if bar.window_start_utc in expected_set}
    return len(matched)


def _bars_by_local_date(calendar: frozen_calendar.FrozenCalendar, source_bars: tuple[rth.SourceBar, ...]) -> dict[str, tuple[rth.SourceBar, ...]]:
    source_tz = ZoneInfo(frozen_calendar.SOURCE_TIMEZONE)
    by_date: dict[str, list[rth.SourceBar]] = {session.session_date: [] for session in calendar.sessions}
    for bar in source_bars:
        key = bar.window_start_utc.astimezone(source_tz).date().isoformat()
        if key in by_date:
            by_date[key].append(bar)
    return {key: tuple(value) for key, value in by_date.items()}


def _blocked_receipt(spec: LiveMonthRthDiagnosticSpec, status: str, findings: tuple[str, ...]) -> dict[str, Any]:
    return {
        "diagnostic_status": status,
        "diagnostic_specification_digest": _diagnostic_spec_digest_for_spec(spec),
        "source_smoke_run_id": spec.source_smoke_run_id,
        "source_smoke_receipt_sha256": spec.source_smoke_receipt_sha256,
        "fixed_session_findings": [{"finding": item} for item in findings],
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_enabled": False,
        "performance_enabled": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
    }


def _validate_smoke_receipt(receipt: dict[str, Any], spec: LiveMonthRthDiagnosticSpec) -> None:
    expected = {
        "smoke_status": "SMOKE_COMPLETED_NONCANONICAL",
        "request_status": monthly.MONTH_ACQUISITION_COMPLETED,
        "classification": "NONCANONICAL_PROVIDER_SMOKE",
        "provenance": "LIVE_PROVIDER_SMOKE_NONCANONICAL",
        "provider_identity": "MASSIVE.COM",
        "ticker": spec.source_ticker,
        "month_key": spec.source_month,
        "attempt_count": 1,
        "accepted_page_count": 1,
        "raw_page_count": 1,
        "pagination_status": monthly.PAGINATION_EXHAUSTED,
        "completeness_status": "COMPLETE",
        "total_normalized_row_count": spec.source_normalized_row_count,
        "first_source_window_start_utc": spec.source_first_window_start_utc,
        "last_source_window_start_utc": spec.source_last_window_start_utc,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_enabled": False,
        "calendar_bar_derivation_enabled": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            if key == "total_normalized_row_count":
                raise LiveMonthRthDiagnosticError("source smoke receipt row count mismatch")
            raise LiveMonthRthDiagnosticError(f"source smoke receipt field mismatch: {key}")


def _load_monthly_payload(
    root: Path,
    manifest_ref: str,
    *,
    expected_run_id: str,
    expected_artifact_id: str,
    expected_artifact_type: str,
    expected_semantic_digest: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        manifest_file = _validate_source_evidence_file(root, manifest_ref, expected_kind="manifest")
    except LiveMonthRthDiagnosticError as exc:
        if str(exc) == SOURCE_EVIDENCE_PATH_INVALID:
            raise LiveMonthRthDiagnosticError("monthly manifest reference is missing") from None
        raise
    manifest = _load_json_bytes(_read_validated_source_file(manifest_file))
    _validate_monthly_manifest_metadata(
        manifest,
        expected_run_id=expected_run_id,
        expected_artifact_type=expected_artifact_type,
    )
    if manifest["artifact_id"] != expected_artifact_id:
        raise LiveMonthRthDiagnosticError("monthly artifact ID mismatch")
    if expected_semantic_digest is not None and manifest["semantic_payload_digest"] != expected_semantic_digest:
        raise LiveMonthRthDiagnosticError("monthly semantic digest mismatch")
    payload_file = _validate_source_evidence_file(root, str(manifest["payload_ref"]), expected_kind="json_payload")
    payload_bytes = _read_validated_source_file(payload_file)
    payload = _load_json_bytes(payload_bytes)
    if artifacts.sha256_bytes(payload_bytes) != manifest["payload_sha256"]:
        raise LiveMonthRthDiagnosticError("monthly payload byte digest mismatch")
    if len(payload_bytes) != int(manifest["payload_byte_size"]):
        raise LiveMonthRthDiagnosticError("monthly payload byte size mismatch")
    if artifacts.semantic_digest(payload) != manifest["semantic_payload_digest"]:
        raise LiveMonthRthDiagnosticError("monthly semantic payload digest mismatch")
    return manifest, payload


def _validate_monthly_parentage(
    root: Path,
    completeness_manifest: dict[str, Any],
    completeness_payload: dict[str, Any],
    *,
    expected_raw_page_count: int,
) -> None:
    if completeness_payload.get("scope") != monthly.PROVIDER_RETRIEVAL_COMPLETE:
        raise LiveMonthRthDiagnosticError("completeness manifest scope mismatch")
    if completeness_payload.get("pagination_status") != monthly.PAGINATION_EXHAUSTED:
        raise LiveMonthRthDiagnosticError("completeness manifest pagination mismatch")
    if completeness_payload.get("request_range_containment_status") != monthly.REQUEST_RANGE_CONTAINED:
        raise LiveMonthRthDiagnosticError("completeness manifest range-containment mismatch")
    if completeness_payload.get("market_session_coverage_status") != monthly.MARKET_SESSION_COVERAGE_NOT_EVALUATED:
        raise LiveMonthRthDiagnosticError("completeness manifest session coverage mismatch")
    if completeness_manifest.get("primary_parent_manifest_ref") is None:
        raise LiveMonthRthDiagnosticError("completeness manifest must retain request parent")
    input_manifest_refs = completeness_manifest.get("input_manifest_refs")
    if not isinstance(input_manifest_refs, list):
        raise LiveMonthRthDiagnosticError("completeness manifest raw-page ancestry must be a list")
    if len(input_manifest_refs) != expected_raw_page_count:
        raise LiveMonthRthDiagnosticError("completeness manifest raw-page ancestry count mismatch")
    accepted_pages = _required_list(completeness_payload.get("accepted_pages"), "accepted_pages")
    if len(accepted_pages) != len(input_manifest_refs):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_COUNT_MISMATCH)
    if int(completeness_payload.get("page_count", len(accepted_pages))) != len(accepted_pages):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_COUNT_MISMATCH)
    input_artifact_ids = completeness_manifest.get("input_artifact_ids")
    if not isinstance(input_artifact_ids, list) or len(input_artifact_ids) != len(input_manifest_refs):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_COUNT_MISMATCH)
    if len(input_manifest_refs) != len({str(item) for item in input_manifest_refs}):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_DUPLICATE)
    if len(input_artifact_ids) != len({str(item) for item in input_artifact_ids}):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_DUPLICATE)
    accepted_raw_ids = [str(item.get("raw_page_artifact_id")) for item in accepted_pages if isinstance(item, dict)]
    if len(accepted_raw_ids) != len(accepted_pages) or len(accepted_raw_ids) != len(set(accepted_raw_ids)):
        raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_DUPLICATE)
    accepted_ids: set[str] = set()
    manifest_ids: set[str] = set()
    for index, (accepted_page, input_ref, input_artifact_id) in enumerate(
        zip(accepted_pages, input_manifest_refs, input_artifact_ids, strict=True),
        start=1,
    ):
        if not isinstance(accepted_page, dict):
            raise LiveMonthRthDiagnosticError(RAW_PAGE_INPUT_UNDECLARED)
        if accepted_page.get("page_ordinal") != index:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_ORDER_MISMATCH)
        try:
            raw_manifest_file = _validate_source_evidence_file(root, str(input_ref), expected_kind="manifest")
            raw_manifest = _load_json_bytes(_read_validated_source_file(raw_manifest_file))
        except LiveMonthRthDiagnosticError as exc:
            if str(exc) == SOURCE_EVIDENCE_PATH_INVALID:
                raise LiveMonthRthDiagnosticError(RAW_PAGE_MANIFEST_MISSING) from None
            raise
        except FileNotFoundError:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_MANIFEST_MISSING) from None
        if raw_manifest.get("run_id") != completeness_manifest.get("run_id"):
            raise LiveMonthRthDiagnosticError(RAW_PAGE_INPUT_UNDECLARED)
        if raw_manifest.get("artifact_type") != monthly.ARTIFACT_RAW_PROVIDER_PAGE:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_INPUT_UNDECLARED)
        _validate_monthly_manifest_metadata(
            raw_manifest,
            expected_run_id=str(completeness_manifest["run_id"]),
            expected_artifact_type=monthly.ARTIFACT_RAW_PROVIDER_PAGE,
        )
        for field_name in (
            "contract_v2_1_digest",
            "contract_v2_base_digest",
            "month_request_digest",
            "month_key",
            "canonical_ticker",
        ):
            if raw_manifest.get(field_name) != completeness_manifest.get(field_name):
                raise LiveMonthRthDiagnosticError(RAW_PAGE_INPUT_UNDECLARED)
        if raw_manifest.get("page_ordinal") != index:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_ORDER_MISMATCH)
        raw_artifact_id = str(raw_manifest["artifact_id"])
        accepted_artifact_id = str(accepted_page.get("raw_page_artifact_id"))
        if str(input_artifact_id) != raw_artifact_id:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_INPUT_UNDECLARED)
        if accepted_artifact_id in accepted_ids or raw_artifact_id in manifest_ids:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_ANCESTRY_DUPLICATE)
        accepted_ids.add(accepted_artifact_id)
        manifest_ids.add(raw_artifact_id)
        if accepted_artifact_id != raw_artifact_id:
            raise LiveMonthRthDiagnosticError(RAW_PAGE_ARTIFACT_ID_MISMATCH)
        if str(accepted_page.get("raw_page_sha256")) != str(raw_manifest["payload_sha256"]):
            raise LiveMonthRthDiagnosticError(RAW_PAGE_PAYLOAD_DIGEST_MISMATCH)
        try:
            payload_file = _validate_source_evidence_file(root, str(raw_manifest["payload_ref"]), expected_kind="raw_payload")
        except LiveMonthRthDiagnosticError as exc:
            if str(exc) == SOURCE_EVIDENCE_PATH_INVALID:
                raise LiveMonthRthDiagnosticError("raw-page payload is missing") from None
            raise
        if payload_file.identity[2] != int(raw_manifest["payload_byte_size"]):
            raise LiveMonthRthDiagnosticError("raw-page payload byte size mismatch")


def _validate_monthly_manifest_metadata(
    manifest: dict[str, Any],
    *,
    expected_run_id: str,
    expected_artifact_type: str,
) -> None:
    required = {
        "schema_version",
        "artifact_id",
        "run_id",
        "artifact_type",
        "stage",
        "payload_ref",
        "payload_sha256",
        "payload_byte_size",
        "payload_media_type",
        "semantic_payload_digest",
        "input_manifest_refs",
    }
    if required - set(manifest):
        raise LiveMonthRthDiagnosticError("monthly manifest is missing required metadata")
    if manifest["schema_version"] != monthly.MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION:
        raise LiveMonthRthDiagnosticError("monthly manifest schema mismatch")
    if manifest["run_id"] != expected_run_id:
        raise LiveMonthRthDiagnosticError("monthly manifest run mismatch")
    if manifest["artifact_type"] != expected_artifact_type:
        raise LiveMonthRthDiagnosticError("monthly manifest artifact type mismatch")
    if manifest["stage"] != monthly.STAGE_BY_ARTIFACT_TYPE[expected_artifact_type]:
        raise LiveMonthRthDiagnosticError("monthly manifest stage mismatch")
    _require_sha256(str(manifest["payload_sha256"]), "payload_sha256")
    _require_sha256(str(manifest["semantic_payload_digest"]), "semantic_payload_digest")
    if int(manifest["payload_byte_size"]) < 0:
        raise LiveMonthRthDiagnosticError("monthly payload byte size must be nonnegative")


def _validate_normalized_pair(spec: LiveMonthRthDiagnosticSpec, ohlcv_payload: dict[str, Any], audit_payload: dict[str, Any]) -> None:
    ohlcv_rows = _required_list(ohlcv_payload.get("rows"), "ohlcv_rows")
    audit_rows = _required_list(audit_payload.get("rows"), "audit_rows")
    if len(ohlcv_rows) != spec.source_normalized_row_count:
        raise LiveMonthRthDiagnosticError("normalized OHLCV row count mismatch")
    if len(audit_rows) != spec.source_normalized_row_count:
        raise LiveMonthRthDiagnosticError("normalized audit row count mismatch")
    ohlcv_starts = [str(row["window_start_utc"]) for row in ohlcv_rows if isinstance(row, dict)]
    audit_starts = [str(row["window_start_utc"]) for row in audit_rows if isinstance(row, dict)]
    if len(ohlcv_starts) != len(ohlcv_rows) or len(audit_starts) != len(audit_rows):
        raise LiveMonthRthDiagnosticError("normalized rows must be objects")
    if ohlcv_starts != audit_starts:
        raise LiveMonthRthDiagnosticError("normalized OHLCV/audit timestamp alignment mismatch")
    if ohlcv_starts != sorted(ohlcv_starts) or len(ohlcv_starts) != len(set(ohlcv_starts)):
        raise LiveMonthRthDiagnosticError("normalized timestamps must be strictly ascending")
    if ohlcv_starts[0] != spec.source_first_window_start_utc or ohlcv_starts[-1] != spec.source_last_window_start_utc:
        raise LiveMonthRthDiagnosticError("normalized first/last timestamp mismatch")


def _required_receipt(by_id: dict[str, Any], artifact_id: str, semantic_digest: str) -> dict[str, Any]:
    item = by_id.get(artifact_id)
    if not isinstance(item, dict):
        raise LiveMonthRthDiagnosticError("normalized artifact receipt missing")
    if item.get("semantic_payload_digest") != semantic_digest:
        raise LiveMonthRthDiagnosticError("normalized artifact receipt digest mismatch")
    if not isinstance(item.get("manifest_ref"), str):
        raise LiveMonthRthDiagnosticError("normalized artifact receipt manifest ref missing")
    return item


def _smoke_receipt_ref(run_id: str) -> str:
    return f"{_opaque_run_id(run_id)}/smoke_receipt/smoke-receipt.json"


def _load_json_bytes(data: bytes) -> dict[str, Any]:
    payload = json.loads(data.decode("utf-8"))
    if not isinstance(payload, dict):
        raise LiveMonthRthDiagnosticError("JSON payload must be an object")
    return payload


def _required_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise LiveMonthRthDiagnosticError(f"{field_name} must be a list")
    return value


def _require_sha256(value: str, field_name: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise LiveMonthRthDiagnosticError(f"{field_name} must be a SHA-256 digest")


def _parse_utc(value: str, field_name: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise LiveMonthRthDiagnosticError(f"{field_name} must be UTC")
    return parsed.astimezone(UTC)


def _required_decimal_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise LiveMonthRthDiagnosticError(f"{field_name} must be an exact Decimal string")
    Decimal(value)
    return value


def _opaque_run_id(value: str) -> str:
    if not value or any(part in value for part in ("/", "\\", "..", ":", "*", "?", "[", "]", "\x00")):
        raise LiveMonthRthDiagnosticError("run ID must be opaque")
    upper = value.upper()
    if any(fragment in upper for fragment in FORBIDDEN_RUN_ID_FRAGMENTS):
        raise LiveMonthRthDiagnosticError("run ID must be opaque")
    return value


def _validated_generated_run_id(value: str) -> str:
    run_id = _opaque_run_id(value)
    if re.fullmatch(r"rthdiag-[0-9a-f]{32}", run_id) is None:
        raise LiveMonthRthDiagnosticError("run ID must match generated diagnostic format")
    return run_id


def _build_synthetic_smoke_source(root: Path, *, complete: bool) -> LiveMonthRthDiagnosticSpec:
    calendar = january_session_view(
        frozen_calendar.generate_frozen_calendar(
            frozen_calendar.default_calendar_request(
                requested_primary_listing_mic="XNAS",
                requested_calendar_token="XNAS",
                official_exchange_evidence_identity=OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY,
                official_exchange_evidence_digest="OFFICIAL_EVIDENCE_DIGEST_PENDING",
            )
        )
    ).calendar
    rows = []
    for session in calendar.sessions:
        if session.session_classification != frozen_calendar.NORMAL_FULL_SESSION:
            continue
        expected = list(rth.expected_source_windows(session))
        if not complete and session.session_date == "2025-01-02":
            expected = expected[1:]
        rows.extend(expected)
    rows = sorted(rows)
    request = monthly.build_month_chunk_request(
        canonical_ticker="FAKEFLOW",
        month_key="2025-01",
        effective_start_date="2025-01-01",
        effective_end_date="2025-01-31",
    )
    page = monthly.build_logical_page_request(request, page_ordinal=1)
    body = _provider_body([int(item.timestamp() * 1000) for item in rows])
    receipt = monthly.execute_fake_monthly_acquisition(
        month_request=request,
        transport=ScriptedFakeTransport([ScriptedExchange(monthly.fake_transport_request(request, page), http_response(200, body))]),
        run_root=root,
        run_id="smoke-c3388f68530c4131a090a895953e3d89",
        clock=monthly.DeterministicClock(),
        sleeper=monthly.RecordingSleeper([]),
        provenance="LIVE_PROVIDER_SMOKE_NONCANONICAL",
        provider_execution_enabled=False,
    )
    normalized = [
        item
        for item in receipt["artifact_receipts"]
        if item["artifact_type"] in {monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV, monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS}
    ]
    smoke_receipt = {
        "smoke_status": "SMOKE_COMPLETED_NONCANONICAL",
        "smoke_specification_digest": "0" * 64,
        "smoke_run_id": "smoke-c3388f68530c4131a090a895953e3d89",
        "classification": "NONCANONICAL_PROVIDER_SMOKE",
        "provenance": "LIVE_PROVIDER_SMOKE_NONCANONICAL",
        "provider_identity": "MASSIVE.COM",
        "ticker": "FAKEFLOW",
        "month_key": "2025-01",
        "request_status": monthly.MONTH_ACQUISITION_COMPLETED,
        "provider_execution_enabled": False,
        "attempt_count": 1,
        "accepted_page_count": 1,
        "pagination_status": monthly.PAGINATION_EXHAUSTED,
        "completeness_status": "COMPLETE",
        "normalized_artifact_receipts": normalized,
        "raw_page_count": 1,
        "total_normalized_row_count": receipt["row_count"],
        "first_source_window_start_utc": rows[0].isoformat().replace("+00:00", "Z"),
        "last_source_window_start_utc": rows[-1].isoformat().replace("+00:00", "Z"),
        "contract_v2_1_digest": contract_v21.contract_digest(contract_v21.default_contract()),
        "strategy_enabled": False,
        "calendar_bar_derivation_enabled": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "acquisition_enabled": False,
        "runtime_migration_enabled": False,
        "fixed_findings": [],
        "sanitization": "NO_KEY_NO_AUTH_HEADER_NO_RAW_URL_NO_NEXT_URL_NO_RAW_BODY_NO_OHLCV_NO_ABSOLUTE_PATHS_NO_RAW_EXCEPTIONS",
    }
    receipt_dir = root / "smoke-c3388f68530c4131a090a895953e3d89" / "smoke_receipt"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / "smoke-receipt.json"
    receipt_path.write_bytes(artifacts.canonical_json_bytes(smoke_receipt))
    by_type = {item["artifact_type"]: item for item in normalized}
    return LiveMonthRthDiagnosticSpec(
        schema_version=DIAGNOSTIC_SCHEMA_VERSION,
        classification=DIAGNOSTIC_CLASSIFICATION,
        source_smoke_run_id="smoke-c3388f68530c4131a090a895953e3d89",
        source_smoke_receipt_sha256=artifacts.sha256_file(receipt_path),
        source_ticker="FAKEFLOW",
        source_month="2025-01",
        source_normalized_row_count=receipt["row_count"],
        source_first_window_start_utc=smoke_receipt["first_source_window_start_utc"],
        source_last_window_start_utc=smoke_receipt["last_source_window_start_utc"],
        source_normalized_ohlcv_artifact_id=by_type[monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV]["artifact_id"],
        source_normalized_ohlcv_semantic_digest=by_type[monthly.ARTIFACT_MONTH_NORMALIZED_15M_OHLCV]["semantic_payload_digest"],
        source_normalized_audit_artifact_id=by_type[monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS]["artifact_id"],
        source_normalized_audit_semantic_digest=by_type[monthly.ARTIFACT_MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS]["semantic_payload_digest"],
        requested_primary_listing_mic="XNAS",
        requested_calendar_token="XNAS",
        identity_evidence_classification=OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY,
        calendar_authority=CALENDAR_AUTHORITY_NOT_OPERATOR_FROZEN,
        calendar_freeze_eligible=False,
        canonical_eligibility=False,
        registry_eligibility=False,
        strategy_enabled=False,
        performance_enabled=False,
    )


def _provider_body(timestamps: list[int]) -> bytes:
    rows = []
    for index, timestamp in enumerate(timestamps):
        value = 100 + index
        rows.append(
            '{"c":%s,"h":%s,"l":%s,"n":1,"o":%s,"t":%s,"v":1000}'
            % (value, value + 1, value - 1, value, timestamp)
        )
    return (
        '{"adjusted":true,"queryCount":'
        + str(len(rows))
        + ',"results":['
        + ",".join(rows)
        + '],"resultsCount":'
        + str(len(rows))
        + ',"count":'
        + str(len(rows))
        + ',"status":"OK","ticker":"FAKEFLOW"}'
    ).encode("utf-8")
