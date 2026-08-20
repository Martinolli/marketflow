from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    method_evidence_improvement_path_selection_redesigned_evidence_service as service,
)


@pytest.fixture(scope="module")
def operator_attestation() -> dict:
    return service.build_method_evidence_improvement_path_selection_using_redesigned_evidence_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-20T12:00:00Z",
        operator_attestation_phrase=service.REQUIRED_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=service.EXPECTED_CANDIDATE_DIGEST,
        operator_confirms_readiness_review_digest=service.EXPECTED_READINESS_REVIEW_DIGEST,
        operator_confirms_reassessment_digest=service.EXPECTED_REASSESSMENT_DIGEST,
        operator_confirms_results_review_digest=service.EXPECTED_RESULTS_REVIEW_DIGEST,
        operator_confirms_records_digest=service.EXPECTED_RECORDS_DIGEST,
        operator_confirms_target_universe=service.EXPECTED_TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_source_readiness_not_ready=True,
        operator_confirms_selected_option=service.SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION,
        operator_confirms_next_artifact_kind=service.NEXT_ARTIFACT_KIND,
        operator_confirms_selection_only=True,
        operator_confirms_no_next_candidate_created=True,
        operator_confirms_no_improvement_approval=True,
        operator_confirms_no_improvement_execution=True,
        operator_confirms_no_evidence_generation=True,
        operator_confirms_no_metric_recomputation=True,
        operator_confirms_no_model_training=True,
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
def selection(operator_attestation: dict) -> dict:
    return service.build_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
        operator_attestation=operator_attestation
    )


def _reject(selection: dict, field: str, value) -> None:
    changed = deepcopy(selection)
    changed[field] = value
    with pytest.raises(service.MethodEvidenceImprovementPathSelectionRedesignedEvidenceError):
        service.validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
            changed
        )


