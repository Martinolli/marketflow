from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import additional_predictive_evidence_execution_candidate_redesigned_labels_operator_review_service as review_service
from marketflow.services import additional_predictive_evidence_execution_candidate_redesigned_labels_service as candidate_service


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    review = review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1()
    assert review["created_offline"] is True
    assert review["provider_requests_made"] is False


def test_artifact_kind_is_correct(review_package) -> None:
    assert review_package["artifact_kind"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"


def test_review_status_is_correct(review_package) -> None:
    assert review_package["review_status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"


def test_reviewed_candidate_digest_matches_expected(review_package) -> None:
    assert review_package["reviewed_additional_predictive_evidence_execution_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST


def test_candidate_checklist_has_zero_blockers(review_package) -> None:
    assert review_package["reviewed_additional_predictive_evidence_execution_candidate_checklist_total"] == 49
    assert review_package["reviewed_additional_predictive_evidence_execution_candidate_checklist_passed"] == 49
    assert review_package["reviewed_additional_predictive_evidence_execution_candidate_checklist_failed"] == 0
    assert review_package["reviewed_additional_predictive_evidence_execution_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest", review_service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_generation_results_review_using_redesigned_labels_digest", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("feature_generation_execution_using_redesigned_labels_digest", candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("feature_values_digest", candidate_service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("feature_generation_approval_using_redesigned_labels_digest", candidate_service.EXPECTED_APPROVAL_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_review_package_digest", candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_digest", candidate_service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", candidate_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", candidate_service.EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", candidate_service.EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", candidate_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST),
        ("research_registry_approval_digest", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", candidate_service.EXPECTED_RECORDS_DIGEST),
        ("redesigned_label_values_digest", candidate_service.EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST),
    ],
)
def test_bound_digest(review_package, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_universe_count_and_order_are_preserved(review_package) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == candidate_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(review_package) -> None:
    assert review_package["meta_record_count"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_feature_generation_results_review_is_ready(review_package) -> None:
    assert review_package["feature_generation_results_review_created"] is True
    assert review_package["feature_generation_results_review_ready"] is True


def test_predictive_evidence_candidate_and_review_are_created(review_package) -> None:
    assert review_package["additional_predictive_evidence_execution_candidate_created"] is True
    assert review_package["additional_predictive_evidence_execution_candidate_using_redesigned_labels_created"] is True
    assert review_package["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created"] is True


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_evidence_results_created",
        "metric_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made",
        "market_data_acquisition_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
    ],
)
def test_closed_action_remains_false(review_package, field: str) -> None:
    assert review_package[field] is False


def test_predictive_usefulness_is_not_accepted(review_package) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"
    assert review_package["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(review_package) -> None:
    assert review_package["profitability"] == "not accepted"
    assert review_package["profitability_acceptance_ready"] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_authority_is_closed(review_package, field: str) -> None:
    assert review_package[field] == "NOT_AUTHORIZED"


def test_source_inputs_are_reviewed(review_package) -> None:
    assert [row["source_input"] for row in review_package["source_inputs"]] == candidate_service.SOURCE_INPUT_IDS
    assert all(row["source_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in review_package["source_inputs"])
    assert all(row["actionability_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in review_package["source_inputs"])


def test_feature_label_matrix_is_reviewed_not_generated(review_package) -> None:
    matrix = review_package["planned_feature_label_matrix"]
    assert matrix["matrix_status"] == "PLANNED_NOT_GENERATED"
    assert matrix["join_execution_performed"] is False
    assert matrix["matrix_created"] is False


def test_planned_execution_activities_are_reviewed(review_package) -> None:
    activities = review_package["planned_execution_activities"]
    assert [row["activity_id"] for row in activities] == candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
    assert all(row["activity_status"] == "PLANNED_NOT_EXECUTED" for row in activities)
    assert all(row["execution_authorized"] is False for row in activities)
    assert all(row["execution_performed"] is False for row in activities)


def test_planned_splits_are_reviewed(review_package) -> None:
    assert review_package["planned_splits"] == candidate_service.PLANNED_SPLITS


def test_planned_model_baseline_family_count_is_nine(review_package) -> None:
    rows = review_package["planned_model_baseline_families"]
    assert len(rows) == 9
    assert [row["model_or_baseline_family"] for row in rows] == candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS
    assert all(row["training_performed"] is False for row in rows)


def test_planned_metric_families_are_reviewed(review_package) -> None:
    rows = review_package["planned_metric_families"]
    assert [row["metric_family"] for row in rows] == candidate_service.PLANNED_METRIC_FAMILY_IDS
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in rows)


def test_planned_outputs_are_not_generated(review_package) -> None:
    rows = review_package["planned_outputs"]
    assert [row["output_id"] for row in rows] == candidate_service.PLANNED_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["actionability_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_review_entries_count_is_twelve(review_package) -> None:
    entries = review_package["per_ticker_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    assert all(row["additional_predictive_evidence_execution_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT" for row in entries)


def test_per_ticker_candidate_digests_are_present(review_package) -> None:
    assert all(len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_per_ticker_review_digests_are_present(review_package) -> None:
    assert all(len(row["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_future_chain_and_gates_are_reviewed(review_package) -> None:
    assert review_package["future_chain"] == review_service.FUTURE_CHAIN
    assert review_package["future_gates"] == review_service.FUTURE_GATES


def test_risk_controls_are_reviewed(review_package) -> None:
    assert review_package["risk_controls"] == review_service.RISK_CONTROLS


def test_checklist_passes(review_package) -> None:
    checklist = review_package["review_checklist"]
    assert [row["check_id"] for row in checklist] == review_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    assert review_package["review_summary"]["passed_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert review_package["review_summary"]["blocker_count"] == 0
    assert review_package["review_summary"]["ready_for_additional_predictive_evidence_execution_approval"] is False


def test_review_digest_is_deterministic(review_package) -> None:
    first = review_service.additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest_v1(review_package)
    second = review_service.additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest_v1(deepcopy(review_package))
    assert first == second == review_package["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"]


def test_per_ticker_review_digests_are_deterministic(review_package) -> None:
    for entry in review_package["per_ticker_review_entries"]:
        assert entry["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"] == review_service.per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_digest_v1(deepcopy(entry))


def test_validator_accepts_valid_review_package(review_package) -> None:
    result = review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(deepcopy(review_package))
    assert result["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID"
    assert result["ready_for_operator_assessment"] is True
    assert result["ready_for_additional_predictive_evidence_execution_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_additional_predictive_evidence_execution_candidate_digest", "0" * 64),
        ("reviewed_additional_predictive_evidence_execution_candidate_status", "WRONG"),
        ("reviewed_additional_predictive_evidence_execution_candidate_blocker_count", 1),
        ("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest", None),
        ("feature_generation_results_review_using_redesigned_labels_digest", None),
        ("feature_values_digest", None),
        ("redesigned_label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_generation_results_review_ready", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created", False),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_invalid_boundary(review_package, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "planned_execution_activities",
        "planned_splits",
        "planned_model_baseline_families",
        "planned_metric_families",
        "future_chain",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_review(review_package, field: str) -> None:
    changed = deepcopy(review_package)
    changed.pop(field)
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(changed)


def test_validator_rejects_missing_review_digest(review_package) -> None:
    changed = deepcopy(review_package)
    changed.pop("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest")
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_additional_predictive_evidence_execution_candidate_digest",
        "per_ticker_additional_predictive_evidence_execution_candidate_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(review_package, field: str) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_review_entries"][0].pop(field)
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(changed)


def test_builder_rejects_invalid_injected_candidate() -> None:
    candidate = candidate_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()
    candidate["additional_predictive_evidence_execution_authorized"] = True
    with pytest.raises(candidate_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(candidate)


def test_markdown_includes_required_sections(review_package) -> None:
    markdown = review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_markdown_v1(review_package)
    sections = [
        "Title", "Additional Predictive Evidence Execution Candidate Review Using Redesigned Labels",
        "Reviewed Candidate", "Bound Evidence", "Dataset and Universe",
        "Source Redesigned Label Profile", "Source Feature Profile", "Reviewed Candidate Objective",
        "Reviewed Source Inputs", "Reviewed Feature / Label Matrix", "Reviewed Execution Activities",
        "Reviewed Splits", "Reviewed Model and Baseline Families", "Reviewed Metric Families",
        "Reviewed Planned Outputs", "Per-Ticker Review Entries", "Future Chain", "Future Gates",
        "Risk Controls", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_writes_once(review_package, tmp_path) -> None:
    result = review_service.write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(tmp_path)
    assert result["review_status"] == review_package["review_status"]
    assert (tmp_path / result["filename"]).is_file()
    with pytest.raises(review_service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsOperatorReviewError):
        review_service.write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1(tmp_path)


def test_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE
    assert services.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1 is review_service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1
    assert services.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1 is review_service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_v1
