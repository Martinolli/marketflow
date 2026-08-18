from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import additional_predictive_evidence_execution_candidate_redesigned_labels_service as service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    candidate = service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1()
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_is_correct(candidate) -> None:
    assert candidate["artifact_kind"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS"


def test_candidate_status_is_correct(candidate) -> None:
    assert candidate["candidate_status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_generation_results_review_using_redesigned_labels_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("feature_generation_execution_using_redesigned_labels_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("feature_generation_approval_using_redesigned_labels_digest", service.EXPECTED_APPROVAL_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_review_package_digest", service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_digest", service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", service.EXPECTED_REDESIGNED_LABEL_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", service.EXPECTED_REDESIGNED_LABEL_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST),
    ],
)
def test_bound_digest(candidate, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_universe_count_and_order_are_preserved(candidate) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.TARGET_UNIVERSE


def test_meta_913_is_preserved(candidate) -> None:
    assert candidate["meta_record_count"] == 913
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_feature_generation_results_review_is_ready(candidate) -> None:
    assert candidate["feature_generation_results_review_created"] is True
    assert candidate["feature_generation_results_review_ready"] is True


def test_ready_for_predictive_evidence_candidate_is_true(candidate) -> None:
    assert candidate["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is True


def test_predictive_evidence_candidate_is_created_and_ready(candidate) -> None:
    assert candidate["additional_predictive_evidence_execution_candidate_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_ready_for_operator_review"] is True


def test_predictive_evidence_candidate_review_is_not_created(candidate) -> None:
    assert candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created"] is False


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
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
    ],
)
def test_closed_action_remains_false(candidate, field: str) -> None:
    assert candidate[field] is False


