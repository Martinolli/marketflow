from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_usefulness_assessment_candidate_service as service


def _source_package() -> dict[str, Any]:
    return {
        "review_status": service.results_review.PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY,
        "predictive_experiment_execution_results_review_package_digest": (
            service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "source_execution_digest": service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST,
        "source_execution_request_id": service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
        "source_execution_approval_digest": (
            service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
        ),
        "predictive_experiment_plan_digest": service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
        "predictive_experiment_plan_review_package_digest": (
            service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
        ),
        "predictive_usefulness_review_candidate_digest": (
            service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_DIGEST
        ),
        "predictive_usefulness_review_candidate_review_package_digest": (
            service.EXPECTED_PREDICTIVE_USEFULNESS_REVIEW_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "swing_registry_approval_digest": service.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "position_swing_registry_approval_digest": (
            service.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
        ),
        "actual_output_count": 13,
        "all_outputs_research_only_non_actionable": True,
        "metrics_labeled_research_only_not_performance_acceptance": True,
        "labels_generated": True,
        "feature_matrices_generated": True,
        "walk_forward_result_generated": True,
        "out_of_sample_result_generated": True,
        "baseline_result_count": 8,
        "metric_result_count": 8,
        "walk_forward_summary_status": "SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT",
        "out_of_sample_summary_status": "CHRONOLOGICAL_OOS_RESEARCH_SPLIT",
        "failure_count": "unavailable",
        "warning_count": "unavailable",
        "leakage_control_status": "PASS",
        "dataset_summary": {
            "dataset_count": 2,
            "swing_row_count": 6,
            "position_swing_row_count": 6,
            "label_available_count": 10,
        },
        "output_root": ".marketflow/predictive_experiments/AAPL/2022_2025",
        "review_summary": {
            "ready_for_operator_review": True,
            "ready_for_predictive_usefulness_assessment": True,
            "predictive_usefulness_accepted": False,
            "profitability_accepted": False,
            "runtime_migration_authorized": False,
            "software_runtime_activation_authorized": False,
        },
    }


def _candidate() -> dict[str, Any]:
    return service.build_predictive_usefulness_assessment_candidate_v1(_source_package())


def _redigest(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["assessment_checklist"] = service._checklist(candidate)
    candidate["assessment_summary"] = service._summary(
        candidate["assessment_checklist"],
        assessment_status=candidate["assessment_status"],
    )
    candidate["predictive_usefulness_assessment_candidate_digest"] = (
        service.predictive_usefulness_assessment_candidate_digest_v1(candidate)
    )
    return candidate


def test_builds_offline_from_supplied_review_package_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("saved source review package should not be rebuilt")

    monkeypatch.setattr(
        service.results_review,
        "build_predictive_experiment_execution_results_review_package_v1",
        fail_if_called,
    )

    assert _candidate()["provider_requests_made"] is False


def test_artifact_kind_schema_and_status_are_assessment_candidate():
    candidate = _candidate()

    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE
    assert candidate["schema_version"] == (
        service.SCHEMA_VERSION_PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_V1
    )
    assert candidate["assessment_status"] == (
        service.PREDICTIVE_USEFULNESS_ASSESSMENT_READY_FOR_OPERATOR_REVIEW
    )


def test_required_source_digests_are_bound():
    candidate = _candidate()

    assert candidate["source_results_review_package_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["predictive_experiment_execution_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_DIGEST
    )
    assert candidate["predictive_experiment_execution_approval_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_DIGEST
    )
    assert candidate["predictive_experiment_plan_digest"] == (
        service.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST
    )


def test_reviewed_result_facts_match_required_counts_and_labels():
    facts = _candidate()["reviewed_result_facts"]

    assert facts["output_count"] == 13
    assert facts["all_outputs_research_only_non_actionable"] is True
    assert facts["metrics_label"] == service.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    assert facts["labels_generated"] is True
    assert facts["feature_matrices_generated"] is True
    assert facts["walk_forward_result_generated"] is True
    assert facts["out_of_sample_result_generated"] is True
    assert facts["baseline_result_count"] == 8
    assert facts["metric_result_count"] == 8


def test_failure_and_warning_counts_are_acknowledged_as_unavailable():
    facts = _candidate()["reviewed_result_facts"]

    assert facts["failure_count_status"] == service.UNAVAILABLE_IN_SOURCE_REPORTS
    assert facts["warning_count_status"] == service.UNAVAILABLE_IN_SOURCE_REPORTS


def test_assessment_classifies_evidence_as_available_but_not_acceptance():
    classification = _candidate()["predictive_evidence_classification"]

    assert classification["data_quality_evidence_status"] == service.PASS
    assert classification["walk_forward_evidence_status"] == service.AVAILABLE_RESEARCH_ONLY
    assert classification["out_of_sample_evidence_status"] == service.AVAILABLE_RESEARCH_ONLY
    assert classification["baseline_comparison_evidence_status"] == service.AVAILABLE_RESEARCH_ONLY
    assert classification["signal_metric_evidence_status"] == service.AVAILABLE_RESEARCH_ONLY
    assert classification["metrics_acceptance_status"] == service.NOT_ACCEPTANCE_EVIDENCE
    assert classification["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["predictive_usefulness_acceptance_recommended"] is False
    assert candidate["profitability"] == "not accepted"
    assert candidate["profitability_acceptance_ready"] is False
    assert candidate["profitability_acceptance_recommended"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "experiment_reexecution_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_guardrail_boolean_fields_remain_false(field: str):
    assert _candidate()[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_authorization_fields_remain_not_authorized(field: str):
    assert _candidate()[field] == service.NOT_AUTHORIZED


def test_limitations_and_next_gates_are_defined():
    candidate = _candidate()

    assert candidate["assessment_limitations"] == service.ASSESSMENT_LIMITATIONS
    assert candidate["additional_evidence_next_gates"] == service.NEXT_GATES


def test_summary_allows_operator_review_but_not_acceptance_or_runtime():
    summary = _candidate()["assessment_summary"]

    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_predictive_usefulness_acceptance_candidate"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_checklist_contains_all_required_check_ids():
    candidate = _candidate()

    assert [item["check_id"] for item in candidate["assessment_checklist"]] == (
        service.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_valid_candidate():
    candidate = _candidate()

    assert {item["status"] for item in candidate["assessment_checklist"]} == {service.PASS}
    assert candidate["assessment_summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["assessment_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["assessment_summary"]["failed_checks"] == 0


def test_candidate_digest_is_deterministic():
    assert _candidate()["predictive_usefulness_assessment_candidate_digest"] == (
        _candidate()["predictive_usefulness_assessment_candidate_digest"]
    )


def test_validator_accepts_valid_assessment_candidate():
    validation = service.validate_predictive_usefulness_assessment_candidate_v1(_candidate())

    assert validation["status"] == "PREDICTIVE_USEFULNESS_ASSESSMENT_CANDIDATE_VALID"
    assert validation["ready_for_predictive_usefulness_acceptance_candidate"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider_requests_made", True),
        ("experiment_reexecution_performed", True),
        ("walk_forward_rerun_performed", True),
        ("label_regeneration_performed", True),
        ("feature_matrix_regeneration_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_migration_active", True),
        ("strategy_runtime_migration", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_or_authorized_values(field: str, value: Any):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(service.PredictiveUsefulnessAssessmentCandidateError):
        service.validate_predictive_usefulness_assessment_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_results_review_package_digest", "0" * 64),
        ("predictive_experiment_execution_digest", "0" * 64),
    ],
)
def test_validator_rejects_unbound_source_digests(field: str, value: Any):
    candidate = deepcopy(_candidate())
    candidate[field] = value
    _redigest(candidate)

    with pytest.raises(service.PredictiveUsefulnessAssessmentCandidateError):
        service.validate_predictive_usefulness_assessment_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("predictive_usefulness_assessment_candidate_digest")

    with pytest.raises(service.PredictiveUsefulnessAssessmentCandidateError):
        service.validate_predictive_usefulness_assessment_candidate_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = service.build_predictive_usefulness_assessment_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Purpose",
        "## Source Predictive Experiment Results",
        "## Assessment Classification",
        "## Evidence Summary",
        "## Limitations",
        "## Additional Evidence / Next Gates",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    candidate = _candidate()
    monkeypatch.setattr(
        service,
        "build_predictive_usefulness_assessment_candidate_v1",
        lambda: candidate,
    )
    output_path = tmp_path / "predictive_usefulness_assessment_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(service.PredictiveUsefulnessAssessmentCandidateError):
        service.write_predictive_usefulness_assessment_candidate_v1(tmp_path)
