from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_generation_candidate_redesigned_labels_operator_review_service as review_service


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made"] is False
    assert result["market_data_acquisition_performed"] is False


def test_review_package_accepts_explicit_candidate() -> None:
    candidate = review_service.candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()
    result = review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1(candidate)
    assert result["reviewed_feature_generation_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST


def test_artifact_kind_is_correct(review_package) -> None:
    assert review_package["artifact_kind"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE"


def test_review_status_is_correct(review_package) -> None:
    assert review_package["review_status"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY"


def test_reviewed_candidate_evidence_matches(review_package) -> None:
    assert review_package["reviewed_feature_generation_candidate_kind"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS"
    assert review_package["reviewed_feature_generation_candidate_status"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"
    assert review_package["reviewed_feature_generation_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST
    assert review_package["reviewed_feature_generation_candidate_checklist_total"] == 47
    assert review_package["reviewed_feature_generation_candidate_checklist_passed"] == 47
    assert review_package["reviewed_feature_generation_candidate_checklist_failed"] == 0
    assert review_package["reviewed_feature_generation_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_generation_candidate_using_redesigned_labels_digest", review_service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", review_service.candidate_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", review_service.candidate_service.EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", review_service.candidate_service.EXPECTED_PLANNING_CANDIDATE_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", review_service.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", review_service.candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", review_service.candidate_service.EXPECTED_APPROVAL_DIGEST),
        ("label_values_digest", review_service.candidate_service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", review_service.candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", review_service.candidate_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_digest_is_bound(review_package, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_universe_count_and_order_are_preserved(review_package) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == review_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(review_package) -> None:
    assert review_package["meta_record_count"] == 913
    assert review_package["per_ticker_record_counts"]["META"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_planning_and_candidate_flags_are_true(review_package) -> None:
    assert review_package["feature_predictive_evidence_planning_approved"] is True
    assert review_package["ready_for_feature_generation_candidate_using_redesigned_labels"] is True
    assert review_package["feature_generation_candidate_created"] is True
    assert review_package["feature_generation_candidate_using_redesigned_labels_created"] is True
    assert review_package["feature_generation_candidate_using_redesigned_labels_ready_for_operator_review"] is True
    assert review_package["feature_generation_candidate_using_redesigned_labels_review_created"] is True


def test_predictive_evidence_candidate_is_not_ready(review_package) -> None:
    assert review_package["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is False


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_approved",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_downstream_action_remains_false(review_package, field: str) -> None:
    assert review_package[field] is False


def test_predictive_usefulness_and_profitability_are_not_accepted(review_package) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"
    assert review_package["profitability"] == "not accepted"


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(review_package, field: str) -> None:
    assert review_package[field] == "NOT_AUTHORIZED"


def test_reviewed_source_inputs_are_preserved(review_package) -> None:
    rows = review_package["reviewed_source_inputs"]
    assert [row["source_input_id"] for row in rows] == review_service.candidate_service.SOURCE_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_planned_feature_families_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_planned_feature_families"]
    assert [row["feature_family_id"] for row in rows] == review_service.candidate_service.PLANNED_FEATURE_FAMILY_IDS
    assert len(rows) == 10
    assert all(row["feature_generation_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW" for row in rows)
    assert all(row["feature_values_created"] is False for row in rows)


def test_planned_feature_groups_are_reviewed(review_package) -> None:
    groups = [group for family in review_package["reviewed_planned_feature_families"] for group in family["planned_feature_groups"]]
    assert [row["feature_group_id"] for row in groups] == review_service.candidate_service.PLANNED_FEATURE_GROUP_IDS
    assert len(groups) == 17
    assert all(row["group_status"] == "PLANNED_NOT_GENERATED" for row in groups)
    assert all(row["feature_generation_performed"] is False for row in groups)


def test_schema_contract_is_reviewed(review_package) -> None:
    contract = review_package["reviewed_feature_schema_contract"]
    assert contract["feature_schema_contract_status"] == "PLANNED_NOT_GENERATED"
    assert contract["planned_schema_fields"] == review_service.candidate_service.FEATURE_SCHEMA_FIELDS
    assert contract["feature_values_created"] is False


def test_alignment_controls_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_feature_label_alignment_controls"]
    assert [row["control_id"] for row in rows] == review_service.candidate_service.ALIGNMENT_CONTROL_IDS
    assert all(row["control_status"] == "PLANNED_FOR_OPERATOR_REVIEW" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_quality_checks_are_reviewed(review_package) -> None:
    rows = review_package["reviewed_quality_checks"]
    assert [row["planned_check_id"] for row in rows] == review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
    assert all(row["planned_check_status"] == "PLANNED_NOT_EXECUTED" for row in rows)


def test_planned_outputs_are_not_generated(review_package) -> None:
    rows = review_package["reviewed_planned_outputs"]
    assert [row["planned_output_id"] for row in rows] == review_service.candidate_service.PLANNED_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_entries_count_is_twelve(review_package) -> None:
    entries = review_package["per_ticker_candidate_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review_service.TARGET_UNIVERSE


def test_per_ticker_candidate_and_review_digests_are_present(review_package) -> None:
    for entry in review_package["per_ticker_candidate_review_entries"]:
        assert len(entry["per_ticker_feature_generation_candidate_digest"]) == 64
        review_digest = entry["per_ticker_feature_generation_candidate_review_digest"]
        assert len(review_digest) == 64
        assert review_digest == review_service.per_ticker_feature_generation_candidate_review_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(review_package) -> None:
    meta = next(row for row in review_package["per_ticker_candidate_review_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_CANDIDATE"


def test_future_chain_gates_and_risks_are_reviewed(review_package) -> None:
    assert review_package["future_chain"] == review_service.candidate_service.FUTURE_CHAIN
    assert review_package["future_gates"] == review_service.candidate_service.FUTURE_GATES
    assert review_package["risk_controls"] == review_service.candidate_service.RISK_CONTROLS


def test_checklist_passes(review_package) -> None:
    assert [row["check_id"] for row in review_package["review_checklist"]] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review_package["review_checklist"])
    assert review_package["review_summary"]["passed_checks"] == len(review_service.REQUIRED_CHECK_IDS)
    assert review_package["review_summary"]["blocker_count"] == 0
    assert review_package["review_summary"]["ready_for_operator_assessment"] is True
    assert review_package["review_summary"]["ready_for_feature_generation_approval"] is False


def test_review_digest_is_deterministic(review_package) -> None:
    first = review_service.feature_generation_candidate_using_redesigned_labels_review_package_digest_v1(review_package)
    second = review_service.feature_generation_candidate_using_redesigned_labels_review_package_digest_v1(deepcopy(review_package))
    assert first == second == review_package["feature_generation_candidate_using_redesigned_labels_review_package_digest"]


def test_per_ticker_review_digests_are_deterministic(review_package) -> None:
    for entry in review_package["per_ticker_candidate_review_entries"]:
        first = review_service.per_ticker_feature_generation_candidate_review_digest_v1(entry)
        second = review_service.per_ticker_feature_generation_candidate_review_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_review_package(review_package) -> None:
    validation = review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(deepcopy(review_package))
    assert validation["status"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_feature_generation_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_feature_generation_candidate_digest", "0" * 64),
        ("reviewed_feature_generation_candidate_status", "WRONG"),
        ("reviewed_feature_generation_candidate_blocker_count", 1),
        ("feature_generation_candidate_using_redesigned_labels_digest", None),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(review_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_predictive_evidence_planning_approved", False),
        ("ready_for_feature_generation_candidate_using_redesigned_labels", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", True),
        ("feature_generation_candidate_created", False),
        ("feature_generation_candidate_using_redesigned_labels_review_created", False),
        ("feature_generation_authorized", True),
        ("feature_generation_performed", True),
        ("feature_values_created", True),
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
    invalid = deepcopy(review_package)
    invalid[field] = value
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_planned_feature_families",
        "reviewed_feature_schema_contract",
        "reviewed_feature_label_alignment_controls",
        "reviewed_quality_checks",
        "future_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_collection(review_package, field: str) -> None:
    invalid = deepcopy(review_package)
    invalid.pop(field)
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


def test_validator_rejects_missing_feature_group(review_package) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_planned_feature_families"][0]["planned_feature_groups"].pop()
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


def test_validator_rejects_missing_review_digest(review_package) -> None:
    invalid = deepcopy(review_package)
    invalid.pop("feature_generation_candidate_using_redesigned_labels_review_package_digest")
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


def test_validator_rejects_missing_per_ticker_candidate_digest(review_package) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_candidate_review_entries"][0].pop("per_ticker_feature_generation_candidate_digest")
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


def test_validator_rejects_missing_per_ticker_review_digest(review_package) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_candidate_review_entries"][0].pop("per_ticker_feature_generation_candidate_review_digest")
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1(invalid)


def test_builder_rejects_candidate_blocker() -> None:
    candidate = review_service.candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()
    candidate["candidate_summary"]["blocker_count"] = 1
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1(candidate)


def test_builder_rejects_changed_candidate_digest() -> None:
    candidate = review_service.candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()
    candidate["feature_generation_candidate_using_redesigned_labels_digest"] = "0" * 64
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1(candidate)


def test_markdown_includes_required_sections(review_package) -> None:
    markdown = review_service.build_feature_generation_candidate_using_redesigned_labels_review_markdown_v1(review_package)
    for heading in [
        "## Title",
        "## Feature Generation Candidate Review Using Redesigned Labels",
        "## Reviewed Candidate",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Source Redesigned Label Profile",
        "## Reviewed Source Inputs",
        "## Reviewed Planned Feature Families",
        "## Reviewed Planned Feature Groups",
        "## Reviewed Feature Schema Contract",
        "## Reviewed Feature / Label Alignment Controls",
        "## Reviewed Quality Checks",
        "## Per-Ticker Review Entries",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert heading in markdown


def test_writer_uses_isolated_directory_and_does_not_overwrite(tmp_path) -> None:
    receipt = review_service.write_feature_generation_candidate_using_redesigned_labels_review_package_v1(tmp_path)
    output = tmp_path / receipt["filename"]
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["feature_generation_candidate_using_redesigned_labels_review_package_digest"] == receipt["feature_generation_candidate_using_redesigned_labels_review_package_digest"]
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.write_feature_generation_candidate_using_redesigned_labels_review_package_v1(tmp_path)


def test_writer_rejects_nested_filename(tmp_path) -> None:
    with pytest.raises(review_service.FeatureGenerationCandidateRedesignedLabelsOperatorReviewError):
        review_service.write_feature_generation_candidate_using_redesigned_labels_review_package_v1(tmp_path, filename="nested/review.json")


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE
    assert services.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY == review_service.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_REVIEW_PACKAGE_READY
    assert services.build_feature_generation_candidate_using_redesigned_labels_review_package_v1 is review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1
    assert services.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1 is review_service.validate_feature_generation_candidate_using_redesigned_labels_review_package_v1
    assert services.write_feature_generation_candidate_using_redesigned_labels_review_package_v1 is review_service.write_feature_generation_candidate_using_redesigned_labels_review_package_v1
    assert services.build_feature_generation_candidate_using_redesigned_labels_review_markdown_v1 is review_service.build_feature_generation_candidate_using_redesigned_labels_review_markdown_v1