def test_predictive_usefulness_is_not_accepted(candidate) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(candidate) -> None:
    assert candidate["profitability"] == "not accepted"
    assert candidate["profitability_acceptance_ready"] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_authority_is_closed(candidate, field: str) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_source_inputs_are_defined(candidate) -> None:
    assert [row["source_input"] for row in candidate["source_inputs"]] == service.SOURCE_INPUT_IDS
    assert all(row["source_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in candidate["source_inputs"])
    assert all(row["actionability_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in candidate["source_inputs"])


def test_feature_label_matrix_is_planned_not_generated(candidate) -> None:
    matrix = candidate["planned_feature_label_matrix"]
    assert matrix["matrix_status"] == "PLANNED_NOT_GENERATED"
    assert matrix["feature_values_digest_bound"] is True
    assert matrix["redesigned_label_values_digest_bound"] is True
    assert matrix["records_digest_bound"] is True
    assert matrix["feature_row_count"] == 203082
    assert matrix["label_row_count"] == 143352
    assert matrix["join_execution_performed"] is False
    assert matrix["matrix_created"] is False


def test_planned_execution_activities_are_defined(candidate) -> None:
    activities = candidate["planned_execution_activities"]
    assert [row["activity_id"] for row in activities] == service.PLANNED_EXECUTION_ACTIVITY_IDS
    assert all(row["activity_status"] == "PLANNED_NOT_EXECUTED" for row in activities)
    assert all(row["execution_authorized"] is False for row in activities)
    assert all(row["execution_performed"] is False for row in activities)


def test_planned_splits_are_defined(candidate) -> None:
    assert candidate["planned_splits"] == service.PLANNED_SPLITS
    assert candidate["planned_splits"]["shuffle_allowed"] is False
    assert candidate["planned_splits"]["chronological_order_required"] is True


def test_planned_model_baseline_family_count_is_nine(candidate) -> None:
    rows = candidate["planned_model_baseline_families"]
    assert [row["model_or_baseline_family"] for row in rows] == service.PLANNED_MODEL_BASELINE_FAMILY_IDS
    assert len(rows) == 9
    assert all(row["training_authorized"] is False for row in rows)
    assert all(row["training_performed"] is False for row in rows)
    assert all(row["metric_computation_performed"] is False for row in rows)


def test_planned_metric_families_are_defined(candidate) -> None:
    rows = candidate["planned_metric_families"]
    assert [row["metric_family"] for row in rows] == service.PLANNED_METRIC_FAMILY_IDS
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in rows)
    assert all(row["metric_computation_authorized"] is False for row in rows)
    assert all(row["metric_computation_performed"] is False for row in rows)


def test_planned_outputs_are_not_generated(candidate) -> None:
    rows = candidate["planned_outputs"]
    assert [row["output_id"] for row in rows] == service.PLANNED_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["actionability_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_entries_count_is_twelve(candidate) -> None:
    entries = candidate["per_ticker_candidate_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == service.TARGET_UNIVERSE
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_PREDICTIVE_EVIDENCE_CANDIDATE"
    assert all(row["historical_record_count"] == 1003 for row in entries if row["ticker"] != "META")


def test_per_ticker_digests_are_present(candidate) -> None:
    assert all(len(row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]) == 64 for row in candidate["per_ticker_candidate_entries"])


def test_future_chain_and_gates_are_defined(candidate) -> None:
    assert candidate["future_chain"] == service.FUTURE_CHAIN
    assert candidate["future_gates"] == service.FUTURE_GATES


def test_risk_controls_are_defined(candidate) -> None:
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_checklist_passes(candidate) -> None:
    checklist = candidate["candidate_checklist"]
    assert [row["check_id"] for row in checklist] == service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    assert candidate["candidate_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["candidate_summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate) -> None:
    first = service.additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(candidate)
    second = service.additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(deepcopy(candidate))
    assert first == second == candidate["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"]


def test_per_ticker_digests_are_deterministic(candidate) -> None:
    for entry in candidate["per_ticker_candidate_entries"]:
        assert entry["per_ticker_additional_predictive_evidence_execution_candidate_digest"] == service.per_ticker_additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest_v1(deepcopy(entry))


def test_validator_accepts_valid_candidate(candidate) -> None:
    result = service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(deepcopy(candidate))
    assert result["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
    assert result["ready_for_operator_review"] is True
    assert result["additional_predictive_evidence_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("feature_generation_results_review_using_redesigned_labels_digest", None),
        ("feature_values_digest", None),
        ("redesigned_label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_generation_results_review_ready", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_created", True),
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
def test_validator_rejects_invalid_boundary(candidate, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(changed)


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
def test_validator_rejects_missing_required_plan(candidate, field: str) -> None:
    changed = deepcopy(candidate)
    changed.pop(field)
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate) -> None:
    changed = deepcopy(candidate)
    changed.pop("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest")
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_candidate_entries"][0].pop("per_ticker_additional_predictive_evidence_execution_candidate_digest")
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(changed)


def test_markdown_includes_required_sections(candidate) -> None:
    markdown = service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_markdown_v1(candidate)
    sections = [
        "Title", "Additional Predictive Evidence Execution Candidate Using Redesigned Labels",
        "Bound Evidence", "Dataset and Universe", "Source Redesigned Label Profile",
        "Source Feature Profile", "Candidate Objective", "Source Inputs",
        "Planned Feature / Label Matrix", "Planned Execution Activities", "Planned Splits",
        "Planned Model and Baseline Families", "Planned Metric Families", "Planned Outputs",
        "Per-Ticker Candidate Entries", "Future Chain", "Future Gates", "Risk Controls",
        "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_writes_once(candidate, tmp_path) -> None:
    result = service.write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(tmp_path)
    assert result["candidate_status"] == candidate["candidate_status"]
    assert (tmp_path / result["filename"]).is_file()
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateRedesignedLabelsError):
        service.write_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1(tmp_path)


def test_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_REDESIGNED_LABELS
    assert services.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1 is service.build_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1
    assert services.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1 is service.validate_additional_predictive_evidence_execution_candidate_using_redesigned_labels_v1
