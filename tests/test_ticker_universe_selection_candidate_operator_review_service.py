from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import (
    ticker_universe_selection_candidate_operator_review_service as review,
)


def _package() -> dict[str, Any]:
    return review.build_ticker_universe_selection_candidate_review_package_v1()


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["ticker_universe_selection_candidate_review_package_digest"] = (
        review.ticker_universe_selection_candidate_review_package_digest_v1(package)
    )
    return package


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("candidate must not be rebuilt by status binding")

    monkeypatch.setattr(
        review.candidate_service,
        "build_ticker_universe_selection_candidate_v1",
        fail_if_called,
    )

    assert _package()["provider_requests_made_in_review"] is False


def test_artifact_kind_is_ticker_universe_selection_candidate_review_package():
    assert _package()["artifact_kind"] == (
        review.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == (
        review.TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_ticker_universe_selection_candidate_digest_matches_expected():
    assert _package()["reviewed_ticker_universe_selection_candidate_digest"] == (
        review.EXPECTED_TICKER_UNIVERSE_SELECTION_CANDIDATE_DIGEST
    )


def test_candidate_checklist_has_zero_blockers():
    package = _package()

    assert package["reviewed_ticker_universe_selection_candidate_checklist_total"] == 64
    assert package["reviewed_ticker_universe_selection_candidate_checklist_passed"] == 64
    assert package["reviewed_ticker_universe_selection_candidate_checklist_failed"] == 0
    assert package["reviewed_ticker_universe_selection_candidate_blocker_count"] == 0


def test_source_evidence_digests_are_bound():
    package = _package()

    assert package["predictive_evidence_scope_expansion_plan_candidate_review_package_digest"] == (
        review.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_evidence_scope_expansion_plan_candidate_digest"] == (
        review.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
    )
    assert package["additional_predictive_evidence_plan_candidate_review_package_digest"] == (
        review.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_usefulness_acceptance_readiness_candidate_review_package_digest"] == (
        review.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST
    )
    assert package["predictive_experiment_results_review_package_digest"] == (
        review.EXPECTED_PREDICTIVE_EXPERIMENT_RESULTS_REVIEW_PACKAGE_DIGEST
    )


def test_existing_baseline_ticker_is_aapl():
    assert _package()["existing_baseline_ticker"] == "AAPL"


def test_proposed_candidate_ticker_count_is_12():
    assert _package()["proposed_candidate_ticker_count"] == 12


def test_proposed_candidate_tickers_are_unique_and_exclude_aapl():
    tickers = _package()["proposed_candidate_ticker_universe"]

    assert tickers == review.DEFAULT_PROPOSED_TICKER_UNIVERSE
    assert len(tickers) == len(set(tickers))
    assert "AAPL" not in tickers


def test_candidate_ticker_list_status_is_unvalidated():
    assert _package()["candidate_ticker_list_status"] == review.CANDIDATE_TICKER_LIST_STATUS


def test_approved_expanded_ticker_universe_is_empty_and_count_zero():
    package = _package()

    assert package["approved_expanded_ticker_universe"] == []
    assert package["approved_expanded_ticker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_approved",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "provider_requests_made_in_review",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_review_execution_and_authority_flags_remain_false(field: str):
    assert _package()[field] is False


def test_candidate_entries_are_proposed_unvalidated():
    assert {entry["candidate_entry_status"] for entry in _package()["candidate_ticker_entries"]} == {
        review.PROPOSED_UNVALIDATED
    }


def test_candidate_entries_have_listing_security_and_exchange_not_verified():
    entries = _package()["candidate_ticker_entries"]

    assert {entry["listing_status"] for entry in entries} == {review.NOT_VERIFIED}
    assert {entry["security_type_status"] for entry in entries} == {review.NOT_VERIFIED}
    assert {entry["exchange_status"] for entry in entries} == {review.NOT_VERIFIED}


def test_candidate_entries_have_authority_statuses_not_created():
    entries = _package()["candidate_ticker_entries"]

    for field in (
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {review.NOT_CREATED}


def test_candidate_entries_runtime_strategy_broker_and_paper_are_not_authorized():
    entries = _package()["candidate_ticker_entries"]

    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "broker_execution",
        "paper_trading",
    ):
        assert {entry[field] for entry in entries} == {review.NOT_AUTHORIZED}


def test_intended_diversity_tags_and_selection_rationale_are_reviewed():
    package = _package()

    assert package["intended_diversity_tags_status"] == review.INTENDED_DIVERSITY_TAGS_STATUS
    assert package["selection_rationale_status"] == review.RESEARCH_ONLY_NON_ACTIONABLE


def test_future_validation_authority_and_outputs_are_reviewed():
    package = _package()

    assert package["future_validation_gate_count"] == 13
    assert package["future_validation_gates"] == review.FUTURE_VALIDATION_GATES
    assert package["future_ticker_authority_chain_step_count"] == 15
    assert len(package["future_ticker_authority_chain"]) == 15
    assert package["planned_output_count"] == 7
    assert {item["generation_status"] for item in package["planned_outputs"]} == {
        review.PLANNED_NOT_GENERATED
    }
    assert {item["actionability_label"] for item in package["planned_outputs"]} == {
        review.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_predictive_profitability_and_runtime_boundaries_remain_closed():
    package = _package()

    assert package["predictive_usefulness"] == "not accepted"
    assert package["predictive_usefulness_acceptance_ready"] is False
    assert package["predictive_usefulness_acceptance_candidate_created"] is False
    assert package["profitability"] == "not accepted"
    assert package["runtime_migration_recommended"] is False
    assert package["runtime_migration_approved"] is False
    assert package["runtime_use"] == review.NOT_AUTHORIZED
    assert package["strategy_use"] == review.NOT_AUTHORIZED
    assert package["paper_trading"] == review.NOT_AUTHORIZED
    assert package["broker_execution"] == review.NOT_AUTHORIZED


def test_review_readiness_flags_remain_false():
    summary = _package()["review_summary"]

    assert summary["ready_for_ticker_universe_selection_approval"] is False
    assert summary["ready_for_live_ticker_validation"] is False
    assert summary["ready_for_new_ticker_authority_chain"] is False
    assert summary["ready_for_acquisition"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _package()["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_ready_review_package():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True


def test_review_package_digest_is_deterministic():
    assert _package()["ticker_universe_selection_candidate_review_package_digest"] == _package()[
        "ticker_universe_selection_candidate_review_package_digest"
    ]


def test_validator_accepts_valid_review_package():
    validation = review.validate_ticker_universe_selection_candidate_review_package_v1(
        _package()
    )

    assert validation["status"] == "TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_ticker_universe_selection_approval"] is False


def test_review_package_can_bind_valid_candidate_object():
    candidate = review.candidate_service.build_ticker_universe_selection_candidate_v1()
    package = review.build_ticker_universe_selection_candidate_review_package_v1(
        candidate=candidate
    )

    assert package["ticker_universe_selection_candidate_binding_mode"] == (
        review.TICKER_UNIVERSE_SELECTION_CANDIDATE_OBJECT_BINDING
    )


def test_review_package_uses_status_binding_by_default():
    assert _package()["ticker_universe_selection_candidate_binding_mode"] == (
        review.TICKER_UNIVERSE_SELECTION_CANDIDATE_STATUS_BINDING
    )


def test_validator_rejects_modified_ticker_universe_selection_candidate_digest():
    package = deepcopy(_package())
    package["reviewed_ticker_universe_selection_candidate_digest"] = "0" * 64
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_candidate_status_changed_away_from_ready():
    package = deepcopy(_package())
    package["reviewed_ticker_universe_selection_candidate_status"] = (
        "TICKER_UNIVERSE_SELECTION_APPROVED"
    )

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_ticker_validation_performed",
        "final_ticker_selection_performed",
        "ticker_universe_selection_approved",
        "scope_expansion_authorized",
        "expanded_ticker_universe_approved",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
        "ready_for_ticker_universe_selection_approval",
        "ready_for_live_ticker_validation",
        "ready_for_new_ticker_authority_chain",
        "ready_for_acquisition",
        "ready_for_additional_predictive_evidence_execution_candidate",
        "ready_for_predictive_usefulness_acceptance_candidate",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    package = deepcopy(_package())
    package[field] = True

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_authorization_values(field: str, value: str):
    package = deepcopy(_package())
    package[field] = value

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_artifact_kind_mismatch():
    package = deepcopy(_package())
    package["artifact_kind"] = "WRONG"

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_review_status_not_ready():
    package = deepcopy(_package())
    package["review_status"] = "TICKER_UNIVERSE_SELECTION_APPROVED"

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_approved_expanded_ticker_universe_not_empty():
    package = deepcopy(_package())
    package["approved_expanded_ticker_universe"] = ["MSFT"]

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_empty_candidate_ticker_list():
    package = deepcopy(_package())
    package["proposed_candidate_ticker_universe"] = []
    package["candidate_ticker_entries"] = []
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_candidate_ticker_list_containing_aapl():
    package = deepcopy(_package())
    package["proposed_candidate_ticker_universe"][0] = "AAPL"
    package["candidate_ticker_entries"][0]["ticker"] = "AAPL"
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_duplicate_proposed_tickers():
    package = deepcopy(_package())
    package["proposed_candidate_ticker_universe"][1] = "MSFT"
    package["candidate_ticker_entries"][1]["ticker"] = "MSFT"
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_candidate_entry_status_not_unvalidated():
    package = deepcopy(_package())
    package["candidate_ticker_entries"][0]["candidate_entry_status"] = "APPROVED"
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_candidate_entry_listing_status_verified():
    package = deepcopy(_package())
    package["candidate_ticker_entries"][0]["listing_status"] = "VERIFIED"
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_candidate_entry_authority_status_created():
    package = deepcopy(_package())
    package["candidate_ticker_entries"][0]["acquisition_authority_status"] = "CREATED"
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_runtime_authorized_on_candidate_entry():
    package = deepcopy(_package())
    package["candidate_ticker_entries"][0]["runtime_use"] = "AUTHORIZED"

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "future_validation_gates",
        "future_ticker_authority_chain",
        "planned_outputs",
    ],
)
def test_validator_rejects_missing_required_components(field: str):
    package = deepcopy(_package())
    package.pop(field)
    _redigest(package)

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_validator_rejects_missing_review_package_digest():
    package = deepcopy(_package())
    package.pop("ticker_universe_selection_candidate_review_package_digest")

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.validate_ticker_universe_selection_candidate_review_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_ticker_universe_selection_candidate_review_markdown_v1(
        _package()
    )

    for section in [
        "## Title",
        "## Reviewed Ticker Universe Selection Candidate",
        "## Source Scope Expansion Evidence",
        "## Proposed Unvalidated Candidate Ticker Universe",
        "## Intended Diversity Tags",
        "## Selection Rationale",
        "## Future Validation Required",
        "## Future Per-Ticker Authority Chain",
        "## Planned Outputs",
        "## Authority Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert section in markdown


def test_writer_rejects_existing_output_file(tmp_path: Path):
    output_path = tmp_path / "ticker_universe_selection_candidate_review_package_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(review.TickerUniverseSelectionCandidateReviewPackageError):
        review.write_ticker_universe_selection_candidate_review_package_v1(tmp_path)


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = review.write_ticker_universe_selection_candidate_review_package_v1(tmp_path)

    assert result["filename"] == "ticker_universe_selection_candidate_review_package_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE == (
        review.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE
    )
    assert services.TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY == (
        review.TICKER_UNIVERSE_SELECTION_CANDIDATE_REVIEW_PACKAGE_READY
    )
    assert services.build_ticker_universe_selection_candidate_review_package_v1 is (
        review.build_ticker_universe_selection_candidate_review_package_v1
    )
    assert services.validate_ticker_universe_selection_candidate_review_package_v1 is (
        review.validate_ticker_universe_selection_candidate_review_package_v1
    )
    assert services.write_ticker_universe_selection_candidate_review_package_v1 is (
        review.write_ticker_universe_selection_candidate_review_package_v1
    )
