from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_generation_candidate_redesigned_labels_service as candidate_service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made"] is False
    assert result["market_data_acquisition_performed"] is False


def test_artifact_kind_is_correct(candidate) -> None:
    assert candidate["artifact_kind"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS"


def test_candidate_status_is_correct(candidate) -> None:
    assert candidate["candidate_status"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", candidate_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", candidate_service.EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", candidate_service.EXPECTED_PLANNING_CANDIDATE_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", candidate_service.EXPECTED_APPROVAL_DIGEST),
        ("label_values_digest", candidate_service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", candidate_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", candidate_service.EXPECTED_RECORDS_DIGEST),
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


def test_planning_approved_is_true(candidate) -> None:
    assert candidate["feature_predictive_evidence_planning_approved"] is True
    assert candidate["feature_predictive_evidence_planning_approval_created"] is True


def test_ready_for_feature_generation_candidate_is_true(candidate) -> None:
    assert candidate["ready_for_feature_generation_candidate_using_redesigned_labels"] is True


def test_ready_for_predictive_evidence_candidate_is_false(candidate) -> None:
    assert candidate["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is False


def test_feature_generation_candidate_created_and_ready_are_true(candidate) -> None:
    assert candidate["feature_generation_candidate_created"] is True
    assert candidate["feature_generation_candidate_using_redesigned_labels_created"] is True
    assert candidate["feature_generation_candidate_using_redesigned_labels_ready_for_operator_review"] is True
    assert candidate["feature_generation_candidate_using_redesigned_labels_review_created"] is False


@pytest.mark.parametrize(
    "field",
    [
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
def test_downstream_action_remains_false(candidate, field: str) -> None:
    assert candidate[field] is False


def test_predictive_usefulness_is_not_accepted(candidate) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(candidate) -> None:
    assert candidate["profitability"] == "not accepted"


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(candidate, field: str) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_planned_feature_families_count_is_ten(candidate) -> None:
    rows = candidate["planned_feature_families"]
    assert [row["feature_family_id"] for row in rows] == candidate_service.PLANNED_FEATURE_FAMILY_IDS
    assert len(rows) == 10
    assert all(row["feature_generation_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW" for row in rows)
    assert all(row["feature_values_created"] is False for row in rows)


def test_planned_feature_groups_are_defined(candidate) -> None:
    groups = [group for family in candidate["planned_feature_families"] for group in family["planned_feature_groups"]]
    assert [row["feature_group_id"] for row in groups] == candidate_service.PLANNED_FEATURE_GROUP_IDS
    assert len(groups) == 17
    assert all(row["group_status"] == "PLANNED_NOT_GENERATED" for row in groups)
    assert all(row["feature_generation_performed"] is False for row in groups)
    assert any(row["leakage_sensitive"] is True for row in groups)


def test_feature_schema_contract_is_defined(candidate) -> None:
    contract = candidate["planned_feature_schema_contract"]
    assert contract["feature_schema_contract_status"] == "PLANNED_NOT_GENERATED"
    assert contract["planned_schema_fields"] == candidate_service.FEATURE_SCHEMA_FIELDS
    assert contract["feature_values_created"] is False


def test_alignment_controls_are_defined(candidate) -> None:
    controls = candidate["planned_feature_label_alignment_controls"]
    assert [row["control_id"] for row in controls] == candidate_service.ALIGNMENT_CONTROL_IDS
    assert all(row["control_status"] == "PLANNED_FOR_OPERATOR_REVIEW" for row in controls)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in controls)


def test_quality_checks_are_defined(candidate) -> None:
    checks = candidate["planned_feature_quality_checks"]
    assert [row["planned_check_id"] for row in checks] == candidate_service.PLANNED_QUALITY_CHECK_IDS
    assert all(row["planned_check_status"] == "PLANNED_NOT_EXECUTED" for row in checks)


def test_source_inputs_are_reviewed_not_regenerated(candidate) -> None:
    rows = candidate["source_inputs"]
    assert [row["source_input_id"] for row in rows] == candidate_service.SOURCE_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


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
        digest = entry["per_ticker_feature_generation_candidate_digest"]
        assert len(digest) == 64
        assert digest == candidate_service.per_ticker_feature_generation_candidate_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(candidate) -> None:
    meta = next(row for row in candidate["per_ticker_candidate_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_CANDIDATE"


def test_non_meta_per_ticker_counts_are_preserved(candidate) -> None:
    assert all(row["historical_record_count"] == 1003 for row in candidate["per_ticker_candidate_entries"] if row["ticker"] != "META")


def test_future_chain_is_defined(candidate) -> None:
    assert candidate["future_chain"] == candidate_service.FUTURE_CHAIN


def test_future_gates_are_defined(candidate) -> None:
    assert candidate["future_gates"] == candidate_service.FUTURE_GATES


def test_risk_controls_are_defined(candidate) -> None:
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(candidate) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == candidate_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"]["passed_checks"] == len(candidate_service.REQUIRED_CHECK_IDS)
    assert candidate["candidate_summary"]["blocker_count"] == 0
    assert candidate["candidate_summary"]["ready_for_feature_generation_approval"] is False


def test_candidate_digest_is_deterministic(candidate) -> None:
    first = candidate_service.feature_generation_candidate_using_redesigned_labels_digest_v1(candidate)
    second = candidate_service.feature_generation_candidate_using_redesigned_labels_digest_v1(deepcopy(candidate))
    assert first == second == candidate["feature_generation_candidate_using_redesigned_labels_digest"]


def test_per_ticker_digests_are_deterministic(candidate) -> None:
    for entry in candidate["per_ticker_candidate_entries"]:
        first = candidate_service.per_ticker_feature_generation_candidate_digest_v1(entry)
        second = candidate_service.per_ticker_feature_generation_candidate_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_candidate(candidate) -> None:
    validation = candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(deepcopy(candidate))
    assert validation["status"] == "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["ready_for_feature_generation_approval"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", None),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", None),
        ("redesigned_label_generation_results_review_package_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_predictive_evidence_planning_approved", False),
        ("ready_for_feature_generation_candidate_using_redesigned_labels", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", True),
        ("feature_generation_candidate_created", False),
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
def test_validator_rejects_invalid_candidate_boundary(candidate, field: str, value) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = value
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "planned_feature_families",
        "planned_feature_schema_contract",
        "planned_feature_label_alignment_controls",
        "planned_feature_quality_checks",
        "future_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_collection(candidate, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_feature_group(candidate) -> None:
    invalid = deepcopy(candidate)
    invalid["planned_feature_families"][0]["planned_feature_groups"].pop()
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_candidate_digest(candidate) -> None:
    invalid = deepcopy(candidate)
    invalid.pop("feature_generation_candidate_using_redesigned_labels_digest")
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(candidate) -> None:
    invalid = deepcopy(candidate)
    invalid["per_ticker_candidate_entries"][0].pop("per_ticker_feature_generation_candidate_digest")
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1(invalid)


def test_markdown_includes_required_sections(candidate) -> None:
    markdown = candidate_service.build_feature_generation_candidate_using_redesigned_labels_markdown_v1(candidate)
    for heading in [
        "## Title",
        "## Feature Generation Candidate Using Redesigned Labels",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Source Redesigned Label Profile",
        "## Candidate Objective",
        "## Source Inputs",
        "## Planned Feature Families",
        "## Planned Feature Groups",
        "## Planned Feature Schema Contract",
        "## Planned Feature / Label Alignment Controls",
        "## Planned Quality Checks",
        "## Per-Ticker Candidate Entries",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert heading in markdown


def test_writer_uses_isolated_directory_and_does_not_overwrite(tmp_path) -> None:
    receipt = candidate_service.write_feature_generation_candidate_using_redesigned_labels_v1(tmp_path)
    output = tmp_path / receipt["filename"]
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["feature_generation_candidate_using_redesigned_labels_digest"] == receipt["feature_generation_candidate_using_redesigned_labels_digest"]
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.write_feature_generation_candidate_using_redesigned_labels_v1(tmp_path)


def test_writer_rejects_nested_filename(tmp_path) -> None:
    with pytest.raises(candidate_service.FeatureGenerationCandidateRedesignedLabelsError):
        candidate_service.write_feature_generation_candidate_using_redesigned_labels_v1(tmp_path, filename="nested/candidate.json")


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS == candidate_service.ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS
    assert services.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW == candidate_service.FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW
    assert services.build_feature_generation_candidate_using_redesigned_labels_v1 is candidate_service.build_feature_generation_candidate_using_redesigned_labels_v1
    assert services.validate_feature_generation_candidate_using_redesigned_labels_v1 is candidate_service.validate_feature_generation_candidate_using_redesigned_labels_v1
    assert services.write_feature_generation_candidate_using_redesigned_labels_v1 is candidate_service.write_feature_generation_candidate_using_redesigned_labels_v1
    assert services.build_feature_generation_candidate_using_redesigned_labels_markdown_v1 is candidate_service.build_feature_generation_candidate_using_redesigned_labels_markdown_v1
