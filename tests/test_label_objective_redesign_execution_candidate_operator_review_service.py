from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    label_objective_redesign_execution_candidate_operator_review_service as review,
)


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_label_objective_redesign_execution_candidate_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = review.build_label_objective_redesign_execution_candidate_review_package_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False
    assert built["market_data_acquisition_performed"] is False


def test_artifact_schema_and_review_status_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE"
    )
    assert package["schema_version"] == (
        "label_objective_redesign_execution_candidate_review_v1"
    )
    assert package["review_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_READY"
    )


def test_reviewed_execution_candidate_is_exact_and_unblocked(package: dict) -> None:
    assert package["reviewed_label_objective_redesign_execution_candidate_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE"
    )
    assert package["reviewed_label_objective_redesign_execution_candidate_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
    )
    assert package["reviewed_label_objective_redesign_execution_candidate_digest"] == (
        review.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    )
    assert package["reviewed_label_objective_redesign_execution_candidate_checklist_total"] == 54
    assert package["reviewed_label_objective_redesign_execution_candidate_checklist_passed"] == 54
    assert package["reviewed_label_objective_redesign_execution_candidate_checklist_failed"] == 0
    assert package["reviewed_label_objective_redesign_execution_candidate_blocker_count"] == 0


@pytest.mark.parametrize(("field", "expected"), list(review.REQUIRED_DIGEST_FIELDS.items()))
def test_required_digest_chain_is_bound(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_dataset_universe_and_counts_are_preserved(package: dict) -> None:
    assert package["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert package["source_profile"] == "RTH_FULL_SESSION_1D"
    assert package["timeframe"] == "1d"
    assert package["date_range_start"] == "2022-01-01"
    assert package["date_range_end"] == "2025-12-31"
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["records_digest"] == review.REQUIRED_DIGEST_FIELDS["records_digest"]


def test_meta_limitation_and_other_counts_are_preserved(package: dict) -> None:
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert package["non_meta_record_count"] == 1003
    assert package["meta_reduced_record_count_preserved"] is True
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in review.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_review_preserves_approved_candidate_state(package: dict) -> None:
    true_fields = [
        "label_objective_redesign_candidate_created",
        "label_objective_redesign_candidate_review_created",
        "label_objective_redesign_approved",
        "label_objective_redesign_approval_created",
        "ready_for_label_objective_redesign_execution_candidate",
        "label_objective_redesign_execution_candidate_created",
        "label_objective_redesign_execution_candidate_ready_for_operator_review",
        "label_objective_redesign_execution_candidate_review_created",
    ]
    assert all(package[field] is True for field in true_fields)


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_authorized",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
    ],
)
def test_redesign_execution_and_generation_gates_remain_closed(
    package: dict, field: str
) -> None:
    assert package[field] is False


def test_predictive_profitability_runtime_and_trading_remain_closed(package: dict) -> None:
    assert package["predictive_usefulness"] == "not accepted"
    assert package["predictive_usefulness_acceptance_candidate_created"] is False
    assert package["profitability"] == "not accepted"
    assert package["runtime_migration_approved"] is False
    assert package["runtime_migration_active"] is False
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert package[field] == "NOT_AUTHORIZED"
    assert package["trade_recommendations_generated"] is False
    assert package["new_strategy_scoring_performed"] is False


