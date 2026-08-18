from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_generation_approval_redesigned_labels_service as approval_service


def build_attestation(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-18T16:00:00Z",
        "operator_attestation_phrase": approval_service.REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        "operator_confirms_feature_generation_candidate_review_digest": approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_feature_generation_candidate_digest": approval_service.EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_feature_predictive_evidence_planning_approval_digest": approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST,
        "operator_confirms_redesigned_label_results_review_digest": approval_service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_redesigned_label_execution_digest": approval_service.EXPECTED_EXECUTION_DIGEST,
        "operator_confirms_redesigned_label_approval_digest": approval_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "operator_confirms_research_registry_approval_digest": approval_service.EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "operator_confirms_records_digest": approval_service.EXPECTED_RECORDS_DIGEST,
        "operator_confirms_label_values_digest": approval_service.EXPECTED_LABEL_VALUES_DIGEST,
        "operator_confirms_target_universe": approval_service.TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_feature_generation_approval_scope_only": True,
        "operator_confirms_feature_generation_authorized": True,
        "operator_confirms_ready_for_feature_generation_execution_using_redesigned_labels": True,
        "operator_confirms_no_feature_generation_performed": True,
        "operator_confirms_no_feature_values_created": True,
        "operator_confirms_no_predictive_evidence_execution_candidate": True,
        "operator_confirms_no_predictive_evidence_execution": True,
        "operator_confirms_no_metric_recomputation": True,
        "operator_confirms_no_model_training": True,
        "operator_confirms_no_predictive_usefulness_acceptance": True,
        "operator_confirms_no_profitability_acceptance": True,
        "operator_confirms_no_runtime_migration_approval": True,
        "operator_confirms_no_strategy_authorization": True,
        "operator_confirms_no_paper_trading": True,
        "operator_confirms_no_broker_execution": True,
        "operator_confirms_no_trade_recommendations": True,
        "operator_confirms_no_api_key_storage_or_printing": True,
        "operator_confirms_no_raw_payload_commit": True,
    }
    values.update(overrides)
    return approval_service.build_feature_generation_approval_using_redesigned_labels_attestation_v1(**values)


@pytest.fixture(scope="module")
def attestation() -> dict:
    return build_attestation()


@pytest.fixture(scope="module")
def approval(attestation) -> dict:
    return approval_service.build_feature_generation_approved_using_redesigned_labels_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation) -> None:
    assert attestation["operator_decision"] == "APPROVE_FEATURE_GENERATION_USING_REDESIGNED_LABELS"
    assert attestation["operator_attestation_version"] == "feature_generation_approval_using_redesigned_labels_operator_attestation_v1"
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approval_builds_offline(monkeypatch: pytest.MonkeyPatch, attestation) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = approval_service.build_feature_generation_approved_using_redesigned_labels_v1(
        operator_attestation=attestation
    )
    assert result["created_offline"] is True
    assert result["provider_requests_made"] is False
    assert result["market_data_acquisition_performed"] is False


def test_approval_accepts_explicit_review_package(attestation) -> None:
    review = approval_service.review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1()
    result = approval_service.build_feature_generation_approved_using_redesigned_labels_v1(
        candidate_review_package=review,
        operator_attestation=attestation,
    )
    assert result["feature_generation_candidate_using_redesigned_labels_review_package_digest"] == approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_artifact_status_and_scope_are_correct(approval) -> None:
    assert approval["artifact_kind"] == "FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS"
    assert approval["approval_status"] == "FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS"
    assert approval["approval_scope"] == "FEATURE_GENERATION_APPROVAL_ONLY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_generation_candidate_using_redesigned_labels_review_package_digest", approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_digest", approval_service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest", approval_service.EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST),
        ("feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest", approval_service.EXPECTED_PLANNING_CANDIDATE_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", approval_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("redesigned_label_generation_execution_digest", approval_service.EXPECTED_EXECUTION_DIGEST),
        ("redesigned_label_generation_approval_digest", approval_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST),
        ("label_values_digest", approval_service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", approval_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", approval_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_digest_is_bound(approval, field: str, expected: str) -> None:
    assert approval[field] == expected


def test_universe_and_meta_are_preserved(approval) -> None:
    assert approval["target_universe_count"] == 12
    assert approval["target_universe"] == approval_service.TARGET_UNIVERSE
    assert approval["meta_record_count"] == 913
    assert approval["per_ticker_record_counts"]["META"] == 913
    assert approval["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_approved",
        "feature_generation_approval_created",
        "feature_generation_authorized",
        "redesigned_feature_generation_authorized",
        "ready_for_feature_generation_execution_using_redesigned_labels",
    ],
)
def test_feature_generation_approval_flag_is_true(approval, field: str) -> None:
    assert approval[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_generation_performed",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "feature_generation_execution_created",
    ],
)
def test_downstream_action_remains_false(approval, field: str) -> None:
    assert approval[field] is False


