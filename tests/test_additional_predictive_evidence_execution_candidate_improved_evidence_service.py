from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow import services
from marketflow.services import (
    additional_predictive_evidence_execution_candidate_improved_evidence_service as candidate_service,
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("socket.socket.connect", lambda *_args, **_kwargs: pytest.fail("network access"))
    result = candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_candidate"] is False


def test_artifact_kind_and_candidate_status_are_exact(candidate: dict) -> None:
    assert candidate["artifact_kind"] == candidate_service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE
    assert candidate["candidate_status"] == candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_READY_FOR_OPERATOR_REVIEW


@pytest.mark.parametrize(("field", "expected"), list(candidate_service.BOUND_DIGESTS.items()))
def test_all_bound_digests_are_exact(candidate: dict, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_source_results_review_digest_is_bound(candidate: dict) -> None:
    assert candidate["source_results_review_digest"] == candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST


def test_dataset_universe_and_meta_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE
    assert candidate["target_universe_count"] == 12
    assert candidate["total_canonical_record_count"] == 11946
    assert candidate["records_digest"] == candidate_service.BOUND_DIGESTS["records_digest"]
    assert candidate["meta_record_count"] == 913
    assert candidate["non_meta_record_count"] == 1003


def test_source_review_and_candidate_readiness_are_true(candidate: dict) -> None:
    assert candidate["source_results_review_ready"] is True
    assert candidate["improved_evidence_planning_results_review_ready"] is True
    assert candidate["ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_using_improved_evidence_created"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review"] is True
    assert candidate["additional_predictive_evidence_execution_candidate_using_improved_evidence_review_created"] is False


@pytest.mark.parametrize("field", [
    "additional_predictive_evidence_execution_approved",
    "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
    "additional_predictive_evidence_results_created", "label_regeneration_authorized",
    "label_regeneration_performed", "new_targets_created", "target_definition_change_authorized",
    "target_definition_change_performed", "feature_generation_authorized",
    "feature_generation_performed", "feature_label_matrix_created",
    "metric_recomputation_performed_in_candidate", "model_training_performed_in_candidate",
    "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created",
    "trade_recommendations_generated", "provider_requests_made_in_candidate",
    "market_data_acquisition_performed_in_candidate", "canonical_dataset_regenerated_in_candidate",
    "predictive_evidence_execution_rerun_performed", "improved_evidence_planning_execution_rerun_performed",
])
def test_all_execution_and_acceptance_actions_remain_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_selected_direction_and_candidate_basis_are_preserved(candidate: dict) -> None:
    assert candidate["selected_redesign_direction"] == candidate_service.SELECTED_DIRECTION
    assert candidate["candidate_basis"] == candidate_service.CANDIDATE_BASIS


def test_candidate_objective_and_scope_are_exact(candidate: dict) -> None:
    assert candidate["additional_predictive_evidence_execution_candidate_objective"] == candidate_service.CANDIDATE_OBJECTIVE
    assert candidate["additional_predictive_evidence_execution_candidate_scope"] == candidate_service.CANDIDATE_SCOPE
    assert candidate["additional_predictive_evidence_execution_candidate_mode"] == "PLANNED_NOT_EXECUTED"
    assert candidate["additional_predictive_evidence_execution_candidate_authority_status"] == "NOT_AUTHORIZED"


def test_planned_source_inputs_are_defined(candidate: dict) -> None:
    assert [row["source_input_id"] for row in candidate["planned_source_inputs"]] == candidate_service.PLANNED_SOURCE_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in candidate["planned_source_inputs"])
    assert all(row["execution_authorized"] is False for row in candidate["planned_source_inputs"])


def test_planned_execution_activities_are_defined_not_executed(candidate: dict) -> None:
    activities = candidate["planned_execution_activities"]
    assert [row["activity_id"] for row in activities] == candidate_service.PLANNED_EXECUTION_ACTIVITY_IDS
    assert all(row["activity_status"] == "PLANNED_NOT_EXECUTED" for row in activities)
    assert all(row["execution_authorized"] is False and row["execution_performed"] is False for row in activities)


def test_label_feature_matrix_boundaries_are_closed(candidate: dict) -> None:
    assert candidate["label_feature_matrix_boundaries"] == candidate_service._label_feature_matrix_boundaries()


def test_model_families_are_planned_not_evaluated(candidate: dict) -> None:
    rows = candidate["planned_model_and_baseline_families"]
    assert [row["model_family_id"] for row in rows] == candidate_service.MODEL_FAMILY_IDS
    assert all(row["model_family_status"] == "PLANNED_NOT_EVALUATED" for row in rows)
    assert all(row["training_performed"] is False for row in rows)


def test_metric_families_are_planned_not_computed(candidate: dict) -> None:
    rows = candidate["planned_metric_families"]
    assert [row["metric_family_id"] for row in rows] == candidate_service.METRIC_FAMILY_IDS
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in rows)
    assert all(row["metric_computation_performed"] is False for row in rows)


def test_future_outputs_are_not_generated(candidate: dict) -> None:
    rows = candidate["planned_future_outputs"]
    assert [row["future_output_id"] for row in rows] == candidate_service.PLANNED_FUTURE_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_predictive_profitability_and_runtime_boundaries_remain_closed(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert candidate[field] == "NOT_AUTHORIZED"


def test_per_ticker_entries_count_and_meta_limitation(candidate: dict) -> None:
    entries = candidate["per_ticker_candidate_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["candidate_note"] == "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE"


def test_per_ticker_digests_are_present_and_deterministic(candidate: dict) -> None:
    for row in candidate["per_ticker_candidate_entries"]:
        digest = row["per_ticker_additional_predictive_evidence_execution_candidate_digest"]
        assert len(digest) == 64
        assert digest == candidate_service.per_ticker_additional_predictive_evidence_execution_candidate_digest_v1(row)


def test_next_chain_gates_and_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["next_chain"] == candidate_service.NEXT_CHAIN
    assert candidate["next_gates"] == candidate_service.NEXT_GATES
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(candidate: dict) -> None:
    assert len(candidate_service.REQUIRED_CHECK_IDS) == 78
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == candidate_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"]["total_checks"] == 78
    assert candidate["candidate_summary"]["passed_checks"] == 78
    assert candidate["candidate_summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    assert candidate["additional_predictive_evidence_execution_candidate_using_improved_evidence_digest"] == candidate_service.additional_predictive_evidence_execution_candidate_using_improved_evidence_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(candidate)
    assert result["status"] == candidate_service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE_USING_IMPROVED_EVIDENCE_VALID
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(("field", "value"), [
    ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"),
    ("source_results_review_digest", None), ("records_digest", None),
    ("target_universe", ["AAPL"]), ("target_universe_count", 11), ("meta_record_count", 1003),
    ("source_results_review_ready", False),
    ("ready_for_optional_additional_predictive_evidence_execution_candidate_using_improved_evidence", False),
    ("additional_predictive_evidence_execution_candidate_created", False),
    ("additional_predictive_evidence_execution_candidate_using_improved_evidence_ready_for_operator_review", False),
    ("additional_predictive_evidence_execution_approved", True),
    ("additional_predictive_evidence_execution_authorized", True),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True), ("label_regeneration_performed", True),
    ("new_targets_created", True), ("target_definition_change_authorized", True),
    ("feature_generation_performed", True), ("feature_label_matrix_created", True),
    ("metric_recomputation_performed_in_candidate", True), ("model_training_performed_in_candidate", True),
    ("predictive_usefulness", "accepted"), ("predictive_usefulness_acceptance_ready", True),
    ("predictive_usefulness_acceptance_candidate_created", True), ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True),
])
def test_validator_rejects_forbidden_or_changed_fields(candidate: dict, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(candidate_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError):
        candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(changed)


@pytest.mark.parametrize("field", [
    "candidate_basis", "planned_source_inputs", "planned_execution_activities",
    "label_feature_matrix_boundaries", "planned_model_and_baseline_families",
    "planned_metric_families", "next_chain", "risk_controls",
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest",
])
def test_validator_rejects_missing_required_structures(candidate: dict, field: str) -> None:
    changed = deepcopy(candidate)
    changed.pop(field)
    with pytest.raises(candidate_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError):
        candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_candidate_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_execution_candidate_digest"
    )
    with pytest.raises(candidate_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError):
        candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(changed)


def test_markdown_includes_all_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_markdown_v1(candidate)
    for section in (
        "## Title", "## Optional Additional Predictive Evidence Execution Candidate Using Improved Evidence",
        "## Source Improved Evidence Planning Results Review", "## Bound Evidence",
        "## Dataset and Universe", "## Candidate Basis", "## Candidate Objective",
        "## Planned Source Inputs", "## Planned Execution Activities",
        "## Label / Feature / Matrix Boundaries", "## Planned Model and Baseline Families",
        "## Planned Metric Families", "## Planned Future Outputs", "## Per-Ticker Candidate Entries",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_public_service_exports_are_available() -> None:
    assert services.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1 is candidate_service.build_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1
    assert services.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1 is candidate_service.validate_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1


def test_writer_is_no_overwrite_and_uses_temporary_directory(tmp_path) -> None:
    result = candidate_service.write_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(tmp_path)
    assert result["payload_byte_size"] > 0
    assert len(result["payload_sha256"]) == 64
    with pytest.raises(candidate_service.AdditionalPredictiveEvidenceExecutionCandidateImprovedEvidenceError):
        candidate_service.write_additional_predictive_evidence_execution_candidate_using_improved_evidence_v1(tmp_path)
