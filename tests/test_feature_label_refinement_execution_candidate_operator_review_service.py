from __future__ import annotations

import json

import pytest

from marketflow.services import feature_label_refinement_execution_candidate_operator_review_service as service


def _review() -> dict:
    return service.build_feature_label_refinement_execution_candidate_review_package_v1()


def _resign(review: dict) -> dict:
    review["review_checklist"] = service._checklist(review)
    review["review_summary"] = service._summary(review["review_checklist"])
    review["feature_label_refinement_execution_candidate_review_package_digest"] = (
        service.feature_label_refinement_execution_candidate_review_package_digest_v1(
            review
        )
    )
    return review


def test_review_builds_offline_without_provider_or_approval_replay(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("provider/approval replay path must not be called")

    monkeypatch.setattr(
        service.candidate_service.approval_service,
        "build_feature_label_refinement_plan_approved_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.candidate_service.plan_service,
        "build_feature_label_refinement_plan_candidate_v1",
        forbidden,
    )

    review = _review()

    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["execution_candidate_binding_mode"] == service.EXECUTION_CANDIDATE_BUILT_OFFLINE_BINDING


def test_review_accepts_an_explicit_valid_candidate_binding():
    candidate = service.candidate_service.build_feature_label_refinement_execution_candidate_v1()
    review = service.build_feature_label_refinement_execution_candidate_review_package_v1(candidate)

    assert review["execution_candidate_binding_mode"] == service.EXECUTION_CANDIDATE_OBJECT_BINDING
    assert review["reviewed_feature_label_refinement_execution_candidate_digest"] == service.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    assert service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)["ready_for_operator_assessment"] is True


def test_review_rejects_an_invalid_explicit_candidate():
    candidate = service.candidate_service.build_feature_label_refinement_execution_candidate_v1()
    candidate["feature_label_refinement_execution_authorized"] = True

    with pytest.raises(service.candidate_service.FeatureLabelRefinementExecutionCandidateError):
        service.build_feature_label_refinement_execution_candidate_review_package_v1(candidate)


def test_review_identity_and_status_are_exact():
    review = _review()

    assert review["artifact_kind"] == service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE
    assert review["schema_version"] == service.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_V1
    assert review["review_status"] == service.FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY
    assert review["feature_label_refinement_execution_candidate_review_created"] is True


