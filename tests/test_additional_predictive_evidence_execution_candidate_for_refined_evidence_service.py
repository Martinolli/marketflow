from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_for_refined_evidence_service as service,
)


def _candidate() -> dict:
    return service.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1()


def test_candidate_builds_offline_without_provider_or_source_replay(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("provider or source replay must not be called")

    monkeypatch.setattr(
        service.results_review,
        "build_feature_label_refinement_results_review_package_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.results_review.execution,
        "execute_feature_label_refinement_v1",
        forbidden,
    )

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["additional_predictive_evidence_execution_performed"] is False


def test_candidate_artifact_kind_and_status_are_exact() -> None:
    candidate = _candidate()

    assert candidate["artifact_kind"] == (
        service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE
    )
    assert candidate["candidate_status"] == (
        service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW
    )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_label_refinement_results_review_package_digest", service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("feature_label_refinement_execution_digest", service.EXPECTED_REFINEMENT_EXECUTION_DIGEST),
        ("feature_label_refinement_execution_approval_digest", service.EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST),
        ("feature_label_refinement_execution_candidate_review_package_digest", service.EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_REVIEW_DIGEST),
        ("feature_label_refinement_execution_candidate_digest", service.EXPECTED_REFINEMENT_EXECUTION_CANDIDATE_DIGEST),
        ("feature_label_refinement_plan_approval_digest", service.EXPECTED_REFINEMENT_PLAN_APPROVAL_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_digests_are_bound(field: str, expected: str) -> None:
    assert _candidate()[field] == expected


def test_target_universe_and_registry_metadata_are_exact() -> None:
    candidate = _candidate()

    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["registry_approved_dataset_metadata"] == (
        service.REGISTRY_APPROVED_DATASET_METADATA
    )
    assert candidate["total_canonical_record_count"] == 11946


def test_per_ticker_record_counts_preserve_meta_limitation() -> None:
    candidate = _candidate()

    assert candidate["meta_record_count"] == 913
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert all(
        candidate["per_ticker_record_counts"][ticker] == 1003
        for ticker in service.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_results_review_readiness_and_candidate_state_are_exact() -> None:
    candidate = _candidate()

    assert candidate["feature_label_refinement_results_review_ready"] is True
    assert candidate[
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning"
    ] is True
    assert candidate[
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence"
    ] is True
    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created"
    ] is True
    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review"
    ] is True


def test_candidate_objective_scope_mode_and_authority_are_exact() -> None:
    candidate = _candidate()

    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_objective"
    ] == service.CANDIDATE_OBJECTIVE
    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_scope"
    ] == service.CANDIDATE_SCOPE
    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_mode"
    ] == service.PLANNED_NOT_EXECUTED
    assert candidate[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status"
    ] == service.NOT_AUTHORIZED


def test_refinement_source_profile_is_bound_without_reading_outputs() -> None:
    candidate = _candidate()

    assert candidate["source_refinement_output_root"] == (
        ".marketflow/feature_label_refinement/expanded_universe_v1/"
    )
    assert candidate["source_refinement_output_count"] == 12
    assert candidate["source_refinement_output_status"] == "REVIEWED_AND_VERIFIED"
    assert candidate["source_refinement_results_review_ready"] is True
    assert candidate["dataset_name"] == "expanded_universe_canonical_dataset_v1"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("refined_label_family_count", 7),
        ("refined_label_coverage_entries", 84),
        ("refined_label_available_values", 82698),
        ("refined_label_unavailable_values", 924),
        ("refined_label_generation_digest", "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8"),
        ("refined_feature_group_count", 9),
        ("refined_feature_category_count", 11),
        ("refined_feature_field_count", 19),
        ("refined_feature_rows", 11946),
        ("refined_feature_null_or_unavailable_values", 1128),
        ("refined_feature_generation_digest", "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00"),
        ("refined_protocol_group_count", 6),
        ("chronological_splits", True),
        ("one_session_embargo", True),
        ("no_shuffle", True),
        ("no_lookahead", True),
        ("refined_walk_forward_fold_count", 4),
        ("refined_walk_forward_evaluation_rows", 3024),
        ("refined_oos_evaluation_rows", 2988),
        ("refined_oos_accuracy_range", "0.119813 to 0.480924"),
        ("model_comparison_group_count", 5),
        ("deterministic_comparisons_evaluated", 7),
        ("unavailable_model_family_requests", 3),
        ("unavailable_model_family_status", "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"),
        ("refined_leakage_status", "PASS"),
        ("failed_leakage_controls", 0),
        ("data_quality_status", "PASS_WITH_PRESERVED_SOURCE_LIMITATION"),
    ],
)
def test_refined_evidence_facts_are_preserved(field: str, expected) -> None:
    assert _candidate()[field] == expected