def test_predictive_usefulness_and_profitability_are_not_accepted(approval) -> None:
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_remain_not_authorized(approval, field: str) -> None:
    assert approval[field] == "NOT_AUTHORIZED"


def test_approved_source_inputs_count_is_ten(approval) -> None:
    rows = approval["approved_source_inputs"]
    assert [row["source_input_id"] for row in rows] == approval_service.review_service.candidate_service.SOURCE_INPUT_IDS
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY" for row in rows)
    assert all(row["generation_status"] == "NOT_REGENERATED" for row in rows)


def test_approved_feature_families_count_is_ten(approval) -> None:
    rows = approval["approved_feature_families"]
    assert [row["feature_family_id"] for row in rows] == approval_service.review_service.candidate_service.PLANNED_FEATURE_FAMILY_IDS
    assert len(rows) == 10
    assert all(row["feature_generation_authorized"] is True for row in rows)
    assert all(row["feature_generation_performed"] is False for row in rows)


def test_approved_feature_groups_count_is_seventeen(approval) -> None:
    rows = approval["approved_feature_groups"]
    assert [row["feature_group_id"] for row in rows] == approval_service.review_service.candidate_service.PLANNED_FEATURE_GROUP_IDS
    assert len(rows) == 17
    assert all(row["feature_generation_authorized"] is True for row in rows)
    assert all(row["feature_values_created"] is False for row in rows)


def test_approved_schema_fields_count_is_sixteen(approval) -> None:
    contract = approval["approved_feature_schema_contract"]
    assert contract["feature_schema_contract_status"] == "APPROVED_FOR_FUTURE_FEATURE_GENERATION_ONLY"
    assert contract["approved_schema_fields"] == approval_service.review_service.candidate_service.FEATURE_SCHEMA_FIELDS
    assert len(contract["approved_schema_fields"]) == 16
    assert contract["feature_values_created"] is False


def test_approved_alignment_controls_count_is_ten(approval) -> None:
    rows = approval["approved_feature_label_alignment_controls"]
    assert [row["control_id"] for row in rows] == approval_service.review_service.candidate_service.ALIGNMENT_CONTROL_IDS
    assert len(rows) == 10
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_approved_quality_checks_count_is_ten(approval) -> None:
    rows = approval["approved_feature_quality_checks"]
    assert [row["quality_check_id"] for row in rows] == approval_service.review_service.candidate_service.PLANNED_QUALITY_CHECK_IDS
    assert len(rows) == 10
    assert all(row["planned_check_status"] == "NOT_EXECUTED" for row in rows)


