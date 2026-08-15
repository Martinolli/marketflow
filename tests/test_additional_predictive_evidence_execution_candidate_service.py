from __future__ import annotations

import json

import pytest

from marketflow.services import additional_predictive_evidence_execution_candidate_service as service


def _candidate() -> dict:
    return service.build_additional_predictive_evidence_execution_candidate_v1()


def test_candidate_builds_offline_without_provider_or_review_replay(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("provider/review path must not be called")

    monkeypatch.setattr(
        service.review_service,
        "build_additional_predictive_evidence_chain_candidate_review_package_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.chain_service.registry_approval,
        "build_research_registry_approved_v1",
        forbidden,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_candidate_identity_and_status_are_exact():
    candidate = _candidate()

    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE
    assert candidate["candidate_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert candidate["additional_predictive_evidence_execution_candidate_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_ready_for_operator_review"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_chain_candidate_review_package_digest", service.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("additional_predictive_evidence_chain_candidate_digest", service.EXPECTED_CHAIN_CANDIDATE_DIGEST),
        ("research_registry_approval_digest", service.chain_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", service.chain_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_generation_digest", service.chain_service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("records_digest", service.chain_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(field, expected):
    assert _candidate()[field] == expected


def test_registry_chain_and_candidate_readiness_are_preserved():
    candidate = _candidate()

    assert candidate["registry_approval_created"] is True
    assert candidate["research_registry_approved"] is True
    assert candidate["additional_predictive_evidence_chain_candidate_created"] is True
    assert candidate["additional_predictive_evidence_chain_candidate_review_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_created"] is True


def test_target_universe_and_registry_metadata_are_exact():
    candidate = _candidate()

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["approved_registry_metadata"] == service.APPROVED_REGISTRY_METADATA
    assert candidate["total_canonical_record_count"] == 11946
    assert candidate["canonical_dataset_generated"] is True
    assert candidate["canonical_dataset_frozen"] is True


def test_per_ticker_entries_preserve_meta_and_source_digests():
    candidate = _candidate()
    entries = candidate["per_ticker_execution_candidate_entries"]

    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert all(
        candidate["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )
    assert next(entry for entry in entries if entry["ticker"] == "META")["meta_reduced_record_count_flag"] is True
    assert all(entry["source_additional_predictive_evidence_chain_candidate_review_digest"] == service.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST for entry in entries)
    assert all(entry["source_additional_predictive_evidence_chain_candidate_digest"] == service.EXPECTED_CHAIN_CANDIDATE_DIGEST for entry in entries)


def test_execution_candidate_scope_and_authority_are_planning_only():
    candidate = _candidate()

    assert candidate["additional_predictive_evidence_execution_candidate_scope"] == service.EXECUTION_CANDIDATE_SCOPE
    assert candidate["additional_predictive_evidence_execution_mode"] == service.PLANNED_NOT_EXECUTED
    assert candidate["additional_predictive_evidence_execution_authority_status"] == service.NOT_AUTHORIZED


def test_execution_candidate_profile_is_exact_and_not_executed():
    assert _candidate()["execution_candidate_profile"] == {
        "dataset_binding": "expanded_universe_canonical_dataset_v1",
        "records_digest": service.chain_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "timeframe": "1d",
        "source_profile": "RTH_FULL_SESSION_1D",
        "execution_profile_status": service.PLANNED_NOT_EXECUTED,
    }


def test_planned_label_set_has_seven_unauthorized_families():
    labels = _candidate()["planned_label_set"]

    assert [item["label_family"] for item in labels] == service.PLANNED_LABEL_FAMILIES
    assert len(labels) == 7
    assert all(item["execution_candidate_status"] == service.PLANNED_FOR_EXECUTION_CANDIDATE_ONLY for item in labels)
    assert all(item["label_generation_authorized"] is False for item in labels)
    assert all(item["label_generation_performed"] is False for item in labels)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in labels)


def test_planned_feature_set_has_ten_unauthorized_families():
    features = _candidate()["planned_feature_set"]

    assert [item["feature_family"] for item in features] == service.PLANNED_FEATURE_FAMILIES
    assert len(features) == 10
    assert all(item["execution_candidate_status"] == service.PLANNED_FOR_EXECUTION_CANDIDATE_ONLY for item in features)
    assert all(item["feature_matrix_generation_authorized"] is False for item in features)
    assert all(item["feature_matrix_generation_performed"] is False for item in features)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in features)


def test_planned_execution_protocol_and_split_profile_are_defined_not_executed():
    candidate = _candidate()
    protocol = candidate["planned_execution_protocol"]

    assert [item["protocol_item"] for item in protocol] == service.PLANNED_EXECUTION_PROTOCOL_IDS
    assert all(item["execution_status"] == service.PLANNED_NOT_EXECUTED for item in protocol)
    assert candidate["planned_split_profile"] == service.PLANNED_SPLIT_PROFILE


def test_planned_metric_families_are_not_computed_or_authorized():
    metrics = _candidate()["planned_metric_families"]

    assert [item["metric_family"] for item in metrics] == service.PLANNED_METRIC_FAMILY_IDS
    assert all(item["computation_status"] == service.PLANNED_NOT_COMPUTED for item in metrics)
    assert all(item["execution_authority_status"] == service.NOT_AUTHORIZED_FOR_EXECUTION for item in metrics)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in metrics)


def test_planned_baselines_are_not_evaluated_or_acceptance_evidence():
    baselines = _candidate()["planned_baselines"]

    assert [item["baseline"] for item in baselines] == service.PLANNED_BASELINE_IDS
    assert all(item["evaluation_status"] == service.PLANNED_NOT_EVALUATED for item in baselines)
    assert all(item["acceptance_evidence_status"] == service.NOT_ACCEPTANCE_EVIDENCE for item in baselines)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in baselines)


def test_future_outputs_are_defined_but_not_generated():
    outputs = _candidate()["future_execution_outputs"]

    assert [item["output_id"] for item in outputs] == service.FUTURE_EXECUTION_OUTPUT_IDS
    assert len(outputs) == 15
    assert all(item["generation_status"] == service.PLANNED_NOT_GENERATED for item in outputs)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("future_execution_chain", service.FUTURE_EXECUTION_CHAIN),
        ("future_gates", service.FUTURE_GATES),
        ("risk_controls", service.RISK_CONTROLS),
    ],
)
def test_future_chain_gates_and_risk_controls_are_exact(field, expected):
    assert _candidate()[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "additional_predictive_evidence_execution_candidate_review_created",
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
    assert _candidate()[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_strategy_and_trading_use_remain_not_authorized(field):
    assert _candidate()[field] == service.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED


def test_checklist_contains_all_required_ids_and_passes():
    candidate = _candidate()
    checklist = candidate["candidate_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in checklist)


def test_summary_counts_are_exact_and_only_review_readiness_opens():
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 69
    assert summary["passed_checks"] == 69
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_additional_predictive_evidence_execution_candidate_review"] is True
    assert summary["ready_for_additional_predictive_evidence_execution_approval"] is False
    assert summary["ready_for_additional_predictive_evidence_execution"] is False


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["additional_predictive_evidence_execution_candidate_digest"] == second["additional_predictive_evidence_execution_candidate_digest"]
    assert first["additional_predictive_evidence_execution_candidate_digest"] == service.additional_predictive_evidence_execution_candidate_digest_v1(first)


def test_per_ticker_execution_candidate_digests_are_deterministic():
    first = _candidate()["per_ticker_execution_candidate_entries"]
    second = _candidate()["per_ticker_execution_candidate_entries"]

    assert [item["per_ticker_additional_predictive_evidence_execution_candidate_digest"] for item in first] == [item["per_ticker_additional_predictive_evidence_execution_candidate_digest"] for item in second]
    assert all(
        item["per_ticker_additional_predictive_evidence_execution_candidate_digest"]
        == service.per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(item)
        for item in first
    )


def test_validator_accepts_valid_candidate():
    validation = service.validate_additional_predictive_evidence_execution_candidate_v1(_candidate())

    assert validation["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("target_universe_count", 11),
        ("research_registry_approved", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_chain_candidate_review_created", False),
        ("additional_predictive_evidence_execution_candidate_created", False),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
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
        ("provider_requests_made", True),
        ("live_provider_transport_enabled", True),
        ("market_data_acquisition_performed", True),
        ("dataset_generation_performed", True),
        ("canonical_dataset_regenerated", True),
    ],
)
def test_validator_rejects_invalid_scalar_boundaries(field, bad_value):
    candidate = _candidate()
    candidate[field] = bad_value

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.validate_additional_predictive_evidence_execution_candidate_v1(candidate)


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.validate_additional_predictive_evidence_execution_candidate_v1(candidate)


@pytest.mark.parametrize(("ticker", "count"), [("META", 1003), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_record_count(ticker, count):
    candidate = _candidate()
    candidate["per_ticker_record_counts"][ticker] = count

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.validate_additional_predictive_evidence_execution_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_chain_candidate_review_package_digest",
        "research_registry_approval_digest",
        "records_digest",
        "planned_label_set",
        "planned_feature_set",
        "planned_execution_protocol",
        "planned_split_profile",
        "planned_metric_families",
        "planned_baselines",
        "future_execution_outputs",
        "future_execution_chain",
        "future_gates",
        "risk_controls",
        "additional_predictive_evidence_execution_candidate_digest",
    ],
)
def test_validator_rejects_missing_required_evidence_or_plan(field):
    candidate = _candidate()
    del candidate[field]

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.validate_additional_predictive_evidence_execution_candidate_v1(candidate)


def test_validator_rejects_missing_per_ticker_digest():
    candidate = _candidate()
    del candidate["per_ticker_execution_candidate_entries"][0][
        "per_ticker_additional_predictive_evidence_execution_candidate_digest"
    ]

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.validate_additional_predictive_evidence_execution_candidate_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = service.build_additional_predictive_evidence_execution_candidate_markdown_v1(_candidate())

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Execution Candidate",
        "## Source Chain Candidate Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Per-Ticker Execution Candidate Entries",
        "## Planned Label Set",
        "## Planned Feature Set",
        "## Planned Execution Protocol",
        "## Planned Split Profile",
        "## Planned Metric Families",
        "## Planned Baselines",
        "## Future Execution Outputs",
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
    result = service.write_additional_predictive_evidence_execution_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert payload == _candidate()
    assert result["payload_sha256"]


def test_writer_refuses_to_overwrite(tmp_path):
    service.write_additional_predictive_evidence_execution_candidate_v1(tmp_path)

    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.write_additional_predictive_evidence_execution_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["../candidate.json", "candidate.txt", "nested/candidate.json"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionCandidateError):
        service.write_additional_predictive_evidence_execution_candidate_v1(
            tmp_path, filename=filename
        )
