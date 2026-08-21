from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    improved_evidence_planning_candidate_redesigned_evidence_operator_review_service as review_service,
)
from marketflow.services import (
    improved_evidence_planning_candidate_redesigned_evidence_service as candidate_service,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    result = review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1()
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_review"] is False
    assert result["market_data_acquisition_performed_in_review"] is False


def test_artifact_kind_is_correct(review_package: dict) -> None:
    assert review_package["artifact_kind"] == review_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE


def test_review_status_is_correct(review_package: dict) -> None:
    assert review_package["review_status"] == review_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY


def test_reviewed_candidate_digest_matches_expected(review_package: dict) -> None:
    assert review_package["source_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST


def test_candidate_checklist_has_zero_blockers(review_package: dict) -> None:
    assert review_package["source_candidate_checklist_total"] == 72
    assert review_package["source_candidate_checklist_passed"] == 72
    assert review_package["source_candidate_checklist_failed"] == 0
    assert review_package["source_candidate_blocker_count"] == 0


def test_candidate_digest_is_bound(review_package: dict) -> None:
    assert review_package["improved_evidence_planning_candidate_using_redesigned_evidence_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST


@pytest.mark.parametrize(
    ("field", "expected"),
    list(candidate_service.BOUND_DIGESTS.items()),
)
def test_source_digest_is_bound(review_package: dict, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_universe_count_and_order_are_preserved(review_package: dict) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == review_service.TARGET_UNIVERSE


def test_meta_913_is_preserved(review_package: dict) -> None:
    assert review_package["meta_record_count"] == 913
    assert review_package["per_ticker_record_counts"]["META"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_source_results_review_ready_is_true(review_package: dict) -> None:
    assert review_package["source_results_review_ready"] is True
    assert review_package["label_objective_redesign_results_review_ready"] is True


def test_ready_for_planning_candidate_is_true(review_package: dict) -> None:
    assert review_package["ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"] is True


def test_candidate_created_and_review_created_are_true(review_package: dict) -> None:
    assert review_package["improved_evidence_planning_candidate_created"] is True
    assert review_package["improved_evidence_planning_candidate_using_redesigned_evidence_created"] is True
    assert review_package["improved_evidence_planning_candidate_using_redesigned_evidence_review_created"] is True


def test_planning_approval_and_execution_are_false(review_package: dict) -> None:
    assert review_package["improved_evidence_planning_approved"] is False
    assert review_package["improved_evidence_planning_authorized"] is False
    assert review_package["improved_evidence_planning_executed"] is False
    assert review_package["review_summary"]["ready_for_improved_evidence_planning_approval"] is False


def test_selected_redesign_direction_is_preserved(review_package: dict) -> None:
    assert review_package["selected_direction"] == review_service.SELECTED_DIRECTION


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
def test_downstream_action_remains_false(review_package: dict, field: str) -> None:
    assert review_package[field] is False


def test_predictive_usefulness_is_not_accepted(review_package: dict) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"
    assert review_package["predictive_usefulness_acceptance_ready"] is False
    assert review_package["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(review_package: dict) -> None:
    assert review_package["profitability"] == "not accepted"
    assert review_package["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_are_not_authorized(review_package: dict, field: str) -> None:
    assert review_package[field] == "NOT_AUTHORIZED"


def test_candidate_basis_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_candidate_basis"] == candidate_service.CANDIDATE_BASIS


def test_candidate_objective_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_candidate_objective"] == {
        "improved_evidence_planning_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
        "improved_evidence_planning_candidate_scope": candidate_service.CANDIDATE_SCOPE,
        "improved_evidence_planning_candidate_mode": candidate_service.CANDIDATE_MODE,
        "improved_evidence_planning_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
    }


def test_improved_evidence_themes_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_improved_evidence_themes"]
    assert [row["theme_id"] for row in rows] == candidate_service.IMPROVED_EVIDENCE_THEME_IDS
    assert all(row["theme_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["execution_authorized"] is False for row in rows)


def test_planned_evidence_components_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_planned_evidence_components"]
    assert [row["component_id"] for row in rows] == candidate_service.PLANNED_EVIDENCE_COMPONENT_IDS
    assert all(row["component_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["model_training_authorized"] is False for row in rows)


def test_planned_data_products_are_not_generated(review_package: dict) -> None:
    rows = review_package["reviewed_planned_data_products"]
    assert [row["data_product_id"] for row in rows] == candidate_service.PLANNED_DATA_PRODUCT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_planned_future_outputs_are_not_generated(review_package: dict) -> None:
    rows = review_package["reviewed_planned_future_outputs"]
    assert [row["future_output_id"] for row in rows] == candidate_service.PLANNED_FUTURE_OUTPUT_IDS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["generated"] is False for row in rows)


def test_per_ticker_entries_count_is_twelve(review_package: dict) -> None:
    entries = review_package["per_ticker_review_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == review_service.TARGET_UNIVERSE


def test_per_ticker_candidate_digests_are_present(review_package: dict) -> None:
    for entry in review_package["per_ticker_review_entries"]:
        assert len(entry["per_ticker_improved_evidence_planning_candidate_digest"]) == 64


def test_per_ticker_review_digests_are_present(review_package: dict) -> None:
    for entry in review_package["per_ticker_review_entries"]:
        digest = entry["per_ticker_improved_evidence_planning_candidate_review_digest"]
        assert len(digest) == 64
        assert digest == review_service.per_ticker_improved_evidence_planning_candidate_review_digest_v1(entry)


def test_meta_per_ticker_entry_preserves_limitation(review_package: dict) -> None:
    meta = next(row for row in review_package["per_ticker_review_entries"] if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["planning_note"] == "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_CANDIDATE"


def test_next_chain_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_next_chain"] == candidate_service.NEXT_CHAIN


def test_next_gates_are_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_next_gates"] == candidate_service.NEXT_GATES


def test_risk_controls_are_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_risk_controls"] == candidate_service.RISK_CONTROLS


def test_checklist_passes(review_package: dict) -> None:
    checklist = review_package["review_checklist"]
    assert [row["check_id"] for row in checklist] == review_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == "PASS" for row in checklist)
    assert review_package["review_summary"]["total_checks"] == 79
    assert review_package["review_summary"]["passed_checks"] == 79
    assert review_package["review_summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(review_package: dict) -> None:
    first = review_service.improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest_v1(review_package)
    second = review_service.improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest_v1(deepcopy(review_package))
    assert first == second == review_package["improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"]


def test_per_ticker_review_digests_are_deterministic(review_package: dict) -> None:
    for entry in review_package["per_ticker_review_entries"]:
        first = review_service.per_ticker_improved_evidence_planning_candidate_review_digest_v1(entry)
        second = review_service.per_ticker_improved_evidence_planning_candidate_review_digest_v1(deepcopy(entry))
        assert first == second


def test_validator_accepts_valid_review(review_package: dict) -> None:
    validation = review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(deepcopy(review_package))
    assert validation["status"] == review_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID
    assert validation["ready_for_operator_assessment"] is True
    assert validation["ready_for_improved_evidence_planning_approval"] is False


def test_builder_accepts_explicit_valid_candidate(review_package: dict) -> None:
    candidate = candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()
    assert review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(candidate) == review_package


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_candidate_digest", "0" * 64),
        ("source_candidate_status", "WRONG"),
        ("source_candidate_blocker_count", 1),
        ("improved_evidence_planning_candidate_using_redesigned_evidence_digest", None),
        ("label_objective_redesign_results_review_using_redesigned_evidence_digest", None),
        ("records_digest", None),
        ("target_universe", list(reversed(review_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("source_results_review_ready", False),
        ("ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence", False),
        ("improved_evidence_planning_candidate_created", False),
        ("improved_evidence_planning_candidate_using_redesigned_evidence_review_created", False),
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
        ("metric_recomputation_performed_in_review", True),
        ("model_training_performed_in_review", True),
    ],
)
def test_validator_rejects_invalid_review_boundary(review_package: dict, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError):
        review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_candidate_basis",
        "reviewed_improved_evidence_themes",
        "reviewed_planned_evidence_components",
        "reviewed_planned_data_products",
        "reviewed_next_chain",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_required_review_section(review_package: dict, field: str) -> None:
    changed = deepcopy(review_package)
    changed.pop(field)
    with pytest.raises(review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError):
        review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(changed)


def test_validator_rejects_missing_review_digest(review_package: dict) -> None:
    changed = deepcopy(review_package)
    changed.pop("improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest")
    with pytest.raises(review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError):
        review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "per_ticker_improved_evidence_planning_candidate_digest",
        "per_ticker_improved_evidence_planning_candidate_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(review_package: dict, field: str) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_review_entries"][0].pop(field)
    with pytest.raises(review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError):
        review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(changed)


def test_markdown_includes_required_sections(review_package: dict) -> None:
    markdown = review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_markdown_v1(review_package)
    sections = [
        "Title",
        "Optional Improved Evidence Planning Candidate Review Using Redesigned Evidence",
        "Reviewed Candidate",
        "Source Redesign Results Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Reviewed Candidate Basis",
        "Reviewed Candidate Objective",
        "Reviewed Improved Evidence Themes",
        "Reviewed Planned Evidence Components",
        "Reviewed Planned Data Products",
        "Reviewed Planned Future Outputs",
        "Per-Ticker Review Entries",
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


def test_writer_writes_canonical_review_once(review_package: dict, tmp_path) -> None:
    result = review_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(tmp_path)
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == review_package
    with pytest.raises(review_service.ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError):
        review_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE is review_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE
    assert services.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1 is review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1
    assert services.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1 is review_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1
    assert services.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_markdown_v1 is review_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_review_markdown_v1
    assert services.write_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1 is review_service.write_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1
