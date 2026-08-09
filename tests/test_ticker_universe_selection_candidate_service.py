from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow import services
from marketflow.services import ticker_universe_selection_candidate_service as ticker_candidate


def _candidate() -> dict[str, Any]:
    return ticker_candidate.build_ticker_universe_selection_candidate_v1()


def _redigest(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["selection_checklist"] = ticker_candidate._checklist(candidate)
    candidate["selection_summary"] = ticker_candidate._summary(candidate["selection_checklist"])
    candidate["ticker_universe_selection_candidate_digest"] = (
        ticker_candidate.ticker_universe_selection_candidate_digest_v1(candidate)
    )
    return candidate


def test_candidate_builds_offline_without_provider_calls():
    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_is_ticker_universe_selection_candidate():
    assert _candidate()["artifact_kind"] == (
        ticker_candidate.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE
    )


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == (
        ticker_candidate.TICKER_UNIVERSE_SELECTION_READY_FOR_OPERATOR_REVIEW
    )


def test_scope_expansion_review_digest_is_bound():
    assert _candidate()[
        "predictive_evidence_scope_expansion_plan_candidate_review_package_digest"
    ] == ticker_candidate.EXPECTED_SCOPE_EXPANSION_REVIEW_PACKAGE_DIGEST


def test_scope_expansion_candidate_digest_is_bound():
    assert _candidate()["predictive_evidence_scope_expansion_plan_candidate_digest"] == (
        ticker_candidate.EXPECTED_SCOPE_EXPANSION_CANDIDATE_DIGEST
    )


def test_additional_predictive_evidence_plan_review_digest_is_bound():
    assert _candidate()[
        "additional_predictive_evidence_plan_candidate_review_package_digest"
    ] == ticker_candidate.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_PLAN_REVIEW_PACKAGE_DIGEST


def test_readiness_review_digest_is_bound():
    assert _candidate()[
        "predictive_usefulness_acceptance_readiness_candidate_review_package_digest"
    ] == ticker_candidate.EXPECTED_ACCEPTANCE_READINESS_REVIEW_PACKAGE_DIGEST


def test_existing_baseline_ticker_is_aapl():
    assert _candidate()["existing_baseline_ticker"] == "AAPL"


def test_proposed_candidate_ticker_count_is_12():
    assert _candidate()["proposed_candidate_ticker_count"] == 12


def test_proposed_candidate_tickers_are_unique():
    tickers = _candidate()["proposed_candidate_ticker_universe"]

    assert len(tickers) == len(set(tickers))


def test_aapl_is_not_in_proposed_candidate_universe():
    assert "AAPL" not in _candidate()["proposed_candidate_ticker_universe"]


def test_candidate_ticker_list_status_is_unvalidated():
    assert _candidate()["candidate_ticker_list_status"] == (
        ticker_candidate.CANDIDATE_TICKER_LIST_STATUS
    )


def test_approved_expanded_ticker_universe_is_empty():
    assert _candidate()["approved_expanded_ticker_universe"] == []


def test_approved_expanded_ticker_count_is_zero():
    assert _candidate()["approved_expanded_ticker_count"] == 0


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
        "provider_requests_made",
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
        "predictive_usefulness_acceptance_candidate_created",
        "runtime_migration_recommended",
        "runtime_migration_approved",
    ],
)
def test_authority_and_execution_flags_remain_false(field: str):
    assert _candidate()[field] is False


def test_candidate_entries_are_proposed_unvalidated():
    assert {entry["candidate_entry_status"] for entry in _candidate()["candidate_ticker_entries"]} == {
        ticker_candidate.PROPOSED_UNVALIDATED
    }


def test_candidate_entries_have_listing_security_and_exchange_not_verified():
    entries = _candidate()["candidate_ticker_entries"]

    assert {entry["listing_status"] for entry in entries} == {ticker_candidate.NOT_VERIFIED}
    assert {entry["security_type_status"] for entry in entries} == {ticker_candidate.NOT_VERIFIED}
    assert {entry["exchange_status"] for entry in entries} == {ticker_candidate.NOT_VERIFIED}


def test_candidate_entries_have_authority_statuses_not_created():
    entries = _candidate()["candidate_ticker_entries"]

    for field in (
        "corporate_action_authority_status",
        "acquisition_authority_status",
        "canonical_dataset_authority_status",
        "registry_approval_status",
    ):
        assert {entry[field] for entry in entries} == {ticker_candidate.NOT_CREATED}


