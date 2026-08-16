from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_for_refined_evidence_operator_review_service as review,
)


def _package() -> dict:
    return review.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1()


def test_review_package_builds_offline_without_provider_or_evidence_replay(
    monkeypatch,
) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("provider or evidence replay must not be called")

    monkeypatch.setattr(
        review.candidate_service.results_review,
        "build_feature_label_refinement_results_review_package_v1",
        forbidden,
    )
    monkeypatch.setattr(
        review.candidate_service.results_review.execution,
        "execute_feature_label_refinement_v1",
        forbidden,
    )

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["additional_predictive_evidence_execution_performed"] is False


def test_review_artifact_kind_and_status_are_exact() -> None:
    package = _package()

    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_READY
    )


def test_reviewed_candidate_identity_checklist_and_digest_are_exact() -> None:
    package = _package()

    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_kind"
    ] == (
        review.candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE
    )
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_status"
    ] == (
        review.candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_READY_FOR_OPERATOR_REVIEW
    )
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    ] == review.EXPECTED_CANDIDATE_DIGEST
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_total"
    ] == 75
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_passed"
    ] == 75
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_checklist_failed"
    ] == 0
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_blocker_count"
    ] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest", review.EXPECTED_CANDIDATE_DIGEST),
        ("feature_label_refinement_results_review_package_digest", review.candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("feature_label_refinement_execution_digest", review.candidate_service.EXPECTED_REFINEMENT_EXECUTION_DIGEST),
        ("feature_label_refinement_execution_approval_digest", review.candidate_service.EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", review.candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", review.candidate_service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST),
        ("research_registry_approval_digest", review.candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", review.candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", review.candidate_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_digests_are_bound(field: str, expected: str) -> None:
    assert _package()[field] == expected


def test_target_universe_registry_metadata_and_record_counts_are_exact() -> None:
    package = _package()

    assert package["target_universe_count"] == 12
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["registry_approved_dataset_metadata"] == (
        review.candidate_service.REGISTRY_APPROVED_DATASET_METADATA
    )
    assert package["total_canonical_record_count"] == 11946
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in review.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_results_review_candidate_and_review_readiness_are_preserved() -> None:
    package = _package()

    for field in (
        "feature_label_refinement_results_review_ready",
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning",
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_created",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_ready_for_operator_review",
    ):
        assert package[field] is True


def test_reviewed_candidate_objective_scope_mode_and_authority_are_exact() -> None:
    package = _package()

    assert package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_objective"
    ] == review.candidate_service.CANDIDATE_OBJECTIVE
    assert package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_scope"
    ] == review.candidate_service.CANDIDATE_SCOPE
    assert package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_mode"
    ] == review.candidate_service.PLANNED_NOT_EXECUTED
    assert package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status"
    ] == review.NOT_AUTHORIZED


def test_refinement_source_profile_is_preserved() -> None:
    package = _package()

    assert package["source_refinement_output_root"] == (
        ".marketflow/feature_label_refinement/expanded_universe_v1/"
    )
    assert package["source_refinement_output_count"] == 12
    assert package["source_refinement_output_status"] == "REVIEWED_AND_VERIFIED"
    assert package["source_refinement_results_review_ready"] is True
    assert package["dataset_name"] == "expanded_universe_canonical_dataset_v1"


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
    assert _package()[field] == expected


def test_reviewed_inputs_are_complete_and_not_reexecuted() -> None:
    inputs = _package()["reviewed_planned_refined_evidence_inputs"]

    assert [item["input_id"] for item in inputs] == (
        review.candidate_service.PLANNED_REFINED_EVIDENCE_INPUT_IDS
    )
    assert all(
        item["source_status"] == review.candidate_service.SOURCE_REVIEWED_NOT_REEXECUTED
        for item in inputs
    )
    assert all(
        item["actionability_label"]
        == review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in inputs
    )


def test_reviewed_activities_are_complete_not_authorized_or_executed() -> None:
    activities = _package()["reviewed_planned_execution_activities"]

    assert [item["activity_id"] for item in activities] == (
        review.candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
    )
    assert all(
        item["execution_status"] == review.candidate_service.PLANNED_NOT_EXECUTED
        for item in activities
    )
    assert all(
        item["authority_status"]
        == review.candidate_service.NOT_AUTHORIZED_FOR_EXECUTION
        for item in activities
    )


def test_reviewed_outputs_are_ten_not_generated_and_research_only() -> None:
    outputs = _package()["reviewed_planned_outputs"]

    assert len(outputs) == 10
    assert [item["output_id"] for item in outputs] == (
        review.candidate_service.PLANNED_OUTPUT_IDS
    )
    assert all(
        item["generation_status"] == review.candidate_service.PLANNED_NOT_GENERATED
        for item in outputs
    )
    assert all(
        item["actionability_label"]
        == review.candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
        for item in outputs
    )


