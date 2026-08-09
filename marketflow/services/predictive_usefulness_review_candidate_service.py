"""Offline predictive usefulness review candidate for research campaign results."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import research_applicability_campaign_execution_results_review_service as results_review


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE = (
    "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_V1 = (
    "predictive_usefulness_review_candidate_v1"
)
PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW = (
    "PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW"
)
PREDICTIVE_USEFULNESS_REVIEW_REQUIRES_ADDITIONAL_RESEARCH_OUTPUTS = (
    "PREDICTIVE_USEFULNESS_REVIEW_REQUIRES_ADDITIONAL_RESEARCH_OUTPUTS"
)

EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST = (
    "c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b"
)
EXPECTED_CAMPAIGN_EXECUTION_DIGEST = results_review.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_EXECUTION_REQUEST_ID = results_review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID
EXPECTED_CAMPAIGN_EXECUTION_APPROVAL_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
)
EXPECTED_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_DIGEST = (
    results_review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_CAMPAIGN_PLAN_REVIEW_DIGEST = results_review.EXPECTED_CAMPAIGN_PLAN_REVIEW_PACKAGE_DIGEST
EXPECTED_DATASET_AVAILABILITY_REVIEW_DIGEST = (
    results_review.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
)
EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST = results_review.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST = (
    results_review.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
)

NOT_AUTHORIZED = results_review.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

ADDITIONAL_EVIDENCE_REQUIRED = [
    "predictive_label_definition",
    "walk_forward_experiment_plan",
    "out_of_sample_split_definition",
    "signal_quality_metrics",
    "baseline_comparison",
    "stability_analysis",
    "false_positive_false_negative_analysis_if_applicable",
    "operator_review_of_predictive_results",
]

REVIEW_QUESTIONS = [
    "Are the research-registry datasets technically loadable and internally consistent?",
    "Are there any data quality blockers before predictive experiments?",
    "Are there validated predictive labels or targets?",
    "Are there walk-forward or out-of-sample experiments available?",
    "Are there metrics that measure predictive signal quality without claiming profitability?",
    "What additional experiments are required before predictive usefulness acceptance?",
]

REMAINING_REQUIRED_TASKS = [
    "Predictive usefulness review candidate operator review package.",
    "Predictive experiment plan candidate.",
    "Walk-forward experiment plan.",
    "Predictive usefulness review after experiments.",
]

REQUIRED_CHECK_IDS = [
    "campaign_results_review_digest_bound",
    "campaign_execution_digest_bound",
    "execution_request_id_bound",
    "outputs_reviewed_12",
    "outputs_research_only_non_actionable",
    "data_quality_checks_passed",
    "module_compatibility_listed",
    "failure_count_zero",
    "warning_count_zero",
    "data_quality_readiness_true",
    "module_compatibility_readiness_true",
    "predictive_experiment_results_available_false",
    "walk_forward_results_available_false",
    "out_of_sample_results_available_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "runtime_migration_recommended_false",
    "provider_requests_made_false",
    "campaign_reexecution_performed_false",
    "new_strategy_scoring_performed_false",
    "walk_forward_validation_performed_false",
    "trade_recommendations_generated_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "additional_evidence_required_defined",
]


class PredictiveUsefulnessReviewCandidateError(ValueError):
    """Raised when a predictive usefulness candidate violates review guardrails."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
    message: str | None = None,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReviewCandidateError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessReviewCandidateError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessReviewCandidateError(f"{field_name} must be false")


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_V1,
        "candidate_status": PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW,
        "created_offline": True,
        "provider_requests_made": False,
        "campaign_reexecution_performed": False,
        "new_strategy_scoring_performed": False,
        "walk_forward_validation_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "operator_review_required": True,
        "campaign_execution_results_review_package_digest": (
            EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_execution_digest": EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": EXPECTED_EXECUTION_REQUEST_ID,
        "campaign_execution_approval_digest": EXPECTED_CAMPAIGN_EXECUTION_APPROVAL_DIGEST,
        "campaign_execution_candidate_review_digest": (
            EXPECTED_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_DIGEST
        ),
        "campaign_plan_review_digest": EXPECTED_CAMPAIGN_PLAN_REVIEW_DIGEST,
        "dataset_availability_review_digest": EXPECTED_DATASET_AVAILABILITY_REVIEW_DIGEST,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "outputs_reviewed": 12,
        "all_outputs_research_only_non_actionable": True,
        "dataset_load_status": PASS,
        "schema_validation_status": PASS,
        "bar_count_consistency_status": PASS,
        "date_range_coverage_status": PASS,
        "ohlc_consistency_status": PASS,
        "volume_consistency_status": PASS,
        "indicator_calculation_status": PASS,
        "module_compatibility_status": "RESEARCH_ONLY_COMPATIBILITY_LISTED",
        "failure_count": 0,
        "warning_count": 0,
        "ready_for_predictive_usefulness_review": True,
        "data_quality_readiness": True,
        "module_compatibility_readiness": True,
        "predictive_evidence_available": False,
        "predictive_experiment_results_available": False,
        "walk_forward_results_available": False,
        "out_of_sample_results_available": False,
        "label_definition_available": False,
        "predictive_metrics_available": False,
        "additional_evidence_required": list(ADDITIONAL_EVIDENCE_REQUIRED),
        "review_questions": list(REVIEW_QUESTIONS),
        "remaining_required_tasks": list(REMAINING_REQUIRED_TASKS),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    data_quality_checks_passed = all(
        candidate.get(field) == PASS
        for field in (
            "dataset_load_status",
            "schema_validation_status",
            "bar_count_consistency_status",
            "date_range_coverage_status",
            "ohlc_consistency_status",
            "volume_consistency_status",
            "indicator_calculation_status",
        )
    )
    return [
        _check("campaign_results_review_digest_bound", EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST, candidate.get("campaign_execution_results_review_package_digest")),
        _check("campaign_execution_digest_bound", EXPECTED_CAMPAIGN_EXECUTION_DIGEST, candidate.get("campaign_execution_digest")),
        _check("execution_request_id_bound", EXPECTED_EXECUTION_REQUEST_ID, candidate.get("execution_request_id")),
        _check("outputs_reviewed_12", 12, candidate.get("outputs_reviewed")),
        _check("outputs_research_only_non_actionable", True, candidate.get("all_outputs_research_only_non_actionable")),
        _check("data_quality_checks_passed", True, data_quality_checks_passed),
        _check("module_compatibility_listed", "RESEARCH_ONLY_COMPATIBILITY_LISTED", candidate.get("module_compatibility_status")),
        _check("failure_count_zero", 0, candidate.get("failure_count")),
        _check("warning_count_zero", 0, candidate.get("warning_count")),
        _check("data_quality_readiness_true", True, candidate.get("data_quality_readiness")),
        _check("module_compatibility_readiness_true", True, candidate.get("module_compatibility_readiness")),
        _check("predictive_experiment_results_available_false", False, candidate.get("predictive_experiment_results_available")),
        _check("walk_forward_results_available_false", False, candidate.get("walk_forward_results_available")),
        _check("out_of_sample_results_available_false", False, candidate.get("out_of_sample_results_available")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, candidate.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, candidate.get("predictive_usefulness_acceptance_ready")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, candidate.get("profitability")),
        _check("profitability_acceptance_ready_false", False, candidate.get("profitability_acceptance_ready")),
        _check("runtime_migration_recommended_false", False, candidate.get("runtime_migration_recommended")),
        _check("provider_requests_made_false", False, candidate.get("provider_requests_made")),
        _check("campaign_reexecution_performed_false", False, candidate.get("campaign_reexecution_performed")),
        _check("new_strategy_scoring_performed_false", False, candidate.get("new_strategy_scoring_performed")),
        _check("walk_forward_validation_performed_false", False, candidate.get("walk_forward_validation_performed")),
        _check("trade_recommendations_generated_false", False, candidate.get("trade_recommendations_generated")),
        _check("runtime_migration_approved_false", False, candidate.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, candidate.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, candidate.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, candidate.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, candidate.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, candidate.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, candidate.get("broker_execution")),
        _check("automatic_stitching_false", False, candidate.get("automatic_stitching")),
        _check("additional_evidence_required_defined", ADDITIONAL_EVIDENCE_REQUIRED, candidate.get("additional_evidence_required")),
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = failed == 0
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_predictive_experiment_planning": ready,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("predictive_usefulness_review_candidate_digest", None)
    return payload


def predictive_usefulness_review_candidate_digest_v1(candidate: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the review candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_predictive_usefulness_review_candidate_v1() -> dict[str, Any]:
    """Build an offline candidate for future predictive usefulness operator review."""
    candidate = _base_candidate()
    candidate["predictive_evidence_classification"] = {
        "data_quality_readiness": candidate["data_quality_readiness"],
        "module_compatibility_readiness": candidate["module_compatibility_readiness"],
        "predictive_evidence_available": candidate["predictive_evidence_available"],
        "predictive_experiment_results_available": (
            candidate["predictive_experiment_results_available"]
        ),
        "walk_forward_results_available": candidate["walk_forward_results_available"],
        "out_of_sample_results_available": candidate["out_of_sample_results_available"],
        "label_definition_available": candidate["label_definition_available"],
        "predictive_metrics_available": candidate["predictive_metrics_available"],
        "predictive_usefulness_acceptance_ready": (
            candidate["predictive_usefulness_acceptance_ready"]
        ),
        "profitability_acceptance_ready": candidate["profitability_acceptance_ready"],
    }
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["predictive_usefulness_review_candidate_digest"] = (
        predictive_usefulness_review_candidate_digest_v1(candidate)
    )
    validate_predictive_usefulness_review_candidate_v1(candidate)
    return candidate


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "candidate") -> None:
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if isinstance(value, str) and value in {
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_MIGRATION_ACTIVE",
            "STRATEGY_RUNTIME_MIGRATION",
        }:
            raise PredictiveUsefulnessReviewCandidateError(
                f"{current_path} must not emit {value}"
            )
        if key in {
            "provider_requests_made",
            "campaign_reexecution_performed",
            "new_strategy_scoring_performed",
            "walk_forward_validation_performed",
            "trade_recommendations_generated",
            "profitability_acceptance_ready",
            "runtime_migration_recommended",
            "runtime_migration_approved",
            "runtime_migration_active",
            "strategy_runtime_migration",
            "automatic_stitching",
        } and value is True:
            raise PredictiveUsefulnessReviewCandidateError(f"{current_path} must be false")
        if (
            key == "predictive_usefulness_acceptance_ready"
            and value is True
            and mapping.get("predictive_experiment_results_available") is not True
        ):
            raise PredictiveUsefulnessReviewCandidateError(
                f"{current_path} must be false without predictive evidence"
            )
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise PredictiveUsefulnessReviewCandidateError(
                f"{current_path} must not be AUTHORIZED"
            )
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise PredictiveUsefulnessReviewCandidateError(
                f"{current_path} must not be accepted"
            )
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_predictive_usefulness_review_candidate_v1(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Validate a predictive usefulness review candidate without granting acceptance."""
    if not isinstance(candidate, dict):
        raise PredictiveUsefulnessReviewCandidateError("candidate must be a JSON object")
    _reject_forbidden_values(candidate)
    _expect(
        candidate.get("artifact_kind"),
        ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE,
        "artifact_kind",
    )
    _expect(
        candidate.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_V1,
        "schema_version",
    )
    if candidate.get("candidate_status") not in {
        PREDICTIVE_USEFULNESS_REVIEW_READY_FOR_OPERATOR_REVIEW,
        PREDICTIVE_USEFULNESS_REVIEW_REQUIRES_ADDITIONAL_RESEARCH_OUTPUTS,
    }:
        raise PredictiveUsefulnessReviewCandidateError("candidate_status mismatch")
    for field in ("created_offline", "research_only", "operator_review_required"):
        _expect_true(candidate.get(field), field)
    for field in (
        "provider_requests_made",
        "campaign_reexecution_performed",
        "new_strategy_scoring_performed",
        "walk_forward_validation_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(candidate.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    _expect(
        candidate.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(candidate.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "campaign_execution_results_review_package_digest": (
            EXPECTED_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "campaign_execution_digest": EXPECTED_CAMPAIGN_EXECUTION_DIGEST,
        "execution_request_id": EXPECTED_EXECUTION_REQUEST_ID,
        "campaign_execution_approval_digest": EXPECTED_CAMPAIGN_EXECUTION_APPROVAL_DIGEST,
        "campaign_execution_candidate_review_digest": (
            EXPECTED_CAMPAIGN_EXECUTION_CANDIDATE_REVIEW_DIGEST
        ),
        "campaign_plan_review_digest": EXPECTED_CAMPAIGN_PLAN_REVIEW_DIGEST,
        "dataset_availability_review_digest": EXPECTED_DATASET_AVAILABILITY_REVIEW_DIGEST,
        "swing_registry_approval_digest": EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "outputs_reviewed": 12,
        "module_compatibility_status": "RESEARCH_ONLY_COMPATIBILITY_LISTED",
        "failure_count": 0,
        "warning_count": 0,
    }.items():
        _expect(candidate.get(field), expected, field)
    for field in (
        "dataset_load_status",
        "schema_validation_status",
        "bar_count_consistency_status",
        "date_range_coverage_status",
        "ohlc_consistency_status",
        "volume_consistency_status",
        "indicator_calculation_status",
    ):
        _expect(candidate.get(field), PASS, field)
    for field in (
        "all_outputs_research_only_non_actionable",
        "ready_for_predictive_usefulness_review",
        "data_quality_readiness",
        "module_compatibility_readiness",
    ):
        _expect_true(candidate.get(field), field)
    for field in (
        "predictive_evidence_available",
        "predictive_experiment_results_available",
        "walk_forward_results_available",
        "out_of_sample_results_available",
        "label_definition_available",
        "predictive_metrics_available",
    ):
        _expect_false(candidate.get(field), field)
    if candidate.get("additional_evidence_required") != ADDITIONAL_EVIDENCE_REQUIRED:
        raise PredictiveUsefulnessReviewCandidateError("additional_evidence_required mismatch")
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise PredictiveUsefulnessReviewCandidateError("candidate_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        REQUIRED_CHECK_IDS,
        "candidate_checklist check IDs",
    )
    expected_checklist = _checklist(candidate)
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise PredictiveUsefulnessReviewCandidateError(
            f"candidate checklist contains failed check: {failed[0]['check_id']}"
        )
    _expect(checklist, expected_checklist, "candidate_checklist")
    expected_summary = _summary(expected_checklist)
    _expect(candidate.get("candidate_summary"), expected_summary, "candidate_summary")
    digest = candidate.get("predictive_usefulness_review_candidate_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReviewCandidateError(
            "predictive_usefulness_review_candidate_digest missing"
        )
    _expect(
        digest,
        predictive_usefulness_review_candidate_digest_v1(candidate),
        "predictive_usefulness_review_candidate_digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_VALID",
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "predictive_usefulness_review_candidate_digest": digest,
        "campaign_execution_results_review_package_digest": candidate[
            "campaign_execution_results_review_package_digest"
        ],
        "campaign_execution_digest": candidate["campaign_execution_digest"],
        "execution_request_id": candidate["execution_request_id"],
        "ready_for_operator_review": candidate["candidate_summary"]["ready_for_operator_review"],
        "ready_for_predictive_experiment_planning": candidate["candidate_summary"][
            "ready_for_predictive_experiment_planning"
        ],
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_predictive_usefulness_review_candidate_markdown_v1(
    candidate: dict[str, Any],
) -> str:
    """Render a sanitized predictive usefulness review candidate summary."""
    validation = validate_predictive_usefulness_review_candidate_v1(candidate)
    summary = candidate["candidate_summary"]
    classification = candidate["predictive_evidence_classification"]
    lines = [
        "# MarketFlow Predictive Usefulness Review Candidate Status",
        "",
        "## Title",
        "- Predictive Usefulness Review Candidate v1.",
        "",
        "## Purpose",
        "- Define the offline evidence boundary for a future predictive usefulness review.",
        "- This candidate does not accept predictive usefulness, profitability, or runtime use.",
        "",
        "## Source Research Results",
        f"- Campaign results review digest: `{candidate['campaign_execution_results_review_package_digest']}`",
        f"- Campaign execution digest: `{candidate['campaign_execution_digest']}`",
        f"- Execution request ID: `{candidate['execution_request_id']}`",
        f"- Outputs reviewed: `{candidate['outputs_reviewed']}`",
        f"- Data quality readiness: `{candidate['data_quality_readiness']}`",
        f"- Module compatibility readiness: `{candidate['module_compatibility_readiness']}`",
        "",
        "## Predictive Evidence Classification",
        f"- predictive_evidence_available: `{classification['predictive_evidence_available']}`",
        f"- predictive_experiment_results_available: `{classification['predictive_experiment_results_available']}`",
        f"- walk_forward_results_available: `{classification['walk_forward_results_available']}`",
        f"- out_of_sample_results_available: `{classification['out_of_sample_results_available']}`",
        f"- label_definition_available: `{classification['label_definition_available']}`",
        f"- predictive_metrics_available: `{classification['predictive_metrics_available']}`",
        f"- predictive_usefulness_acceptance_ready: `{classification['predictive_usefulness_acceptance_ready']}`",
        f"- profitability_acceptance_ready: `{classification['profitability_acceptance_ready']}`",
        "",
        "## Additional Evidence Required",
    ]
    lines.extend(f"- `{item}`" for item in candidate["additional_evidence_required"])
    lines.extend(
        [
            "",
            "## Boundary Conditions",
            f"- provider_requests_made: `{candidate['provider_requests_made']}`",
            f"- campaign_reexecution_performed: `{candidate['campaign_reexecution_performed']}`",
            f"- new_strategy_scoring_performed: `{candidate['new_strategy_scoring_performed']}`",
            f"- walk_forward_validation_performed: `{candidate['walk_forward_validation_performed']}`",
            f"- trade_recommendations_generated: `{candidate['trade_recommendations_generated']}`",
            f"- runtime_migration_recommended: `{candidate['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{candidate['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{candidate['runtime_migration_active']}`",
            f"- runtime_use: `{candidate['runtime_use']}`",
            f"- strategy_use: `{candidate['strategy_use']}`",
            f"- paper_trading: `{candidate['paper_trading']}`",
            f"- broker_execution: `{candidate['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Candidate digest: `{validation['predictive_usefulness_review_candidate_digest']}`",
            "",
            "## Remaining Required Tasks",
        ]
    )
    lines.extend(f"{index}. {task}" for index, task in enumerate(candidate["remaining_required_tasks"], start=1))
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made.",
            "- No predictive experiments or walk-forward validation were executed.",
            "- No strategy scoring or trade recommendations were generated.",
            "- No runtime migration, paper trading, or broker execution was authorized.",
            "- Predictive usefulness and profitability remain not accepted.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_usefulness_review_candidate_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the predictive usefulness review candidate JSON without overwriting output."""
    candidate = build_predictive_usefulness_review_candidate_v1()
    validation = validate_predictive_usefulness_review_candidate_v1(candidate)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_usefulness_review_candidate_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveUsefulnessReviewCandidateError(
            "predictive usefulness review candidate filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveUsefulnessReviewCandidateError(
            "predictive usefulness review candidate output already exists"
        )
    payload = canonical_json_bytes(candidate)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