def test_candidate_entries_runtime_strategy_broker_and_paper_are_not_authorized():
    entries = _candidate()["candidate_ticker_entries"]

    for field in (
        "research_use_status",
        "runtime_use",
        "strategy_use",
        "broker_execution",
        "paper_trading",
    ):
        assert {entry[field] for entry in entries} == {ticker_candidate.NOT_AUTHORIZED}


def test_intended_diversity_tags_are_marked_unverified():
    candidate = _candidate()

    assert candidate["intended_diversity_tags_status"] == (
        ticker_candidate.INTENDED_DIVERSITY_TAGS_STATUS
    )
    assert {
        entry["intended_diversity_tags_status"]
        for entry in candidate["candidate_ticker_entries"]
    } == {ticker_candidate.INTENDED_DIVERSITY_TAGS_STATUS}


def test_selection_rationale_is_research_only():
    assert _candidate()["selection_rationale_status"] == ticker_candidate.RESEARCH_ONLY_NON_ACTIONABLE


def test_future_validation_gates_are_defined():
    assert _candidate()["future_validation_gates"] == ticker_candidate.FUTURE_VALIDATION_GATES


def test_future_authority_chain_has_15_steps():
    candidate = _candidate()

    assert candidate["future_ticker_authority_chain_step_count"] == 15
    assert len(candidate["future_ticker_authority_chain"]) == 15


def test_planned_outputs_are_not_generated():
    assert {item["generation_status"] for item in _candidate()["planned_outputs"]} == {
        ticker_candidate.PLANNED_NOT_GENERATED
    }


def test_planned_outputs_are_research_only_non_actionable():
    assert {item["actionability_label"] for item in _candidate()["planned_outputs"]} == {
        ticker_candidate.RESEARCH_ONLY_NON_ACTIONABLE
    }


