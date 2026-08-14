from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import additional_predictive_evidence_chain_candidate_service as service


def _candidate() -> dict:
    return service.build_additional_predictive_evidence_chain_candidate_v1()


def test_candidate_builds_offline_without_replaying_approval_or_provider_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("approval/provider path must not be called")

    monkeypatch.setattr(service.registry_approval, "build_research_registry_approved_v1", forbidden)
    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_candidate_identity_and_ready_state_are_exact():
    candidate = _candidate()

    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE
    assert candidate["candidate_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_READY_FOR_OPERATOR_REVIEW
    assert candidate["registry_approval_created"] is True
    assert candidate["research_registry_approved"] is True
    assert candidate["ready_for_additional_predictive_evidence_chain_candidate"] is True
    assert candidate["additional_predictive_evidence_chain_candidate_created"] is True
    assert candidate["additional_predictive_evidence_chain_ready_for_operator_review"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("research_registry_candidate_review_package_digest", service.EXPECTED_RESEARCH_REGISTRY_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("canonical_dataset_freeze_digest", service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_generation_digest", service.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_required_source_evidence_is_bound(field, expected):
    assert _candidate()[field] == expected


def test_target_universe_and_registry_metadata_are_exact():
    candidate = _candidate()

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["approved_registry_metadata"] == service.APPROVED_REGISTRY_METADATA
    assert candidate["total_canonical_record_count"] == 11946
    assert candidate["canonical_dataset_generated"] is True
    assert candidate["canonical_dataset_frozen"] is True


def test_per_ticker_counts_and_planning_entries_preserve_meta_limitation():
    candidate = _candidate()
    entries = candidate["per_ticker_predictive_evidence_planning_entries"]

    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert all(
        candidate["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )
    assert next(entry for entry in entries if entry["ticker"] == "META")["meta_reduced_record_count_flag"] is True
    assert all(
        entry["meta_reduced_record_count_flag"] is False
        for entry in entries
        if entry["ticker"] != "META"
    )


def test_chain_scope_and_authority_are_planning_only():
    candidate = _candidate()

    assert candidate["additional_predictive_evidence_chain_scope"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_SCOPE
    assert candidate["additional_predictive_evidence_mode"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_MODE
    assert candidate["additional_predictive_evidence_authority_status"] == service.NOT_AUTHORIZED


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_evidence_planning_dimensions", service.PREDICTIVE_EVIDENCE_PLANNING_DIMENSIONS),
        ("future_additional_predictive_evidence_chain", service.FUTURE_ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN),
        ("future_gates", service.FUTURE_GATES),
        ("risk_controls", service.RISK_CONTROLS),
    ],
)
def test_planning_collections_are_complete(field, expected):
    assert _candidate()[field] == expected


def test_planned_label_families_are_defined_but_not_generated():
    items = _candidate()["planned_label_families"]

    assert [item["label_family_id"] for item in items] == service.PLANNED_LABEL_FAMILY_IDS
    assert all(item["generation_status"] == service.PLANNED_NOT_GENERATED for item in items)
    assert all(item["execution_authority_status"] == service.NOT_AUTHORIZED_FOR_EXECUTION for item in items)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in items)


def test_planned_feature_families_are_defined_but_not_generated():
    items = _candidate()["planned_feature_families"]

    assert [item["feature_family_id"] for item in items] == service.PLANNED_FEATURE_FAMILY_IDS
    assert all(item["generation_status"] == service.PLANNED_NOT_GENERATED for item in items)
    assert all(item["execution_authority_status"] == service.NOT_AUTHORIZED_FOR_EXECUTION for item in items)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in items)


def test_evaluation_protocol_is_defined_but_not_executed():
    items = _candidate()["planned_evaluation_protocol"]

    assert [item["protocol_item_id"] for item in items] == service.PLANNED_EVALUATION_PROTOCOL
    assert all(item["execution_status"] == "PLANNED_NOT_EXECUTED" for item in items)


def test_planned_outputs_are_not_generated_and_non_actionable():
    items = _candidate()["planned_outputs"]

    assert [item["output_id"] for item in items] == service.PLANNED_OUTPUT_IDS
    assert all(item["generation_status"] == service.PLANNED_NOT_GENERATED for item in items)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in items)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "label_generation_authorized",
        "label_generation_performed",
        "feature_matrix_generation_authorized",
        "feature_matrix_generation_performed",
        "walk_forward_validation_authorized",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_authorized",
        "out_of_sample_evaluation_performed",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
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


def test_checklist_has_all_required_ids_and_all_checks_pass():
    candidate = _candidate()
    checklist = candidate["candidate_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in checklist)


def test_summary_counts_are_exact_and_keep_future_gates_closed():
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 60
    assert summary["passed_checks"] == 60
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False
    assert summary["ready_for_predictive_usefulness_reassessment"] is False


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["additional_predictive_evidence_chain_candidate_digest"] == second["additional_predictive_evidence_chain_candidate_digest"]
    assert first["additional_predictive_evidence_chain_candidate_digest"] == service.additional_predictive_evidence_chain_candidate_digest_v1(first)


def test_per_ticker_candidate_digests_are_deterministic():
    first = _candidate()["per_ticker_predictive_evidence_planning_entries"]
    second = _candidate()["per_ticker_predictive_evidence_planning_entries"]

    assert [item["per_ticker_additional_predictive_evidence_chain_candidate_digest"] for item in first] == [item["per_ticker_additional_predictive_evidence_chain_candidate_digest"] for item in second]
    assert all(
        item["per_ticker_additional_predictive_evidence_chain_candidate_digest"]
        == service.per_ticker_additional_predictive_evidence_chain_candidate_digest_v1(item)
        for item in first
    )


def test_validator_accepts_valid_candidate():
    validation = service.validate_additional_predictive_evidence_chain_candidate_v1(_candidate())

    assert validation["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_CHAIN_CANDIDATE_VALID"
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
        ("ready_for_additional_predictive_evidence_chain_candidate", False),
        ("additional_predictive_evidence_chain_candidate_created", False),
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

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.validate_additional_predictive_evidence_chain_candidate_v1(candidate)


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.validate_additional_predictive_evidence_chain_candidate_v1(candidate)


@pytest.mark.parametrize(("ticker", "count"), [("META", 1003), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_record_count(ticker, count):
    candidate = _candidate()
    candidate["per_ticker_record_counts"][ticker] = count

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.validate_additional_predictive_evidence_chain_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "research_registry_approval_digest",
        "records_digest",
        "predictive_evidence_planning_dimensions",
        "planned_label_families",
        "planned_feature_families",
        "planned_evaluation_protocol",
        "future_additional_predictive_evidence_chain",
        "future_gates",
        "risk_controls",
        "additional_predictive_evidence_chain_candidate_digest",
    ],
)
def test_validator_rejects_missing_required_evidence_or_planning_field(field):
    candidate = _candidate()
    del candidate[field]

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.validate_additional_predictive_evidence_chain_candidate_v1(candidate)


def test_validator_rejects_forbidden_artifact_values_recursively():
    candidate = _candidate()
    candidate["planned_outputs"][0]["unexpected_status"] = "PREDICTIVE_USEFULNESS_ACCEPTED"

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.validate_additional_predictive_evidence_chain_candidate_v1(candidate)


def test_markdown_includes_required_sections():
    markdown = service.build_additional_predictive_evidence_chain_candidate_markdown_v1(_candidate())

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Chain Candidate",
        "## Source Research Registry Approval",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Per-Ticker Predictive Evidence Planning Entries",
        "## Planned Label Families",
        "## Planned Feature Families",
        "## Planned Evaluation Protocol",
        "## Future Predictive Evidence Chain",
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
    result = service.write_additional_predictive_evidence_chain_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))

    assert payload == _candidate()
    assert result["payload_sha256"]


def test_writer_refuses_to_overwrite(tmp_path):
    service.write_additional_predictive_evidence_chain_candidate_v1(tmp_path)

    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.write_additional_predictive_evidence_chain_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["../candidate.json", "candidate.txt", "nested/candidate.json"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename):
    with pytest.raises(service.AdditionalPredictiveEvidenceChainCandidateError):
        service.write_additional_predictive_evidence_chain_candidate_v1(tmp_path, filename=filename)
