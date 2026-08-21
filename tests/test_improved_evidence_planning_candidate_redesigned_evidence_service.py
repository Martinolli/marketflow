from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    improved_evidence_planning_candidate_redesigned_evidence_service as candidate_service,
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_candidate"] is False
    assert result["market_data_acquisition_performed_in_candidate"] is False


def test_artifact_kind_is_correct(candidate: dict) -> None:
    assert candidate["artifact_kind"] == candidate_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE


def test_candidate_status_is_correct(candidate: dict) -> None:
    assert candidate["candidate_status"] == candidate_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW


@pytest.mark.parametrize(
    ("field", "expected"),
    list(candidate_service.BOUND_DIGESTS.items()),
)
def test_bound_digest_is_exact(candidate: dict, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_source_results_review_digest_is_bound(candidate: dict) -> None:
    assert candidate["source_results_review_digest"] == candidate_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST


def test_universe_count_and_order_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(candidate: dict) -> None:
    assert candidate["meta_record_count"] == 913
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_source_results_review_ready_is_true(candidate: dict) -> None:
    assert candidate["source_results_review_ready"] is True
    assert candidate["label_objective_redesign_results_review_ready"] is True


def test_ready_for_planning_candidate_is_true(candidate: dict) -> None:
    assert candidate["ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"] is True


def test_planning_candidate_created_and_ready_are_true(candidate: dict) -> None:
    assert candidate["improved_evidence_planning_candidate_created"] is True
    assert candidate["improved_evidence_planning_candidate_using_redesigned_evidence_created"] is True
    assert candidate["improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review"] is True


def test_planning_approval_and_execution_are_false(candidate: dict) -> None:
    assert candidate["improved_evidence_planning_approved"] is False
    assert candidate["improved_evidence_planning_authorized"] is False
    assert candidate["improved_evidence_planning_executed"] is False


def test_selected_redesign_direction_is_preserved(candidate: dict) -> None:
    assert candidate["selected_direction"] == candidate_service.SELECTED_DIRECTION


@pytest.mark.parametrize(
    "field",
    [
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "features_generated",
        "feature_label_matrix_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_downstream_action_remains_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_predictive_usefulness_is_not_accepted(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(candidate: dict) -> None:
    assert candidate["profitability"] == "not accepted"
    assert candidate["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_are_not_authorized(candidate: dict, field: str) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_candidate_basis_is_preserved(candidate: dict) -> None:
    assert candidate["candidate_basis"] == candidate_service.CANDIDATE_BASIS
    assert candidate["candidate_basis"]["selected_direction"] == candidate_service.SELECTED_DIRECTION


def test_candidate_objective_is_defined(candidate: dict) -> None:
    assert candidate["improved_evidence_planning_candidate_objective"] == candidate_service.CANDIDATE_OBJECTIVE
    assert candidate["improved_evidence_planning_candidate_scope"] == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
    assert candidate["improved_evidence_planning_candidate_mode"] == "PLANNED_NOT_EXECUTED"
    assert candidate["improved_evidence_planning_candidate_authority_status"] == "NOT_AUTHORIZED"


def test_improved_evidence_themes_are_defined(candidate: dict) -> None:
    rows = candidate["improved_evidence_themes"]
    assert [row["theme_id"] for row in rows] == candidate_service.IMPROVED_EVIDENCE_THEME_IDS
    assert all(row["theme_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["approval_required_before_execution"] is True for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)
    assert all(row["label_regeneration_authorized"] is False for row in rows)


def test_planned_evidence_components_are_defined(candidate: dict) -> None:
    rows = candidate["planned_evidence_components"]
    assert [row["component_id"] for row in rows] == candidate_service.PLANNED_EVIDENCE_COMPONENT_IDS
    assert all(row["component_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)
    assert all(row["model_training_authorized"] is False for row in rows)


def test_planned_data_products_are_not_generated(candidate: dict) -> None:
    rows = candidate["planned_data_products"]
    assert [row["data_product_id"] for row in rows] == candidate_service.PLANNED_DATA_PRODUCT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_planned_future_outputs_are_not_generated(candidate: dict) -> None:
    rows = candidate["planned_future_outputs"]
    assert [row["future_output_id"] for row in rows] == candidate_service.PLANNED_FUTURE_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_per_ticker_entries_count_is_twelve(candidate: dict) -> None:
    entries = candidate["per_ticker_planning_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE


def test_per_ticker_digests_are_present(candidate: dict) -> None:
    for entry in candidate["per_ticker_planning_entries"]:
        digest = entry["per_ticker_improved_evidence_planning_candidate_digest"]
        assert len(digest) == 64
        assert digest == candidate_service.per_ticker_improved_evidence_planning_candidate_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(candidate: dict) -> None:
    meta = next(row for row in candidate["per_ticker_planning_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_CANDIDATE"


def test_next_chain_is_defined(candidate: dict) -> None:
    assert candidate["next_chain"] == candidate_service.NEXT_CHAIN


def test_next_gates_are_defined(candidate: dict) -> None:
    assert candidate["next_gates"] == candidate_service.NEXT_GATES


def test_risk_controls_are_defined(candidate: dict) -> None:
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(candidate: dict) -> None:
    checklist = candidate["candidate_checklist"]
    assert [row["check_id"] for row in checklist] == candidate_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    assert candidate["candidate_summary"]["total_checks"] == 72
    assert candidate["candidate_summary"]["passed_checks"] == 72
    assert candidate["candidate_summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    first = candidate_service.improved_evidence_planning_candidate_using_redesigned_evidence_digest_v1(candidate)
    second = candidate_service.improved_evidence_planning_candidate_using_redesigned_evidence_digest_v1(deepcopy(candidate))
    assert first == second == candidate["improved_evidence_planning_candidate_using_redesigned_evidence_digest"]


def test_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    for entry in candidate["per_ticker_planning_entries"]:
        first = candidate_service.per_ticker_improved_evidence_planning_candidate_digest_v1(entry)
        second = candidate_service.per_ticker_improved_evidence_planning_candidate_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    validation = candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(deepcopy(candidate))
    assert validation["status"] == candidate_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID
    assert validation["ready_for_operator_review"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("source_results_review_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("source_results_review_ready", False),
        ("ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence", False),
        ("improved_evidence_planning_candidate_created", False),
        ("improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review", False),
        ("improved_evidence_planning_approved", True),
        ("improved_evidence_planning_executed", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("features_generated", True),
        ("feature_label_matrix_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("predictive_evidence_execution_rerun_performed", True),
        ("metric_recomputation_performed_in_candidate", True),
        ("model_training_performed_in_candidate", True),
    ],
)
def test_validator_rejects_invalid_boundary(candidate: dict, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(candidate_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceError):
        candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "candidate_basis",
        "improved_evidence_themes",
        "planned_evidence_components",
        "planned_data_products",
        "next_chain",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_section(candidate: dict, field: str) -> None:
    changed = deepcopy(candidate)
    changed.pop(field)
    with pytest.raises(candidate_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceError):
        candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed.pop("improved_evidence_planning_candidate_using_redesigned_evidence_digest")
    with pytest.raises(candidate_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceError):
        candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_planning_entries"][0].pop("per_ticker_improved_evidence_planning_candidate_digest")
    with pytest.raises(candidate_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceError):
        candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(changed)


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_markdown_v1(candidate)
    sections = [
        "Title",
        "Optional Improved Evidence Planning Candidate Using Redesigned Evidence",
        "Source Redesign Results Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Candidate Basis",
        "Candidate Objective",
        "Improved Evidence Themes",
        "Planned Evidence Components",
        "Planned Data Products",
        "Planned Future Outputs",
        "Per-Ticker Planning Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_candidate_once(candidate: dict, tmp_path) -> None:
    result = candidate_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_v1(tmp_path)
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == candidate
    with pytest.raises(candidate_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceError):
        candidate_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE is candidate_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE
    assert services.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1 is candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1
    assert services.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1 is candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1
    assert services.build_improved_evidence_planning_candidate_using_redesigned_evidence_markdown_v1 is candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_markdown_v1
    assert services.write_improved_evidence_planning_candidate_using_redesigned_evidence_v1 is candidate_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_v1
