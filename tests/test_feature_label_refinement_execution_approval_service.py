from __future__ import annotations

from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import feature_label_refinement_execution_approval_service as approval


def _attestation(**overrides) -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-15T12:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
        **approval._expected_digest_confirmations(),
        **{
            name: True
            for name in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
        },
    }
    kwargs.update(overrides)
    return approval.build_feature_label_refinement_execution_approval_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def source_review() -> dict:
    return approval.review_service.build_feature_label_refinement_execution_candidate_review_package_v1()


def _build(source_review: dict, attestation: dict | None = None) -> dict:
    return approval.build_feature_label_refinement_execution_approved_v1(
        feature_label_refinement_execution_candidate_review_package=deepcopy(
            source_review
        ),
        operator_attestation=_attestation() if attestation is None else attestation,
    )


def _validate(approved: dict, source_review: dict) -> dict:
    with patch.object(approval, "_source_review", return_value=deepcopy(source_review)):
        return approval.validate_feature_label_refinement_execution_approved_v1(
            approved
        )


@pytest.fixture(scope="module")
def approved(source_review: dict) -> dict:
    return _build(source_review)


def test_attestation_builder_creates_exact_required_fields() -> None:
    attestation = _attestation()
    assert attestation["operator_decision"] == (
        approval.OPERATOR_DECISION_APPROVE_FEATURE_LABEL_REFINEMENT_EXECUTION
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1
    )
    assert attestation["operator_attestation_phrase"] == (
        "APPROVE FEATURE LABEL REFINEMENT EXECUTION MSFT NVDA AMZN GOOGL META "
        "TSLA JPM XOM JNJ WMT CAT LMT "
        "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY"
    )
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline_without_network(
    source_review: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _build(source_review)
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


def test_default_source_review_builder_path_is_supported(source_review: dict) -> None:
    validation = {
        "feature_label_refinement_execution_candidate_review_package_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        )
    }
    with (
        patch.object(
            approval.review_service,
            "build_feature_label_refinement_execution_candidate_review_package_v1",
            return_value=deepcopy(source_review),
        ),
        patch.object(
            approval.review_service,
            "validate_feature_label_refinement_execution_candidate_review_package_v1",
            return_value=validation,
        ),
    ):
        artifact = approval.build_feature_label_refinement_execution_approved_v1(
            operator_attestation=_attestation()
        )
    assert artifact["feature_label_refinement_execution_approved"] is True


def test_artifact_schema_status_scope_and_authority(approved: dict) -> None:
    assert approved["artifact_kind"] == (
        approval.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED
    )
    assert approved["schema_version"] == (
        approval.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_V1
    )
    assert approved["approval_status"] == (
        approval.FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED
    )
    assert approved["approval_scope"] == (
        approval.FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_ONLY
    )
    assert approved["feature_label_refinement_execution_objective"] == (
        "EXECUTE_FEATURE_LABEL_REFINEMENT_FOR_APPROVED_PLAN"
    )
    assert approved["feature_label_refinement_execution_mode"] == (
        approval.AUTHORIZED_NOT_EXECUTED
    )
    assert approved["feature_label_refinement_execution_authority_status"] == (
        approval.AUTHORIZED_FOR_FUTURE_REFINEMENT_EXECUTION_ONLY
    )


@pytest.mark.parametrize(
    "field",
    [
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "ready_for_feature_label_refinement_execution",
        "refined_label_generation_authorized",
        "refined_feature_generation_authorized",
        "refined_walk_forward_validation_authorized",
        "refined_out_of_sample_evaluation_authorized",
        "refined_metrics_recomputation_authorized",
        "model_comparison_authorized",
        "refinement_execution_authorized_by_this_artifact",
        "label_generation_authorized_by_this_artifact",
        "feature_generation_authorized_by_this_artifact",
        "walk_forward_validation_authorized_by_this_artifact",
        "out_of_sample_evaluation_authorized_by_this_artifact",
        "metrics_recomputation_authorized_by_this_artifact",
        "model_comparison_authorized_by_this_artifact",
    ],
)
def test_only_future_refinement_execution_capabilities_are_authorized(
    approved: dict, field: str
) -> None:
    assert approved[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "refined_label_generation_performed",
        "refined_feature_generation_performed",
        "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_performed",
        "model_comparison_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_execution_results_and_downstream_authorities_remain_false(
    approved: dict, field: str
) -> None:
    assert approved[field] is False


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_label_refinement_execution_candidate_review_package_digest", approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_execution_candidate_digest", approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("feature_label_refinement_plan_approval_digest", approval.EXPECTED_PLAN_APPROVAL_DIGEST),
        ("feature_label_refinement_plan_candidate_review_package_digest", approval.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_plan_candidate_digest", approval.EXPECTED_PLAN_CANDIDATE_DIGEST),
        ("predictive_evidence_improvement_candidate_review_package_digest", approval.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", approval.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", approval.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", approval.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", approval.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", approval.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", approval.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_all_source_digests_are_bound(
    approved: dict, field: str, expected: str
) -> None:
    assert approved[field] == expected


def test_target_universe_and_record_counts_are_exact(approved: dict) -> None:
    assert approved["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert approved["target_universe_count"] == 12
    assert approved["per_ticker_record_counts"] == {
        ticker: (913 if ticker == "META" else 1003)
        for ticker in approval.TARGET_UNIVERSE
    }


def test_readiness_failure_basis_remains_not_ready(approved: dict) -> None:
    assert {
        key: approved["readiness_failure_basis"][key]
        for key in (
            "stability_consistency_required",
            "baseline_outperformance_consistency_required",
            "readiness_decision",
            "readiness_reason",
        )
    } == {
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
    }


@pytest.mark.parametrize(
    "field,id_field,expected_ids",
    [
        ("approved_execution_steps", "step_id", approval.review_service.candidate_service.PLANNED_EXECUTION_STEP_IDS),
        ("approved_label_refinement_execution_groups", "group_id", approval.review_service.candidate_service.LABEL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("approved_feature_refinement_execution_groups", "group_id", approval.review_service.candidate_service.FEATURE_REFINEMENT_EXECUTION_GROUP_IDS),
        ("approved_protocol_refinement_execution_groups", "group_id", approval.review_service.candidate_service.PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("approved_model_comparison_execution_groups", "group_id", approval.review_service.candidate_service.MODEL_COMPARISON_EXECUTION_GROUP_IDS),
    ],
)
def test_steps_and_groups_are_authorized_not_executed(
    approved: dict, field: str, id_field: str, expected_ids: list[str]
) -> None:
    rows = approved[field]
    assert [row[id_field] for row in rows] == expected_ids
    assert all(row["authorization_status"] == approval.AUTHORIZED_NOT_EXECUTED for row in rows)
    assert all(row["execution_status"] == approval.NOT_EXECUTED for row in rows)
    assert all(row["research_only"] is True for row in rows)
    assert all(row["non_actionable"] is True for row in rows)


def test_future_outputs_are_authorized_not_generated(approved: dict) -> None:
    outputs = approved["future_execution_outputs"]
    assert len(outputs) == 12
    assert all(row["generation_status"] == approval.AUTHORIZED_NOT_GENERATED for row in outputs)
    assert all(row["actionability_label"] == approval.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)


def test_per_ticker_approvals_preserve_counts_boundaries_and_digests(
    approved: dict,
) -> None:
    entries = approved["per_ticker_feature_label_refinement_execution_approvals"]
    assert [row["ticker"] for row in entries] == approval.TARGET_UNIVERSE
    assert len({row["per_ticker_feature_label_refinement_execution_approval_digest"] for row in entries}) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["readiness_status"] == "NOT_READY"
        assert row["feature_label_refinement_execution_authorized"] is True
        assert row["feature_label_refinement_executed"] is False
        assert row["predictive_usefulness"] == approval.NOT_ACCEPTED
        assert row["profitability"] == approval.NOT_ACCEPTED
        assert row["runtime_use"] == approval.NOT_AUTHORIZED
        assert row["per_ticker_feature_label_refinement_execution_approval_digest"] == (
            approval.per_ticker_feature_label_refinement_execution_approval_digest_v1(row)
        )


def test_checklist_summary_and_digest_are_complete(
    approved: dict, source_review: dict
) -> None:
    assert [row["check_id"] for row in approved["approval_checklist"]] == approval.REQUIRED_CHECK_IDS
    assert all(row["status"] == approval.PASS for row in approved["approval_checklist"])
    assert approved["approval_summary"]["total_checks"] == 89
    assert approved["approval_summary"]["passed_checks"] == 89
    assert approved["approval_summary"]["failed_checks"] == 0
    assert approved["approval_summary"]["blocker_count"] == 0
    assert approved["feature_label_refinement_execution_approval_digest"] == (
        approval.feature_label_refinement_execution_approval_digest_v1(approved)
    )
    assert _validate(deepcopy(approved), source_review)["status"] == (
        approval.FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_VALID
    )


def test_artifact_is_deterministic(source_review: dict) -> None:
    first = _build(source_review)
    second = _build(source_review)
    assert canonical_json_bytes(first) == canonical_json_bytes(second)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("operator_decision", "REJECT"),
        ("operator_attestation_phrase", "APPROVE"),
        ("operator_attestation_version", "wrong"),
        ("operator_confirms_target_universe", ["MSFT"]),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_readiness_reason", "READY"),
        ("operator_confirms_feature_label_refinement_execution_candidate_review_digest", "0" * 64),
        ("operator_confirms_feature_label_refinement_execution_candidate_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
    ],
)
def test_attestation_mismatch_fails_closed(
    source_review: dict, field: str, bad_value
) -> None:
    attestation = _attestation()
    attestation[field] = bad_value
    with pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError):
        _build(source_review, attestation)


@pytest.mark.parametrize(
    "field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_every_required_operator_confirmation_fails_closed_when_false(
    source_review: dict, field: str
) -> None:
    attestation = _attestation()
    attestation[field] = False
    with pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError):
        _build(source_review, attestation)


@pytest.mark.parametrize("field", ["operator_reference", "operator_attestation_timestamp_utc"])
def test_operator_identity_and_timestamp_are_required(
    source_review: dict, field: str
) -> None:
    attestation = _attestation()
    attestation[field] = " "
    with pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError):
        _build(source_review, attestation)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("feature_label_refinement_execution_approved", False),
        ("feature_label_refinement_execution_authorized", False),
        ("ready_for_feature_label_refinement_execution", False),
        ("feature_label_refinement_executed", True),
        ("feature_label_refinement_results_created", True),
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
def test_artifact_boundary_mutation_fails_validation(
    approved: dict, source_review: dict, field: str, bad_value
) -> None:
    mutated = deepcopy(approved)
    mutated[field] = bad_value
    with pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError):
        _validate(mutated, source_review)


def test_forbidden_artifact_label_fails_validation(
    approved: dict, source_review: dict
) -> None:
    mutated = deepcopy(approved)
    mutated["injected"] = "FEATURE_LABEL_REFINEMENT_EXECUTED"
    with pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError):
        _validate(mutated, source_review)


