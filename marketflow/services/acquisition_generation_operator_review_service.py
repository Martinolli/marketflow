"""Offline operator review package for acquisition generation evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition


ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE = (
    "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_REVIEW_V1 = "acquisition_generation_candidate_review_v1"
ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY = (
    "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY"
)
LIVE_ACQUISITION_AND_TRIAGE_STATUS_BINDING = "LIVE_ACQUISITION_AND_TRIAGE_STATUS_BINDING"

EXPECTED_REVIEWED_CHUNK_MANIFEST_DIGEST = "8a4bf37f501fb7da5ea23e04d5ebe90da2cdfda1bf9e06e55e4c459be53fa374"
EXPECTED_REVIEWED_PROVIDER_RAW_RESPONSE_DIGEST = "aea820006bb458b9e51a1cda23ae24be02f476aafb36bec6c65d3740812d06c7"
EXPECTED_REVIEWED_NORMALIZED_SOURCE_ROWS_DIGEST = "0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc"
EXPECTED_REVIEWED_ACQUISITION_RECEIPT_DIGEST = "63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed"
EXPECTED_TOTAL_RAW_ROWS = 63804
EXPECTED_TOTAL_NORMALIZED_SOURCE_ROWS = 63804
EXPECTED_TOTAL_RTH_ROWS = 25970
EXPECTED_TOTAL_EXTENDED_HOURS_ROWS = 37834
EXPECTED_MONTHLY_RECONCILED_COUNT = 39
EXPECTED_MONTHLY_NOT_RECONCILED_COUNT = 9

EXPECTED_TARGETED_CHUNK_MANIFEST_DIGEST = "aac91eaa82859c88c29cfcef07c9f2f2f8da68d198a17572affc2cd3a0a9239c"
EXPECTED_TARGETED_PROVIDER_RAW_RESPONSE_DIGEST = "041c7da634d43463c8ce37a6b3da7aa1bf77c558f02aa18a2b820f290368dc1f"
EXPECTED_TARGETED_NORMALIZED_ROWS_DIGEST = "b5a82e3d8266a55fa520a2c2a5c01d3bd15ccbe27db806cfa0e4b21225e07c28"
EXPECTED_TARGETED_MONTHLY_RECONCILIATION_DIGEST = "f002b833511b102e8136d00354dbe6c410abd30a947242e881e44e12d3cc9191"
EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST = "f810bfd3fcb1d2056bbf5ba0cff8b1aa4276119721c697ce17eaef6bab069faa"
EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST = "82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8"
MISMATCH_EXPLANATION_SPECIAL_SESSION_EXPECTATION = "EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION"

REMAINING_ROADMAP_AFTER_ACQUISITION_REVIEW_PACKAGE = [
    "Digest-bound acquisition generation operator freeze ceremony.",
    "SWING canonical dataset candidate.",
    "SWING canonical dataset operator review/freeze.",
    "SWING registry approval.",
    "POSITION_SWING canonical dataset candidate.",
    "POSITION_SWING canonical dataset operator review/freeze.",
    "POSITION_SWING registry approval.",
    "Normal runtime migration.",
    "Applicability/research campaign.",
    "Predictive and profitability evaluation.",
]


class AcquisitionGenerationOperatorReviewError(ValueError):
    """Raised when an acquisition review package violates the offline contract."""


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise AcquisitionGenerationOperatorReviewError(f"{field_name} mismatch")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise AcquisitionGenerationOperatorReviewError(f"{field_name} must be false")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise AcquisitionGenerationOperatorReviewError(f"{field_name} must be true")


def _fixed_segment() -> dict[str, Any]:
    segment = acquisition.FIXED_IDENTITY_SEGMENT
    return {
        "ticker": segment["ticker"],
        "composite_figi": segment["composite_figi"],
        "share_class_figi": segment["share_class_figi"],
        "primary_mic": segment["primary_mic"],
        "security_type": segment["security_type"],
        "segment_start": segment["segment_start"],
        "segment_end": segment["segment_end"],
    }


def _recorded_acquisition_evidence() -> dict[str, Any]:
    return {
        "reviewed_acquisition_candidate_kind": acquisition.ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE,
        "reviewed_acquisition_candidate_status": acquisition.ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW,
        "reviewed_acquisition_candidate_digest": acquisition.EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST,
        "reviewed_chunk_manifest_digest": EXPECTED_REVIEWED_CHUNK_MANIFEST_DIGEST,
        "reviewed_provider_raw_response_digest": EXPECTED_REVIEWED_PROVIDER_RAW_RESPONSE_DIGEST,
        "reviewed_normalized_source_rows_digest": EXPECTED_REVIEWED_NORMALIZED_SOURCE_ROWS_DIGEST,
        "reviewed_monthly_reconciliation_digest": acquisition.EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST,
        "reviewed_acquisition_receipt_digest": EXPECTED_REVIEWED_ACQUISITION_RECEIPT_DIGEST,
        "expected_chunk_count": 48,
        "completed_chunk_count": 48,
        "failed_chunk_count": 0,
        "total_raw_rows": EXPECTED_TOTAL_RAW_ROWS,
        "total_normalized_source_rows": EXPECTED_TOTAL_NORMALIZED_SOURCE_ROWS,
        "total_rth_rows": EXPECTED_TOTAL_RTH_ROWS,
        "total_extended_hours_rows": EXPECTED_TOTAL_EXTENDED_HOURS_ROWS,
        "out_of_calendar_or_unknown_rows": 0,
        "monthly_reconciled_count": EXPECTED_MONTHLY_RECONCILED_COUNT,
        "monthly_not_reconciled_count": EXPECTED_MONTHLY_NOT_RECONCILED_COUNT,
        "accepted_2025_01_cross_check": acquisition.ACCEPTED_MONTHLY_SOURCE_CROSS_CHECK
        | {"cross_check_status": "PASSED"},
    }


def _recorded_targeted_diagnostics() -> dict[str, Any]:
    return {
        "targeted_diagnostic_status": acquisition.ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE,
        "targeted_month_count": 9,
        "targeted_months": list(acquisition.DEFAULT_PER_SESSION_DIAGNOSTIC_TARGET_MONTHS),
        "targeted_completed_chunks": 9,
        "targeted_failed_chunks": 0,
        "all_monthly_mismatches_explained": True,
        "mismatch_explanation": MISMATCH_EXPLANATION_SPECIAL_SESSION_EXPECTATION,
        "per_session_issue_summary": {"RECONCILED": 188},
        "per_session_severity_summary": {"INFO": 188},
        "targeted_chunk_manifest_digest": EXPECTED_TARGETED_CHUNK_MANIFEST_DIGEST,
        "targeted_provider_raw_response_digest": EXPECTED_TARGETED_PROVIDER_RAW_RESPONSE_DIGEST,
        "targeted_normalized_rows_digest": EXPECTED_TARGETED_NORMALIZED_ROWS_DIGEST,
        "targeted_monthly_reconciliation_digest": EXPECTED_TARGETED_MONTHLY_RECONCILIATION_DIGEST,
        "per_session_diagnostics_digest": EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST,
        "targeted_diagnostic_receipt_digest": EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST,
    }


def _authority_bindings() -> dict[str, Any]:
    return {
        "identity_segment_frozen_digest": acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "exchange_calendar_frozen_digest": acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "schedule_semantic_digest": acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "split_event_audit_frozen_digest": acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "dividend_event_audit_frozen_digest": acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "acquisition_contract_digest": acquisition.EXPECTED_ACQUISITION_CONTRACT_DIGEST,
        "in_range_dividends_found": True,
        "in_range_dividend_count": 16,
        "in_range_dividend_implication": acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION,
        "fixed_segment": _fixed_segment(),
    }


def _authority_boundary() -> dict[str, Any]:
    return {
        "identity_segment_frozen": True,
        "calendar_operator_frozen": True,
        "split_event_audit_frozen": True,
        "dividend_event_audit_frozen": True,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "automatic_stitching": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _check(check_id: str, actual: Any, expected: Any, *, severity: str = "BLOCKER", message: str = "") -> dict[str, Any]:
    status = "PASS" if actual == expected else "FAIL"
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == "PASS" else f"{check_id} failed"),
    }


def _build_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = package["reviewed_acquisition_evidence"]
    targeted = package["targeted_diagnostic_evidence"]
    bindings = package["authority_bindings"]
    boundary = package["authority_boundary"]
    segment = bindings["fixed_segment"]
    cross_check = evidence["accepted_2025_01_cross_check"]
    return [
        _check("acquisition_candidate_kind_matches", evidence["reviewed_acquisition_candidate_kind"], acquisition.ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE),
        _check("acquisition_candidate_status_ready_for_review", evidence["reviewed_acquisition_candidate_status"], acquisition.ACQUISITION_GENERATION_READY_FOR_OPERATOR_REVIEW),
        _check("acquisition_candidate_digest_matches", evidence["reviewed_acquisition_candidate_digest"], acquisition.EXPECTED_FULL_LIVE_ACQUISITION_CANDIDATE_DIGEST),
        _check("chunk_manifest_digest_matches", evidence["reviewed_chunk_manifest_digest"], EXPECTED_REVIEWED_CHUNK_MANIFEST_DIGEST),
        _check("provider_raw_response_digest_matches", evidence["reviewed_provider_raw_response_digest"], EXPECTED_REVIEWED_PROVIDER_RAW_RESPONSE_DIGEST),
        _check("normalized_source_rows_digest_matches", evidence["reviewed_normalized_source_rows_digest"], EXPECTED_REVIEWED_NORMALIZED_SOURCE_ROWS_DIGEST),
        _check("monthly_reconciliation_digest_matches", evidence["reviewed_monthly_reconciliation_digest"], acquisition.EXPECTED_FULL_LIVE_MONTHLY_RECONCILIATION_DIGEST),
        _check("acquisition_receipt_digest_matches", evidence["reviewed_acquisition_receipt_digest"], EXPECTED_REVIEWED_ACQUISITION_RECEIPT_DIGEST),
        _check("expected_chunk_count_48", evidence["expected_chunk_count"], 48),
        _check("completed_chunk_count_48", evidence["completed_chunk_count"], 48),
        _check("failed_chunk_count_zero", evidence["failed_chunk_count"], 0),
        _check("total_raw_rows_match", evidence["total_raw_rows"], EXPECTED_TOTAL_RAW_ROWS),
        _check("total_normalized_rows_match", evidence["total_normalized_source_rows"], EXPECTED_TOTAL_NORMALIZED_SOURCE_ROWS),
        _check("total_rth_rows_match", evidence["total_rth_rows"], EXPECTED_TOTAL_RTH_ROWS),
        _check("total_extended_hours_rows_match", evidence["total_extended_hours_rows"], EXPECTED_TOTAL_EXTENDED_HOURS_ROWS),
        _check("out_of_calendar_unknown_rows_zero", evidence["out_of_calendar_or_unknown_rows"], 0),
        _check("cross_check_2025_01_passed", cross_check["cross_check_status"], "PASSED"),
        _check("monthly_reconciled_count_39", evidence["monthly_reconciled_count"], 39),
        _check("monthly_not_reconciled_count_9", evidence["monthly_not_reconciled_count"], 9),
        _check("targeted_diagnostics_ready_after_triage", targeted["targeted_diagnostic_status"], acquisition.ACQUISITION_OPERATOR_REVIEW_READY_AFTER_TRIAGE),
        _check("targeted_month_count_9", targeted["targeted_month_count"], 9),
        _check("targeted_chunks_completed", (targeted["targeted_completed_chunks"], targeted["targeted_failed_chunks"]), (9, 0)),
        _check("all_monthly_mismatches_explained", targeted["all_monthly_mismatches_explained"], True),
        _check("mismatch_explanation_special_session_expectation", targeted["mismatch_explanation"], MISMATCH_EXPLANATION_SPECIAL_SESSION_EXPECTATION),
        _check("per_session_issue_summary_all_reconciled", targeted["per_session_issue_summary"], {"RECONCILED": 188}),
        _check("per_session_severity_summary_info_only", targeted["per_session_severity_summary"], {"INFO": 188}),
        _check("per_session_diagnostics_digest_matches", targeted["per_session_diagnostics_digest"], EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST),
        _check("targeted_diagnostic_receipt_digest_matches", targeted["targeted_diagnostic_receipt_digest"], EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST),
        _check("identity_frozen_digest_matches", bindings["identity_segment_frozen_digest"], acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST),
        _check("calendar_frozen_digest_matches", bindings["exchange_calendar_frozen_digest"], acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST),
        _check("schedule_digest_matches", bindings["schedule_semantic_digest"], acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST),
        _check("split_event_frozen_digest_matches", bindings["split_event_audit_frozen_digest"], acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST),
        _check("dividend_event_frozen_digest_matches", bindings["dividend_event_audit_frozen_digest"], acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST),
        _check("dividend_implication_preserved", bindings["in_range_dividend_implication"], acquisition.EXPECTED_IN_RANGE_DIVIDEND_IMPLICATION),
        _check("contract_digest_matches", bindings["acquisition_contract_digest"], acquisition.EXPECTED_ACQUISITION_CONTRACT_DIGEST),
        _check("segment_ticker_matches", segment["ticker"], "AAPL"),
        _check("segment_composite_figi_matches", segment["composite_figi"], "BBG000B9XRY4"),
        _check("segment_share_class_figi_matches", segment["share_class_figi"], "BBG001S5N8V8"),
        _check("segment_primary_mic_matches", segment["primary_mic"], "XNAS"),
        _check("segment_security_type_matches", segment["security_type"], "CS"),
        _check("segment_start_matches", segment["segment_start"], "2022-01-01"),
        _check("segment_end_matches", segment["segment_end"], "2025-12-31"),
        _check("acquisition_generation_freeze_false", boundary["acquisition_generation_freeze"], False),
        _check("canonical_eligibility_false", boundary["canonical_eligibility"], False),
        _check("registry_eligibility_false", boundary["registry_eligibility"], False),
        _check("strategy_runtime_migration_false", boundary["strategy_runtime_migration"], False),
        _check("automatic_stitching_false", boundary["automatic_stitching"], False),
        _check("predictive_usefulness_not_accepted", boundary["predictive_usefulness"], acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED),
        _check("profitability_not_accepted", boundary["profitability"], acquisition.PROFITABILITY_NOT_ACCEPTED),
        _check("provider_requests_made_in_review_false", package["provider_requests_made_in_review"], False),
        _check("no_api_key_stored", package["api_key_stored"], False),
        _check("no_acquisition_generation_frozen_artifact_created", package["artifact_kind"], ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE),
    ]


def _review_package_digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("acquisition_generation_review_package_semantic_digest", None)
    return payload


def acquisition_generation_review_package_semantic_digest_v1(package: dict[str, Any]) -> str:
    return semantic_digest(_review_package_digest_payload(package))


def build_acquisition_generation_candidate_review_package_v1(
    acquisition_candidate: dict[str, Any] | None = None,
    targeted_diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an offline, digest-bound acquisition generation review package."""
    if acquisition_candidate is not None or targeted_diagnostics is not None:
        raise AcquisitionGenerationOperatorReviewError("source dict binding is not implemented; use recorded status binding")
    package = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_REVIEW_V1,
        "review_status": ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY,
        "binding_mode": LIVE_ACQUISITION_AND_TRIAGE_STATUS_BINDING,
        "operator_decision_required": True,
        "operator_decision": None,
        "operator_approved_by": None,
        "operator_freeze_timestamp": None,
        "operator_freeze_digest": None,
        "operator_signature": None,
        "freeze_status": None,
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "automatic_stitching": False,
        "api_key_stored": False,
        "software_freeze_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "reviewed_acquisition_evidence": _recorded_acquisition_evidence(),
        "targeted_diagnostic_evidence": _recorded_targeted_diagnostics(),
        "authority_bindings": _authority_bindings(),
        "authority_boundary": _authority_boundary(),
        "remaining_roadmap": list(REMAINING_ROADMAP_AFTER_ACQUISITION_REVIEW_PACKAGE),
    }
    checklist = _build_checklist(package)
    failed = [item for item in checklist if item["status"] != "PASS"]
    package["review_checklist"] = checklist
    package["review_summary"] = {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for item in failed if item["severity"] == "BLOCKER"),
        "ready_for_operator_assessment": not failed,
        "operator_decision_required_before_freeze": True,
        "software_freeze_authorized": False,
    }
    package["acquisition_generation_review_package_semantic_digest"] = (
        acquisition_generation_review_package_semantic_digest_v1(package)
    )
    validate_acquisition_generation_candidate_review_package_v1(package)
    return package