def test_planned_refined_evidence_inputs_are_reviewed_not_reexecuted() -> None:
    inputs = _candidate()["planned_refined_evidence_inputs"]

    assert [item["input_id"] for item in inputs] == (
        service.PLANNED_REFINED_EVIDENCE_INPUT_IDS
    )
    assert all(
        item["source_status"] == service.SOURCE_REVIEWED_NOT_REEXECUTED
        for item in inputs
    )
    assert all(
        item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in inputs
    )


def test_planned_execution_activities_are_not_authorized_or_executed() -> None:
    activities = _candidate()["planned_execution_activities"]

    assert [item["activity_id"] for item in activities] == (
        service.PLANNED_EXECUTION_ACTIVITY_IDS
    )
    assert all(
        item["execution_status"] == service.PLANNED_NOT_EXECUTED
        for item in activities
    )
    assert all(
        item["authority_status"] == service.NOT_AUTHORIZED_FOR_EXECUTION
        for item in activities
    )
    assert all(
        item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in activities
    )


def test_planned_outputs_are_not_generated_and_research_only() -> None:
    outputs = _candidate()["planned_outputs"]

    assert [item["output_id"] for item in outputs] == service.PLANNED_OUTPUT_IDS
    assert all(
        item["generation_status"] == service.PLANNED_NOT_GENERATED
        for item in outputs
    )
    assert all(
        item["actionability_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def test_per_ticker_entries_are_complete_ordered_and_digest_bound() -> None:
    entries = _candidate()["per_ticker_candidate_entries"]
    digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )

    assert len(entries) == 12
    assert [item["ticker"] for item in entries] == service.TARGET_UNIVERSE
    assert all(item[digest_key] for item in entries)
    assert all(
        item[digest_key]
        == service.per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
            item
        )
        for item in entries
    )
    meta = next(item for item in entries if item["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["refinement_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG_IN_REFINED_EVIDENCE_CHAIN"
    )
    assert all(
        item["historical_record_count"] == 1003
        and item["meta_reduced_record_count_flag"] is False
        for item in entries
        if item["ticker"] != "META"
    )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("future_refined_evidence_execution_chain", service.FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN),
        ("future_gates", service.FUTURE_GATES),
        ("risk_controls", service.RISK_CONTROLS),
    ],
)
def test_future_chain_gates_and_risk_controls_are_defined(
    field: str, expected: list[str]
) -> None:
    assert _candidate()[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_generation_performed",
        "canonical_dataset_regenerated",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_performed",
        "model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",
        "additional_predictive_evidence_execution_for_refined_evidence_approved",
        "additional_predictive_evidence_execution_for_refined_evidence_authorized",
        "additional_predictive_evidence_execution_for_refined_evidence_executed",
        "additional_predictive_evidence_results_for_refined_evidence_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
    ],
)
def test_execution_acceptance_and_runtime_flags_remain_false(field: str) -> None:
    assert _candidate()[field] is False