def test_execution_candidate_objective_scope_mode_and_authority_are_preserved(
    package: dict,
) -> None:
    assert package["label_objective_redesign_execution_candidate_objective"] == (
        "PREPARE_LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_FOR_APPROVED_REDESIGN_PLAN"
    )
    assert package["label_objective_redesign_execution_candidate_scope"] == (
        "EXECUTION_CANDIDATE_ONLY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    assert package["label_objective_redesign_execution_candidate_mode"] == "PLANNED_NOT_EXECUTED"
    assert package["label_objective_redesign_execution_candidate_authority_status"] == "NOT_AUTHORIZED"


def test_problem_basis_is_preserved(package: dict) -> None:
    assert package["problem_basis"] == {
        "two_readiness_gates_not_ready": True,
        "original_readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "refined_readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE",
        "method_diagnostic_conclusion": "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION",
        "overall_method_signal_status": "WEAK_OR_MIXED",
        "baseline_outperformance_status": "INSUFFICIENT_OR_MIXED",
        "oos_generalization_status": "LOW_TO_MIXED",
    }


def test_planned_execution_activities_are_reviewed_and_unexecuted(package: dict) -> None:
    rows = package["reviewed_planned_execution_activities"]
    assert [row["activity_id"] for row in rows] == review.candidate_service.PLANNED_EXECUTION_ACTIVITIES
    assert len(rows) == 14
    assert all(row["activity_status"] == "PLANNED_NOT_EXECUTED" for row in rows)
    assert all(row["authorization_status"] == "NOT_AUTHORIZED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)
    assert all(row["research_only"] is True and row["non_actionable"] is True for row in rows)


def test_planned_workstreams_are_reviewed_and_unexecuted(package: dict) -> None:
    rows = package["reviewed_planned_workstreams"]
    assert [row["workstream_id"] for row in rows] == review.candidate_service.PLANNED_WORKSTREAMS
    assert len(rows) == 10
    assert all(row["workstream_status"] == "PLANNED_FOR_EXECUTION_CANDIDATE_ONLY" for row in rows)
    assert all(row["authorization_status"] == "NOT_AUTHORIZED" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_label_family_outputs_are_reviewed_and_not_generated(package: dict) -> None:
    rows = package["reviewed_planned_label_family_outputs"]
    assert len(rows) == 10
    assert [row["label_family_candidate_id"] for row in rows] == (
        review.candidate_service.candidate_service.LABEL_FAMILY_CANDIDATES
    )
    assert all(row["planned_output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["label_generation_authorized"] is False for row in rows)
    assert all(row["label_generation_performed"] is False for row in rows)


def test_execution_outputs_are_reviewed_and_not_generated(package: dict) -> None:
    rows = package["reviewed_planned_execution_outputs"]
    assert len(rows) == 8
    assert [row["output_id"] for row in rows] == review.candidate_service.PLANNED_EXECUTION_OUTPUTS
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["authority"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_per_ticker_review_entries_preserve_order_counts_and_boundaries(package: dict) -> None:
    entries = package["per_ticker_review_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == review.TARGET_UNIVERSE
    for entry in entries:
        ticker = entry["ticker"]
        assert entry["historical_record_count"] == package["per_ticker_record_counts"][ticker]
        assert entry["label_objective_redesign_execution_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT"
        assert entry["label_objective_redesign_authorized"] is False
        assert entry["label_objective_redesign_executed"] is False
        assert entry["redesigned_label_generation_authorized"] is False
        assert entry["redesigned_label_generation_performed"] is False
        assert entry["predictive_usefulness"] == "not accepted"
        assert entry["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_entry_preserves_limitation(package: dict) -> None:
    entries = {entry["ticker"]: entry for entry in package["per_ticker_review_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["redesign_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
    )
    assert all(
        entry["historical_record_count"] == 1003
        and entry["meta_reduced_record_count_flag"] is False
        for ticker, entry in entries.items()
        if ticker != "META"
    )


def test_per_ticker_candidate_and_review_digests_are_present_and_valid(package: dict) -> None:
    for entry in package["per_ticker_review_entries"]:
        assert len(entry["per_ticker_label_objective_redesign_execution_candidate_digest"]) == 64
        assert len(entry["per_ticker_label_objective_redesign_execution_candidate_review_digest"]) == 64
        assert entry["source_label_objective_redesign_execution_candidate_digest"] == review.EXPECTED_EXECUTION_CANDIDATE_DIGEST
        assert entry["per_ticker_label_objective_redesign_execution_candidate_review_digest"] == (
            review.per_ticker_label_objective_redesign_execution_candidate_review_digest_v1(entry)
        )


def test_future_chain_gates_and_risk_controls_are_reviewed(package: dict) -> None:
    assert package["reviewed_future_chain"] == review.candidate_service.FUTURE_CHAIN
    assert len(package["reviewed_future_chain"]) == 10
    assert package["reviewed_future_gates"] == review.candidate_service.FUTURE_GATES
    assert len(package["reviewed_future_gates"]) == 12
    assert package["reviewed_risk_controls"] == review.candidate_service.RISK_CONTROLS
    assert len(package["reviewed_risk_controls"]) == 14


def test_checklist_and_summary_pass(package: dict) -> None:
    assert len(package["review_checklist"]) == len(review.CHECK_IDS) == 61
    assert all(item["status"] == "PASS" for item in package["review_checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in package["review_checklist"])
    assert package["review_summary"] == {
        "total_checks": 61,
        "passed_checks": 61,
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_assessment": True,
        "ready_for_label_objective_redesign_execution_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_review_and_per_ticker_digests_are_deterministic(package: dict) -> None:
    second = review.build_label_objective_redesign_execution_candidate_review_package_v1()
    assert second == package
    assert package["label_objective_redesign_execution_candidate_review_package_digest"] == (
        review.label_objective_redesign_execution_candidate_review_package_digest_v1(package)
    )
    assert [entry["per_ticker_label_objective_redesign_execution_candidate_review_digest"] for entry in second["per_ticker_review_entries"]] == [
        entry["per_ticker_label_objective_redesign_execution_candidate_review_digest"]
        for entry in package["per_ticker_review_entries"]
    ]


def test_validator_accepts_valid_review_package(package: dict) -> None:
    result = review.validate_label_objective_redesign_execution_candidate_review_package_v1(package)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert result["blocker_count"] == 0
    assert result["ready_for_operator_assessment"] is True
    assert result["ready_for_label_objective_redesign_execution_approval"] is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_label_objective_redesign_execution_candidate_digest", "0" * 64),
        ("reviewed_label_objective_redesign_execution_candidate_status", "WRONG"),
        ("reviewed_label_objective_redesign_execution_candidate_blocker_count", 1),
        ("label_objective_redesign_execution_candidate_digest", "0" * 64),
        ("label_objective_redesign_approval_digest", "0" * 64),
        ("label_objective_redesign_candidate_review_package_digest", "0" * 64),
        ("records_digest", "0" * 64),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("label_objective_redesign_approved", False),
        ("ready_for_label_objective_redesign_execution_candidate", False),
        ("label_objective_redesign_execution_candidate_created", False),
        ("label_objective_redesign_execution_candidate_review_created", False),
        ("label_objective_redesign_authorized", True),
        ("label_objective_redesign_executed", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_changed_or_authorizing_top_level_values(
    package: dict, field: str, bad_value: object
) -> None:
    mutated = deepcopy(package)
    mutated[field] = bad_value
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.validate_label_objective_redesign_execution_candidate_review_package_v1(mutated)


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_execution_candidate_digest",
        "label_objective_redesign_approval_digest",
        "label_objective_redesign_candidate_review_package_digest",
        "records_digest",
        "reviewed_planned_execution_activities",
        "reviewed_planned_workstreams",
        "reviewed_planned_label_family_outputs",
        "reviewed_future_chain",
        "reviewed_risk_controls",
        "label_objective_redesign_execution_candidate_review_package_digest",
    ],
)
def test_validator_rejects_missing_required_evidence(
    package: dict, field: str
) -> None:
    mutated = deepcopy(package)
    mutated.pop(field)
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.validate_label_objective_redesign_execution_candidate_review_package_v1(mutated)


def test_validator_rejects_missing_per_ticker_candidate_digest(package: dict) -> None:
    mutated = deepcopy(package)
    mutated["per_ticker_review_entries"][0].pop(
        "per_ticker_label_objective_redesign_execution_candidate_digest"
    )
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.validate_label_objective_redesign_execution_candidate_review_package_v1(mutated)


def test_validator_rejects_missing_per_ticker_review_digest(package: dict) -> None:
    mutated = deepcopy(package)
    mutated["per_ticker_review_entries"][0].pop(
        "per_ticker_label_objective_redesign_execution_candidate_review_digest"
    )
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.validate_label_objective_redesign_execution_candidate_review_package_v1(mutated)


def test_validator_rejects_execution_candidate_checklist_blocker(package: dict) -> None:
    mutated = deepcopy(package)
    mutated["review_checklist"][0]["status"] = "FAIL"
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.validate_label_objective_redesign_execution_candidate_review_package_v1(mutated)


def test_markdown_includes_all_required_sections(package: dict) -> None:
    markdown = review.build_label_objective_redesign_execution_candidate_review_markdown_v1(package)
    headings = [
        "Title",
        "Label Objective Redesign Execution Candidate Review Package",
        "Reviewed Execution Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Candidate Objective",
        "Problem Basis",
        "Reviewed Planned Execution Activities",
        "Reviewed Planned Workstreams",
        "Reviewed Planned Label Family Outputs",
        "Reviewed Planned Execution Outputs",
        "Per-Ticker Review Entries",
        "Future Chain",
        "Future Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in headings)
    assert "no redesign authorization or execution" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path, package: dict
) -> None:
    result = review.write_label_objective_redesign_execution_candidate_review_package_v1(tmp_path)
    path = tmp_path / result["filename"]
    assert json.loads(path.read_text(encoding="utf-8")) == package
    assert result["payload_sha256"]
    with pytest.raises(review.LabelObjectiveRedesignExecutionCandidateReviewError):
        review.write_label_objective_redesign_execution_candidate_review_package_v1(tmp_path)
