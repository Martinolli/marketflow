from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    label_objective_redesign_execution_candidate_service as candidate,
)


@pytest.fixture(scope="module")
def package() -> dict:
    return candidate.build_label_objective_redesign_execution_candidate_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = candidate.build_label_objective_redesign_execution_candidate_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False


def test_artifact_kind_schema_and_status_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE"
    )
    assert package["schema_version"] == (
        "label_objective_redesign_execution_candidate_v1"
    )
    assert package["candidate_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
    )


@pytest.mark.parametrize(
    ("field", "expected"), list(candidate.REQUIRED_DIGEST_FIELDS.items())
)
def test_required_digest_chain_is_bound(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_dataset_universe_count_and_order_are_preserved(package: dict) -> None:
    assert package["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert package["source_profile"] == "RTH_FULL_SESSION_1D"
    assert package["timeframe"] == "1d"
    assert package["date_range_start"] == "2022-01-01"
    assert package["date_range_end"] == "2025-12-31"
    assert package["target_universe"] == candidate.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946


def test_meta_913_and_other_record_counts_are_preserved(package: dict) -> None:
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert package["meta_reduced_record_count_preserved"] is True
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in candidate.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_approved_state_and_candidate_readiness_are_preserved(package: dict) -> None:
    assert package["label_objective_redesign_candidate_created"] is True
    assert package["label_objective_redesign_candidate_review_created"] is True
    assert package["label_objective_redesign_approved"] is True
    assert package["label_objective_redesign_approval_created"] is True
    assert package["ready_for_label_objective_redesign_execution_candidate"] is True


def test_execution_candidate_created_and_ready_only(package: dict) -> None:
    assert package["label_objective_redesign_execution_candidate_created"] is True
    assert package["label_objective_redesign_execution_candidate_ready_for_operator_review"] is True
    assert package["label_objective_redesign_execution_candidate_review_created"] is False
    assert package["operator_review_required"] is True


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
def test_execution_and_generation_gates_remain_closed(
    package: dict, field: str
) -> None:
    assert package[field] is False


def test_predictive_and_profitability_acceptance_remain_closed(package: dict) -> None:
    assert package["predictive_usefulness"] == "not accepted"
    assert package["predictive_usefulness_acceptance_ready"] is False
    assert package["predictive_usefulness_acceptance_recommended"] is False
    assert package["predictive_usefulness_acceptance_candidate_created"] is False
    assert package["profitability"] == "not accepted"
    assert package["profitability_acceptance_ready"] is False
    assert package["profitability_acceptance_recommended"] is False


def test_runtime_trading_and_recommendations_remain_closed(package: dict) -> None:
    assert package["runtime_migration_approved"] is False
    assert package["runtime_migration_active"] is False
    assert package["runtime_use"] == "NOT_AUTHORIZED"
    assert package["strategy_use"] == "NOT_AUTHORIZED"
    assert package["paper_trading"] == "NOT_AUTHORIZED"
    assert package["broker_execution"] == "NOT_AUTHORIZED"
    assert package["automatic_stitching"] is False
    assert package["new_strategy_scoring_performed"] is False
    assert package["trade_recommendations_generated"] is False


def test_execution_candidate_objective_scope_and_mode_are_exact(package: dict) -> None:
    assert package["label_objective_redesign_execution_candidate_objective"] == (
        candidate.EXECUTION_CANDIDATE_OBJECTIVE
    )
    assert package["label_objective_redesign_execution_candidate_scope"] == (
        "EXECUTION_CANDIDATE_ONLY_NOT_AUTHORIZATION_NOT_EXECUTION"
    )
    assert package["label_objective_redesign_execution_candidate_mode"] == (
        "PLANNED_NOT_EXECUTED"
    )
    assert package["label_objective_redesign_execution_candidate_authority_status"] == (
        "NOT_AUTHORIZED"
    )


def test_problem_basis_is_preserved(package: dict) -> None:
    assert package["problem_basis"] == {
        "two_readiness_gates_not_ready": True,
        "original_readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "refined_readiness_decision": (
            "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE"
        ),
        "method_diagnostic_conclusion": "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION",
        "overall_method_signal_status": "WEAK_OR_MIXED",
        "baseline_outperformance_status": "INSUFFICIENT_OR_MIXED",
        "oos_generalization_status": "LOW_TO_MIXED",
    }


def test_planned_execution_activities_are_complete_and_unexecuted(package: dict) -> None:
    rows = package["planned_execution_activities"]
    assert [item["activity_id"] for item in rows] == candidate.PLANNED_EXECUTION_ACTIVITIES
    assert len(rows) == 14
    assert all(item["activity_status"] == "PLANNED_NOT_EXECUTED" for item in rows)
    assert all(item["authorization_status"] == "NOT_AUTHORIZED" for item in rows)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in rows)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in rows)