def test_a_attestation_builder_creates_required_fields(operator_attestation):
    assert operator_attestation["operator_decision"] == service.OPERATOR_DECISION
    assert operator_attestation["selected_option"] == service.SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION
    assert all(operator_attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_b_selection_package_builds_offline(selection):
    assert selection["created_offline"] is True
    assert selection["provider_requests_made_in_selection"] is False


def test_c_artifact_kind_is_correct(selection):
    assert selection["artifact_kind"] == service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE


def test_d_selection_status_is_correct(selection):
    assert selection["selection_status"] == service.METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE


def test_e_selection_scope_is_correct(selection):
    assert selection["selection_scope"] == service.METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY


def test_f_candidate_review_digest_is_bound(selection):
    assert selection["method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_g_candidate_digest_is_bound(selection):
    assert selection["method_evidence_improvement_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_h_readiness_review_digest_is_bound(selection):
    assert selection["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_i_reassessment_digest_is_bound(selection):
    assert selection["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_j_results_review_digest_is_bound(selection):
    assert selection["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_k_records_digest_is_bound(selection):
    assert selection["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_l_universe_count_and_order_are_preserved(selection):
    assert selection["target_universe_count"] == 12
    assert selection["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_m_meta_913_is_preserved(selection):
    assert selection["meta_record_count"] == 913
    assert selection["meta_reduced_record_count_preserved"] is True


def test_n_source_readiness_decision_is_not_ready(selection):
    assert selection["source_readiness_decision"] == service.SOURCE_READINESS_DECISION
    assert selection["selection_basis"]["readiness_decision_not_ready"] is True


def test_o_selected_option_is_option_a(selection):
    assert selection["selected_method_evidence_improvement_option"] == service.SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION


def test_p_selected_option_matches_recommendation(selection):
    assert selection["selection_basis"]["selected_option_matches_recommendation"] is True


def test_q_path_selected_and_selection_created_are_true(selection):
    assert selection["method_evidence_improvement_path_selected"] is True
    assert selection["method_evidence_improvement_path_selection_created"] is True


def test_r_next_artifact_kind_is_bound(selection):
    assert selection["next_artifact_kind"] == service.NEXT_ARTIFACT_KIND


def test_s_next_artifact_created_is_false(selection):
    assert selection["next_artifact_created"] is False
    assert selection["label_objective_target_definition_review_candidate_created"] is False


def test_t_improvement_approval_and_execution_are_false(selection):
    assert selection["method_evidence_improvement_approved"] is False
    assert selection["method_evidence_improvement_authorized"] is False
    assert selection["method_evidence_improvement_executed"] is False


def test_u_improved_evidence_planning_candidate_is_false(selection):
    assert selection["improved_evidence_planning_candidate_created"] is False
    assert selection["additional_predictive_evidence_executed"] is False


def test_v_predictive_usefulness_is_not_accepted(selection):
    assert selection["predictive_usefulness"] == "not accepted"


def test_w_acceptance_ready_and_candidate_are_false(selection):
    assert selection["predictive_usefulness_acceptance_ready"] is False
    assert selection["predictive_usefulness_acceptance_candidate_created"] is False


def test_x_profitability_is_not_accepted(selection):
    assert selection["profitability"] == "not accepted"


def test_y_runtime_is_not_authorized(selection):
    assert selection["runtime_use"] == "NOT_AUTHORIZED"
    assert selection["strategy_use"] == "NOT_AUTHORIZED"


def test_z_trade_recommendations_are_false(selection):
    assert selection["trade_recommendations_generated"] is False


def test_aa_path_options_are_preserved(selection):
    assert [row["option_id"] for row in selection["path_options"]] == service.PATH_OPTION_IDS


def test_ab_only_option_a_is_selected(selection):
    assert [row["option_id"] for row in selection["path_options"] if row["selected"]] == [service.SELECTED_METHOD_EVIDENCE_IMPROVEMENT_OPTION]


def test_ac_selection_basis_is_preserved(selection):
    assert selection["selection_decision_basis"] == service.SELECTION_DECISION_BASIS
    assert selection["selection_basis"]["oos_cross_sectional_delta_vs_majority"] == "0.00309917"


def test_ad_next_candidate_scope_is_defined(selection):
    assert selection["next_candidate_scope"]["label_objective_target_definition_review_candidate_status"] == "PLANNED_NOT_CREATED"
    assert selection["next_candidate_scope"]["label_objective_target_definition_review_candidate_authority_status"] == "NOT_AUTHORIZED"


def test_ae_planned_next_candidate_areas_are_defined(selection):
    assert [row["review_area"] for row in selection["planned_next_candidate_review_areas"]] == service.PLANNED_NEXT_CANDIDATE_REVIEW_AREAS
    assert all(row["status"] == "PLANNED_NOT_EXECUTED" for row in selection["planned_next_candidate_review_areas"])


def test_af_per_ticker_entries_count_is_12(selection):
    assert len(selection["per_ticker_selection_entries"]) == 12


def test_ag_per_ticker_selection_digests_are_present(selection):
    assert all(len(row["per_ticker_method_evidence_improvement_path_selection_digest"]) == 64 for row in selection["per_ticker_selection_entries"])


def test_ah_next_chain_is_defined(selection):
    assert selection["next_chain"] == service.NEXT_CHAIN
    assert selection["next_gates"] == service.NEXT_GATES


def test_ai_risk_controls_are_defined(selection):
    assert selection["risk_controls"] == service.RISK_CONTROLS


def test_aj_checklist_passes(selection):
    assert selection["selection_summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert selection["selection_summary"]["failed_checks"] == 0


def test_ak_selection_digest_is_deterministic(selection):
    assert service.method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(selection) == selection["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"]


def test_al_per_ticker_selection_digests_are_deterministic(selection):
    for entry in selection["per_ticker_selection_entries"]:
        assert service.per_ticker_method_evidence_improvement_path_selection_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_method_evidence_improvement_path_selection_digest"]


def test_am_validator_accepts_valid_selection(selection):
    result = service.validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(selection)
    assert result["blocker_count"] == 0


def test_an_validator_rejects_wrong_artifact_kind(selection):
    _reject(selection, "artifact_kind", "WRONG")


def test_ao_validator_rejects_wrong_selection_status(selection):
    _reject(selection, "selection_status", "WRONG")


def test_ap_validator_rejects_wrong_scope(selection):
    _reject(selection, "selection_scope", "WRONG")


def test_aq_validator_rejects_selected_option_not_option_a(selection):
    _reject(selection, "selected_method_evidence_improvement_option", service.PATH_OPTION_IDS[1])


def test_ar_validator_rejects_next_artifact_created_true(selection):
    _reject(selection, "next_artifact_created", True)


def test_as_validator_rejects_improvement_approval_true(selection):
    _reject(selection, "method_evidence_improvement_approved", True)


def test_at_validator_rejects_improved_evidence_candidate_true(selection):
    _reject(selection, "improved_evidence_planning_candidate_created", True)


def test_au_validator_rejects_predictive_usefulness_accepted(selection):
    _reject(selection, "predictive_usefulness", "accepted")


def test_av_validator_rejects_acceptance_ready_true(selection):
    _reject(selection, "predictive_usefulness_acceptance_ready", True)


def test_aw_validator_rejects_runtime_authorized(selection):
    _reject(selection, "runtime_use", "AUTHORIZED")


def test_ax_validator_rejects_trade_recommendations_true(selection):
    _reject(selection, "trade_recommendations_generated", True)


def test_ay_validator_rejects_wrong_operator_decision(selection):
    changed = deepcopy(selection)
    changed["operator_attestation"]["operator_decision"] = "WRONG"
    with pytest.raises(service.MethodEvidenceImprovementPathSelectionRedesignedEvidenceError):
        service.validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(changed)


def test_az_validator_rejects_wrong_attestation_phrase(selection):
    changed = deepcopy(selection)
    changed["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(service.MethodEvidenceImprovementPathSelectionRedesignedEvidenceError):
        service.validate_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(changed)


def test_ba_validator_rejects_missing_path_options(selection):
    _reject(selection, "path_options", None)


def test_bb_validator_rejects_missing_next_candidate_scope(selection):
    _reject(selection, "next_candidate_scope", None)


def test_bc_markdown_includes_required_sections(selection):
    markdown = service.build_method_evidence_improvement_path_selection_using_redesigned_evidence_markdown_v1(selection)
    for section in (
        "## Operator Attestation", "## Source Candidate Review", "## Bound Evidence",
        "## Dataset and Universe", "## Path Options", "## Selected Option",
        "## Selection Basis", "## Next Candidate Scope",
        "## Planned Next-Candidate Review Areas", "## Per-Ticker Selection Entries",
        "## Next Chain", "## Next Gates", "## Risk Controls",
        "## Predictive Usefulness Boundary", "## Profitability Boundary",
        "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_bd_writer_creates_canonical_json_without_overwrite(tmp_path, operator_attestation):
    receipt = service.write_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
        tmp_path,
        operator_attestation=operator_attestation,
    )
    payload = json.loads((tmp_path / "method_evidence_improvement_path_selection_using_redesigned_evidence_v1.json").read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE
    assert len(receipt["payload_sha256"]) == 64
    with pytest.raises(service.MethodEvidenceImprovementPathSelectionRedesignedEvidenceError):
        service.write_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
            tmp_path,
            operator_attestation=operator_attestation,
        )


def test_be_attestation_mismatch_fails_closed(operator_attestation):
    changed = deepcopy(operator_attestation)
    changed["operator_confirms_meta_record_count"] = 1003
    with pytest.raises(service.MethodEvidenceImprovementPathSelectionRedesignedEvidenceError):
        service.build_method_evidence_improvement_path_selection_using_redesigned_evidence_v1(
            operator_attestation=changed
        )