def test_predictive_usefulness_remains_not_accepted():
    assert _candidate()["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false():
    assert _candidate()["predictive_usefulness_acceptance_ready"] is False


def test_predictive_usefulness_acceptance_candidate_created_remains_false():
    assert _candidate()["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_remains_not_accepted():
    assert _candidate()["profitability"] == "not accepted"


def test_runtime_strategy_paper_and_broker_remain_not_authorized():
    candidate = _candidate()

    assert candidate["runtime_use"] == ticker_candidate.NOT_AUTHORIZED
    assert candidate["strategy_use"] == ticker_candidate.NOT_AUTHORIZED
    assert candidate["paper_trading"] == ticker_candidate.NOT_AUTHORIZED
    assert candidate["broker_execution"] == ticker_candidate.NOT_AUTHORIZED


def test_readiness_flags_remain_false():
    summary = _candidate()["selection_summary"]

    assert summary["ready_for_ticker_universe_selection_approval"] is False
    assert summary["ready_for_live_ticker_validation"] is False
    assert summary["ready_for_new_ticker_authority_chain"] is False
    assert summary["ready_for_acquisition"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["selection_checklist"]] == (
        ticker_candidate.REQUIRED_CHECK_IDS
    )


def test_all_checks_pass_for_accepted_candidate():
    assert {item["status"] for item in _candidate()["selection_checklist"]} == {
        ticker_candidate.PASS
    }


def test_summary_counts_total_passed_and_failed_correctly():
    summary = _candidate()["selection_summary"]

    assert summary["total_checks"] == len(ticker_candidate.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(ticker_candidate.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_review"] is True


def test_candidate_digest_is_deterministic():
    assert _candidate()["ticker_universe_selection_candidate_digest"] == _candidate()[
        "ticker_universe_selection_candidate_digest"
    ]


def test_validator_accepts_valid_candidate():
    validation = ticker_candidate.validate_ticker_universe_selection_candidate_v1(_candidate())

    assert validation["status"] == "TICKER_UNIVERSE_SELECTION_CANDIDATE_VALID"
    assert validation["ready_for_ticker_universe_selection_approval"] is False


def test_builder_accepts_deterministic_12_ticker_override():
    override = [
        "ABC",
        "DEF",
        "GHI",
        "JKL",
        "MNO",
        "PQR",
        "STU",
        "VWX",
        "YZA",
        "BCD",
        "EFG",
        "HIJ",
    ]
    candidate = ticker_candidate.build_ticker_universe_selection_candidate_v1(
        proposed_tickers=override
    )

    assert candidate["proposed_candidate_ticker_universe"] == override


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made",
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
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    candidate = deepcopy(_candidate())
    candidate[field] = True

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


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
    candidate = deepcopy(_candidate())
    candidate[field] = value

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_artifact_kind_mismatch():
    candidate = deepcopy(_candidate())
    candidate["artifact_kind"] = "WRONG"

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_candidate_status_not_ready():
    candidate = deepcopy(_candidate())
    candidate["candidate_status"] = "TICKER_UNIVERSE_SELECTION_APPROVED"

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_approved_expanded_ticker_universe_not_empty():
    candidate = deepcopy(_candidate())
    candidate["approved_expanded_ticker_universe"] = ["MSFT"]

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_empty_candidate_ticker_list():
    candidate = deepcopy(_candidate())
    candidate["proposed_candidate_ticker_universe"] = []
    candidate["candidate_ticker_entries"] = []
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_candidate_ticker_list_containing_aapl():
    candidate = deepcopy(_candidate())
    candidate["proposed_candidate_ticker_universe"][0] = "AAPL"
    candidate["candidate_ticker_entries"][0]["ticker"] = "AAPL"
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_duplicate_proposed_tickers():
    candidate = deepcopy(_candidate())
    candidate["proposed_candidate_ticker_universe"][1] = "MSFT"
    candidate["candidate_ticker_entries"][1]["ticker"] = "MSFT"
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_candidate_entry_status_not_unvalidated():
    candidate = deepcopy(_candidate())
    candidate["candidate_ticker_entries"][0]["candidate_entry_status"] = "APPROVED"
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_candidate_entry_listing_status_verified():
    candidate = deepcopy(_candidate())
    candidate["candidate_ticker_entries"][0]["listing_status"] = "VERIFIED"
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_candidate_entry_authority_status_created():
    candidate = deepcopy(_candidate())
    candidate["candidate_ticker_entries"][0]["acquisition_authority_status"] = "CREATED"
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_runtime_authorized_on_candidate_entry():
    candidate = deepcopy(_candidate())
    candidate["candidate_ticker_entries"][0]["runtime_use"] = "AUTHORIZED"

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "future_validation_gates",
        "future_ticker_authority_chain",
        "planned_outputs",
    ],
)
def test_validator_rejects_missing_required_components(field: str):
    candidate = deepcopy(_candidate())
    candidate.pop(field)
    _redigest(candidate)

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_validator_rejects_missing_candidate_digest():
    candidate = deepcopy(_candidate())
    candidate.pop("ticker_universe_selection_candidate_digest")

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.validate_ticker_universe_selection_candidate_v1(candidate)


def test_markdown_writer_includes_required_sections():
    markdown = ticker_candidate.build_ticker_universe_selection_candidate_markdown_v1(
        _candidate()
    )

    for section in [
        "## Title",
        "## Purpose",
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
    output_path = tmp_path / "ticker_universe_selection_candidate_v1.json"
    output_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ticker_candidate.TickerUniverseSelectionCandidateError):
        ticker_candidate.write_ticker_universe_selection_candidate_v1(tmp_path)


def test_writer_creates_non_overwriting_json_file(tmp_path: Path):
    result = ticker_candidate.write_ticker_universe_selection_candidate_v1(tmp_path)

    assert result["filename"] == "ticker_universe_selection_candidate_v1.json"
    assert Path(result["path"]).exists()
    assert result["payload_byte_size"] > 0


def test_public_exports_are_available():
    assert services.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE == (
        ticker_candidate.ARTIFACT_KIND_TICKER_UNIVERSE_SELECTION_CANDIDATE
    )
    assert services.DEFAULT_PROPOSED_TICKER_UNIVERSE == (
        ticker_candidate.DEFAULT_PROPOSED_TICKER_UNIVERSE
    )
    assert services.build_ticker_universe_selection_candidate_v1 is (
        ticker_candidate.build_ticker_universe_selection_candidate_v1
    )
    assert services.validate_ticker_universe_selection_candidate_v1 is (
        ticker_candidate.validate_ticker_universe_selection_candidate_v1
    )
    assert services.write_ticker_universe_selection_candidate_v1 is (
        ticker_candidate.write_ticker_universe_selection_candidate_v1
    )