def test_planned_workstreams_are_complete_and_unexecuted(package: dict) -> None:
    rows = package["planned_workstreams"]
    assert [item["workstream_id"] for item in rows] == candidate.PLANNED_WORKSTREAMS
    assert len(rows) == 10
    assert all(item["workstream_status"] == "PLANNED_FOR_EXECUTION_CANDIDATE_ONLY" for item in rows)
    assert all(item["authorization_status"] == "NOT_AUTHORIZED" for item in rows)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in rows)


def test_planned_label_family_outputs_are_complete_and_not_generated(
    package: dict,
) -> None:
    rows = package["planned_label_family_outputs"]
    assert [item["label_family_candidate_id"] for item in rows] == (
        candidate.candidate_service.LABEL_FAMILY_CANDIDATES
    )
    assert len(rows) == 10
    assert all(item["planned_output_status"] == "PLANNED_NOT_GENERATED" for item in rows)
    assert all(item["label_generation_authorized"] is False for item in rows)
    assert all(item["label_generation_performed"] is False for item in rows)


def test_planned_execution_outputs_are_complete_and_not_generated(package: dict) -> None:
    rows = package["planned_execution_outputs"]
    assert [item["output_id"] for item in rows] == candidate.PLANNED_EXECUTION_OUTPUTS
    assert len(rows) == 8
    assert all(item["output_status"] == "PLANNED_NOT_GENERATED" for item in rows)
    assert all(item["authority"] == "RESEARCH_ONLY_NON_ACTIONABLE" for item in rows)


