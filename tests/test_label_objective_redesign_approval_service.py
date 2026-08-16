from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import label_objective_redesign_approval_service as approval


def _attestation() -> dict:
    return approval.build_label_objective_redesign_approval_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-16T18:30:00Z",
        operator_attestation_phrase=(
            approval.REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE
        ),
        operator_confirms_label_objective_redesign_candidate_review_digest=(
            approval.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        operator_confirms_label_objective_redesign_candidate_digest=(
            approval.EXPECTED_CANDIDATE_DIGEST
        ),
        operator_confirms_operator_method_path_selection_digest=(
            approval.candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST
        ),
        operator_confirms_method_diagnostic_review_digest=(
            approval.candidate_service.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST
        ),
        operator_confirms_planning_tree_review_digest=(
            approval.candidate_service.EXPECTED_PLANNING_TREE_REVIEW_DIGEST
        ),
        operator_confirms_latest_readiness_digest=(
            approval.candidate_service.EXPECTED_LATEST_READINESS_DIGEST
        ),
        operator_confirms_research_registry_approval_digest=(
            approval.candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        operator_confirms_records_digest=(
            approval.candidate_service.EXPECTED_RECORDS_DIGEST
        ),
        operator_confirms_target_universe=approval.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_selected_method_path=(
            approval.candidate_service.SELECTED_METHOD_PATH
        ),
        operator_confirms_two_readiness_gates_not_ready=True,
        operator_confirms_label_objective_redesign_approval_scope_only=True,
        operator_confirms_label_objective_redesign_approved=True,
        operator_confirms_ready_for_label_objective_redesign_execution_candidate=True,
        operator_confirms_no_label_objective_redesign_authorization=True,
        operator_confirms_no_label_objective_redesign_execution=True,
        operator_confirms_no_redesigned_label_generation_authorization=True,
        operator_confirms_no_redesigned_label_generation=True,
        operator_confirms_no_additional_predictive_evidence_execution_candidate=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_strategy_authorization=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


@pytest.fixture(scope="module")
def attestation() -> dict:
    return _attestation()


@pytest.fixture(scope="module")
def package(attestation: dict) -> dict:
    return approval.build_label_objective_redesign_approved_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == (
        "2026-08-16T18:30:00Z"
    )
    assert attestation["operator_decision"] == (
        "APPROVE_LABEL_OBJECTIVE_REDESIGN"
    )
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        approval.OPERATOR_ATTESTATION_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1
    )
    assert all(
        attestation[field] is True
        for field in approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
    )


def test_approval_builds_offline(
    attestation: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = approval.build_label_objective_redesign_approved_v1(
        operator_attestation=attestation
    )
    assert built["created_offline"] is True
    assert built["provider_requests_made"] is False


def test_artifact_status_and_scope_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_APPROVED"
    assert package["schema_version"] == "label_objective_redesign_approval_v1"
    assert package["approval_status"] == "LABEL_OBJECTIVE_REDESIGN_APPROVED"
    assert package["approval_scope"] == "LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY"


@pytest.mark.parametrize(
    ("field", "expected"), list(approval.REQUIRED_DIGEST_FIELDS.items())
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
    assert package["target_universe"] == approval.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946


def test_meta_913_and_other_record_counts_are_preserved(package: dict) -> None:
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert package["meta_reduced_record_count_preserved"] is True
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in approval.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_selected_method_and_approved_objective_are_exact(package: dict) -> None:
    assert package["selected_method_path"] == (
        "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
    )
    assert package["label_objective_redesign_objective"] == (
        approval.candidate_service.LABEL_OBJECTIVE_REDESIGN_OBJECTIVE
    )
    assert package["label_objective_redesign_scope"] == (
        "LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY_NOT_EXECUTION"
    )
    assert package["label_objective_redesign_mode"] == "APPROVED_NOT_EXECUTED"
    assert package["label_objective_redesign_authority_status"] == (
        "APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY"
    )


def test_approval_created_and_ready_for_future_candidate(package: dict) -> None:
    assert package["label_objective_redesign_candidate_created"] is True
    assert package["label_objective_redesign_candidate_review_created"] is True
    assert package["label_objective_redesign_approved"] is True
    assert package["label_objective_redesign_approval_created"] is True
    assert package["ready_for_label_objective_redesign_execution_candidate"] is True


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


def test_problem_basis_is_approved_without_change(package: dict) -> None:
    assert package["approved_problem_basis"] == {
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


def test_approved_hypotheses_count_and_state_are_exact(package: dict) -> None:
    rows = package["approved_hypotheses"]
    assert [item["hypothesis_id"] for item in rows] == (
        approval.candidate_service.DIAGNOSTIC_HYPOTHESES
    )
    assert len(rows) == 13
    assert all(item["approval_status"] == "APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY" for item in rows)
    assert all(item["test_status"] == "NOT_TESTED" for item in rows)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in rows)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in rows)


def test_approved_redesign_dimensions_count_and_state_are_exact(package: dict) -> None:
    rows = package["approved_redesign_dimensions"]
    assert [item["dimension_id"] for item in rows] == (
        approval.candidate_service.REDESIGN_DIMENSIONS
    )
    assert len(rows) == 14
    assert all(item["approval_status"] == "APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY" for item in rows)
    assert all(item["design_status"] == "NOT_DESIGNED" for item in rows)
    assert all(item["authorization_status"] == "NOT_AUTHORIZED_FOR_EXECUTION" for item in rows)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in rows)


def test_approved_label_family_candidates_count_and_state_are_exact(
    package: dict,
) -> None:
    rows = package["approved_label_family_candidates"]
    assert [item["label_family_candidate_id"] for item in rows] == (
        approval.candidate_service.LABEL_FAMILY_CANDIDATES
    )
    assert len(rows) == 10
    assert all(item["approval_status"] == "APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY" for item in rows)
    assert all(item["candidate_status"] == "PLANNED_NOT_GENERATED" for item in rows)
    assert all(item["label_generation_authorized"] is False for item in rows)
    assert all(item["label_generation_performed"] is False for item in rows)


def test_approved_evaluation_questions_count_and_state_are_exact(package: dict) -> None:
    rows = package["approved_evaluation_questions"]
    assert [item["question_id"] for item in rows] == (
        approval.candidate_service.EVALUATION_QUESTIONS
    )
    assert len(rows) == 10
    assert all(item["approval_status"] == "APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY" for item in rows)
    assert all(item["question_status"] == "PLANNED_FOR_FUTURE_REVIEW" for item in rows)
    assert all(item["answer_status"] == "NOT_ANSWERED" for item in rows)
    assert all(item["requires_execution"] is False for item in rows)


def test_per_ticker_approval_entries_preserve_order_counts_and_scope(
    package: dict,
) -> None:
    entries = package["per_ticker_approval_entries"]
    assert len(entries) == 12
    assert [item["ticker"] for item in entries] == approval.TARGET_UNIVERSE
    for item in entries:
        assert item["historical_record_count"] == approval.candidate_service.EXPECTED_RECORD_COUNTS[item["ticker"]]
        assert item["label_objective_redesign_candidate_status"] == "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT"
        assert item["label_objective_redesign_approval_status"] == "APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY"
        assert item["label_objective_redesign_approved"] is True
        assert item["label_objective_redesign_authorized"] is False
        assert item["label_objective_redesign_executed"] is False
        assert item["redesigned_label_generation_authorized"] is False
        assert item["predictive_usefulness"] == "not accepted"
        assert item["runtime_use"] == "NOT_AUTHORIZED"


def test_meta_per_ticker_approval_preserves_limitation(package: dict) -> None:
    entries = {item["ticker"]: item for item in package["per_ticker_approval_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["redesign_note"] == (
        "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
    )
    assert all(
        entries[ticker]["meta_reduced_record_count_flag"] is False
        for ticker in approval.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_per_ticker_approval_digests_are_present_and_deterministic(
    package: dict, attestation: dict
) -> None:
    rebuilt = approval.build_label_objective_redesign_approved_v1(
        operator_attestation=attestation
    )
    assert all(
        len(item["per_ticker_label_objective_redesign_approval_digest"]) == 64
        for item in package["per_ticker_approval_entries"]
    )
    assert [
        item["per_ticker_label_objective_redesign_approval_digest"]
        for item in package["per_ticker_approval_entries"]
    ] == [
        item["per_ticker_label_objective_redesign_approval_digest"]
        for item in rebuilt["per_ticker_approval_entries"]
    ]


def test_next_chain_gates_and_risk_controls_are_exact(package: dict) -> None:
    assert package["next_chain"] == approval.NEXT_CHAIN
    assert len(package["next_chain"]) == 11
    assert package["next_gates"] == approval.NEXT_GATES
    assert len(package["next_gates"]) == 13
    assert package["risk_controls"] == approval.RISK_CONTROLS
    assert len(package["risk_controls"]) == 14


def test_checklist_and_summary_pass(package: dict) -> None:
    assert [item["check_id"] for item in package["approval_checklist"]] == approval.CHECK_IDS
    assert all(item["status"] == "PASS" for item in package["approval_checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in package["approval_checklist"])
    assert package["approval_summary"]["total_checks"] == len(approval.CHECK_IDS)
    assert package["approval_summary"]["passed_checks"] == len(approval.CHECK_IDS)
    assert package["approval_summary"]["failed_checks"] == 0
    assert package["approval_summary"]["blocker_count"] == 0
    assert package["approval_summary"]["label_objective_redesign_approved"] is True
    assert package["approval_summary"]["label_objective_redesign_authorized"] is False


def test_approval_digest_is_present_and_deterministic(
    package: dict, attestation: dict
) -> None:
    rebuilt = approval.build_label_objective_redesign_approved_v1(
        operator_attestation=attestation
    )
    digest = package["label_objective_redesign_approval_digest"]
    assert len(digest) == 64
    assert digest == rebuilt["label_objective_redesign_approval_digest"]
    assert digest == approval.label_objective_redesign_approval_digest_v1(package)


def test_validator_accepts_valid_approval(package: dict) -> None:
    result = approval.validate_label_objective_redesign_approved_v1(package)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_APPROVAL_VALID"
    assert result["label_objective_redesign_approved"] is True
    assert result["ready_for_label_objective_redesign_execution_candidate"] is True
    assert result["label_objective_redesign_authorized"] is False
    assert result["label_objective_redesign_executed"] is False
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("label_objective_redesign_candidate_review_package_digest", None),
        ("label_objective_redesign_candidate_digest", None),
        ("operator_method_path_selection_digest", None),
        ("records_digest", None),
        ("selected_method_path", "OPTION_A_PAUSE_AND_ARCHIVE_RESEARCH_CHAIN"),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("meta_record_count", 1003),
        ("label_objective_redesign_approved", False),
        ("label_objective_redesign_approval_created", False),
        ("ready_for_label_objective_redesign_execution_candidate", False),
        ("label_objective_redesign_authorized", True),
        ("label_objective_redesign_executed", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
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
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.validate_label_objective_redesign_approved_v1(invalid)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_target_universe", list(reversed(approval.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_meta_record_count", 1003),
        ("operator_confirms_non_meta_record_count", 913),
        ("operator_confirms_selected_method_path", "WRONG"),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_builder_rejects_invalid_attestation_fields(
    attestation: dict, field: str, value: object
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = value
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.build_label_objective_redesign_approved_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize(
    "field", approval.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS
)
def test_builder_rejects_missing_true_confirmation(
    attestation: dict, field: str
) -> None:
    invalid = deepcopy(attestation)
    invalid[field] = False
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.build_label_objective_redesign_approved_v1(
            operator_attestation=invalid
        )


def test_validator_rejects_missing_risk_controls(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["risk_controls"] = []
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.validate_label_objective_redesign_approved_v1(invalid)


def test_validator_rejects_missing_approval_digest(package: dict) -> None:
    invalid = deepcopy(package)
    invalid.pop("label_objective_redesign_approval_digest")
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.validate_label_objective_redesign_approved_v1(invalid)


def test_validator_rejects_missing_per_ticker_approval_digest(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["per_ticker_approval_entries"][0].pop(
        "per_ticker_label_objective_redesign_approval_digest"
    )
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.validate_label_objective_redesign_approved_v1(invalid)


def test_markdown_includes_all_required_sections(package: dict) -> None:
    markdown = approval.build_label_objective_redesign_approved_markdown_v1(package)
    for section in [
        "Title",
        "Label Objective Redesign Approval",
        "Operator Attestation",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Problem Basis",
        "Approved Hypotheses",
        "Approved Redesign Dimensions",
        "Approved Label Family Candidates",
        "Approved Evaluation Questions",
        "Per-Ticker Approval Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ]:
        assert f"## {section}" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    package: dict, attestation: dict, tmp_path
) -> None:
    result = approval.write_label_objective_redesign_approved_v1(
        tmp_path, operator_attestation=attestation
    )
    path = tmp_path / result["filename"]
    assert json.loads(path.read_text(encoding="utf-8")) == package
    assert result["payload_sha256"]
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.write_label_objective_redesign_approved_v1(
            tmp_path, operator_attestation=attestation
        )


@pytest.mark.parametrize("filename", ["approval.txt", "../approval.json"])
def test_writer_rejects_unsafe_or_non_json_filename(
    attestation: dict, tmp_path, filename: str
) -> None:
    with pytest.raises(approval.LabelObjectiveRedesignApprovalError):
        approval.write_label_objective_redesign_approved_v1(
            tmp_path,
            operator_attestation=attestation,
            filename=filename,
        )
