"""Offline operator review of the redesigned-label predictive evidence candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_execution_candidate_redesigned_labels_service as candidate_service


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1 = (
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID"
)

DEFAULT_BRANCH = "feature/additional-predictive-evidence-execution-candidate-review-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "03b01234513831e8a2df6233cfa332404b46d82c"
EXPECTED_CANDIDATE_DIGEST = "f11550ab63f21f2f08b896296324e0f0b1cb99a27ae186cfc347028e5ddf9cd5"
EXPECTED_CANDIDATE_CHECK_COUNT = 49
READY_FOR_OPERATOR_ASSESSMENT = "READY_FOR_OPERATOR_ASSESSMENT"
PASS = candidate_service.PASS
FAIL = candidate_service.FAIL
BLOCKER = candidate_service.BLOCKER
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED

FUTURE_CHAIN = list(candidate_service.FUTURE_CHAIN)
FUTURE_GATES = list(candidate_service.FUTURE_GATES)
RISK_CONTROLS = list(candidate_service.RISK_CONTROLS)

REQUIRED_CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "additional_predictive_evidence_execution_candidate_digest_bound",
    "feature_generation_results_review_digest_bound",
    "feature_generation_execution_digest_bound",
    "feature_values_digest_bound",
    "feature_generation_approval_digest_bound",
    "redesigned_label_results_review_digest_bound",
    "redesigned_label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_candidate_universe",
    "records_digest_preserved",
    "label_values_digest_preserved",
    "feature_values_digest_preserved",
    "meta_913_preserved",
    "feature_generation_results_review_ready_true",
    "ready_for_predictive_evidence_candidate_true",
    "additional_predictive_evidence_execution_candidate_created_true",
    "additional_predictive_evidence_execution_candidate_review_created_true",
    "additional_predictive_evidence_execution_candidate_ready_true",
    "predictive_evidence_execution_authorized_false",
    "predictive_evidence_executed_false",
    "feature_label_matrix_reviewed_not_generated",
    "planned_execution_activities_reviewed",
    "planned_splits_reviewed",
    "planned_model_baseline_families_9_reviewed",
    "planned_metric_families_reviewed",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "per_ticker_entries_12",
    "per_ticker_candidate_digests_present",
    "per_ticker_review_digests_present",
    "metric_recomputation_false",
    "model_training_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "redesigned_label_regeneration_false",
    "feature_regeneration_false",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "future_chain_reviewed",
    "future_gates_reviewed",
    "risk_controls_reviewed",
    "no_tracked_marketflow_files",
]

FORBIDDEN_ARTIFACT_VALUES = {
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
    "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


class AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(ValueError):
    """Raised when the operator-review package violates its review-only contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            f"{field} mismatch"
        )


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the semantic digest for one per-ticker review entry."""
    payload = deepcopy(entry)
    payload.pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_review_digest",
        None,
    )
    return semantic_digest(payload)


def _per_ticker_review_entries(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for source in candidate["per_ticker_candidate_entries"]:
        entry = deepcopy(source)
        entry[
            "additional_predictive_evidence_execution_candidate_review_status"
        ] = READY_FOR_OPERATOR_ASSESSMENT
        entry[
            "source_additional_predictive_evidence_execution_candidate_digest"
        ] = EXPECTED_CANDIDATE_DIGEST
        entry[
            "per_ticker_additional_predictive_evidence_execution_candidate_review_digest"
        ] = per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_digest_v1(
            entry
        )
        entries.append(entry)
    return entries


def _base_review(candidate: dict[str, Any]) -> dict[str, Any]:
    omitted = {
        "artifact_kind",
        "schema_version",
        "candidate_status",
        "branch",
        "base_commit",
        "candidate_checklist",
        "candidate_summary",
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest",
        "per_ticker_candidate_entries",
    }
    preserved = {
        key: deepcopy(value)
        for key, value in candidate.items()
        if key not in omitted
    }
    preserved.update(
        {
            "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE,
            "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_V1,
            "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY,
            "branch": DEFAULT_BRANCH,
            "base_commit": DEFAULT_BASE_COMMIT,
            "reviewed_additional_predictive_evidence_execution_candidate_kind": candidate["artifact_kind"],
            "reviewed_additional_predictive_evidence_execution_candidate_status": candidate["candidate_status"],
            "reviewed_additional_predictive_evidence_execution_candidate_digest": candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"],
            "reviewed_additional_predictive_evidence_execution_candidate_checklist_total": candidate["candidate_summary"]["total_checks"],
            "reviewed_additional_predictive_evidence_execution_candidate_checklist_passed": candidate["candidate_summary"]["passed_checks"],
            "reviewed_additional_predictive_evidence_execution_candidate_checklist_failed": candidate["candidate_summary"]["failed_checks"],
            "reviewed_additional_predictive_evidence_execution_candidate_blocker_count": candidate["candidate_summary"]["blocker_count"],
            "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"],
            "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created": True,
            "per_ticker_review_entries": _per_ticker_review_entries(candidate),
            "future_chain": list(FUTURE_CHAIN),
            "future_gates": list(FUTURE_GATES),
            "risk_controls": list(RISK_CONTROLS),
        }
    )
    return preserved


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    entries = review.get("per_ticker_review_entries", [])
    outputs = review.get("planned_outputs", [])
    values: dict[str, tuple[Any, Any]] = {
        "candidate_kind_matches": (candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS, review.get("reviewed_additional_predictive_evidence_execution_candidate_kind")),
        "candidate_status_ready_for_review": (candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW, review.get("reviewed_additional_predictive_evidence_execution_candidate_status")),
        "candidate_digest_matches_expected": (EXPECTED_CANDIDATE_DIGEST, review.get("reviewed_additional_predictive_evidence_execution_candidate_digest")),
        "candidate_checklist_zero_blockers": (0, review.get("reviewed_additional_predictive_evidence_execution_candidate_blocker_count")),
        "additional_predictive_evidence_execution_candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, review.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest")),
        "feature_generation_results_review_digest_bound": (candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST, review.get("feature_generation_results_review_using_redesigned_labels_digest")),
        "feature_generation_execution_digest_bound": (candidate_service.EXPECTED_EXECUTION_DIGEST, review.get("feature_generation_execution_using_redesigned_labels_digest")),
        "feature_values_digest_bound": (candidate_service.EXPECTED_FEATURE_VALUES_DIGEST, review.get("feature_values_digest")),
        "feature_generation_approval_digest_bound": (candidate_service.EXPECTED_APPROVAL_DIGEST, review.get("feature_generation_approval_using_redesigned_labels_digest")),
        "redesigned_label_results_review_digest_bound": (candidate_service.EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST, review.get("redesigned_label_generation_results_review_package_digest")),
        "redesigned_label_values_digest_bound": (candidate_service.EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, review.get("redesigned_label_values_digest")),
        "research_registry_digest_bound": (candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST, review.get("research_registry_approval_digest")),
        "records_digest_bound": (candidate_service.EXPECTED_RECORDS_DIGEST, review.get("records_digest")),
        "target_universe_12_preserved": (12, review.get("target_universe_count")),
        "target_universe_matches_candidate_universe": (candidate_service.TARGET_UNIVERSE, review.get("target_universe")),
        "records_digest_preserved": (candidate_service.EXPECTED_RECORDS_DIGEST, review.get("records_digest")),
        "label_values_digest_preserved": (candidate_service.EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST, review.get("redesigned_label_values_digest")),
        "feature_values_digest_preserved": (candidate_service.EXPECTED_FEATURE_VALUES_DIGEST, review.get("feature_values_digest")),
        "meta_913_preserved": (913, review.get("meta_record_count")),
        "feature_generation_results_review_ready_true": (True, review.get("feature_generation_results_review_ready")),
        "ready_for_predictive_evidence_candidate_true": (True, review.get("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels")),
        "additional_predictive_evidence_execution_candidate_created_true": (True, review.get("additional_predictive_evidence_execution_candidate_created")),
        "additional_predictive_evidence_execution_candidate_review_created_true": (True, review.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created")),
        "additional_predictive_evidence_execution_candidate_ready_true": (True, review.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review")),
        "predictive_evidence_execution_authorized_false": (False, review.get("additional_predictive_evidence_execution_authorized")),
        "predictive_evidence_executed_false": (False, review.get("additional_predictive_evidence_executed")),
        "feature_label_matrix_reviewed_not_generated": (candidate_service.PLANNED_NOT_GENERATED, review.get("planned_feature_label_matrix", {}).get("matrix_status")),
        "planned_execution_activities_reviewed": (candidate_service._planned_activities(), review.get("planned_execution_activities")),
        "planned_splits_reviewed": (candidate_service.PLANNED_SPLITS, review.get("planned_splits")),
        "planned_model_baseline_families_9_reviewed": (9, len(review.get("planned_model_baseline_families", []))),
        "planned_metric_families_reviewed": (candidate_service._planned_metric_families(), review.get("planned_metric_families")),
        "planned_outputs_not_generated": (True, bool(outputs) and all(row.get("output_status") == candidate_service.PLANNED_NOT_GENERATED for row in outputs)),
        "planned_outputs_research_only": (True, bool(outputs) and all(row.get("actionability_label") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)),
        "per_ticker_entries_12": (12, len(entries)),
        "per_ticker_candidate_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_digest"), str) and len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64 for row in entries)),
        "per_ticker_review_digests_present": (True, bool(entries) and all(isinstance(row.get("per_ticker_additional_predictive_evidence_execution_candidate_review_digest"), str) and len(row["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]) == 64 for row in entries)),
        "metric_recomputation_false": (False, review.get("metric_recomputation_performed")),
        "model_training_false": (False, review.get("model_training_performed")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, review.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, review.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, review.get("runtime_use")),
        "strategy_not_authorized": (NOT_AUTHORIZED, review.get("strategy_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, review.get("broker_execution")),
        "trade_recommendations_false": (False, review.get("trade_recommendations_generated")),
        "provider_requests_made_false": (False, review.get("provider_requests_made")),
        "market_data_acquisition_false": (False, review.get("market_data_acquisition_performed")),
        "dataset_regeneration_false": (False, review.get("canonical_dataset_regenerated")),
        "redesigned_label_regeneration_false": (False, review.get("redesigned_label_regeneration_performed")),
        "feature_regeneration_false": (False, review.get("feature_regeneration_performed")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, review.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, review.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, review.get("runtime_migration_approval_created")),
        "future_chain_reviewed": (FUTURE_CHAIN, review.get("future_chain")),
        "future_gates_reviewed": (FUTURE_GATES, review.get("future_gates")),
        "risk_controls_reviewed": (RISK_CONTROLS, review.get("risk_controls")),
        "no_tracked_marketflow_files": (True, review.get("no_tracked_marketflow_files")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "predictive_evidence_execution_authorized": False,
        "predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    payload = deepcopy(review_package)
    payload.pop(
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest",
        None,
    )
    return semantic_digest(payload)


def build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Build a review package after validating the source candidate."""
    source = (
        candidate_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(source)
    if source["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"] != EXPECTED_CANDIDATE_DIGEST:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "candidate digest changed"
        )
    review = _base_review(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review[
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"
    ] = additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest_v1(
        review
    )
    validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
        review
    )
    return review


