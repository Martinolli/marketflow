"""Offline SWING registry approval candidate helpers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import swing_canonical_dataset_operator_freeze_service as swing_freeze
from marketflow.services import swing_canonical_dataset_service as swing


ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE = "SWING_REGISTRY_APPROVAL_CANDIDATE"
SCHEMA_VERSION_SWING_REGISTRY_APPROVAL_CANDIDATE_V1 = "swing_registry_approval_candidate_v1"
SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW = "SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW"
SWING_FROZEN_STATUS_BINDING = "SWING_FROZEN_STATUS_BINDING"
SWING_FROZEN_ARTIFACT_BINDING = "SWING_FROZEN_ARTIFACT_BINDING"

EXPECTED_SWING_FROZEN_DIGEST = "03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e"
EXPECTED_SWING_REVIEW_PACKAGE_DIGEST = swing_freeze.EXPECTED_SWING_REVIEW_PACKAGE_DIGEST
EXPECTED_SWING_CANDIDATE_DIGEST = swing_freeze.EXPECTED_SWING_CANDIDATE_DIGEST
EXPECTED_DATASET_ROWS_DIGEST = swing_freeze.EXPECTED_DATASET_ROWS_DIGEST
EXPECTED_DATASET_MANIFEST_DIGEST = swing_freeze.EXPECTED_DATASET_MANIFEST_DIGEST
EXPECTED_SOURCE_ROWS_DIGEST = swing_freeze.EXPECTED_SOURCE_ROWS_DIGEST
EXPECTED_MATERIALIZATION_RECEIPT_DIGEST = swing_freeze.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST
EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST = swing_freeze.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST
EXPECTED_SWING_BAR_COUNT = swing_freeze.EXPECTED_SWING_BAR_COUNT
EXPECTED_SOURCE_RTH_ROWS_CONSUMED = swing_freeze.EXPECTED_SOURCE_RTH_ROWS_CONSUMED
EXPECTED_SOURCE_RTH_ROWS_EXCLUDED = swing_freeze.EXPECTED_SOURCE_RTH_ROWS_EXCLUDED
EXPECTED_FULL_SESSIONS_USED = swing_freeze.EXPECTED_FULL_SESSIONS_USED
EXPECTED_SPECIAL_SESSIONS_EXCLUDED = swing_freeze.EXPECTED_SPECIAL_SESSIONS_EXCLUDED
EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED = swing_freeze.EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED
EXPECTED_CROSS_CHECK_STATUS = swing_freeze.EXPECTED_CROSS_CHECK_STATUS
EXPECTED_CROSS_CHECK_SWING_BARS = swing_freeze.EXPECTED_CROSS_CHECK_SWING_BARS
EXPECTED_SPECIAL_SESSION_POLICY = swing_freeze.EXPECTED_SPECIAL_SESSION_POLICY

PROPOSED_REGISTRY_KEY = "AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1"
PROPOSED_REGISTRY_SCOPE = "RESEARCH_DATASET"
NOT_AUTHORIZED = "NOT_AUTHORIZED"

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_CHECK_IDS = [
    "swing_canonical_dataset_frozen_true",
    "swing_frozen_digest_matches",
    "swing_review_package_digest_matches",
    "swing_candidate_digest_matches",
    "dataset_rows_digest_matches",
    "dataset_manifest_digest_matches",
    "source_rows_digest_matches",
    "materialization_receipt_digest_matches",
    "identity_frozen_digest_matches",
    "calendar_frozen_digest_matches",
    "schedule_digest_matches",
    "split_event_frozen_digest_matches",
    "dividend_event_frozen_digest_matches",
    "acquisition_generation_frozen_digest_matches",
    "dataset_profile_swing",
    "dataset_bar_rule_rth_half_session_195m",
    "swing_bar_count_1988",
    "source_rth_rows_consumed_25844",
    "source_rth_rows_excluded_126",
    "full_sessions_used_994",
    "special_session_policy_full_ordinary_only",
    "special_sessions_excluded_9",
    "special_session_rows_excluded_126",
    "cross_check_2025_01_passed",
    "cross_check_2025_01_swing_bars_40",
    "dividend_implication_preserved",
    "registry_key_constructed",
    "registry_scope_research_dataset",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "registry_activation_false",
    "registry_approval_created_false",
    "canonical_eligibility_false",
    "registry_eligibility_false",
    "strategy_runtime_migration_false",
    "automatic_stitching_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "provider_requests_made_false",
]

REMAINING_REQUIRED_TASKS = [
    "SWING registry operator review package.",
    "SWING registry approval ceremony.",
    "POSITION_SWING canonical dataset candidate.",
]


class SwingRegistryApprovalError(ValueError):
    """Raised when a SWING registry approval candidate violates guardrails."""


def _check(check_id: str, expected: Any, actual: Any, *, message: str | None = None) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SwingRegistryApprovalError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SwingRegistryApprovalError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SwingRegistryApprovalError(f"{field_name} must be true")


def _fixed_segment() -> dict[str, Any]:
    segment = acquisition.FIXED_IDENTITY_SEGMENT
    return {
        "ticker": segment["ticker"],
        "composite_figi": segment["composite_figi"],
        "share_class_figi": segment["share_class_figi"],
        "primary_mic": segment["primary_mic"],
        "security_type": segment["security_type"],
        "range_start": segment["segment_start"],
        "range_end": segment["segment_end"],
    }


def _authority_bindings() -> dict[str, Any]:
    return {
        "identity_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_generation_frozen_digest": EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
    }


def _recorded_swing_frozen_evidence() -> dict[str, Any]:
    return {
        "swing_canonical_dataset_frozen": True,
        "swing_canonical_dataset_frozen_digest": EXPECTED_SWING_FROZEN_DIGEST,
        "swing_review_package_digest": EXPECTED_SWING_REVIEW_PACKAGE_DIGEST,
        "swing_candidate_digest": EXPECTED_SWING_CANDIDATE_DIGEST,
        "dataset_rows_digest": EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": EXPECTED_DATASET_MANIFEST_DIGEST,
        "source_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "swing_bar_count": EXPECTED_SWING_BAR_COUNT,
        "source_rth_rows_consumed": EXPECTED_SOURCE_RTH_ROWS_CONSUMED,
        "source_rth_rows_excluded": EXPECTED_SOURCE_RTH_ROWS_EXCLUDED,
        "full_sessions_used": EXPECTED_FULL_SESSIONS_USED,
        "special_session_policy": EXPECTED_SPECIAL_SESSION_POLICY,
        "special_sessions_excluded": EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
        "special_session_rows_excluded": EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED,
        "cross_check_2025_01_status": EXPECTED_CROSS_CHECK_STATUS,
        "cross_check_2025_01_swing_bars": EXPECTED_CROSS_CHECK_SWING_BARS,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "source_adjusted_data_used": True,
    }


def _frozen_evidence_from_artifact(frozen_artifact: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = swing_freeze.validate_swing_canonical_dataset_frozen_v1(frozen_artifact)
    except swing_freeze.SwingCanonicalDatasetOperatorFreezeError as exc:
        raise SwingRegistryApprovalError(f"source SWING frozen artifact invalid: {exc}") from exc
    _expect(
        validation["swing_canonical_dataset_frozen_semantic_digest"],
        EXPECTED_SWING_FROZEN_DIGEST,
        "source SWING frozen semantic digest",
    )
    return {
        "swing_canonical_dataset_frozen": frozen_artifact["swing_canonical_dataset_frozen"],
        "swing_canonical_dataset_frozen_digest": frozen_artifact["swing_canonical_dataset_frozen_semantic_digest"],
        "swing_review_package_digest": frozen_artifact["source_swing_review_package_semantic_digest"],
        "swing_candidate_digest": frozen_artifact["source_swing_candidate_digest"],
        "dataset_rows_digest": frozen_artifact["source_dataset_rows_digest"],
        "dataset_manifest_digest": frozen_artifact["source_dataset_manifest_digest"],
        "source_rows_digest": frozen_artifact["source_normalized_rows_digest"],
        "materialization_receipt_digest": frozen_artifact["source_materialization_receipt_digest"],
        "swing_bar_count": frozen_artifact["swing_bar_count"],
        "source_rth_rows_consumed": frozen_artifact["source_rth_rows_consumed"],
        "source_rth_rows_excluded": frozen_artifact["source_rth_rows_excluded"],
        "full_sessions_used": frozen_artifact["full_sessions_used"],
        "special_session_policy": frozen_artifact["special_session_policy"],
        "special_sessions_excluded": frozen_artifact["special_sessions_excluded"],
        "special_session_rows_excluded": frozen_artifact["special_session_rows_excluded"],
        "cross_check_2025_01_status": frozen_artifact["cross_check_2025_01_status"],
        "cross_check_2025_01_swing_bars": frozen_artifact["cross_check_2025_01_swing_bars"],
        "in_range_dividends_found": frozen_artifact["in_range_dividends_found"],
        "in_range_dividend_count": frozen_artifact["in_range_dividend_count"],
        "in_range_dividend_implication": frozen_artifact["in_range_dividend_implication"],
        "source_adjusted_data_used": frozen_artifact["source_adjusted_data_used"],
    }


def _build_checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _check("swing_canonical_dataset_frozen_true", True, candidate.get("swing_canonical_dataset_frozen")),
        _check("swing_frozen_digest_matches", EXPECTED_SWING_FROZEN_DIGEST, candidate.get("swing_canonical_dataset_frozen_digest")),
        _check("swing_review_package_digest_matches", EXPECTED_SWING_REVIEW_PACKAGE_DIGEST, candidate.get("swing_review_package_digest")),
        _check("swing_candidate_digest_matches", EXPECTED_SWING_CANDIDATE_DIGEST, candidate.get("swing_candidate_digest")),
        _check("dataset_rows_digest_matches", EXPECTED_DATASET_ROWS_DIGEST, candidate.get("dataset_rows_digest")),
        _check("dataset_manifest_digest_matches", EXPECTED_DATASET_MANIFEST_DIGEST, candidate.get("dataset_manifest_digest")),
        _check("source_rows_digest_matches", EXPECTED_SOURCE_ROWS_DIGEST, candidate.get("source_rows_digest")),
        _check("materialization_receipt_digest_matches", EXPECTED_MATERIALIZATION_RECEIPT_DIGEST, candidate.get("materialization_receipt_digest")),
        _check("identity_frozen_digest_matches", acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST, candidate.get("identity_frozen_digest")),
        _check("calendar_frozen_digest_matches", acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST, candidate.get("calendar_frozen_digest")),
        _check("schedule_digest_matches", acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST, candidate.get("schedule_digest")),
        _check("split_event_frozen_digest_matches", acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST, candidate.get("split_event_frozen_digest")),
        _check("dividend_event_frozen_digest_matches", acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST, candidate.get("dividend_event_frozen_digest")),
        _check("acquisition_generation_frozen_digest_matches", EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST, candidate.get("acquisition_generation_frozen_digest")),
        _check("dataset_profile_swing", swing.DATASET_PROFILE_SWING, candidate.get("dataset_profile")),
        _check("dataset_bar_rule_rth_half_session_195m", swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M, candidate.get("dataset_bar_rule")),
        _check("swing_bar_count_1988", EXPECTED_SWING_BAR_COUNT, candidate.get("swing_bar_count")),
        _check("source_rth_rows_consumed_25844", EXPECTED_SOURCE_RTH_ROWS_CONSUMED, candidate.get("source_rth_rows_consumed")),
        _check("source_rth_rows_excluded_126", EXPECTED_SOURCE_RTH_ROWS_EXCLUDED, candidate.get("source_rth_rows_excluded")),
        _check("full_sessions_used_994", EXPECTED_FULL_SESSIONS_USED, candidate.get("full_sessions_used")),
        _check("special_session_policy_full_ordinary_only", EXPECTED_SPECIAL_SESSION_POLICY, candidate.get("special_session_policy")),
        _check("special_sessions_excluded_9", EXPECTED_SPECIAL_SESSIONS_EXCLUDED, candidate.get("special_sessions_excluded")),
        _check("special_session_rows_excluded_126", EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED, candidate.get("special_session_rows_excluded")),
        _check("cross_check_2025_01_passed", EXPECTED_CROSS_CHECK_STATUS, candidate.get("cross_check_2025_01_status")),
        _check("cross_check_2025_01_swing_bars_40", EXPECTED_CROSS_CHECK_SWING_BARS, candidate.get("cross_check_2025_01_swing_bars")),
        _check("dividend_implication_preserved", acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION, candidate.get("in_range_dividend_implication")),
        _check("registry_key_constructed", PROPOSED_REGISTRY_KEY, candidate.get("proposed_registry_key")),
        _check("registry_scope_research_dataset", PROPOSED_REGISTRY_SCOPE, candidate.get("proposed_registry_scope")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("proposed_runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("proposed_strategy_use")),
        _check("registry_activation_false", False, candidate.get("proposed_registry_activation")),
        _check("registry_approval_created_false", False, candidate.get("registry_approval_created")),
        _check("canonical_eligibility_false", False, candidate.get("canonical_eligibility")),
        _check("registry_eligibility_false", False, candidate.get("registry_eligibility")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item["status"] == PASS)
    failed = total - passed
    blocker_count = sum(1 for item in checklist if item["status"] == FAIL and item["severity"] == BLOCKER)
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_registry_review": failed == 0,
        "operator_approval_required": True,
        "software_registry_approval": False,
        "runtime_migration_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("swing_registry_approval_candidate_semantic_digest", None)
    return payload


def swing_registry_approval_candidate_semantic_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a SWING registry approval candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_swing_registry_approval_candidate_v1(
    *,
    swing_frozen_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline candidate for later SWING registry approval review."""
    binding_mode = SWING_FROZEN_STATUS_BINDING
    frozen_evidence = _recorded_swing_frozen_evidence()
    if swing_frozen_artifact is not None:
        binding_mode = SWING_FROZEN_ARTIFACT_BINDING
        frozen_evidence = _frozen_evidence_from_artifact(swing_frozen_artifact)
    identity = _fixed_segment()
    authority = _authority_bindings()
    candidate: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE,
        "schema_version": SCHEMA_VERSION_SWING_REGISTRY_APPROVAL_CANDIDATE_V1,
        "candidate_status": SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW,
        "binding_mode": binding_mode,
        "operator_review_required": True,
        "operator_approval_required": True,
        "created_offline": True,
        "provider_requests_made": False,
        "registry_approval_created": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "registry_candidate_profile": swing.DATASET_PROFILE_SWING,
        "registry_candidate_dataset_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "registry_candidate_ticker": identity["ticker"],
        "registry_candidate_range_start": identity["range_start"],
        "registry_candidate_range_end": identity["range_end"],
        "registry_candidate_version": "v1",
        "registry_candidate_status": SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW,
        "dataset_profile": swing.DATASET_PROFILE_SWING,
        "dataset_bar_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "ticker": identity["ticker"],
        "composite_figi": identity["composite_figi"],
        "share_class_figi": identity["share_class_figi"],
        "primary_mic": identity["primary_mic"],
        "security_type": identity["security_type"],
        "range_start": identity["range_start"],
        "range_end": identity["range_end"],
        "dataset_version_candidate": "v1",
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": True,
        "proposed_registry_key": PROPOSED_REGISTRY_KEY,
        "proposed_registry_scope": PROPOSED_REGISTRY_SCOPE,
        "proposed_runtime_use": NOT_AUTHORIZED,
        "proposed_strategy_use": NOT_AUTHORIZED,
        "proposed_registry_activation": False,
        "requires_operator_registry_review": True,
        "requires_registry_approval_ceremony": True,
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
        **frozen_evidence,
        **authority,
    }
    checklist = _build_checklist(candidate)
    candidate["registry_candidate_checklist"] = checklist
    candidate["registry_candidate_summary"] = _summary(checklist)
    candidate["swing_registry_approval_candidate_semantic_digest"] = (
        swing_registry_approval_candidate_semantic_digest_v1(candidate)
    )
    validate_swing_registry_approval_candidate_v1(candidate)
    return candidate


