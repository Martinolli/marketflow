from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    predictive_evidence_operator_method_path_selection_service as selection,
)


def _attestation() -> dict:
    return selection.build_predictive_evidence_operator_method_path_selection_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-16T12:00:00Z",
        operator_attestation_phrase=(
            selection.REQUIRED_OPERATOR_METHOD_PATH_SELECTION_ATTESTATION_PHRASE
        ),
        operator_confirms_method_diagnostic_review_digest=(
            selection.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST
        ),
        operator_confirms_planning_tree_review_digest=(
            selection.EXPECTED_PLANNING_TREE_REVIEW_DIGEST
        ),
        operator_confirms_latest_readiness_digest=(
            selection.EXPECTED_LATEST_READINESS_DIGEST
        ),
        operator_confirms_research_registry_approval_digest=(
            selection.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        operator_confirms_records_digest=selection.EXPECTED_RECORDS_DIGEST,
        operator_confirms_target_universe=selection.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_original_readiness_not_ready=True,
        operator_confirms_refined_readiness_not_ready=True,
        operator_confirms_predictive_usefulness_not_accepted=True,
        operator_confirms_profitability_not_accepted=True,
        operator_confirms_runtime_not_authorized=True,
        operator_confirms_acceptance_option_not_allowed=True,
        operator_confirms_selected_method_path=(
            selection.SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE
        ),
        operator_confirms_selection_scope_only=True,
        operator_confirms_no_label_objective_redesign_candidate_created=True,
        operator_confirms_no_execution_authorized=True,
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
    return selection.build_predictive_evidence_operator_method_path_selection_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_all_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == (
        selection.OPERATOR_DECISION_SELECT_LABEL_OBJECTIVE_REDESIGN_CANDIDATE
    )
    assert attestation["operator_attestation_phrase"] == (
        selection.REQUIRED_OPERATOR_METHOD_PATH_SELECTION_ATTESTATION_PHRASE
    )
    assert attestation["operator_attestation_version"] == (
        selection.OPERATOR_ATTESTATION_VERSION_V1
    )
    assert attestation["operator_attestation_timestamp_utc"] == (
        "2026-08-16T12:00:00Z"
    )
    for field in selection.BOOLEAN_CONFIRMATION_FIELDS:
        assert attestation[field] is True


def test_selection_builds_offline_without_provider_calls(
    attestation: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = selection.build_predictive_evidence_operator_method_path_selection_v1(
        operator_attestation=attestation
    )
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_selection"] is False


def test_artifact_status_scope_and_selection_state_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        selection.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION
    )
    assert package["selection_status"] == (
        selection.PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTED
    )
    assert package["selection_scope"] == (
        selection.METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION
    )
    assert package["operator_method_path_selection_created"] is True
    assert package["operator_method_path_selection_ready"] is True
    assert package["method_path_selected"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    list(selection.REQUIRED_DIGEST_FIELDS.items()),
)
def test_required_digest_chain_is_bound(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_dataset_universe_and_meta_limitation_are_preserved(package: dict) -> None:
    assert package["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert package["source_profile"] == "RTH_FULL_SESSION_1D"
    assert package["timeframe"] == "1d"
    assert package["target_universe"] == selection.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert package["meta_reduced_record_count_preserved"] is True
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in selection.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_selected_path_opens_only_future_candidate_gate(package: dict) -> None:
    assert package["selected_method_path"] == (
        "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
    )
    assert package["selected_next_artifact_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_CANDIDATE"
    )
    assert package["selected_path_status"] == (
        "SELECTED_FOR_FUTURE_CANDIDATE_ONLY"
    )
    assert package["ready_for_label_objective_redesign_candidate"] is True
    assert package["label_objective_redesign_candidate_created"] is False
    assert package["execution_authorized"] is False


def test_selection_rationale_and_evidence_comparison_are_exact(package: dict) -> None:
    assert package["selection_reason"] == selection.SELECTION_REASON
    assert package["selection_basis"] == selection.SELECTION_BASIS
    assert package["evidence_comparison"] == {
        "original_oos_majority_accuracy": "0.539491",
        "original_oos_previous_direction_accuracy": "0.495984",
        "original_oos_ticker_cross_sectional_accuracy": "0.502677",
        "original_oos_brier_score": "0.24875351",
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "refined_signal_consistency": "WEAK_OR_MIXED",
        "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
        "refined_model_comparison": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
    }


def test_method_options_and_states_are_exact(package: dict) -> None:
    options = package["method_options"]
    assert [item["option_id"] for item in options] == selection.OPTION_IDS
    assert {item["option_id"]: item["status"] for item in options} == (
        selection.OPTION_STATES
    )
    assert all(item["execution_authorized"] is False for item in options)
    assert all(item["candidate_created"] is False for item in options)


def test_next_chain_and_risk_controls_are_exact(package: dict) -> None:
    assert package["next_chain"] == selection.NEXT_CHAIN
    assert len(package["next_chain"]) == 9
    assert package["risk_controls"] == selection.RISK_CONTROLS
    assert len(package["risk_controls"]) == 14


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_candidate_created",
        "feature_method_redesign_candidate_created",
        "data_scope_expansion_candidate_created",
        "new_modeling_approach_candidate_created",
        "execution_authorized",
        "provider_requests_made_in_selection",
        "live_provider_transport_enabled_in_selection",
        "market_data_acquisition_performed_in_selection",
        "dataset_regeneration_performed_in_selection",
        "predictive_evidence_rerun_performed",
        "metrics_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
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
def test_execution_candidate_and_authority_actions_remain_false(
    package: dict, field: str
) -> None:
    assert package[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", selection.NOT_ACCEPTED),
        ("profitability", selection.NOT_ACCEPTED),
        ("runtime_use", selection.NOT_AUTHORIZED),
        ("strategy_use", selection.NOT_AUTHORIZED),
        ("paper_trading", selection.NOT_AUTHORIZED),
        ("broker_execution", selection.NOT_AUTHORIZED),
    ],
)
def test_final_authorities_remain_closed(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_checklist_and_summary_pass(package: dict) -> None:
    checklist = package["review_checklist"]
    assert [item["check_id"] for item in checklist] == selection.CHECK_IDS
    assert all(
        set(item)
        == {"check_id", "status", "expected", "actual", "severity", "message"}
        for item in checklist
    )
    assert all(item["status"] == selection.PASS for item in checklist)
    summary = package["review_summary"]
    assert summary["total_checks"] == len(selection.CHECK_IDS) == 33
    assert summary["passed_checks"] == 33
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["selected_method_path"] == (
        selection.SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE
    )
    assert summary["ready_for_label_objective_redesign_candidate"] is True
    assert summary["label_objective_redesign_candidate_created"] is False
    assert summary["acceptance_candidate_allowed"] is False


def test_selection_digest_is_deterministic(package: dict) -> None:
    repeated = selection.build_predictive_evidence_operator_method_path_selection_v1(
        operator_attestation=_attestation()
    )
    field = "predictive_evidence_operator_method_path_selection_digest"
    assert repeated[field] == package[field]
    assert repeated[field] == (
        selection.predictive_evidence_operator_method_path_selection_digest_v1(
            repeated
        )
    )
    assert len(repeated[field]) == 64


def test_validator_accepts_valid_package(package: dict) -> None:
    validation = selection.validate_predictive_evidence_operator_method_path_selection_v1(
        package
    )
    assert validation["status"] == (
        "PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION_VALID"
    )
    assert validation["selected_method_path"] == (
        selection.SELECTED_METHOD_PATH_OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE
    )
    assert validation["ready_for_label_objective_redesign_candidate"] is True
    assert validation["label_objective_redesign_candidate_created"] is False
    assert validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("selection_status", "WRONG"),
        ("selection_scope", "EXECUTION_AUTHORIZED"),
        ("predictive_evidence_method_diagnostic_review_package_digest", None),
        ("predictive_evidence_planning_tree_review_package_digest", None),
        ("latest_readiness_rerun_using_refined_evidence_digest", None),
        ("research_registry_approval_digest", None),
        ("records_digest", None),
        ("selected_method_path", "OPTION_D_FEATURE_METHOD_REDESIGN_CANDIDATE"),
        ("label_objective_redesign_candidate_created", True),
        ("execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("target_universe", list(reversed(selection.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("risk_controls", []),
        ("predictive_evidence_operator_method_path_selection_digest", None),
    ],
)
def test_validator_rejects_changed_contract_fields(
    package: dict, field: str, replacement: object
) -> None:
    invalid = deepcopy(package)
    invalid[field] = replacement
    with pytest.raises(selection.PredictiveEvidenceOperatorMethodPathSelectionError):
        selection.validate_predictive_evidence_operator_method_path_selection_v1(
            invalid
        )


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_attestation_timestamp_utc", "not-a-timestamp"),
        ("operator_attestation_version", "WRONG"),
        ("operator_reference", ""),
        ("operator_confirms_method_diagnostic_review_digest", "0" * 64),
        ("operator_confirms_planning_tree_review_digest", "0" * 64),
        ("operator_confirms_latest_readiness_digest", "0" * 64),
        ("operator_confirms_research_registry_approval_digest", "0" * 64),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(selection.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        (
            "operator_confirms_selected_method_path",
            "OPTION_D_FEATURE_METHOD_REDESIGN_CANDIDATE",
        ),
    ],
)
def test_builder_rejects_invalid_attestation_values(
    field: str, replacement: object
) -> None:
    invalid = _attestation()
    invalid[field] = replacement
    with pytest.raises(selection.PredictiveEvidenceOperatorMethodPathSelectionError):
        selection.build_predictive_evidence_operator_method_path_selection_v1(
            operator_attestation=invalid
        )


@pytest.mark.parametrize("field", selection.BOOLEAN_CONFIRMATION_FIELDS)
def test_builder_rejects_missing_or_false_required_confirmation(field: str) -> None:
    invalid = _attestation()
    invalid[field] = False
    with pytest.raises(selection.PredictiveEvidenceOperatorMethodPathSelectionError):
        selection.build_predictive_evidence_operator_method_path_selection_v1(
            operator_attestation=invalid
        )


def test_validator_rejects_acceptance_option_allowed(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["method_options"][-1]["status"] = "ALLOWED"
    with pytest.raises(selection.PredictiveEvidenceOperatorMethodPathSelectionError):
        selection.validate_predictive_evidence_operator_method_path_selection_v1(
            invalid
        )


def test_markdown_contains_required_sections(package: dict) -> None:
    markdown = selection.build_predictive_evidence_operator_method_path_selection_markdown_v1(
        package
    )
    for heading in (
        "Title",
        "Operator Method Path Selection",
        "Operator Attestation",
        "Bound Evidence",
        "Dataset and Universe",
        "Evidence Comparison",
        "Method Options",
        "Selected Method Path",
        "Selection Rationale",
        "Next Chain",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_emits_canonical_json_and_does_not_overwrite(
    tmp_path, attestation: dict
) -> None:
    result = selection.write_predictive_evidence_operator_method_path_selection_v1(
        tmp_path,
        operator_attestation=attestation,
    )
    output_path = tmp_path / result["filename"]
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    selection.validate_predictive_evidence_operator_method_path_selection_v1(
        payload
    )
    with pytest.raises(selection.PredictiveEvidenceOperatorMethodPathSelectionError):
        selection.write_predictive_evidence_operator_method_path_selection_v1(
            tmp_path,
            operator_attestation=attestation,
        )