def test_predictive_profitability_and_runtime_authorities_remain_closed() -> None:
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED
    assert candidate["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert candidate[field] == service.NOT_AUTHORIZED


def test_checklist_contains_all_required_ids_and_passes() -> None:
    checklist = _candidate()["candidate_checklist"]

    assert [item["check_id"] for item in checklist] == service.REQUIRED_CHECK_IDS
    assert all(item["status"] == service.PASS for item in checklist)
    assert all(
        set(item) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for item in checklist
    )


def test_summary_counts_and_downstream_readiness_are_exact() -> None:
    summary = _candidate()["candidate_summary"]

    assert summary["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 75
    assert summary["passed_checks"] == 75
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True
    assert summary[
        "ready_for_additional_predictive_evidence_execution_approval_for_refined_evidence"
    ] is False
    assert summary[
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence"
    ] is False


def test_candidate_digest_is_deterministic() -> None:
    first = _candidate()
    second = _candidate()
    field = (
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )

    assert first[field] == second[field]
    assert first[field] == (
        service.additional_predictive_evidence_execution_candidate_for_refined_evidence_digest_v1(
            first
        )
    )


def test_per_ticker_digests_are_deterministic() -> None:
    first = _candidate()["per_ticker_candidate_entries"]
    second = _candidate()["per_ticker_candidate_entries"]
    field = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )

    assert [item[field] for item in first] == [item[field] for item in second]


def test_validator_accepts_valid_candidate() -> None:
    result = service.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
        _candidate()
    )

    assert result["status"] == (
        service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_VALID
    )
    assert result["ready_for_operator_review"] is True
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"),
        (("candidate_status",), "WRONG"),
        (("feature_label_refinement_results_review_package_digest",), "0" * 64),
        (("feature_label_refinement_execution_digest",), "0" * 64),
        (("feature_label_refinement_results_review_ready",), False),
        (("feature_label_refinement_results_support_future_additional_predictive_evidence_planning",), False),
        (("ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",), False),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_created",), False),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status",), "AUTHORIZED"),
        (("target_universe_count",), 11),
        (("target_universe",), list(reversed(service.TARGET_UNIVERSE))),
        (("total_canonical_record_count",), 11945),
        (("records_digest",), "0" * 64),
        (("meta_record_count",), 1003),
        (("per_ticker_record_counts", "MSFT"), 1002),
        (("refined_label_family_count",), 6),
        (("refined_feature_group_count",), 8),
        (("refined_feature_field_count",), 18),
        (("model_comparison_group_count",), 4),
        (("refined_leakage_status",), "FAIL"),
        (("failed_leakage_controls",), 1),
        (("additional_predictive_evidence_execution_for_refined_evidence_approved",), True),
        (("additional_predictive_evidence_execution_for_refined_evidence_authorized",), True),
        (("additional_predictive_evidence_execution_for_refined_evidence_executed",), True),
        (("additional_predictive_evidence_results_for_refined_evidence_created",), True),
        (("predictive_usefulness",), "accepted"),
        (("predictive_usefulness_acceptance_ready",), True),
        (("predictive_usefulness_acceptance_recommended",), True),
        (("predictive_usefulness_acceptance_candidate_created",), True),
        (("profitability",), "accepted"),
        (("profitability_acceptance_ready",), True),
        (("profitability_acceptance_recommended",), True),
        (("runtime_migration_approved",), True),
        (("runtime_use",), "AUTHORIZED"),
        (("strategy_use",), "AUTHORIZED"),
        (("paper_trading",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("automatic_stitching",), True),
        (("feature_label_refinement_execution_rerun_performed",), True),
        (("refined_label_generation_rerun_performed",), True),
        (("refined_feature_generation_rerun_performed",), True),
        (("refined_metrics_recomputation_performed",), True),
        (("model_comparison_rerun_performed",), True),
        (("new_strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
    ],
)
def test_validator_rejects_contract_mutations(
    path: tuple[str, ...], bad_value
) -> None:
    candidate = deepcopy(_candidate())
    target = candidate
    for field in path[:-1]:
        target = target[field]
    target[path[-1]] = bad_value

    with pytest.raises(
        service.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError
    ):
        service.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            candidate
        )


@pytest.mark.parametrize(
    "field",
    [
        "planned_refined_evidence_inputs",
        "planned_execution_activities",
        "planned_outputs",
        "future_refined_evidence_execution_chain",
        "future_gates",
        "risk_controls",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",
    ],
)
def test_validator_rejects_missing_planning_or_digest_fields(field: str) -> None:
    candidate = deepcopy(_candidate())
    candidate.pop(field)

    with pytest.raises(
        service.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError
    ):
        service.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            candidate
        )


def test_validator_rejects_missing_per_ticker_digest() -> None:
    candidate = deepcopy(_candidate())
    candidate["per_ticker_candidate_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )

    with pytest.raises(
        service.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError
    ):
        service.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            candidate
        )


def test_markdown_includes_all_required_sections() -> None:
    markdown = service.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_markdown_v1(
        _candidate()
    )

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Execution Candidate for Refined Evidence",
        "## Source Feature/Label Refinement Results Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Refined Evidence Source Profile",
        "## Refined Evidence Facts",
        "## Planned Refined Evidence Inputs",
        "## Planned Execution Activities",
        "## Planned Outputs",
        "## Per-Ticker Candidate Entries",
        "## Future Refined-Evidence Execution Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Execution Boundary",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_emits_canonical_json_and_refuses_overwrite(tmp_path) -> None:
    result = service.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
        tmp_path
    )
    path = tmp_path / result["filename"]
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload == _candidate()
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"]
    with pytest.raises(
        service.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError
    ):
        service.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            tmp_path
        )


@pytest.mark.parametrize("filename", ["../candidate.json", "candidate.txt", "nested/candidate.json"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename: str) -> None:
    with pytest.raises(
        service.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceError
    ):
        service.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1(
            tmp_path, filename=filename
        )