def validate_swing_registry_approval_candidate_v1(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate a SWING registry approval candidate without approving registry use."""
    if not isinstance(candidate, dict):
        raise SwingRegistryApprovalError("candidate must be a JSON object")
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_SWING_REGISTRY_APPROVAL_CANDIDATE_V1, "schema_version")
    _expect(candidate.get("candidate_status"), SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    _expect(candidate.get("registry_candidate_status"), SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW, "registry_candidate_status")
    if candidate.get("binding_mode") not in {SWING_FROZEN_STATUS_BINDING, SWING_FROZEN_ARTIFACT_BINDING}:
        raise SwingRegistryApprovalError("binding_mode mismatch")
    for field in (
        "operator_review_required",
        "operator_approval_required",
        "created_offline",
        "requires_operator_registry_review",
        "requires_registry_approval_ceremony",
        "identity_segment_frozen",
        "calendar_operator_frozen",
        "split_event_audit_frozen",
        "dividend_event_audit_frozen",
        "acquisition_generation_freeze",
        "swing_canonical_dataset_frozen",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "registry_approval_created",
        "registry_eligibility",
        "canonical_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "proposed_registry_activation",
    ):
        _expect_false(candidate.get(field), field)
    _expect(candidate.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _expect(candidate.get("proposed_runtime_use"), NOT_AUTHORIZED, "proposed_runtime_use")
    _expect(candidate.get("proposed_strategy_use"), NOT_AUTHORIZED, "proposed_strategy_use")
    _expect(candidate.get("proposed_registry_scope"), PROPOSED_REGISTRY_SCOPE, "proposed_registry_scope")
    _expect(candidate.get("proposed_registry_key"), PROPOSED_REGISTRY_KEY, "proposed_registry_key")
    for field, expected in {
        "registry_candidate_profile": swing.DATASET_PROFILE_SWING,
        "registry_candidate_dataset_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "registry_candidate_ticker": "AAPL",
        "registry_candidate_range_start": "2022-01-01",
        "registry_candidate_range_end": "2025-12-31",
        "registry_candidate_version": "v1",
        "dataset_profile": swing.DATASET_PROFILE_SWING,
        "dataset_bar_rule": swing.DATASET_BAR_RULE_RTH_HALF_SESSION_195M,
        "ticker": "AAPL",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "primary_mic": "XNAS",
        "security_type": "CS",
        "range_start": "2022-01-01",
        "range_end": "2025-12-31",
        "dataset_version_candidate": "v1",
        "swing_canonical_dataset_frozen_digest": EXPECTED_SWING_FROZEN_DIGEST,
        "swing_review_package_digest": EXPECTED_SWING_REVIEW_PACKAGE_DIGEST,
        "swing_candidate_digest": EXPECTED_SWING_CANDIDATE_DIGEST,
        "dataset_rows_digest": EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": EXPECTED_DATASET_MANIFEST_DIGEST,
        "source_rows_digest": EXPECTED_SOURCE_ROWS_DIGEST,
        "materialization_receipt_digest": EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "swing_bar_count": EXPECTED_SWING_BAR_COUNT,
        "source_rth_rows_consumed": EXPECTED_SOURCE_RTH_ROWS_CONSUMED,
        "source_rth_rows_excluded": EXPECTED_SOURCE_RTH_ROWS_EXCLUDED,
        "full_sessions_used": EXPECTED_FULL_SESSIONS_USED,
        "special_session_policy": EXPECTED_SPECIAL_SESSION_POLICY,
        "special_sessions_excluded": EXPECTED_SPECIAL_SESSIONS_EXCLUDED,
        "special_session_rows_excluded": EXPECTED_SPECIAL_SESSION_ROWS_EXCLUDED,
        "cross_check_2025_01_status": EXPECTED_CROSS_CHECK_STATUS,
        "cross_check_2025_01_swing_bars": EXPECTED_CROSS_CHECK_SWING_BARS,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        **_authority_bindings(),
    }.items():
        _expect(candidate.get(field), expected, field)
    _expect_true(candidate.get("in_range_dividends_found"), "in_range_dividends_found")
    _expect_true(candidate.get("source_adjusted_data_used"), "source_adjusted_data_used")
    _expect(candidate.get("remaining_required_tasks"), REMAINING_REQUIRED_TASKS, "remaining_required_tasks")
    checklist = candidate.get("registry_candidate_checklist")
    if not isinstance(checklist, list):
        raise SwingRegistryApprovalError("registry_candidate_checklist must be a list")
    _expect([item.get("check_id") for item in checklist if isinstance(item, dict)], REQUIRED_CHECK_IDS, "registry_candidate_checklist check IDs")
    expected_checklist = _build_checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise SwingRegistryApprovalError(f"registry candidate checklist contains failed check: {failed[0]['check_id']}")
    _expect(checklist, expected_checklist, "registry_candidate_checklist")
    summary = _summary(checklist)
    _expect(candidate.get("registry_candidate_summary"), summary, "registry_candidate_summary")
    _expect_true(summary.get("ready_for_operator_registry_review"), "ready_for_operator_registry_review")
    _expect_true(summary.get("operator_approval_required"), "operator_approval_required")
    _expect_false(summary.get("software_registry_approval"), "software_registry_approval")
    _expect_false(summary.get("runtime_migration_authorized"), "runtime_migration_authorized")
    digest = candidate.get("swing_registry_approval_candidate_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise SwingRegistryApprovalError("swing_registry_approval_candidate_semantic_digest missing")
    _expect(digest, swing_registry_approval_candidate_semantic_digest_v1(candidate), "swing_registry_approval_candidate_semantic_digest")
    return {
        "status": "SWING_REGISTRY_APPROVAL_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "proposed_registry_key": candidate["proposed_registry_key"],
        "swing_registry_approval_candidate_semantic_digest": digest,
        "swing_canonical_dataset_frozen_digest": EXPECTED_SWING_FROZEN_DIGEST,
        "dataset_rows_digest": EXPECTED_DATASET_ROWS_DIGEST,
        "dataset_manifest_digest": EXPECTED_DATASET_MANIFEST_DIGEST,
        "total_checks": summary["total_checks"],
        "passed_checks": summary["passed_checks"],
        "failed_checks": summary["failed_checks"],
        "blocker_count": summary["blocker_count"],
        "ready_for_operator_registry_review": True,
        "registry_approval_created": False,
        "registry_eligibility": False,
        "canonical_eligibility": False,
        "strategy_runtime_migration": False,
        "provider_requests_made": False,
    }


def build_swing_registry_approval_candidate_markdown_v1(candidate: dict[str, Any]) -> str:
    """Render a sanitized SWING registry approval candidate status document."""
    validation = validate_swing_registry_approval_candidate_v1(candidate)
    summary = candidate["registry_candidate_summary"]
    lines = [
        "# MarketFlow SWING Registry Approval Candidate Status",
        "",
        "## Title",
        "- SWING Registry Approval Candidate v1.",
        "",
        "## Proposed Registry Entry",
        f"- Artifact kind: `{candidate['artifact_kind']}`",
        f"- Candidate status: `{candidate['candidate_status']}`",
        f"- Proposed registry key: `{candidate['proposed_registry_key']}`",
        f"- Proposed registry scope: `{candidate['proposed_registry_scope']}`",
        f"- Proposed runtime use: `{candidate['proposed_runtime_use']}`",
        f"- Proposed strategy use: `{candidate['proposed_strategy_use']}`",
        f"- Proposed registry activation: `{candidate['proposed_registry_activation']}`",
        "",
        "## Frozen SWING Dataset Evidence",
        f"- SWING frozen digest: `{candidate['swing_canonical_dataset_frozen_digest']}`",
        f"- SWING review package digest: `{candidate['swing_review_package_digest']}`",
        f"- SWING candidate digest: `{candidate['swing_candidate_digest']}`",
        f"- Dataset rows digest: `{candidate['dataset_rows_digest']}`",
        f"- Dataset manifest digest: `{candidate['dataset_manifest_digest']}`",
        f"- Source rows digest: `{candidate['source_rows_digest']}`",
        f"- Materialization receipt digest: `{candidate['materialization_receipt_digest']}`",
        "",
        "## Dataset Summary",
        f"- Dataset profile: `{candidate['dataset_profile']}`",
        f"- Dataset bar rule: `{candidate['dataset_bar_rule']}`",
        f"- SWING bar count: `{candidate['swing_bar_count']}`",
        f"- Source RTH rows consumed: `{candidate['source_rth_rows_consumed']}`",
        f"- Source RTH rows excluded: `{candidate['source_rth_rows_excluded']}`",
        "",
        "## 2025-01 Cross-Check",
        f"- Cross-check status: `{candidate['cross_check_2025_01_status']}`",
        f"- Cross-check SWING bars: `{candidate['cross_check_2025_01_swing_bars']}`",
        "",
        "## Special-Session Policy",
        f"- Policy: `{candidate['special_session_policy']}`",
        f"- Special sessions excluded: `{candidate['special_sessions_excluded']}`",
        f"- Special session rows excluded: `{candidate['special_session_rows_excluded']}`",
        "",
        "## Authority Bindings",
        f"- Identity frozen digest: `{candidate['identity_frozen_digest']}`",
        f"- Calendar frozen digest: `{candidate['calendar_frozen_digest']}`",
        f"- Schedule digest: `{candidate['schedule_digest']}`",
        f"- Split-event audit frozen digest: `{candidate['split_event_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{candidate['dividend_event_frozen_digest']}`",
        f"- Acquisition generation frozen digest: `{candidate['acquisition_generation_frozen_digest']}`",
        "",
        "## Dividend Implication",
        f"- In-range dividends found: `{candidate['in_range_dividends_found']}`",
        f"- In-range dividend count: `{candidate['in_range_dividend_count']}`",
        f"- Implication: `{candidate['in_range_dividend_implication']}`",
        f"- Source adjusted data used: `{candidate['source_adjusted_data_used']}`",
        "",
        "## Registry Boundary",
        f"- Registry approval created: `{candidate['registry_approval_created']}`",
        f"- Registry eligibility: `{candidate['registry_eligibility']}`",
        f"- Canonical eligibility: `{candidate['canonical_eligibility']}`",
        f"- Strategy runtime migration: `{candidate['strategy_runtime_migration']}`",
        f"- Predictive usefulness: `{candidate['predictive_usefulness']}`",
        f"- Profitability: `{candidate['profitability']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Ready for operator registry review: `{summary['ready_for_operator_registry_review']}`",
        f"- Software registry approval: `{summary['software_registry_approval']}`",
        f"- Runtime migration authorized: `{summary['runtime_migration_authorized']}`",
        "",
        "## Remaining Required Tasks",
    ]
    lines.extend(f"{index}. {task}" for index, task in enumerate(candidate["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made: `False`",
            "- No Massive.com / Polygon provider data was fetched.",
            "- No acquisition rows or SWING bars were regenerated.",
            "- No SWING registry approval, registry eligibility, or runtime migration occurred.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
            "## Candidate Digest",
            f"- Candidate digest: `{validation['swing_registry_approval_candidate_semantic_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_swing_registry_approval_candidate_v1(
    output_dir: str | Path,
    *,
    swing_frozen_artifact: dict[str, Any] | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the SWING registry approval candidate JSON artifact without overwriting output."""
    candidate = build_swing_registry_approval_candidate_v1(swing_frozen_artifact=swing_frozen_artifact)
    validation = validate_swing_registry_approval_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_registry_approval_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise SwingRegistryApprovalError("SWING registry approval candidate filename must be a simple JSON filename")
    path = directory / output_name
    if path.exists():
        raise SwingRegistryApprovalError("SWING registry approval candidate output already exists")
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