def test_reviewed_candidate_evidence_is_exact_and_zero_blocker():
    review = _review()

    assert review["reviewed_feature_label_refinement_execution_candidate_kind"] == service.candidate_service.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE
    assert review["reviewed_feature_label_refinement_execution_candidate_status"] == service.candidate_service.FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert review["reviewed_feature_label_refinement_execution_candidate_digest"] == service.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    assert review["reviewed_feature_label_refinement_execution_candidate_checklist_total"] == 81
    assert review["reviewed_feature_label_refinement_execution_candidate_checklist_passed"] == 81
    assert review["reviewed_feature_label_refinement_execution_candidate_checklist_failed"] == 0
    assert review["reviewed_feature_label_refinement_execution_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_label_refinement_execution_candidate_digest", service.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("feature_label_refinement_plan_approval_digest", service.candidate_service.EXPECTED_PLAN_APPROVAL_DIGEST),
        ("feature_label_refinement_plan_candidate_review_package_digest", service.candidate_service.EXPECTED_PLAN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_plan_candidate_digest", service.candidate_service.EXPECTED_PLAN_CANDIDATE_DIGEST),
        ("predictive_evidence_improvement_candidate_review_package_digest", service.candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("predictive_evidence_improvement_candidate_digest", service.candidate_service.EXPECTED_IMPROVEMENT_CANDIDATE_DIGEST),
        ("predictive_usefulness_acceptance_readiness_review_digest", service.candidate_service.EXPECTED_READINESS_REVIEW_DIGEST),
        ("predictive_usefulness_reassessment_review_package_digest", service.candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", service.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", service.candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("research_registry_approval_digest", service.candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", service.candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", service.candidate_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(field, expected):
    assert _review()[field] == expected


def test_target_universe_and_record_counts_are_exact():
    review = _review()

    assert review["target_universe"] == service.TARGET_UNIVERSE
    assert review["target_universe_count"] == 12
    assert review["per_ticker_record_counts"]["META"] == 913
    assert all(
        review["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_reviewed_objective_scope_mode_and_authority_are_exact():
    review = _review()

    assert review["feature_label_refinement_execution_candidate_objective"] == service.candidate_service.EXECUTION_CANDIDATE_OBJECTIVE
    assert review["feature_label_refinement_execution_candidate_scope"] == service.candidate_service.EXECUTION_CANDIDATE_SCOPE
    assert review["feature_label_refinement_execution_mode"] == service.candidate_service.PLANNED_NOT_EXECUTED
    assert review["feature_label_refinement_execution_authority_status"] == service.NOT_AUTHORIZED


def test_reviewed_readiness_basis_and_profile_are_exact():
    review = _review()

    assert review["reviewed_readiness_failure_basis"] == service.candidate_service._readiness_failure_basis()
    assert review["reviewed_execution_candidate_profile"] == service.candidate_service._execution_candidate_profile()
    assert review["reviewed_readiness_failure_basis"]["readiness_decision"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
    assert review["reviewed_readiness_failure_basis"]["readiness_reason"] == "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE"


def test_reviewed_execution_steps_are_complete_and_unauthorized():
    steps = _review()["reviewed_planned_execution_steps"]

    assert [item["step_id"] for item in steps] == service.candidate_service.PLANNED_EXECUTION_STEP_IDS
    assert len(steps) == 13
    assert all(item["execution_status"] == service.candidate_service.PLANNED_NOT_EXECUTED for item in steps)
    assert all(item["authorization_status"] == service.candidate_service.NOT_AUTHORIZED_FOR_EXECUTION for item in steps)
    assert all(item["actionability_label"] == service.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in steps)


@pytest.mark.parametrize(
    ("field", "group_ids"),
    [
        ("reviewed_label_refinement_execution_groups", service.candidate_service.LABEL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("reviewed_feature_refinement_execution_groups", service.candidate_service.FEATURE_REFINEMENT_EXECUTION_GROUP_IDS),
        ("reviewed_protocol_refinement_execution_groups", service.candidate_service.PROTOCOL_REFINEMENT_EXECUTION_GROUP_IDS),
        ("reviewed_model_comparison_execution_groups", service.candidate_service.MODEL_COMPARISON_EXECUTION_GROUP_IDS),
    ],
)
def test_reviewed_groups_are_complete_research_only_and_unauthorized(field, group_ids):
    groups = _review()[field]

    assert [item["group_id"] for item in groups] == group_ids
    assert all(item["execution_candidate_status"] == service.candidate_service.PLANNED_FOR_EXECUTION_CANDIDATE_ONLY for item in groups)
    assert all(item["authorization_status"] == service.NOT_AUTHORIZED for item in groups)
    assert all(item["execution_status"] == service.candidate_service.NOT_EXECUTED for item in groups)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in groups)


def test_reviewed_outputs_are_complete_not_generated_and_research_only():
    outputs = _review()["reviewed_planned_execution_outputs"]

    assert [item["output_name"] for item in outputs] == service.candidate_service.PLANNED_EXECUTION_OUTPUT_NAMES
    assert len(outputs) == 12
    assert all(item["generation_status"] == service.candidate_service.PLANNED_NOT_GENERATED for item in outputs)
    assert all(item["actionability_label"] == service.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs)


def test_per_ticker_review_entries_preserve_meta_and_all_boundaries():
    entries = _review()["per_ticker_execution_candidate_review_entries"]

    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["refinement_note"] == "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_FEATURE_PLAN"
    assert all(entry["historical_record_count"] == 1003 for entry in entries if entry["ticker"] != "META")
    assert all(entry["feature_label_refinement_execution_candidate_review_status"] == service.READY_FOR_OPERATOR_ASSESSMENT for entry in entries)
    assert all(entry["feature_label_refinement_execution_authorized"] is False for entry in entries)
    assert all(entry["feature_label_refinement_executed"] is False for entry in entries)
    assert all(entry["source_feature_label_refinement_execution_candidate_digest"] == service.EXPECTED_EXECUTION_CANDIDATE_DIGEST for entry in entries)


def test_per_ticker_candidate_and_review_digests_are_present_and_deterministic():
    first = _review()["per_ticker_execution_candidate_review_entries"]
    second = _review()["per_ticker_execution_candidate_review_entries"]

    assert first == second
    for entry in first:
        assert len(entry["per_ticker_feature_label_refinement_execution_candidate_digest"]) == 64
        digest = entry["per_ticker_feature_label_refinement_execution_candidate_review_digest"]
        assert len(digest) == 64
        assert digest == service.per_ticker_feature_label_refinement_execution_candidate_review_digest_v1(entry)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
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
    assert _review()[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_authority_remains_not_authorized(field):
    assert _review()[field] == service.NOT_AUTHORIZED


def test_reviewed_future_chain_gates_and_risk_controls_are_exact():
    review = _review()

    assert review["reviewed_future_execution_chain"] == service.candidate_service.FUTURE_EXECUTION_CHAIN
    assert review["reviewed_future_gates"] == service.candidate_service.FUTURE_GATES
    assert review["reviewed_risk_controls"] == service.candidate_service.RISK_CONTROLS


def test_checklist_contains_all_required_checks_and_all_pass():
    review = _review()
    checklist = review["review_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(item["severity"] == service.BLOCKER for item in checklist)


def test_summary_counts_and_boundaries_are_exact():
    summary = _review()["review_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 89
    assert summary["passed_checks"] == 89
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_feature_label_refinement_execution_approval"] is False
    assert summary["ready_for_feature_label_refinement_execution"] is False
    assert summary["ready_for_additional_predictive_evidence_execution_candidate"] is False
    assert summary["predictive_usefulness_accepted"] is False
    assert summary["profitability_accepted"] is False
    assert summary["runtime_migration_authorized"] is False


def test_review_digest_is_deterministic_and_semantic():
    first = _review()
    second = _review()

    assert first["feature_label_refinement_execution_candidate_review_package_digest"] == second["feature_label_refinement_execution_candidate_review_package_digest"]
    assert first["feature_label_refinement_execution_candidate_review_package_digest"] == service.feature_label_refinement_execution_candidate_review_package_digest_v1(first)


def test_validator_accepts_valid_review_package():
    validation = service.validate_feature_label_refinement_execution_candidate_review_package_v1(_review())

    assert validation["status"] == "FEATURE_LABEL_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_operator_assessment"] is True
    assert validation["blocker_count"] == 0
    assert validation["feature_label_refinement_execution_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_feature_label_refinement_execution_candidate_digest", "0" * 64),
        ("reviewed_feature_label_refinement_execution_candidate_status", "WRONG"),
        ("feature_label_refinement_execution_candidate_digest", "0" * 64),
        ("feature_label_refinement_plan_approval_digest", "0" * 64),
        ("feature_label_refinement_plan_candidate_review_package_digest", "0" * 64),
        ("feature_label_refinement_plan_approved", False),
        ("ready_for_feature_label_refinement_execution_candidate", False),
        ("feature_label_refinement_execution_candidate_created", False),
        ("feature_label_refinement_execution_candidate_review_created", False),
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
    review = _review()
    review[field] = value
    _resign(review)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_validator_rejects_target_universe_mismatch():
    review = _review()
    review["target_universe"] = list(reversed(review["target_universe"]))
    _resign(review)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("reviewed_planned_execution_steps", []),
        ("reviewed_planned_execution_outputs", []),
        ("reviewed_future_execution_chain", []),
        ("reviewed_future_gates", []),
        ("reviewed_risk_controls", []),
    ],
)
def test_validator_rejects_missing_reviewed_contract_sections(field, replacement):
    review = _review()
    review[field] = replacement
    _resign(review)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_validator_rejects_changed_readiness_decision_and_reason():
    for field, value in (
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "READY"),
    ):
        review = _review()
        review["reviewed_readiness_failure_basis"][field] = value
        _resign(review)
        with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
            service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_validator_rejects_missing_or_changed_per_ticker_candidate_digest():
    for value in (None, "0" * 64):
        review = _review()
        review["per_ticker_execution_candidate_review_entries"][0][
            "per_ticker_feature_label_refinement_execution_candidate_digest"
        ] = value
        _resign(review)
        with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
            service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_validator_rejects_missing_or_changed_per_ticker_review_digest():
    for value in (None, "0" * 64):
        review = _review()
        review["per_ticker_execution_candidate_review_entries"][0][
            "per_ticker_feature_label_refinement_execution_candidate_review_digest"
        ] = value
        _resign(review)
        with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
            service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


@pytest.mark.parametrize("forbidden", sorted(service.FORBIDDEN_ARTIFACT_VALUES))
def test_validator_rejects_forbidden_artifact_values_at_any_depth(forbidden):
    review = _review()
    review["nested_probe"] = {"value": forbidden}
    _resign(review)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_validator_rejects_missing_review_package_digest():
    review = _review()
    review.pop("feature_label_refinement_execution_candidate_review_package_digest")

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.validate_feature_label_refinement_execution_candidate_review_package_v1(review)


def test_markdown_contains_all_required_sections_and_guardrails():
    markdown = service.build_feature_label_refinement_execution_candidate_review_markdown_v1(_review())

    for section in (
        "## Title",
        "## Feature/Label Refinement Execution Candidate Review Package",
        "## Reviewed Execution Candidate",
        "## Source Plan Approval",
        "## Execution Candidate Objective",
        "## Readiness Failure Basis",
        "## Execution Candidate Profile",
        "## Reviewed Planned Execution Steps",
        "## Reviewed Label Refinement Execution Groups",
        "## Reviewed Feature Refinement Execution Groups",
        "## Reviewed Protocol Refinement Execution Groups",
        "## Reviewed Model Comparison Execution Groups",
        "## Per-Ticker Execution Candidate Review Entries",
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
    assert "Review only" in markdown


def test_writer_creates_canonical_json_in_requested_directory(tmp_path):
    result = service.write_feature_label_refinement_execution_candidate_review_package_v1(tmp_path)
    path = tmp_path / "feature_label_refinement_execution_candidate_review_v1.json"

    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload == _review()
    assert result["filename"] == path.name
    assert result["payload_byte_size"] == path.stat().st_size
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_to_overwrite_existing_output(tmp_path):
    service.write_feature_label_refinement_execution_candidate_review_package_v1(tmp_path)

    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.write_feature_label_refinement_execution_candidate_review_package_v1(tmp_path)


@pytest.mark.parametrize("filename", ["review.txt", "../review.json", "nested/review.json"])
def test_writer_rejects_non_simple_json_filename(tmp_path, filename):
    with pytest.raises(service.FeatureLabelRefinementExecutionCandidateReviewPackageError):
        service.write_feature_label_refinement_execution_candidate_review_package_v1(
            tmp_path, filename=filename
        )