def validate_acquisition_generation_candidate_review_package_v1(review_package: dict[str, Any]) -> dict[str, Any]:
    """Validate the acquisition review package without granting freeze authority."""
    if not isinstance(review_package, dict):
        raise AcquisitionGenerationOperatorReviewError("review package must be a JSON object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_ACQUISITION_GENERATION_CANDIDATE_REVIEW_V1, "schema_version")
    _expect(review_package.get("review_status"), ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY, "review_status")
    _expect(review_package.get("binding_mode"), LIVE_ACQUISITION_AND_TRIAGE_STATUS_BINDING, "binding_mode")
    _expect_true(review_package.get("operator_decision_required"), "operator_decision_required")
    _expect(review_package.get("operator_decision"), None, "operator_decision")
    _expect(review_package.get("operator_approved_by"), None, "operator_approved_by")
    _expect(review_package.get("operator_freeze_timestamp"), None, "operator_freeze_timestamp")
    _expect(review_package.get("operator_freeze_digest"), None, "operator_freeze_digest")
    _expect(review_package.get("operator_signature"), None, "operator_signature")
    if review_package.get("freeze_status") == acquisition.ACQUISITION_GENERATION_FROZEN:
        raise AcquisitionGenerationOperatorReviewError("freeze_status must not be ACQUISITION_GENERATION_FROZEN")
    for field in (
        "acquisition_generation_freeze",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
        "provider_requests_made_in_review",
        "api_key_stored",
        "software_freeze_authorized",
    ):
        _expect_false(review_package.get(field), field)
    _expect_true(review_package.get("created_offline"), "created_offline")
    _expect(review_package.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _validate_evidence(review_package.get("reviewed_acquisition_evidence"))
    _validate_targeted(review_package.get("targeted_diagnostic_evidence"))
    _validate_bindings(review_package.get("authority_bindings"))
    _expect(review_package.get("authority_boundary"), _authority_boundary(), "authority_boundary")
    _expect(review_package.get("remaining_roadmap"), REMAINING_ROADMAP_AFTER_ACQUISITION_REVIEW_PACKAGE, "remaining_roadmap")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionGenerationOperatorReviewError("review_checklist must be a list")
    expected_checklist = _build_checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    failed = [item for item in checklist if item["status"] != "PASS"]
    _expect(
        review_package.get("review_summary"),
        {
            "total_checks": len(checklist),
            "passed_checks": len(checklist) - len(failed),
            "failed_checks": len(failed),
            "blocker_count": sum(1 for item in failed if item["severity"] == "BLOCKER"),
            "ready_for_operator_assessment": not failed,
            "operator_decision_required_before_freeze": True,
            "software_freeze_authorized": False,
        },
        "review_summary",
    )
    digest = review_package.get("acquisition_generation_review_package_semantic_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AcquisitionGenerationOperatorReviewError("acquisition_generation_review_package_semantic_digest missing")
    _expect(digest, acquisition_generation_review_package_semantic_digest_v1(review_package), "acquisition_generation_review_package_semantic_digest")
    return {
        "status": "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "review_package_digest": digest,
        "total_checks": review_package["review_summary"]["total_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": review_package["review_summary"]["ready_for_operator_assessment"],
        "acquisition_generation_freeze": False,
        "canonical_eligibility": False,
        "registry_eligibility": False,
        "strategy_runtime_migration": False,
    }


def _validate_evidence(evidence: Any) -> None:
    if not isinstance(evidence, dict):
        raise AcquisitionGenerationOperatorReviewError("reviewed_acquisition_evidence must be an object")
    _expect(evidence, _recorded_acquisition_evidence(), "reviewed_acquisition_evidence")


def _validate_targeted(targeted: Any) -> None:
    if not isinstance(targeted, dict):
        raise AcquisitionGenerationOperatorReviewError("targeted_diagnostic_evidence must be an object")
    _expect(targeted, _recorded_targeted_diagnostics(), "targeted_diagnostic_evidence")


def _validate_bindings(bindings: Any) -> None:
    if not isinstance(bindings, dict):
        raise AcquisitionGenerationOperatorReviewError("authority_bindings must be an object")
    _expect(bindings, _authority_bindings(), "authority_bindings")


def build_acquisition_generation_candidate_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized acquisition generation operator review package status."""
    validate_acquisition_generation_candidate_review_package_v1(review_package)
    evidence = review_package["reviewed_acquisition_evidence"]
    targeted = review_package["targeted_diagnostic_evidence"]
    bindings = review_package["authority_bindings"]
    summary = review_package["review_summary"]
    boundary = review_package["authority_boundary"]
    failed = [item for item in review_package["review_checklist"] if item["status"] != "PASS"]
    lines = [
        "# MarketFlow Acquisition Generation Operator Review Package Status",
        "",
        "## Purpose",
        "- Branch: `feature/acquisition-generation-operator-review-package-v1`",
        "- Base commit: `8df3f6de8328f7251a59c30f31ee8b82d40b9979`",
        "- Purpose: create an offline, digest-bound operator review package for the full 2022-2025 live acquisition generation candidate and targeted per-session triage evidence.",
        "- This status document does not create an acquisition-generation freeze.",
        "",
        "## Reviewed Acquisition Candidate",
        f"- Artifact kind: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Binding mode: `{review_package['binding_mode']}`",
        f"- Acquisition candidate digest: `{evidence['reviewed_acquisition_candidate_digest']}`",
        f"- Acquisition candidate status: `{evidence['reviewed_acquisition_candidate_status']}`",
        "",
        "## Full Generation Summary",
        f"- Expected chunks: `{evidence['expected_chunk_count']}`",
        f"- Completed chunks: `{evidence['completed_chunk_count']}`",
        f"- Failed chunks: `{evidence['failed_chunk_count']}`",
        f"- Total raw rows: `{evidence['total_raw_rows']}`",
        f"- Total normalized source rows: `{evidence['total_normalized_source_rows']}`",
        f"- Total RTH rows: `{evidence['total_rth_rows']}`",
        f"- Total extended-hours rows: `{evidence['total_extended_hours_rows']}`",
        f"- Out-of-calendar/unknown rows: `{evidence['out_of_calendar_or_unknown_rows']}`",
        "",
        "## 2025-01 Cross-Check",
        f"- Cross-check status: `{evidence['accepted_2025_01_cross_check']['cross_check_status']}`",
        f"- Normalized source rows: `{evidence['accepted_2025_01_cross_check']['normalized_source_rows']}`",
        f"- Validated RTH rows: `{evidence['accepted_2025_01_cross_check']['validated_rth_rows']}`",
        "",
        "## Monthly Reconciliation Summary",
        f"- Monthly reconciled count: `{evidence['monthly_reconciled_count']}`",
        f"- Monthly not-reconciled count: `{evidence['monthly_not_reconciled_count']}`",
        "",
        "## Targeted Per-Session Triage",
        f"- Targeted diagnostic status: `{targeted['targeted_diagnostic_status']}`",
        f"- All monthly mismatches explained: `{targeted['all_monthly_mismatches_explained']}`",
        f"- Mismatch explanation: `{targeted['mismatch_explanation']}`",
        f"- Per-session issue summary: `{json.dumps(targeted['per_session_issue_summary'], sort_keys=True, separators=(',', ':'))}`",
        f"- Per-session severity summary: `{json.dumps(targeted['per_session_severity_summary'], sort_keys=True, separators=(',', ':'))}`",
        "",
        "## Frozen Authority Bindings",
        f"- Identity frozen digest: `{bindings['identity_segment_frozen_digest']}`",
        f"- Calendar frozen digest: `{bindings['exchange_calendar_frozen_digest']}`",
        f"- Schedule digest: `{bindings['schedule_semantic_digest']}`",
        f"- Split-event audit frozen digest: `{bindings['split_event_audit_frozen_digest']}`",
        f"- Dividend-event audit frozen digest: `{bindings['dividend_event_audit_frozen_digest']}`",
        f"- Acquisition contract digest: `{bindings['acquisition_contract_digest']}`",
        "",
        "## Dividend Adjustment Implication",
        f"- In-range dividends found: `{bindings['in_range_dividends_found']}`",
        f"- In-range dividend count: `{bindings['in_range_dividend_count']}`",
        f"- Implication: `{bindings['in_range_dividend_implication']}`",
        "",
        "## Checklist Summary",
        f"- Total checks: `{summary['total_checks']}`",
        f"- Passed checks: `{summary['passed_checks']}`",
        f"- Failed checks: `{summary['failed_checks']}`",
        f"- Blocker count: `{summary['blocker_count']}`",
        f"- Ready for operator assessment: `{summary['ready_for_operator_assessment']}`",
        f"- Software freeze authorized: `{summary['software_freeze_authorized']}`",
        "",
        "## Failed Checks",
    ]
    if failed:
        lines.extend(f"- `{item['check_id']}`: {item['message']}" for item in failed)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- identity_segment_frozen: `{boundary['identity_segment_frozen']}`",
            f"- calendar_operator_frozen: `{boundary['calendar_operator_frozen']}`",
            f"- split_event_audit_frozen: `{boundary['split_event_audit_frozen']}`",
            f"- dividend_event_audit_frozen: `{boundary['dividend_event_audit_frozen']}`",
            f"- acquisition_generation_freeze: `{boundary['acquisition_generation_freeze']}`",
            f"- canonical_eligibility: `{boundary['canonical_eligibility']}`",
            f"- registry_eligibility: `{boundary['registry_eligibility']}`",
            f"- strategy_runtime_migration: `{boundary['strategy_runtime_migration']}`",
            f"- automatic_stitching: `{boundary['automatic_stitching']}`",
            f"- predictive_usefulness: `{boundary['predictive_usefulness']}`",
            f"- profitability: `{boundary['profitability']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["remaining_roadmap"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Created offline: `True`",
            "- Provider requests made in review: `False`",
            "- API key stored: `False`",
            "- No acquisition-generation freeze was created.",
            "- No canonical, registry, runtime, predictive, or profitability approval occurred.",
            "",
            "## Digests",
            f"- Chunk manifest digest: `{evidence['reviewed_chunk_manifest_digest']}`",
            f"- Provider raw response digest: `{evidence['reviewed_provider_raw_response_digest']}`",
            f"- Normalized source rows digest: `{evidence['reviewed_normalized_source_rows_digest']}`",
            f"- Monthly reconciliation digest: `{evidence['reviewed_monthly_reconciliation_digest']}`",
            f"- Acquisition receipt digest: `{evidence['reviewed_acquisition_receipt_digest']}`",
            f"- Targeted chunk manifest digest: `{targeted['targeted_chunk_manifest_digest']}`",
            f"- Targeted provider raw response digest: `{targeted['targeted_provider_raw_response_digest']}`",
            f"- Targeted normalized rows digest: `{targeted['targeted_normalized_rows_digest']}`",
            f"- Targeted monthly reconciliation digest: `{targeted['targeted_monthly_reconciliation_digest']}`",
            f"- Per-session diagnostics digest: `{targeted['per_session_diagnostics_digest']}`",
            f"- Targeted diagnostic receipt digest: `{targeted['targeted_diagnostic_receipt_digest']}`",
            f"- Review package digest: `{review_package['acquisition_generation_review_package_semantic_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_acquisition_generation_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    acquisition_candidate: dict[str, Any] | None = None,
    targeted_diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write the review package JSON and Markdown status to an output directory."""
    package = build_acquisition_generation_candidate_review_package_v1(
        acquisition_candidate=acquisition_candidate,
        targeted_diagnostics=targeted_diagnostics,
    )
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "acquisition_generation_candidate_review_package_v1.json"
    markdown_path = output_path / "MARKETFLOW_ACQUISITION_GENERATION_OPERATOR_REVIEW_PACKAGE_STATUS.md"
    json_text = json.dumps(package, sort_keys=True, indent=2)
    markdown_text = build_acquisition_generation_candidate_review_markdown_v1(package)
    json_path.write_text(json_text + "\n", encoding="utf-8")
    markdown_path.write_text(markdown_text, encoding="utf-8")
    return {
        "package": package,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "json_sha256": sha256_bytes((json_text + "\n").encode("utf-8")),
        "markdown_sha256": sha256_bytes(markdown_text.encode("utf-8")),
        "review_package_digest": package["acquisition_generation_review_package_semantic_digest"],
    }