def test_markdown_records_approval_and_non_authority(approved: dict) -> None:
    markdown = approval.build_feature_label_refinement_execution_approved_markdown_v1(
        approved
    )
    assert "FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVED" in markdown
    assert "AUTHORIZED_NOT_EXECUTED" in markdown
    assert "not accepted" in markdown
    assert "89/89" in markdown
    assert approved["feature_label_refinement_execution_approval_digest"] in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path, source_review: dict
) -> None:
    with patch.object(approval, "_source_review", return_value=deepcopy(source_review)):
        receipt = approval.write_feature_label_refinement_execution_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )
    path = tmp_path / receipt["filename"]
    payload = path.read_bytes()
    parsed = json.loads(payload)
    assert payload == canonical_json_bytes(parsed)
    assert receipt["payload_sha256"] == sha256_bytes(payload)
    with (
        patch.object(approval, "_source_review", return_value=deepcopy(source_review)),
        pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError),
    ):
        approval.write_feature_label_refinement_execution_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )


@pytest.mark.parametrize("filename", ["../approval.json", "approval.txt"])
def test_writer_rejects_unsafe_filename(
    tmp_path, source_review: dict, filename: str
) -> None:
    with (
        patch.object(approval, "_source_review", return_value=deepcopy(source_review)),
        pytest.raises(approval.FeatureLabelRefinementExecutionApprovalError),
    ):
        approval.write_feature_label_refinement_execution_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
            filename=filename,
        )