def test_per_ticker_entries_preserve_order_counts_and_closed_authority(
    package: dict,
) -> None:
    entries = package["per_ticker_entries"]
    assert len(entries) == 12
    assert [item["ticker"] for item in entries] == candidate.TARGET_UNIVERSE
    for item in entries:
        assert item["historical_record_count"] == candidate.candidate_service.EXPECTED_RECORD_COUNTS[item["ticker"]]
        assert item["label_objective_redesign_approval_status"] == "APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY"
        assert item["label_objective_redesign_execution_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW"
        assert item["label_objective_redesign_authorized"] is False
        assert item["label_objective_redesign_executed"] is False
        assert item["redesigned_label_generation_authorized"] is False
        assert item["predictive_usefulness"] == "not accepted"
        assert item["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_entry_preserves_limitation(package: dict) -> None:
    entries = {item["ticker"]: item for item in package["per_ticker_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["redesign_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
    )
    assert all(
        entries[ticker]["meta_reduced_record_count_flag"] is False
        for ticker in candidate.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_per_ticker_digests_are_present_and_deterministic(package: dict) -> None:
    rebuilt = candidate.build_label_objective_redesign_execution_candidate_v1()
    assert all(
        len(item["per_ticker_label_objective_redesign_execution_candidate_digest"]) == 64
        for item in package["per_ticker_entries"]
    )
    assert [
        item["per_ticker_label_objective_redesign_execution_candidate_digest"]
        for item in package["per_ticker_entries"]
    ] == [
        item["per_ticker_label_objective_redesign_execution_candidate_digest"]
        for item in rebuilt["per_ticker_entries"]
    ]


def test_future_chain_gates_and_risk_controls_are_exact(package: dict) -> None:
    assert package["future_chain"] == candidate.FUTURE_CHAIN
    assert len(package["future_chain"]) == 10
    assert package["future_gates"] == candidate.FUTURE_GATES
    assert len(package["future_gates"]) == 12
    assert package["risk_controls"] == candidate.RISK_CONTROLS
    assert len(package["risk_controls"]) == 14


def test_checklist_and_summary_pass(package: dict) -> None:
    assert [item["check_id"] for item in package["review_checklist"]] == candidate.CHECK_IDS
    assert all(item["status"] == "PASS" for item in package["review_checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in package["review_checklist"])
    assert package["review_summary"]["total_checks"] == len(candidate.CHECK_IDS) == 54
    assert package["review_summary"]["passed_checks"] == 54
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["blocker_count"] == 0
    assert package["review_summary"]["ready_for_operator_review"] is True
    assert package["review_summary"]["ready_for_label_objective_redesign_execution_approval"] is False


def test_candidate_digest_is_present_and_deterministic(package: dict) -> None:
    rebuilt = candidate.build_label_objective_redesign_execution_candidate_v1()
    digest = package["label_objective_redesign_execution_candidate_digest"]
    assert len(digest) == 64
    assert digest == rebuilt["label_objective_redesign_execution_candidate_digest"]
    assert digest == candidate.label_objective_redesign_execution_candidate_digest_v1(package)


def test_validator_accepts_valid_candidate(package: dict) -> None:
    result = candidate.validate_label_objective_redesign_execution_candidate_v1(package)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTION_CANDIDATE_VALID"
    assert result["ready_for_operator_review"] is True
    assert result["ready_for_label_objective_redesign_execution_approval"] is False
    assert result["ready_for_label_objective_redesign_execution"] is False
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("label_objective_redesign_approval_digest", None),
        ("label_objective_redesign_candidate_review_package_digest", None),
        ("records_digest", None),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("label_objective_redesign_approved", False),
        ("ready_for_label_objective_redesign_execution_candidate", False),
        ("label_objective_redesign_execution_candidate_created", False),
        ("label_objective_redesign_execution_candidate_review_created", True),
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
def test_validator_rejects_wrong_fields_and_open_authorities(
    package: dict, field: str, value: object
) -> None:
    invalid = deepcopy(package)
    invalid[field] = value
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.validate_label_objective_redesign_execution_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "planned_execution_activities",
        "planned_workstreams",
        "planned_label_family_outputs",
        "planned_execution_outputs",
        "future_chain",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_planning_sections(
    package: dict, field: str
) -> None:
    invalid = deepcopy(package)
    invalid[field] = []
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.validate_label_objective_redesign_execution_candidate_v1(invalid)


def test_validator_rejects_missing_candidate_digest(package: dict) -> None:
    invalid = deepcopy(package)
    invalid.pop("label_objective_redesign_execution_candidate_digest")
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.validate_label_objective_redesign_execution_candidate_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["per_ticker_entries"][0].pop(
        "per_ticker_label_objective_redesign_execution_candidate_digest"
    )
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.validate_label_objective_redesign_execution_candidate_v1(invalid)


def test_markdown_includes_all_required_sections(package: dict) -> None:
    markdown = candidate.build_label_objective_redesign_execution_candidate_markdown_v1(
        package
    )
    for section in [
        "Title",
        "Label Objective Redesign Execution Candidate",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Candidate Objective",
        "Problem Basis",
        "Planned Execution Activities",
        "Planned Workstreams",
        "Planned Label Family Outputs",
        "Planned Execution Outputs",
        "Per-Ticker Entries",
        "Future Chain",
        "Future Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]:
        assert f"## {section}" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    package: dict, tmp_path
) -> None:
    result = candidate.write_label_objective_redesign_execution_candidate_v1(
        tmp_path
    )
    path = tmp_path / result["filename"]
    assert json.loads(path.read_text(encoding="utf-8")) == package
    assert result["payload_sha256"]
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.write_label_objective_redesign_execution_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["candidate.txt", "../candidate.json"])
def test_writer_rejects_unsafe_or_non_json_filename(tmp_path, filename: str) -> None:
    with pytest.raises(candidate.LabelObjectiveRedesignExecutionCandidateError):
        candidate.write_label_objective_redesign_execution_candidate_v1(
            tmp_path, filename=filename
        )
