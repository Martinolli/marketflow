from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import additional_predictive_evidence_execution_approval_service as approval


def _attestation_kwargs(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-15T00:00:00Z",
        "operator_attestation_phrase": (
            approval.REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ATTESTATION_PHRASE
        ),
        "operator_confirms_execution_candidate_review_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_execution_candidate_digest": (
            approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
        ),
        "operator_confirms_chain_candidate_review_digest": (
            approval.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_confirms_research_registry_approval_digest": (
            approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        "operator_confirms_canonical_dataset_freeze_digest": (
            approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST
        ),
        "operator_confirms_canonical_dataset_generation_digest": (
            approval.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
        ),
        "operator_confirms_records_digest": approval.EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": list(approval.TARGET_UNIVERSE),
        "operator_confirms_target_count": 12,
        "operator_confirms_dataset_name": approval.APPROVED_REGISTRY_METADATA[
            "dataset_name"
        ],
        "operator_confirms_total_canonical_record_count": 11946,
        **{field: True for field in approval.BOOLEAN_CONFIRMATION_FIELDS},
    }
    values.update(overrides)
    return values


def _attestation(**overrides) -> dict:
    return approval.build_additional_predictive_evidence_execution_approval_attestation_v1(
        **_attestation_kwargs(**overrides)
    )


def _approved() -> dict:
    return approval.build_additional_predictive_evidence_execution_approved_v1(
        operator_attestation=_attestation()
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert set(approval.DIGEST_CONFIRMATION_EXPECTATIONS) <= set(attestation)
    assert set(approval.BOOLEAN_CONFIRMATION_FIELDS) <= set(attestation)
    assert (
        attestation["operator_decision"]
        == approval.OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION
    )
    assert (
        attestation["operator_attestation_phrase"]
        == approval.REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"


def test_approval_artifact_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
):
    from marketflow.services import acquisition_generation_service as acquisition

    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False
    assert artifact["live_provider_transport_enabled_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "artifact_kind",
            approval.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED,
        ),
        ("approval_status", approval.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED),
        (
            "approval_scope",
            approval.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY,
        ),
        ("additional_predictive_evidence_execution_approved", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("ready_for_additional_predictive_evidence_execution", True),
        ("additional_predictive_evidence_executed", False),
        ("additional_predictive_evidence_results_created", False),
        ("label_generation_authorized", True),
        ("label_generation_performed", False),
        ("feature_matrix_generation_authorized", True),
        ("feature_matrix_generation_performed", False),
        ("walk_forward_validation_authorized", True),
        ("walk_forward_validation_performed", False),
        ("out_of_sample_evaluation_authorized", True),
        ("out_of_sample_evaluation_performed", False),
        ("baseline_comparison_authorized", True),
        ("baseline_comparison_performed", False),
        ("signal_quality_metrics_authorized", True),
        ("signal_quality_metrics_performed", False),
        ("stability_analysis_authorized", True),
        ("stability_analysis_performed", False),
        ("leakage_control_review_authorized", True),
        ("leakage_control_review_performed", False),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", False),
        ("predictive_usefulness", approval.NOT_ACCEPTED),
        ("profitability", approval.NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", approval.NOT_AUTHORIZED),
        ("strategy_use", approval.NOT_AUTHORIZED),
        ("paper_trading", approval.NOT_AUTHORIZED),
        ("broker_execution", approval.NOT_AUTHORIZED),
        ("automatic_stitching", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
    ],
)
def test_approval_and_closed_boundary_fields(field: str, expected):
    assert _approved()[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "additional_predictive_evidence_execution_candidate_review_package_digest",
            approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        ),
        (
            "additional_predictive_evidence_execution_candidate_digest",
            approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        ),
        (
            "additional_predictive_evidence_chain_candidate_review_package_digest",
            approval.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        ),
        (
            "additional_predictive_evidence_chain_candidate_digest",
            approval.EXPECTED_CHAIN_CANDIDATE_DIGEST,
        ),
        (
            "research_registry_approval_digest",
            approval.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        ),
        (
            "canonical_dataset_freeze_digest",
            approval.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        ),
        (
            "canonical_dataset_generation_digest",
            approval.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        ),
        ("records_digest", approval.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_digests_are_bound(field: str, expected: str):
    assert _approved()[field] == expected


def test_target_universe_and_registry_metadata_are_exact():
    artifact = _approved()

    assert artifact["target_universe"] == approval.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["registry_approved_dataset_metadata"] == approval.APPROVED_REGISTRY_METADATA
    assert artifact["total_canonical_record_count"] == 11946
    assert artifact["records_digest"] == approval.EXPECTED_RECORDS_DIGEST


def test_per_ticker_entries_preserve_meta_limitation_and_closed_execution_state():
    entries = _approved()["approved_per_ticker_execution_entries"]

    assert [entry["ticker"] for entry in entries] == approval.TARGET_UNIVERSE
    assert len(entries) == 12
    for entry in entries:
        expected_count = 913 if entry["ticker"] == "META" else 1003
        assert entry["historical_record_count"] == expected_count
        assert entry["meta_reduced_record_count_flag"] is (entry["ticker"] == "META")
        assert entry["additional_predictive_evidence_execution_authorized"] is True
        assert entry["additional_predictive_evidence_executed"] is False
        assert entry["predictive_usefulness"] == approval.NOT_ACCEPTED
        assert entry["runtime_use"] == approval.NOT_AUTHORIZED
        assert len(
            entry["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        ) == 64


def test_approved_sets_and_outputs_have_exact_counts_and_non_performed_states():
    artifact = _approved()

    assert len(artifact["approved_label_set"]) == 7
    assert len(artifact["approved_feature_set"]) == 10
    assert len(artifact["approved_execution_protocol"]) == 9
    assert len(artifact["approved_metric_families"]) == 9
    assert len(artifact["approved_baselines"]) == 6
    assert len(artifact["future_execution_outputs"]) == 15
    assert all(item["label_generation_performed"] is False for item in artifact["approved_label_set"])
    assert all(item["feature_matrix_generation_performed"] is False for item in artifact["approved_feature_set"])
    assert all(item["performed"] is False for item in artifact["approved_metric_families"])
    assert all(item["performed"] is False for item in artifact["approved_baselines"])
    assert all(item["generated"] is False for item in artifact["future_execution_outputs"])
    assert all(
        item["generation_status"] == approval.AUTHORIZED_NOT_GENERATED
        for item in artifact["future_execution_outputs"]
    )


def test_approved_split_profile_is_future_only():
    artifact = _approved()

    assert artifact["approved_split_profile"] == approval.APPROVED_SPLIT_PROFILE
    assert artifact["walk_forward_validation_authorized"] is True
    assert artifact["walk_forward_validation_performed"] is False
    assert artifact["out_of_sample_evaluation_performed"] is False


def test_approval_checklist_has_required_shape_and_all_checks_pass():
    artifact = _approved()

    assert [item["check_id"] for item in artifact["approval_checklist"]] == (
        approval.REQUIRED_APPROVAL_CHECK_IDS
    )
    assert {tuple(item) for item in artifact["approval_checklist"]} == {
        ("check_id", "status", "expected", "actual", "severity", "message")
    }
    assert {item["status"] for item in artifact["approval_checklist"]} == {approval.PASS}


def test_approval_summary_has_zero_failures_and_closed_downstream_authority():
    summary = _approved()["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["additional_predictive_evidence_execution_approved_by_operator"] is True
    assert summary["additional_predictive_evidence_execution_authorized"] is True
    assert summary["additional_predictive_evidence_executed"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_decision", "REJECT", "operator_decision_approved"),
        ("operator_attestation_phrase", "APPROVE", "operator_attestation_phrase_matches"),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE)), "operator_confirms_target_universe"),
        ("operator_confirms_target_count", 11, "operator_confirms_target_count"),
        ("operator_confirms_dataset_name", "wrong", "operator_confirms_dataset_name"),
        ("operator_confirms_total_canonical_record_count", 11945, "operator_confirms_total_canonical_record_count_11946"),
        ("operator_confirms_execution_candidate_review_digest", "0" * 64, "operator_confirms_execution_candidate_review_digest"),
        ("operator_confirms_execution_candidate_digest", "0" * 64, "operator_confirms_execution_candidate_digest"),
        ("operator_confirms_chain_candidate_review_digest", "0" * 64, "operator_confirms_chain_candidate_review_digest"),
        ("operator_confirms_research_registry_approval_digest", "0" * 64, "operator_confirms_research_registry_approval_digest"),
        ("operator_confirms_canonical_dataset_freeze_digest", "0" * 64, "operator_confirms_canonical_dataset_freeze_digest"),
        ("operator_confirms_canonical_dataset_generation_digest", "0" * 64, "operator_confirms_canonical_dataset_generation_digest"),
        ("operator_confirms_records_digest", "0" * 64, "operator_confirms_records_digest"),
        ("operator_confirms_meta_reduced_record_count_preserved", False, "operator_confirms_meta_reduced_record_count_preserved"),
        ("operator_confirms_approval_scope_execution_only", False, "operator_confirms_approval_scope_execution_only"),
        ("operator_confirms_execution_authorized", False, "operator_confirms_execution_authorized"),
        ("operator_confirms_label_generation_authorized", False, "operator_confirms_label_generation_authorized"),
        ("operator_confirms_feature_matrix_generation_authorized", False, "operator_confirms_feature_matrix_generation_authorized"),
        ("operator_confirms_walk_forward_validation_authorized", False, "operator_confirms_walk_forward_validation_authorized"),
        ("operator_confirms_out_of_sample_evaluation_authorized", False, "operator_confirms_out_of_sample_evaluation_authorized"),
        ("operator_confirms_baseline_comparison_authorized", False, "operator_confirms_baseline_comparison_authorized"),
        ("operator_confirms_signal_quality_metrics_authorized", False, "operator_confirms_signal_quality_metrics_authorized"),
        ("operator_confirms_stability_analysis_authorized", False, "operator_confirms_stability_analysis_authorized"),
        ("operator_confirms_leakage_control_review_authorized", False, "operator_confirms_leakage_control_review_authorized"),
        ("operator_confirms_predictive_experiment_rerun_authorized", False, "operator_confirms_predictive_experiment_rerun_authorized"),
        ("operator_confirms_no_execution_performed", False, "operator_confirms_no_execution_performed"),
        ("operator_confirms_no_results_created", False, "operator_confirms_no_results_created"),
        ("operator_confirms_no_label_generation_performed", False, "operator_confirms_no_label_generation_performed"),
        ("operator_confirms_no_feature_matrix_generation_performed", False, "operator_confirms_no_feature_matrix_generation_performed"),
        ("operator_confirms_no_walk_forward_validation_performed", False, "operator_confirms_no_walk_forward_validation_performed"),
        ("operator_confirms_no_out_of_sample_evaluation_performed", False, "operator_confirms_no_out_of_sample_evaluation_performed"),
        ("operator_confirms_no_predictive_usefulness_acceptance", False, "operator_confirms_no_predictive_usefulness_acceptance"),
        ("operator_confirms_no_profitability_acceptance", False, "operator_confirms_no_profitability_acceptance"),
        ("operator_confirms_no_runtime_migration_approval", False, "operator_confirms_no_runtime_migration_approval"),
        ("operator_confirms_no_runtime_activation", False, "operator_confirms_no_runtime_activation"),
        ("operator_confirms_no_strategy_authorization", False, "operator_confirms_no_strategy_authorization"),
        ("operator_confirms_no_paper_trading", False, "operator_confirms_no_paper_trading"),
        ("operator_confirms_no_broker_execution", False, "operator_confirms_no_broker_execution"),
        ("operator_confirms_no_trade_recommendations", False, "operator_confirms_no_trade_recommendations"),
        ("operator_confirms_no_api_key_storage_or_printing", False, "operator_confirms_no_api_key_storage_or_printing"),
        ("operator_confirms_no_raw_payload_commit", False, "operator_confirms_no_raw_payload_commit"),
    ],
)
def test_builder_rejects_wrong_or_missing_operator_confirmations(
    field: str, value, match: str
):
    with pytest.raises(
        approval.AdditionalPredictiveEvidenceExecutionApprovalError, match=match
    ):
        approval.build_additional_predictive_evidence_execution_approved_v1(
            operator_attestation=_attestation(**{field: value})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("additional_predictive_evidence_execution_approved", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("ready_for_additional_predictive_evidence_execution", False),
        ("additional_predictive_evidence_executed", True),
        ("additional_predictive_evidence_results_created", True),
        ("label_generation_authorized", False),
        ("feature_matrix_generation_authorized", False),
        ("walk_forward_validation_authorized", False),
        ("out_of_sample_evaluation_authorized", False),
        ("baseline_comparison_authorized", False),
        ("signal_quality_metrics_authorized", False),
        ("stability_analysis_authorized", False),
        ("leakage_control_review_authorized", False),
        ("predictive_experiment_rerun_authorized", False),
        ("label_generation_performed", True),
        ("feature_matrix_generation_performed", True),
        ("walk_forward_validation_performed", True),
        ("out_of_sample_evaluation_performed", True),
        ("baseline_comparison_performed", True),
        ("signal_quality_metrics_performed", True),
        ("stability_analysis_performed", True),
        ("leakage_control_review_performed", True),
        ("predictive_experiment_rerun_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("canonical_dataset_regenerated_in_approval", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("target_universe_count", 11),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
    ],
)
def test_validator_rejects_invalid_approval_mutations(field: str, value):
    artifact = _approved()
    artifact[field] = value

    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)


def test_validator_rejects_wrong_universe_and_record_counts():
    artifact = _approved()
    artifact["target_universe"] = list(reversed(artifact["target_universe"]))
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)

    artifact = _approved()
    artifact["approved_per_ticker_execution_entries"][4]["historical_record_count"] = 1003
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)

    artifact = _approved()
    artifact["approved_per_ticker_execution_entries"][0]["historical_record_count"] = 1002
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)


