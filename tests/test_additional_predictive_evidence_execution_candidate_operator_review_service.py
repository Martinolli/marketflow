from __future__ import annotations

import json

import pytest

from marketflow.services import additional_predictive_evidence_execution_candidate_operator_review_service as service


def _review() -> dict:
    return service.build_additional_predictive_evidence_execution_candidate_review_package_v1()


def test_review_builds_offline_without_provider_or_upstream_replay(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("provider/upstream review path must not be called")

    monkeypatch.setattr(
        service.candidate_service.review_service,
        "build_additional_predictive_evidence_chain_candidate_review_package_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.candidate_service.chain_service.registry_approval,
        "build_research_registry_approved_v1",
        forbidden,
    )

    review = _review()

    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False


def test_review_identity_and_status_are_exact():
    review = _review()

    assert review["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE
    assert review["review_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY
    assert review["additional_predictive_evidence_execution_candidate_review_created"] is True


def test_default_and_provided_candidate_binding_modes_are_supported():
    default = _review()
    candidate = service.candidate_service.build_additional_predictive_evidence_execution_candidate_v1()
    provided = service.build_additional_predictive_evidence_execution_candidate_review_package_v1(candidate)

    assert default["execution_candidate_binding_mode"] == service.EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING
    assert provided["execution_candidate_binding_mode"] == service.EXECUTION_CANDIDATE_OBJECT_BINDING
    assert default["reviewed_additional_predictive_evidence_execution_candidate_digest"] == provided["reviewed_additional_predictive_evidence_execution_candidate_digest"]


def test_reviewed_execution_candidate_identity_and_checklist_are_bound():
    review = _review()

    assert review["reviewed_additional_predictive_evidence_execution_candidate_kind"] == service.candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE
    assert review["reviewed_additional_predictive_evidence_execution_candidate_status"] == service.candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert review["reviewed_additional_predictive_evidence_execution_candidate_digest"] == service.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    assert review["reviewed_additional_predictive_evidence_execution_candidate_checklist_total"] == 69
    assert review["reviewed_additional_predictive_evidence_execution_candidate_checklist_passed"] == 69
    assert review["reviewed_additional_predictive_evidence_execution_candidate_checklist_failed"] == 0
    assert review["reviewed_additional_predictive_evidence_execution_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_execution_candidate_digest", service.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("additional_predictive_evidence_chain_candidate_review_package_digest", service.candidate_service.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("additional_predictive_evidence_chain_candidate_digest", service.candidate_service.EXPECTED_CHAIN_CANDIDATE_DIGEST),
        ("research_registry_approval_digest", service.candidate_service.chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", service.candidate_service.chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_generation_digest", service.candidate_service.chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("records_digest", service.candidate_service.chain_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(field, expected):
    assert _review()[field] == expected


def test_registry_chain_and_candidate_review_state_are_preserved():
    review = _review()

    assert review["registry_approval_created"] is True
    assert review["research_registry_approved"] is True
    assert review["additional_predictive_evidence_chain_candidate_review_created"] is True
    assert review["additional_predictive_evidence_execution_candidate_created"] is True
    assert review["additional_predictive_evidence_execution_candidate_review_created"] is True


def test_target_universe_and_registry_metadata_are_preserved():
    review = _review()

    assert review["target_universe_count"] == 12
    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["reviewed_registry_approved_dataset_metadata"] == service.APPROVED_REGISTRY_METADATA
    assert review["total_canonical_record_count"] == 11946
    assert review["canonical_dataset_generated"] is True
    assert review["canonical_dataset_frozen"] is True


def test_per_ticker_review_entries_preserve_meta_and_candidate_digests():
    review = _review()
    entries = review["per_ticker_execution_candidate_review_entries"]

    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert review["per_ticker_record_counts"]["META"] == 913
    assert all(
        review["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )
    assert next(entry for entry in entries if entry["ticker"] == "META")["meta_reduced_record_count_flag"] is True
    assert all(entry["additional_predictive_evidence_execution_candidate_review_status"] == service.READY_FOR_OPERATOR_ASSESSMENT for entry in entries)
    assert all(entry["source_additional_predictive_evidence_execution_candidate_digest"] == service.EXPECTED_EXECUTION_CANDIDATE_DIGEST for entry in entries)


def test_execution_candidate_scope_and_authority_remain_candidate_only():
    review = _review()

    assert review["additional_predictive_evidence_execution_candidate_scope"] == service.candidate_service.EXECUTION_CANDIDATE_SCOPE
    assert review["additional_predictive_evidence_execution_mode"] == service.candidate_service.PLANNED_NOT_EXECUTED
    assert review["additional_predictive_evidence_execution_authority_status"] == service.NOT_AUTHORIZED


def test_execution_candidate_profile_is_reviewed_exactly():
    candidate = service.candidate_service.build_additional_predictive_evidence_execution_candidate_v1()

    assert _review()["reviewed_execution_candidate_profile"] == candidate["execution_candidate_profile"]


def test_label_set_is_reviewed_and_remains_unauthorized():
    labels = _review()["reviewed_planned_label_set"]

    assert [item["label_family"] for item in labels] == service.candidate_service.PLANNED_LABEL_FAMILIES
    assert len(labels) == 7
    assert all(item["label_generation_authorized"] is False for item in labels)
    assert all(item["label_generation_performed"] is False for item in labels)


def test_feature_set_is_reviewed_and_remains_unauthorized():
    features = _review()["reviewed_planned_feature_set"]

    assert [item["feature_family"] for item in features] == service.candidate_service.PLANNED_FEATURE_FAMILIES
    assert len(features) == 10
    assert all(item["feature_matrix_generation_authorized"] is False for item in features)
    assert all(item["feature_matrix_generation_performed"] is False for item in features)


def test_execution_protocol_and_split_profile_are_reviewed_not_executed():
    review = _review()
    protocol = review["reviewed_planned_execution_protocol"]

    assert [item["protocol_item"] for item in protocol] == service.candidate_service.PLANNED_EXECUTION_PROTOCOL_IDS
    assert all(item["execution_status"] == service.candidate_service.PLANNED_NOT_EXECUTED for item in protocol)
    assert review["reviewed_planned_split_profile"] == service.candidate_service.PLANNED_SPLIT_PROFILE


def test_metric_families_are_reviewed_not_computed():
    metrics = _review()["reviewed_planned_metric_families"]

    assert [item["metric_family"] for item in metrics] == service.candidate_service.PLANNED_METRIC_FAMILY_IDS
    assert all(item["computation_status"] == service.candidate_service.PLANNED_NOT_COMPUTED for item in metrics)


def test_baselines_are_reviewed_not_evaluated_or_acceptance_evidence():
    baselines = _review()["reviewed_planned_baselines"]

    assert [item["baseline"] for item in baselines] == service.candidate_service.PLANNED_BASELINE_IDS
    assert all(item["evaluation_status"] == service.candidate_service.PLANNED_NOT_EVALUATED for item in baselines)
    assert all(item["acceptance_evidence_status"] == service.candidate_service.NOT_ACCEPTANCE_EVIDENCE for item in baselines)


def test_future_outputs_are_reviewed_and_not_generated():
    outputs = _review()["reviewed_future_execution_outputs"]

    assert [item["output_id"] for item in outputs] == service.candidate_service.FUTURE_EXECUTION_OUTPUT_IDS
    assert len(outputs) == 15
    assert all(item["generation_status"] == service.candidate_service.PLANNED_NOT_GENERATED for item in outputs)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("reviewed_future_execution_chain", service.candidate_service.FUTURE_EXECUTION_CHAIN),
        ("reviewed_future_gates", service.candidate_service.FUTURE_GATES),
        ("reviewed_risk_controls", service.candidate_service.RISK_CONTROLS),
    ],
)
def test_future_chain_gates_and_risk_controls_are_reviewed(field, expected):
    assert _review()[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "label_generation_authorized",
        "label_generation_performed",
        "feature_matrix_generation_authorized",
        "feature_matrix_generation_performed",
        "walk_forward_validation_authorized",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_authorized",
        "out_of_sample_evaluation_performed",
        "baseline_comparison_authorized",
        "baseline_comparison_performed",
        "signal_quality_metrics_authorized",
        "signal_quality_metrics_performed",
        "stability_analysis_authorized",
        "stability_analysis_performed",
        "leakage_control_review_authorized",
        "leakage_control_review_performed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_candidate_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
    ],
)
def test_execution_and_activation_flags_remain_false(field):
    assert _review()[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_strategy_and_trading_use_remain_not_authorized(field):
    assert _review()[field] == service.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    review = _review()

    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED


def test_checklist_contains_all_required_ids_and_passes():
    review = _review()
    checklist = review["review_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in checklist)


def test_summary_counts_are_exact_and_future_authorities_remain_closed():
    summary = _review()["review_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 74
    assert summary["passed_checks"] == 74
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_additional_predictive_evidence_execution_approval"] is False
    assert summary["ready_for_additional_predictive_evidence_execution"] is False


def test_review_package_digest_is_deterministic():
    first = _review()
    second = _review()

    assert first["additional_predictive_evidence_execution_candidate_review_package_digest"] == second["additional_predictive_evidence_execution_candidate_review_package_digest"]
    assert first["additional_predictive_evidence_execution_candidate_review_package_digest"] == service.additional_predictive_evidence_execution_candidate_review_package_digest_v1(first)


def test_per_ticker_review_digests_are_deterministic():
    first = _review()["per_ticker_execution_candidate_review_entries"]
    second = _review()["per_ticker_execution_candidate_review_entries"]

    assert [item["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"] for item in first] == [item["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"] for item in second]
    assert all(
        item["per_ticker_additional_predictive_evidence_execution_candidate_review_digest"]
        == service.per_ticker_additional_predictive_evidence_execution_candidate_review_digest_v1(item)
        for item in first
    )


def test_validator_accepts_valid_review_package():
    validation = service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(_review())

    assert validation["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_additional_predictive_evidence_execution_candidate_digest", "0" * 64),
        ("reviewed_additional_predictive_evidence_execution_candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("research_registry_approved", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_candidate_review_created", False),
        ("additional_predictive_evidence_execution_approved", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("additional_predictive_evidence_results_created", True),
        ("label_generation_authorized", True),
        ("label_generation_performed", True),
        ("feature_matrix_generation_authorized", True),
        ("feature_matrix_generation_performed", True),
        ("walk_forward_validation_authorized", True),
        ("walk_forward_validation_performed", True),
        ("out_of_sample_evaluation_authorized", True),
        ("out_of_sample_evaluation_performed", True),
        ("baseline_comparison_performed", True),
        ("signal_quality_metrics_performed", True),
        ("stability_analysis_performed", True),
        ("leakage_control_review_performed", True),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
    ],
)
def test_validator_rejects_invalid_scalar_boundaries(field, bad_value):
    review = _review()
    review[field] = bad_value

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(review)


def test_validator_rejects_target_universe_mismatch():
    review = _review()
    review["target_universe"] = list(reversed(review["target_universe"]))

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(review)


@pytest.mark.parametrize(("ticker", "count"), [("META", 1003), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_record_count(ticker, count):
    review = _review()
    review["per_ticker_record_counts"][ticker] = count

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(review)


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_execution_candidate_digest",
        "additional_predictive_evidence_execution_candidate_review_package_digest",
        "reviewed_planned_label_set",
        "reviewed_planned_feature_set",
        "reviewed_planned_execution_protocol",
        "reviewed_planned_split_profile",
        "reviewed_planned_metric_families",
        "reviewed_planned_baselines",
        "reviewed_future_execution_outputs",
        "reviewed_future_execution_chain",
        "reviewed_future_gates",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_required_evidence_or_plan(field):
    review = _review()
    del review[field]

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(review)


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_additional_predictive_evidence_execution_candidate_digest",
        "per_ticker_additional_predictive_evidence_execution_candidate_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(field):
    review = _review()
    del review["per_ticker_execution_candidate_review_entries"][0][field]

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.validate_additional_predictive_evidence_execution_candidate_review_package_v1(review)


def test_builder_rejects_changed_execution_candidate_digest():
    candidate = service.candidate_service.build_additional_predictive_evidence_execution_candidate_v1()
    candidate["additional_predictive_evidence_execution_candidate_digest"] = "0" * 64

    with pytest.raises((
        service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError,
        service.candidate_service.AdditionalPredictiveEvidenceExecutionCandidateError,
    )):
        service.build_additional_predictive_evidence_execution_candidate_review_package_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = service.build_additional_predictive_evidence_execution_candidate_review_markdown_v1(_review())

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Execution Candidate Review Package",
        "## Reviewed Execution Candidate",
        "## Source Chain Candidate Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Per-Ticker Execution Candidate Review Entries",
        "## Reviewed Label Set",
        "## Reviewed Feature Set",
        "## Reviewed Execution Protocol",
        "## Reviewed Split Profile",
        "## Reviewed Metric Families",
        "## Reviewed Baselines",
        "## Reviewed Future Execution Outputs",
        "## Future Execution Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_emits_canonical_json_in_isolated_directory(tmp_path):
    result = service.write_additional_predictive_evidence_execution_candidate_review_package_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert payload == _review()
    assert result["payload_sha256"]


def test_writer_refuses_to_overwrite(tmp_path):
    service.write_additional_predictive_evidence_execution_candidate_review_package_v1(tmp_path)

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.write_additional_predictive_evidence_execution_candidate_review_package_v1(tmp_path)


@pytest.mark.parametrize("filename", ["../review.json", "review.txt", "nested/review.json"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateReviewPackageError):
        service.write_additional_predictive_evidence_execution_candidate_review_package_v1(
            tmp_path, filename=filename
        )
