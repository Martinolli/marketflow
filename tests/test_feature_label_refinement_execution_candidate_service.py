from __future__ import annotations

import json

import pytest

from marketflow.services import feature_label_refinement_execution_candidate_service as service


def _candidate() -> dict:
    return service.build_feature_label_refinement_execution_candidate_v1()


def _resign(candidate: dict) -> dict:
    candidate["candidate_checklist"] = service._checklist(candidate)
    candidate["candidate_summary"] = service._summary(candidate["candidate_checklist"])
    candidate["feature_label_refinement_execution_candidate_digest"] = (
        service.feature_label_refinement_execution_candidate_digest_v1(candidate)
    )
    return candidate


def test_candidate_builds_offline_without_provider_or_source_replay(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("provider/source replay path must not be called")

    monkeypatch.setattr(
        service.approval_service,
        "build_feature_label_refinement_plan_approved_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.plan_service,
        "build_feature_label_refinement_plan_candidate_v1",
        forbidden,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_candidate_identity_and_status_are_exact():
    candidate = _candidate()

    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE
    assert candidate["schema_version"] == service.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_V1
    assert candidate["candidate_status"] == service.FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert candidate["feature_label_refinement_execution_candidate_created"] is True
    assert candidate["feature_label_refinement_execution_candidate_ready_for_operator_review"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_label_refinement_plan_approval_digest", service.EXPECTED_PLAN_APPROVAL_DIGEST),
        ("feature_label_refinement_plan_candidate_review_package_digest", service.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_plan_candidate_digest", service.EXPECTED_PLAN_CANDIDATE_DIGEST),
        ("predictive_evidence_improvement_candidate_review_package_digest", service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", service.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", service.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", service.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(field, expected):
    assert _candidate()[field] == expected


def test_target_universe_and_record_counts_are_exact():
    candidate = _candidate()

    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["target_universe_count"] == 12
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert all(
        candidate["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_execution_candidate_objective_and_authority_are_exact():
    candidate = _candidate()

    assert candidate["feature_label_refinement_execution_candidate_objective"] == service.EXECUTION_CANDIDATE_OBJECTIVE
    assert candidate["feature_label_refinement_execution_candidate_scope"] == service.EXECUTION_CANDIDATE_SCOPE
    assert candidate["feature_label_refinement_execution_mode"] == service.PLANNED_NOT_EXECUTED
    assert candidate["feature_label_refinement_execution_authority_status"] == service.NOT_AUTHORIZED


def test_readiness_failure_basis_is_preserved():
    basis = _candidate()["readiness_failure_basis"]

    assert basis == service._readiness_failure_basis()
    assert basis["readiness_decision"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
    assert basis["readiness_reason"] == "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"
    assert basis["leakage_status"] == service.PASS
    assert basis["failed_leakage_controls"] == 0


def test_execution_candidate_profile_is_exact_and_not_executed():
    profile = _candidate()["execution_candidate_profile"]

    assert profile == service._execution_candidate_profile()
    assert profile["total_canonical_record_count"] == 11946
    assert profile["records_digest"] == service.EXPECTED_RECORDS_DIGEST
    assert profile["execution_profile_status"] == service.PLANNED_NOT_EXECUTED


def test_planned_execution_steps_are_defined_not_executed():
    steps = _candidate()["planned_execution_steps"]

    assert [item["step_id"] for item in steps] == service.PLANNED_EXECUTION_STEP_IDS
    assert all(item["execution_status"] == service.PLANNED_NOT_EXECUTED for item in steps)
    assert all(item["authorization_status"] == service.NOT_AUTHORIZED_FOR_EXECUTION for item in steps)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in steps)


@pytest.mark.parametrize(
    ("field", "group_ids"),
    [
        ("planned_label_refinement_execution_groups", service.LABEL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("planned_feature_refinement_execution_groups", service.FEATURE_REFINEMENT_EXECUTION_GROUP_IDS),
        ("planned_protocol_refinement_execution_groups", service.PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("planned_model_comparison_execution_groups", service.MODEL_COMPARISON_EXECUTION_GROUP_IDS),
    ],
)
def test_planned_groups_are_complete_research_only_and_unauthorized(field, group_ids):
    groups = _candidate()[field]

    assert [item["group_id"] for item in groups] == group_ids
    assert all(item["execution_candidate_status"] == service.PLANNED_FOR_EXECUTION_CANDIDATE_ONLY for item in groups)
    assert all(item["authorization_status"] == service.NOT_AUTHORIZED for item in groups)
    assert all(item["execution_status"] == service.NOT_EXECUTED for item in groups)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in groups)


def test_planned_outputs_are_not_generated_and_research_only():
    outputs = _candidate()["planned_execution_outputs"]

    assert [item["output_name"] for item in outputs] == service.PLANNED_EXECUTION_OUTPUT_NAMES
    assert all(item["generation_status"] == service.PLANNED_NOT_GENERATED for item in outputs)
    assert all(item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)


def test_per_ticker_entries_preserve_meta_and_candidate_boundaries():
    entries = _candidate()["per_ticker_execution_candidate_entries"]

    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["refinement_note"] == "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
    assert all(entry["historical_record_count"] == 1003 for entry in entries if entry["ticker"] != "META")
    assert all(entry["meta_reduced_record_count_flag"] is False for entry in entries if entry["ticker"] != "META")
    assert all("refinement_note" not in entry for entry in entries if entry["ticker"] != "META")
    assert all(entry["feature_label_refinement_execution_authorized"] is False for entry in entries)
    assert all(entry["feature_label_refinement_executed"] is False for entry in entries)


def test_per_ticker_digests_are_present_and_deterministic():
    first = _candidate()["per_ticker_execution_candidate_entries"]
    second = _candidate()["per_ticker_execution_candidate_entries"]

    assert first == second
    for entry in first:
        digest = entry["per_ticker_feature_label_refinement_execution_candidate_digest"]
        assert len(digest) == 64
        assert digest == service.per_ticker_feature_label_refinement_execution_candidate_digest_v1(entry)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "predictive_execution_rerun_performed",
        "label_generation_rerun_performed",
        "feature_matrix_rerun_performed",
        "walk_forward_validation_rerun_performed",
        "out_of_sample_evaluation_rerun_performed",
        "metrics_recomputation_performed",
        "improvement_execution_performed",
        "refinement_option_execution_performed",
        "label_refinement_execution_performed",
        "feature_refinement_execution_performed",
        "protocol_refinement_execution_performed",
        "model_comparison_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "feature_label_refinement_execution_candidate_review_created",
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "refined_label_generation_authorized",
        "refined_label_generation_performed",
        "refined_feature_generation_authorized",
        "refined_feature_generation_performed",
        "refined_walk_forward_validation_authorized",
        "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_authorized",
        "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_authorized",
        "refined_metrics_recomputation_performed",
        "model_comparison_authorized",
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
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "feature_label_refinement_execution_approval_created",
        "feature_label_refinement_execution_artifact_created",
        "additional_predictive_evidence_execution_candidate_artifact_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ],
)
def test_every_execution_and_downstream_authority_flag_remains_false(field):
    assert _candidate()[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_authority_remains_not_authorized(field):
    assert _candidate()[field] == service.NOT_AUTHORIZED


def test_future_chain_gates_and_risk_controls_are_exact():
    candidate = _candidate()

    assert candidate["future_execution_chain"] == service.FUTURE_EXECUTION_CHAIN
    assert candidate["future_gates"] == service.FUTURE_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_checklist_contains_all_required_checks_and_all_pass():
    candidate = _candidate()
    checklist = candidate["candidate_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(item["severity"] == service.BLOCKER for item in checklist)


def test_summary_counts_and_boundaries_are_exact():
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 81
    assert summary["passed_checks"] == 81
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary["ready_for_feature_label_refinement_execution_approval"] is False
    assert summary["ready_for_feature_label_refinement_execution"] is False
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False


def test_candidate_digest_is_deterministic_and_semantic():
    first = _candidate()
    second = _candidate()

    assert first["feature_label_refinement_execution_candidate_digest"] == second["feature_label_refinement_execution_candidate_digest"]
    assert first["feature_label_refinement_execution_candidate_digest"] == service.feature_label_refinement_execution_candidate_digest_v1(first)


def test_validator_accepts_valid_candidate():
    validation = service.validate_feature_label_refinement_execution_candidate_v1(_candidate())

    assert validation["status"] == "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_VALID"
    assert validation["ready_for_operator_review"] is True
    assert validation["blocker_count"] == 0
    assert validation["feature_label_refinement_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("feature_label_refinement_plan_approval_digest", "0" * 64),
        ("feature_label_refinement_plan_candidate_review_package_digest", "0" * 64),
        ("feature_label_refinement_plan_approved", False),
        ("ready_for_feature_label_refinement_execution_candidate", False),
        ("feature_label_refinement_execution_candidate_created", False),
        ("feature_label_refinement_execution_authority_status", "AUTHORIZED"),
        ("feature_label_refinement_execution_approved", True),
        ("feature_label_refinement_execution_authorized", True),
        ("feature_label_refinement_executed", True),
        ("feature_label_refinement_results_created", True),
        ("refined_label_generation_authorized", True),
        ("refined_label_generation_performed", True),
        ("refined_feature_generation_authorized", True),
        ("refined_feature_generation_performed", True),
        ("model_comparison_authorized", True),
        ("model_comparison_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("predictive_execution_rerun_performed", True),
        ("label_generation_rerun_performed", True),
        ("feature_matrix_rerun_performed", True),
        ("walk_forward_validation_rerun_performed", True),
        ("out_of_sample_evaluation_rerun_performed", True),
        ("metrics_recomputation_performed", True),
        ("improvement_execution_performed", True),
        ("refinement_option_execution_performed", True),
        ("label_refinement_execution_performed", True),
        ("feature_refinement_execution_performed", True),
        ("protocol_refinement_execution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_invalid_or_authorizing_top_level_values(field, value):
    candidate = _candidate()
    candidate[field] = value
    _resign(candidate)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.validate_feature_label_refinement_execution_candidate_v1(candidate)


def test_validator_rejects_target_universe_mismatch():
    candidate = _candidate()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))
    _resign(candidate)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.validate_feature_label_refinement_execution_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("planned_execution_steps", []),
        ("planned_execution_outputs", []),
        ("future_execution_chain", []),
        ("future_gates", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_missing_planned_contract_sections(field, replacement):
    candidate = _candidate()
    candidate[field] = replacement
    _resign(candidate)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.validate_feature_label_refinement_execution_candidate_v1(candidate)


def test_validator_rejects_changed_readiness_decision_and_reason():
    for field, value in (
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "READY"),
    ):
        candidate = _candidate()
        candidate["readiness_failure_basis"][field] = value
        _resign(candidate)
        with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
            service.validate_feature_label_refinement_execution_candidate_v1(candidate)


def test_validator_rejects_missing_or_changed_per_ticker_digest():
    for value in (None, "0" * 64):
        candidate = _candidate()
        candidate["per_ticker_execution_candidate_entries"][0][
            "per_ticker_feature_label_refinement_execution_candidate_digest"
        ] = value
        _resign(candidate)
        with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
            service.validate_feature_label_refinement_execution_candidate_v1(candidate)


@pytest.mark.parametrize("forbidden", sorted(service.FORBIDDEN_ARTIFACT_VALUES))
def test_validator_rejects_forbidden_artifact_values_at_any_depth(forbidden):
    candidate = _candidate()
    candidate["nested_probe"] = {"value": forbidden}
    _resign(candidate)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.validate_feature_label_refinement_execution_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = _candidate()
    candidate.pop("feature_label_refinement_execution_candidate_digest")

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.validate_feature_label_refinement_execution_candidate_v1(candidate)


def test_markdown_contains_required_sections_and_guardrails():
    markdown = service.build_feature_label_refinement_execution_candidate_markdown_v1(_candidate())

    for section in (
        "## Title",
        "## Feature/Label Refinement Execution Candidate",
        "## Source Plan Approval",
        "## Execution Candidate Objective",
        "## Readiness Failure Basis",
        "## Execution Candidate Profile",
        "## Planned Execution Steps",
        "## Planned Label Refinement Execution Groups",
        "## Planned Feature Refinement Execution Groups",
        "## Planned Protocol Refinement Execution Groups",
        "## Planned Model Comparison Execution Groups",
        "## Per-Ticker Execution Candidate Entries",
        "## Future Execution Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Execution Boundary",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown
    assert "META`" in markdown and "913" in markdown
    assert "Candidate only" in markdown


def test_writer_creates_canonical_json_in_requested_directory(tmp_path):
    result = service.write_feature_label_refinement_execution_candidate_v1(tmp_path)
    path = tmp_path / "feature_label_refinement_execution_candidate_v1.json"

    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload == _candidate()
    assert result["filename"] == path.name
    assert result["payload_byte_size"] == path.stat().st_size
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_to_overwrite_existing_output(tmp_path):
    service.write_feature_label_refinement_execution_candidate_v1(tmp_path)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.write_feature_label_refinement_execution_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["candidate.txt", "../candidate.json", "nested/candidate.json"])
def test_writer_rejects_non_simple_json_filename(tmp_path, filename):
    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateError):
        service.write_feature_label_refinement_execution_candidate_v1(
            tmp_path, filename=filename
        )


def test_writer_returns_none_only_through_pytest_assertions(tmp_path):
    result = service.write_feature_label_refinement_execution_candidate_v1(
        tmp_path, filename="candidate.json"
    )

    assert result["status"] == "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_VALID"