def test_validator_rejects_missing_or_wrong_operator_attestation():
    artifact = _approved()
    artifact.pop("operator_attestation")
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)

    artifact = _approved()
    artifact["operator_attestation"]["operator_decision"] = "REJECT"
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)


def test_builder_rejects_mutated_source_review_package():
    source = (
        approval.candidate_review.build_additional_predictive_evidence_execution_candidate_review_package_v1()
    )
    source["additional_predictive_evidence_execution_candidate_digest"] = "0" * 64

    with pytest.raises(
        approval.AdditionalPredictiveEvidenceExecutionApprovalError,
        match="source execution candidate review package invalid",
    ):
        approval.build_additional_predictive_evidence_execution_approved_v1(
            execution_candidate_review_package=source,
            operator_attestation=_attestation(),
        )


def test_approval_and_per_ticker_digests_are_deterministic():
    first = _approved()
    second = _approved()

    assert (
        first["additional_predictive_evidence_execution_approval_digest"]
        == second["additional_predictive_evidence_execution_approval_digest"]
    )
    assert [
        entry["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        for entry in first["approved_per_ticker_execution_entries"]
    ] == [
        entry["per_ticker_additional_predictive_evidence_execution_approval_digest"]
        for entry in second["approved_per_ticker_execution_entries"]
    ]


def test_validator_rejects_missing_or_stale_approval_digest():
    artifact = _approved()
    artifact.pop("additional_predictive_evidence_execution_approval_digest")
    with pytest.raises(
        approval.AdditionalPredictiveEvidenceExecutionApprovalError, match="digest missing"
    ):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)

    artifact = _approved()
    artifact["additional_predictive_evidence_execution_approval_digest"] = "0" * 64
    with pytest.raises(approval.AdditionalPredictiveEvidenceExecutionApprovalError):
        approval.validate_additional_predictive_evidence_execution_approved_v1(artifact)