def test_per_ticker_approval_entries_count_is_twelve(approval) -> None:
    entries = approval["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == approval_service.TARGET_UNIVERSE
    assert all(row["feature_generation_authorized"] is True for row in entries)
    assert all(row["feature_generation_performed"] is False for row in entries)


def test_per_ticker_approval_digests_are_present(approval) -> None:
    for entry in approval["per_ticker_approval_entries"]:
        digest = entry["per_ticker_feature_generation_approval_digest"]
        assert len(digest) == 64
        assert digest == approval_service.per_ticker_feature_generation_approval_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(approval) -> None:
    meta = next(row for row in approval["per_ticker_approval_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_APPROVAL"


def test_next_chain_gates_and_risk_controls_are_defined(approval) -> None:
    assert approval["next_chain"] == approval_service.NEXT_CHAIN
    assert approval["next_gates"] == approval_service.NEXT_GATES
    assert approval["risk_controls"] == approval_service.RISK_CONTROLS


def test_checklist_passes(approval) -> None:
    assert [row["check_id"] for row in approval["approval_checklist"]] == approval_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["approval_checklist"])
    assert approval["approval_summary"]["passed_checks"] == len(approval_service.REQUIRED_CHECK_IDS)
    assert approval["approval_summary"]["blocker_count"] == 0
    assert approval["approval_summary"]["feature_generation_authorized"] is True
    assert approval["approval_summary"]["feature_generation_performed"] is False


def test_approval_digest_is_deterministic(approval, attestation) -> None:
    first = approval_service.feature_generation_approval_using_redesigned_labels_digest_v1(approval)
    second_approval = approval_service.build_feature_generation_approved_using_redesigned_labels_v1(operator_attestation=deepcopy(attestation))
    assert first == second_approval["feature_generation_approval_using_redesigned_labels_digest"]
    assert first == approval["feature_generation_approval_using_redesigned_labels_digest"]


def test_per_ticker_approval_digests_are_deterministic(approval) -> None:
    for entry in approval["per_ticker_approval_entries"]:
        first = approval_service.per_ticker_feature_generation_approval_digest_v1(entry)
        second = approval_service.per_ticker_feature_generation_approval_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_approval(approval) -> None:
    validation = approval_service.validate_feature_generation_approved_using_redesigned_labels_v1(deepcopy(approval))
    assert validation["status"] == "FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS"
    assert validation["feature_generation_authorized"] is True
    assert validation["feature_generation_performed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("feature_generation_candidate_using_redesigned_labels_review_package_digest", None),
        ("feature_generation_candidate_using_redesigned_labels_digest", None),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", None),
        ("label_values_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(approval_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("feature_generation_approved", False),
        ("feature_generation_authorized", False),
        ("ready_for_feature_generation_execution_using_redesigned_labels", False),
        ("feature_generation_performed", True),
        ("feature_values_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
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
def test_validator_rejects_invalid_approval_boundary(approval, field: str, value) -> None:
    invalid = deepcopy(approval)
    invalid[field] = value
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.validate_feature_generation_approved_using_redesigned_labels_v1(invalid)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
        ("operator_confirms_feature_generation_candidate_review_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(approval_service.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
    ],
)
def test_builder_rejects_invalid_attestation(field: str, value) -> None:
    attestation = build_attestation()
    attestation[field] = value
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.build_feature_generation_approved_using_redesigned_labels_v1(operator_attestation=attestation)


@pytest.mark.parametrize("field", approval_service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)
def test_builder_rejects_missing_required_confirmation(field: str) -> None:
    attestation = build_attestation()
    attestation[field] = False
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.build_feature_generation_approved_using_redesigned_labels_v1(operator_attestation=attestation)


def test_validator_rejects_missing_risk_controls(approval) -> None:
    invalid = deepcopy(approval)
    invalid.pop("risk_controls")
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.validate_feature_generation_approved_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_approval_digest(approval) -> None:
    invalid = deepcopy(approval)
    invalid.pop("feature_generation_approval_using_redesigned_labels_digest")
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.validate_feature_generation_approved_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_per_ticker_approval_digest(approval) -> None:
    invalid = deepcopy(approval)
    invalid["per_ticker_approval_entries"][0].pop("per_ticker_feature_generation_approval_digest")
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.validate_feature_generation_approved_using_redesigned_labels_v1(invalid)


def test_builder_rejects_invalid_source_review(attestation) -> None:
    review = approval_service.review_service.build_feature_generation_candidate_using_redesigned_labels_review_package_v1()
    review["review_summary"]["blocker_count"] = 1
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.build_feature_generation_approved_using_redesigned_labels_v1(candidate_review_package=review, operator_attestation=attestation)


def test_markdown_includes_required_sections(approval) -> None:
    markdown = approval_service.build_feature_generation_approved_using_redesigned_labels_markdown_v1(approval)
    for heading in [
        "## Title",
        "## Feature Generation Approval Using Redesigned Labels",
        "## Operator Attestation",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Approved Source Inputs",
        "## Approved Feature Families",
        "## Approved Feature Groups",
        "## Approved Feature Schema Contract",
        "## Approved Feature / Label Alignment Controls",
        "## Approved Quality Checks",
        "## Per-Ticker Approval Entries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert heading in markdown


def test_writer_uses_isolated_directory_and_does_not_overwrite(tmp_path, attestation) -> None:
    receipt = approval_service.write_feature_generation_approved_using_redesigned_labels_v1(tmp_path, operator_attestation=attestation)
    output = tmp_path / receipt["filename"]
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["feature_generation_approval_using_redesigned_labels_digest"] == receipt["feature_generation_approval_using_redesigned_labels_digest"]
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.write_feature_generation_approved_using_redesigned_labels_v1(tmp_path, operator_attestation=attestation)


def test_writer_rejects_nested_filename(tmp_path, attestation) -> None:
    with pytest.raises(approval_service.FeatureGenerationApprovalRedesignedLabelsError):
        approval_service.write_feature_generation_approved_using_redesigned_labels_v1(tmp_path, operator_attestation=attestation, filename="nested/approval.json")


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS == approval_service.ARTIFACT_KIND_FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS
    assert services.FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS == approval_service.FEATURE_GENERATION_APPROVED_USING_REDESIGNED_LABELS
    assert services.FEATURE_GENERATION_APPROVAL_ONLY == approval_service.FEATURE_GENERATION_APPROVAL_ONLY
    assert services.REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE == approval_service.REQUIRED_FEATURE_GENERATION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE
    assert services.build_feature_generation_approved_using_redesigned_labels_v1 is approval_service.build_feature_generation_approved_using_redesigned_labels_v1
    assert services.validate_feature_generation_approved_using_redesigned_labels_v1 is approval_service.validate_feature_generation_approved_using_redesigned_labels_v1
    assert services.write_feature_generation_approved_using_redesigned_labels_v1 is approval_service.write_feature_generation_approved_using_redesigned_labels_v1