def test_per_ticker_review_entries_are_complete_ordered_and_digest_bound() -> None:
    entries = _package()["per_ticker_candidate_review_entries"]
    candidate_digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    )
    review_digest_key = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"
    )

    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == review.TARGET_UNIVERSE
    assert all(entry[candidate_digest_key] for entry in entries)
    assert all(entry[review_digest_key] for entry in entries)
    assert all(
        entry[review_digest_key]
        == review.per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest_v1(
            entry
        )
        for entry in entries
    )
    assert all(
        entry[
            "source_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
        ]
        == review.EXPECTED_CANDIDATE_DIGEST
        for entry in entries
    )
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("reviewed_future_refined_evidence_execution_chain", review.candidate_service.FUTURE_REFINED_EVIDENCE_EXECUTION_CHAIN),
        ("reviewed_future_gates", review.candidate_service.FUTURE_GATES),
        ("reviewed_risk_controls", review.candidate_service.RISK_CONTROLS),
    ],
)
def test_reviewed_future_chain_gates_and_risk_controls_are_exact(
    field: str, expected: list[str]
) -> None:
    assert _package()[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_performed",
        "model_comparison_rerun_performed",
        "additional_predictive_evidence_execution_performed",
        "additional_predictive_evidence_execution_approval_created",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
    assert _package()[field] is False


def test_predictive_profitability_and_runtime_authorities_remain_closed() -> None:
    package = _package()

    assert package["predictive_usefulness"] == review.NOT_ACCEPTED
    assert package["profitability"] == review.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert package[field] == review.NOT_AUTHORIZED


def test_checklist_contains_all_required_ids_and_passes() -> None:
    checklist = _package()["review_checklist"]

    assert [item["check_id"] for item in checklist] == review.REQUIRED_CHECK_IDS
    assert all(item["status"] == review.PASS for item in checklist)
    assert all(
        set(item) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for item in checklist
    )


def test_summary_counts_and_downstream_readiness_are_exact() -> None:
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS) == 84
    assert summary["passed_checks"] == 84
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary[
        "ready_for_additional_predictive_evidence_execution_approval_for_refined_evidence"
    ] is False
    assert summary[
        "ready_for_additional_predictive_evidence_execution_for_refined_evidence"
    ] is False


def test_review_package_digest_is_deterministic() -> None:
    first = _package()
    second = _package()
    field = (
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"
    )

    assert first[field] == second[field]
    assert first[field] == (
        review.additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest_v1(
            first
        )
    )


def test_per_ticker_review_digests_are_deterministic() -> None:
    first = _package()["per_ticker_candidate_review_entries"]
    second = _package()["per_ticker_candidate_review_entries"]
    field = (
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest"
    )

    assert [entry[field] for entry in first] == [entry[field] for entry in second]


def test_build_accepts_exact_explicit_candidate() -> None:
    candidate = (
        review.candidate_service.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_v1()
    )
    package = review.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        candidate
    )

    assert package["candidate_binding_mode"] == review.CANDIDATE_OBJECT_BINDING
    assert package[
        "reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest"
    ] == review.EXPECTED_CANDIDATE_DIGEST


def test_validator_accepts_valid_review_package() -> None:
    result = review.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        _package()
    )

    assert result["status"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_FOR_REFINED_EVIDENCE_REVIEW_PACKAGE_VALID
    )
    assert result["ready_for_operator_assessment"] is True
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"),
        (("review_status",), "WRONG"),
        (("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",), "0" * 64),
        (("reviewed_additional_predictive_evidence_execution_candidate_for_refined_evidence_status",), "WRONG"),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",), "0" * 64),
        (("feature_label_refinement_results_review_package_digest",), "0" * 64),
        (("feature_label_refinement_execution_digest",), "0" * 64),
        (("feature_label_refinement_results_review_ready",), False),
        (("feature_label_refinement_results_support_future_additional_predictive_evidence_planning",), False),
        (("ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",), False),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_created",), False),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_review_created",), False),
        (("additional_predictive_evidence_execution_candidate_for_refined_evidence_authority_status",), "AUTHORIZED"),
        (("target_universe_count",), 11),
        (("target_universe",), list(reversed(review.TARGET_UNIVERSE))),
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
        (("additional_predictive_evidence_execution_approval_created",), True),
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
    package = deepcopy(_package())
    target = package
    for field in path[:-1]:
        target = target[field]
    target[path[-1]] = bad_value

    with pytest.raises(
        review.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError
    ):
        review.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_planned_refined_evidence_inputs",
        "reviewed_planned_execution_activities",
        "reviewed_planned_outputs",
        "reviewed_future_refined_evidence_execution_chain",
        "reviewed_future_gates",
        "reviewed_risk_controls",
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest",
    ],
)
def test_validator_rejects_missing_planning_or_digest_fields(field: str) -> None:
    package = deepcopy(_package())
    package.pop(field)

    with pytest.raises(
        review.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError
    ):
        review.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
            package
        )


@pytest.mark.parametrize(
    "digest_field",
    [
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_digest",
        "per_ticker_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(digest_field: str) -> None:
    package = deepcopy(_package())
    package["per_ticker_candidate_review_entries"][0].pop(digest_field)

    with pytest.raises(
        review.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError
    ):
        review.validate_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
            package
        )


def test_markdown_includes_all_required_sections() -> None:
    markdown = review.build_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_markdown_v1(
        _package()
    )

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Execution Candidate for Refined Evidence Review Package",
        "## Reviewed Candidate",
        "## Source Feature/Label Refinement Results Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Refined Evidence Source Profile",
        "## Refined Evidence Facts",
        "## Reviewed Refined Evidence Inputs",
        "## Reviewed Execution Activities",
        "## Reviewed Planned Outputs",
        "## Per-Ticker Candidate Review Entries",
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
    result = review.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
        tmp_path
    )
    path = tmp_path / result["filename"]
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload == _package()
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"]
    with pytest.raises(
        review.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError
    ):
        review.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
            tmp_path
        )


@pytest.mark.parametrize(
    "filename", ["../review.json", "review.txt", "nested/review.json"]
)
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename: str) -> None:
    with pytest.raises(
        review.AdditionalPredictiveEvidenceExecutionCandidateForRefinedEvidenceReviewPackageError
    ):
        review.write_additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_v1(
            tmp_path, filename=filename
        )