def test_markdown_includes_required_sections_and_boundaries():
    markdown = approval.build_additional_predictive_evidence_execution_approved_markdown_v1(
        _approved()
    )

    for heading in (
        "## Title",
        "## Approved Additional Predictive Evidence Execution",
        "## Operator Attestation",
        "## Source Execution Candidate Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Approved Per-Ticker Execution Summary",
        "## Approved Label Set",
        "## Approved Feature Set",
        "## Approved Execution Protocol",
        "## Approved Metrics and Baselines",
        "## Future Execution Outputs",
        "## Execution Boundary",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Approval Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown
    assert "No provider request" in markdown
    assert "performs no execution" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(tmp_path: Path):
    result = approval.write_additional_predictive_evidence_execution_approved_v1(
        tmp_path, operator_attestation=_attestation()
    )
    path = Path(result["path"])

    assert path.name == "additional_predictive_evidence_execution_approved_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert approval.validate_additional_predictive_evidence_execution_approved_v1(payload)[
        "blocker_count"
    ] == 0
    assert result["payload_byte_size"] == path.stat().st_size
    assert len(result["payload_sha256"]) == 64
    with pytest.raises(
        approval.AdditionalPredictiveEvidenceExecutionApprovalError,
        match="already exists",
    ):
        approval.write_additional_predictive_evidence_execution_approved_v1(
            tmp_path, operator_attestation=_attestation()
        )


@pytest.mark.parametrize("filename", ["../escape.json", "approval.txt"])
def test_writer_rejects_unsafe_or_non_json_filenames(tmp_path: Path, filename: str):
    with pytest.raises(
        approval.AdditionalPredictiveEvidenceExecutionApprovalError,
        match="simple JSON filename",
    ):
        approval.write_additional_predictive_evidence_execution_approved_v1(
            tmp_path,
            operator_attestation=_attestation(),
            filename=filename,
        )


def test_approval_service_exports_are_public():
    import marketflow.services as services

    for name in (
        "ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY",
        "REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ATTESTATION_PHRASE",
        "build_additional_predictive_evidence_execution_approval_attestation_v1",
        "build_additional_predictive_evidence_execution_approved_v1",
        "validate_additional_predictive_evidence_execution_approved_v1",
        "write_additional_predictive_evidence_execution_approved_v1",
        "build_additional_predictive_evidence_execution_approved_markdown_v1",
        "additional_predictive_evidence_execution_approval_digest_v1",
        "per_ticker_additional_predictive_evidence_execution_approval_digest_v1",
    ):
        assert name in services.__all__
        assert hasattr(services, name)
