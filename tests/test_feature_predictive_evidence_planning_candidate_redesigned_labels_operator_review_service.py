from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_predictive_evidence_planning_candidate_redesigned_labels_operator_review_service as review_service
from marketflow.services import feature_predictive_evidence_planning_candidate_redesigned_labels_service as candidate_service


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made"] is False
    assert result["market_data_acquisition_performed"] is False


def test_artifact_kind_is_correct(review_package) -> None:
    assert review_package["artifact_kind"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"


def test_review_status_is_correct(review_package) -> None:
    assert review_package["review_status"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"


def test_reviewed_candidate_digest_matches_expected(review_package) -> None:
    assert review_package["reviewed_feature_predictive_evidence_planning_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST


def test_candidate_checklist_has_zero_blockers(review_package) -> None:
    assert review_package["reviewed_feature_predictive_evidence_planning_candidate_checklist_total"] == 48
    assert review_package["reviewed_feature_predictive_evidence_planning_candidate_checklist_passed"] == 48
    assert review_package["reviewed_feature_predictive_evidence_planning_candidate_checklist_failed"] == 0
    assert review_package["reviewed_feature_predictive_evidence_planning_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", review_service.EXPECTED_CANDIDATE_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", candidate_service.EXPECTED_APPROVAL_DIGEST),
        ("redesigned_label_generation_candidate_review_package_digest", candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("redesigned_label_generation_candidate_digest", candidate_service.EXPECTED_CANDIDATE_DIGEST),
        ("research_registry_approval_digest", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", candidate_service.EXPECTED_RECORDS_DIGEST),
        ("label_values_digest", candidate_service.EXPECTED_LABEL_VALUES_DIGEST),
    ],
)
def test_bound_digest(review_package, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_universe_count_and_order_are_preserved(review_package) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == candidate_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(review_package) -> None:
    assert review_package["meta_record_count"] == 913
    assert review_package["per_ticker_record_counts"]["META"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_results_review_ready_is_true(review_package) -> None:
    assert review_package["redesigned_label_generation_results_review_ready"] is True


def test_planning_candidate_and_review_created_are_true(review_package) -> None:
    assert review_package["feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created"] is True
    assert review_package["feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_ready_for_operator_review"] is True
    assert review_package["feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_review_created"] is True


def test_planning_approval_remains_false(review_package) -> None:
    assert review_package["feature_predictive_evidence_planning_approved"] is False
    assert review_package["review_summary"]["ready_for_feature_predictive_evidence_planning_approval"] is False


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
def test_downstream_action_remains_false(review_package, field: str) -> None:
    assert review_package[field] is False


def test_predictive_usefulness_is_not_accepted(review_package) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"


def test_profitability_is_not_accepted(review_package) -> None:
    assert review_package["profitability"] == "not accepted"


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(review_package, field: str) -> None:
    assert review_package[field] == "NOT_AUTHORIZED"


def test_source_inputs_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_source_inputs"]
    assert [row["source_input_id"] for row in rows] == candidate_service.SOURCE_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in rows)


def test_planned_feature_families_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_planned_feature_families"]
    assert [row["feature_family_id"] for row in rows] == candidate_service.PLANNED_FEATURE_FAMILY_IDS
    assert all(row["feature_generation_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["feature_generation_authorized"] is False for row in rows)


def test_planned_predictive_components_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_planned_predictive_evidence_components"]
    assert [row["component_id"] for row in rows] == candidate_service.PLANNED_PREDICTIVE_COMPONENT_IDS
    assert all(row["component_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)


def test_planned_model_baseline_families_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_planned_model_baseline_families"]
    assert [row["model_or_baseline_family_id"] for row in rows] == candidate_service.PLANNED_MODEL_BASELINE_FAMILY_IDS
    assert all(row["model_or_baseline_status"] == "PLANNED_NOT_EVALUATED" for row in rows)
    assert all(row["training_authorized"] is False for row in rows)


def test_planned_outputs_are_not_generated(review_package) -> None:
    rows = review_package["reviewed_planned_outputs"]
    assert [row["planned_output_id"] for row in rows] == candidate_service.PLANNED_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_redesigned_label_row_count_is_preserved(review_package) -> None:
    assert review_package["label_value_row_count"] == 143352


def test_available_and_unavailable_counts_are_preserved(review_package) -> None:
    assert review_package["available_label_value_count"] == 142200
    assert review_package["unavailable_label_value_count"] == 1152


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("label_family_count", 10),
        ("threshold_strategy_count", 7),
        ("horizon_strategy_count", 5),
    ],
)
def test_redesigned_label_profile_count(review_package, field: str, expected: int) -> None:
    assert review_package[field] == expected


def test_per_ticker_entries_count_is_twelve(review_package) -> None:
    entries = review_package["per_ticker_candidate_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE


def test_per_ticker_candidate_digests_are_present(review_package) -> None:
    for entry in review_package["per_ticker_candidate_review_entries"]:
        assert len(entry["per_ticker_feature_predictive_evidence_planning_candidate_digest"]) == 64


def test_per_ticker_review_digests_are_present(review_package) -> None:
    for entry in review_package["per_ticker_candidate_review_entries"]:
        digest = entry["per_ticker_feature_predictive_evidence_planning_candidate_review_digest"]
        assert len(digest) == 64
        assert digest == review_service.per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(entry)


def test_meta_review_entry_preserves_limitation(review_package) -> None:
    meta = next(row for row in review_package["per_ticker_candidate_review_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_AND_PREDICTIVE_EVIDENCE_PLANNING"


def test_future_chain_is_reviewed(review_package) -> None:
    assert review_package["reviewed_future_chain"] == candidate_service.FUTURE_CHAIN


def test_future_gates_are_reviewed(review_package) -> None:
    assert review_package["reviewed_future_gates"] == candidate_service.FUTURE_GATES


def test_risk_controls_are_reviewed(review_package) -> None:
    assert review_package["reviewed_risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(review_package) -> None:
    assert [row["check_id"] for row in review_package["review_checklist"]] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review_package["review_checklist"])
    assert review_package["review_summary"]["passed_checks"] == 57
    assert review_package["review_summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(review_package) -> None:
    first = review_service.feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest_v1(review_package)
    second = review_service.feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest_v1(deepcopy(review_package))
    assert first == second == review_package["feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"]


def test_per_ticker_review_digests_are_deterministic(review_package) -> None:
    for entry in review_package["per_ticker_candidate_review_entries"]:
        first = review_service.per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(entry)
        second = review_service.per_ticker_feature_predictive_evidence_planning_candidate_review_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_review_package(review_package) -> None:
    validation = review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(deepcopy(review_package))
    assert validation["status"] == "FEATURE_PREDICTIVE_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_feature_predictive_evidence_planning_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_feature_predictive_evidence_planning_candidate_digest", "0" * 64),
        ("reviewed_feature_predictive_evidence_planning_candidate_status", "WRONG"),
        ("reviewed_feature_predictive_evidence_planning_candidate_blocker_count", 1),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", None),
        ("redesigned_label_generation_results_review_package_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("redesigned_label_generation_results_review_ready", False),
        ("ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels", False),
        ("feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created", False),
        ("feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_review_created", False),
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
def test_validator_rejects_invalid_review_boundary(review_package, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_source_inputs",
        "reviewed_planned_feature_families",
        "reviewed_planned_predictive_evidence_components",
        "reviewed_planned_model_baseline_families",
        "reviewed_future_chain",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_review_section(review_package, field: str) -> None:
    changed = deepcopy(review_package)
    changed.pop(field)
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(changed)


def test_validator_rejects_missing_review_digest(review_package) -> None:
    changed = deepcopy(review_package)
    changed.pop("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest")
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(changed)


def test_validator_rejects_missing_per_ticker_candidate_digest(review_package) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_candidate_review_entries"][0].pop(
        "per_ticker_feature_predictive_evidence_planning_candidate_digest"
    )
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(changed)


def test_validator_rejects_missing_per_ticker_review_digest(review_package) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_candidate_review_entries"][0].pop(
        "per_ticker_feature_predictive_evidence_planning_candidate_review_digest"
    )
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(changed)


def test_markdown_includes_required_sections(review_package) -> None:
    markdown = review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_markdown_v1(review_package)
    sections = [
        "Title",
        "Feature / Predictive Evidence Planning Candidate Review Using Redesigned Labels",
        "Reviewed Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Source Redesigned Label Profile",
        "Reviewed Source Inputs",
        "Reviewed Planned Feature Families",
        "Reviewed Planned Predictive Evidence Components",
        "Reviewed Planned Model and Baseline Families",
        "Reviewed Planned Outputs",
        "Per-Ticker Review Entries",
        "Future Chain",
        "Future Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_review_once(review_package, tmp_path) -> None:
    result = review_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(tmp_path)
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == review_package
    with pytest.raises(review_service.FeaturePredictiveEvidencePlanningCandidateRedesignedLabelsOperatorReviewError):
        review_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1 is review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1
    assert services.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1 is review_service.validate_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1
    assert services.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_markdown_v1 is review_service.build_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_markdown_v1
    assert services.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1 is review_service.write_feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_v1
