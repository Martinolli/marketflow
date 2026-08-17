from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_predictive_evidence_planning_candidate_redesigned_labels_service as candidate_service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made"] is False
    assert result["market_data_acquisition_performed"] is False


def test_artifact_kind_is_correct(candidate) -> None:
    assert candidate["artifact_kind"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS"


def test_candidate_status_is_correct(candidate) -> None:
    assert candidate["candidate_status"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("redesigned_label_generation_results_review_package_digest", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", candidate_service.EXPECTED_APPROVAL_DIGEST),
        ("redesigned_label_generation_candidate_review_package_digest", candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("redesigned_label_generation_candidate_digest", candidate_service.EXPECTED_CANDIDATE_DIGEST),
        ("label_objective_redesign_results_review_package_digest", candidate_service.EXPECTED_LABEL_OBJECTIVE_RESULTS_REVIEW_DIGEST),
        ("label_objective_redesign_execution_digest", candidate_service.EXPECTED_LABEL_OBJECTIVE_EXECUTION_DIGEST),
        ("operator_method_path_selection_digest", candidate_service.EXPECTED_METHOD_SELECTION_DIGEST),
        ("research_registry_approval_digest", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", candidate_service.EXPECTED_RECORDS_DIGEST),
        ("label_values_digest", candidate_service.EXPECTED_LABEL_VALUES_DIGEST),
    ],
)
def test_required_digest_is_bound(candidate, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_universe_count_and_order_are_preserved(candidate) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(candidate) -> None:
    assert candidate["meta_record_count"] == 913
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_results_review_ready_is_true(candidate) -> None:
    assert candidate["redesigned_label_generation_results_review_ready"] is True


def test_ready_for_planning_candidate_is_true(candidate) -> None:
    assert candidate["ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"] is True


def test_planning_candidate_created_and_ready_are_true(candidate) -> None:
    assert candidate["feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created"] is True
    assert candidate["feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review"] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_candidate_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "trade_recommendations_generated",
    ],
)
def test_downstream_action_remains_false(candidate, field: str) -> None:
    assert candidate[field] is False


def test_predictive_usefulness_is_not_accepted(candidate) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"


def test_profitability_is_not_accepted(candidate) -> None:
    assert candidate["profitability"] == "not accepted"


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(candidate, field: str) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_redesigned_label_row_count_is_preserved(candidate) -> None:
    assert candidate["label_value_row_count"] == 143352


def test_available_and_unavailable_counts_are_preserved(candidate) -> None:
    assert candidate["available_label_value_count"] == 142200
    assert candidate["unavailable_label_value_count"] == 1152


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("label_family_count", 10),
        ("threshold_strategy_count", 7),
        ("horizon_strategy_count", 5),
    ],
)
def test_redesigned_label_profile_count(candidate, field: str, expected: int) -> None:
    assert candidate[field] == expected


def test_source_inputs_are_defined(candidate) -> None:
    assert [row["source_input_id"] for row in candidate["source_inputs"]] == candidate_service.SOURCE_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in candidate["source_inputs"])
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in candidate["source_inputs"])