def _reject_forbidden_values(value: Any, *, path: str = "review") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Fail closed unless the artifact is the exact non-authorizing review."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_values(review_package)
    source = candidate_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()
    expected_base = _base_review(source)
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "review_checklist missing"
        )
    expected_checklist = _checklist(review_package)
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist check IDs")
    if any(row["status"] != PASS for row in expected_checklist):
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "review checklist contains a failed check"
        )
    _expect(checklist, expected_checklist, "review_checklist")
    summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), summary, "review_summary")
    for entry in review_package["per_ticker_review_entries"]:
        candidate_digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_digest"
        )
        review_digest = entry.get(
            "per_ticker_additional_predictive_evidence_execution_candidate_review_digest"
        )
        if not isinstance(candidate_digest, str) or len(candidate_digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
                "per-ticker candidate digest missing"
            )
        if not isinstance(review_digest, str) or len(review_digest) != 64:
            raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
                "per-ticker review digest missing"
            )
        _expect(
            review_digest,
            per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_digest_v1(entry),
            "per-ticker review digest",
        )
    digest = review_package.get(
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "review package digest missing"
        )
    _expect(
        digest,
        additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest_v1(review_package),
        "review package digest",
    )
    return {
        "status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": digest,
        "reviewed_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "ready_for_operator_assessment": True,
        "ready_for_additional_predictive_evidence_execution_approval": False,
        "blocker_count": 0,
        "predictive_evidence_execution_authorized": False,
        "predictive_evidence_executed": False,
        "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized Markdown summary of the candidate review."""
    validation = validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Additional Predictive Evidence Execution Candidate Review Using Redesigned Labels Status", "",
        "## Title", "- Additional Predictive Evidence Execution Candidate Operator Review Package Using Redesigned Labels v1.", "",
        "## Additional Predictive Evidence Execution Candidate Review Using Redesigned Labels", f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest']}`.", "",
        "## Reviewed Candidate", f"- Kind/status/digest/checks/blockers: `{review_package['reviewed_additional_predictive_evidence_execution_candidate_kind']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_status']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_digest']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_checklist_passed']}` / `{review_package['reviewed_additional_predictive_evidence_execution_candidate_blocker_count']}`.", "",
        "## Bound Evidence", f"- Feature review/execution/values: `{review_package['feature_generation_results_review_using_redesigned_labels_digest']}` / `{review_package['feature_generation_execution_using_redesigned_labels_digest']}` / `{review_package['feature_values_digest']}`.", "",
        "## Dataset and Universe", f"- `{review_package['dataset_name']}` contains `{review_package['total_canonical_record_count']}` records for `{' '.join(review_package['target_universe'])}`; META remains `{review_package['meta_record_count']}`.", "",
        "## Source Redesigned Label Profile", f"- Rows/available/unavailable/families/thresholds/horizons: `{review_package['label_value_row_count']}` / `{review_package['available_label_value_count']}` / `{review_package['unavailable_label_value_count']}` / `{review_package['label_family_count']}` / `{review_package['threshold_strategy_count']}` / `{review_package['horizon_strategy_count']}`.", "",
        "## Source Feature Profile", f"- Outputs/families/groups/schema/rows: `{review_package['feature_output_count']}` / `{review_package['feature_family_count']}` / `{review_package['feature_group_count']}` / `{review_package['feature_schema_field_count']}` / `{review_package['feature_value_row_count']}`.", "",
        "## Reviewed Candidate Objective", f"- `{review_package['additional_predictive_evidence_execution_candidate_objective']}`; `{review_package['additional_predictive_evidence_execution_candidate_scope']}` / `{review_package['additional_predictive_evidence_execution_candidate_mode']}` / `{review_package['additional_predictive_evidence_execution_candidate_authority_status']}`.", "",
        "## Reviewed Source Inputs",
    ]
    lines.extend(f"- `{row['source_input']}`: `{row['source_status']}` / `{row['actionability_label']}`" for row in review_package["source_inputs"])
    lines.extend(["", "## Reviewed Feature / Label Matrix", f"- `{review_package['planned_feature_label_matrix']['matrix_status']}`; the join remains unexecuted and no matrix exists.", "", "## Reviewed Execution Activities"])
    lines.extend(f"- `{row['activity_id']}`: `{row['activity_status']}`" for row in review_package["planned_execution_activities"])
    lines.extend(["", "## Reviewed Splits"])
    lines.extend(f"- {key}: `{value}`" for key, value in review_package["planned_splits"].items())
    lines.extend(["", "## Reviewed Model and Baseline Families"])
    lines.extend(f"- `{row['model_or_baseline_family']}`: `{row['model_or_baseline_status']}`" for row in review_package["planned_model_baseline_families"])
    lines.extend(["", "## Reviewed Metric Families"])
    lines.extend(f"- `{row['metric_family']}`: `{row['metric_status']}`" for row in review_package["planned_metric_families"])
    lines.extend(["", "## Reviewed Planned Outputs"])
    lines.extend(f"- `{row['output_id']}`: `{row['output_status']}`" for row in review_package["planned_outputs"])
    lines.extend(["", "## Per-Ticker Review Entries"])
    lines.extend(f"- `{row['ticker']}`: `{row['historical_record_count']}` records; `{row['additional_predictive_evidence_execution_candidate_review_status']}`" for row in review_package["per_ticker_review_entries"])
    lines.extend(["", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(review_package["future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in review_package["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["risk_controls"])
    lines.extend([
        "", "## Checklist Summary", f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "", "## Guardrails", "- Review only: no predictive approval, authorization, execution, matrix generation, metrics, training, scoring, acceptance, profitability, runtime, recommendation, broker, or trading authority or action.", "- Candidate review readiness supports operator assessment only; any execution approval remains a separate future decision.", "",
    ])
    return "\n".join(lines)


def write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
) -> dict[str, Any]:
    """Write one canonical review package without overwriting an artifact."""
    review = build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(
        candidate=candidate
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1.json"
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError(
            "review package output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": review["review_status"],
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": review["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"],
    }