def test_planned_feature_families_are_defined(candidate) -> None:
    rows = candidate["planned_feature_families"]
    assert [row["feature_family_id"] for row in rows] == candidate_service.PLANNED_FEATURE_FAMILY_IDS
    assert all(row["feature_generation_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["feature_generation_authorized"] is False for row in rows)
    assert all(row["feature_generation_performed"] is False for row in rows)


def test_planned_predictive_components_are_defined(candidate) -> None:
    rows = candidate["planned_predictive_evidence_components"]
    assert [row["component_id"] for row in rows] == candidate_service.PLANNED_PREDICTIVE_COMPONENT_IDS
    assert all(row["component_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)
    assert all(row["execution_performed"] is False for row in rows)


def test_planned_model_baseline_families_are_defined(candidate) -> None:
    rows = candidate["planned_model_baseline_families"]
    assert [row["model_or_baseline_family_id"] for row in rows] == candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS
    assert all(row["model_or_baseline_status"] == "PLANNED_NOT_EVALUATED" for row in rows)
    assert all(row["training_authorized"] is False for row in rows)
    assert all(row["training_performed"] is False for row in rows)


def test_planned_outputs_are_not_generated(candidate) -> None:
    rows = candidate["planned_outputs"]
    assert [row["planned_output_id"] for row in rows] == candidate_service.PLANNED_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_entries_count_is_twelve(candidate) -> None:
    entries = candidate["per_ticker_candidate_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE


def test_per_ticker_digests_are_present(candidate) -> None:
    for entry in candidate["per_ticker_candidate_entries"]:
        digest = entry["per_ticker_feature_predictive_evidence_planning_candidate_digest"]
        assert len(digest) == 64
        assert digest == candidate_service.per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(candidate) -> None:
    meta = next(row for row in candidate["per_ticker_candidate_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING"


def test_future_chain_is_defined(candidate) -> None:
    assert candidate["future_chain"] == candidate_service.FUTURE_CHAIN


def test_future_gates_are_defined(candidate) -> None:
    assert candidate["future_gates"] == candidate_service.FUTURE_GATES


def test_risk_controls_are_defined(candidate) -> None:
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(candidate) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == candidate_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"]["passed_checks"] == 48
    assert candidate["candidate_summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate) -> None:
    first = candidate_service.feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest_v1(candidate)
    second = candidate_service.feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest_v1(deepcopy(candidate))
    assert first == second == candidate["feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest"]


def test_per_ticker_digests_are_deterministic(candidate) -> None:
    for entry in candidate["per_ticker_candidate_entries"]:
        first = candidate_service.per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(entry)
        second = candidate_service.per_ticker_feature_predictive_evidence_planning_candidate_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_candidate(candidate) -> None:
    validation = candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(deepcopy(candidate))
    assert validation["status"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
    assert validation["ready_for_operator_review"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("redesigned_label_generation_results_review_package_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("redesigned_label_generation_results_review_ready", False),
        ("ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels", False),
        ("feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created", False),
        ("feature_generation_candidate_created", True),
        ("feature_generation_performed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_invalid_candidate_boundary(candidate, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(candidate_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError):
        candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "source_inputs",
        "planned_feature_families",
        "planned_predictive_evidence_components",
        "planned_model_baseline_families",
        "future_chain",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_plan_section(candidate, field: str) -> None:
    changed = deepcopy(candidate)
    changed.pop(field)
    with pytest.raises(candidate_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError):
        candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate) -> None:
    changed = deepcopy(candidate)
    changed.pop("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest")
    with pytest.raises(candidate_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError):
        candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_candidate_entries"][0].pop(
        "per_ticker_feature_predictive_evidence_planning_candidate_digest"
    )
    with pytest.raises(candidate_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError):
        candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(changed)


def test_markdown_includes_required_sections(candidate) -> None:
    markdown = candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_markdown_v1(candidate)
    sections = [
        "Title",
        "Feature / Predictive Evidence Planning Candidate Using Redesigned Labels",
        "Bound Evidence",
        "Dataset and Universe",
        "Source Redesigned Label Profile",
        "Source Inputs",
        "Planned Feature Families",
        "Planned Predictive Evidence Components",
        "Planned Model and Baseline Families",
        "Planned Outputs",
        "Per-Ticker Candidate Entries",
        "Future Chain",
        "Future Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_candidate_once(candidate, tmp_path) -> None:
    result = candidate_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(tmp_path)
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == candidate
    with pytest.raises(candidate_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsError):
        candidate_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1 is candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1
    assert services.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1 is candidate_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1
    assert services.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_markdown_v1 is candidate_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_markdown_v1
    assert services.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1 is candidate_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_v1
