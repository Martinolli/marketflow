from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import label_objective_target_definition_review_approval_redesigned_evidence_service as service


@pytest.fixture(scope="module")
def operator_attestation() -> dict:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-20T12:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_candidate_review_digest": service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "operator_confirms_candidate_digest": service.EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_path_selection_digest": service.EXPECTED_PATH_SELECTION_DIGEST,
        "operator_confirms_readiness_review_digest": service.EXPECTED_READINESS_REVIEW_DIGEST,
        "operator_confirms_reassessment_digest": service.EXPECTED_REASSESSMENT_DIGEST,
        "operator_confirms_results_review_digest": service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "operator_confirms_records_digest": service.EXPECTED_RECORDS_DIGEST,
        "operator_confirms_target_universe": service.EXPECTED_TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_option": service.SELECTED_OPTION,
    }
    for field in service.ATTESTATION_BOOLEAN_FIELDS:
        kwargs[field] = True
    return service.build_label_objective_target_definition_review_approval_using_redesigned_evidence_attestation_v1(
        **kwargs
    )


@pytest.fixture(scope="module")
def approval(operator_attestation: dict) -> dict:
    return service.build_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
        operator_attestation=operator_attestation
    )


def _reject(approval: dict, field: str, value) -> None:
    changed = deepcopy(approval); changed[field] = value
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError):
        service.validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(changed)


def test_a_attestation_builder_creates_required_fields(operator_attestation):
    assert operator_attestation["operator_decision"] == service.OPERATOR_DECISION
    assert operator_attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert all(operator_attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_b_approval_package_builds_offline(approval):
    assert approval["created_offline"] is True
    assert approval["provider_requests_made_in_approval"] is False


def test_c_artifact_kind_is_correct(approval):
    assert approval["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE


def test_d_approval_status_is_correct(approval):
    assert approval["approval_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE


def test_e_approval_scope_is_correct(approval):
    assert approval["approval_scope"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVAL_ONLY


def test_f_candidate_review_digest_is_bound(approval):
    assert approval["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_g_candidate_digest_is_bound(approval):
    assert approval["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_h_path_selection_digest_is_bound(approval):
    assert approval["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == service.EXPECTED_PATH_SELECTION_DIGEST


def test_i_readiness_review_digest_is_bound(approval):
    assert approval["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_j_reassessment_digest_is_bound(approval):
    assert approval["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_k_results_review_digest_is_bound(approval):
    assert approval["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_l_records_digest_is_bound(approval):
    assert approval["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_m_universe_count_and_order_are_preserved(approval):
    assert approval["target_universe_count"] == 12
    assert approval["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_n_meta_913_is_preserved(approval):
    assert approval["meta_record_count"] == 913
    assert approval["meta_reduced_record_count_preserved"] is True


def test_o_selected_option_is_option_a(approval):
    assert approval["selected_method_evidence_improvement_option"] == service.SELECTED_OPTION


def test_p_approval_authorization_and_ready_are_true(approval):
    assert approval["label_objective_target_definition_review_approved"] is True
    assert approval["label_objective_target_definition_review_authorized"] is True
    assert approval["ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence"] is True


def test_q_review_executed_is_false(approval):
    assert approval["label_objective_target_definition_review_executed"] is False


def test_r_label_regeneration_remains_false(approval):
    assert approval["label_regeneration_authorized"] is False
    assert approval["label_regeneration_performed"] is False


def test_s_new_targets_created_remains_false(approval):
    assert approval["new_targets_created"] is False


def test_t_target_definition_change_authorized_remains_false(approval):
    assert approval["target_definition_change_authorized"] is False
    assert approval["target_definition_change_performed"] is False


def test_u_predictive_usefulness_is_not_accepted(approval):
    assert approval["predictive_usefulness"] == "not accepted"


def test_v_acceptance_ready_and_candidate_are_false(approval):
    assert approval["predictive_usefulness_acceptance_ready"] is False
    assert approval["predictive_usefulness_acceptance_candidate_created"] is False


def test_w_profitability_is_not_accepted(approval):
    assert approval["profitability"] == "not accepted"


def test_x_runtime_is_not_authorized(approval):
    assert approval["runtime_use"] == "NOT_AUTHORIZED"
    assert approval["strategy_use"] == "NOT_AUTHORIZED"


def test_y_trade_recommendations_are_false(approval):
    assert approval["trade_recommendations_generated"] is False


def test_z_approved_dimensions_count_is_12(approval):
    assert len(approval["approved_dimensions"]) == 12
    assert [row["dimension_id"] for row in approval["approved_dimensions"]] == service.REVIEW_DIMENSION_IDS


def test_aa_approved_label_families_count_is_10(approval):
    assert len(approval["approved_label_family_review_plan"]) == 10
    assert all(row["review_execution_authorized"] is True for row in approval["approved_label_family_review_plan"])


def test_ab_approved_diagnostic_questions_count_is_10(approval):
    assert len(approval["approved_diagnostic_questions"]) == 10
    assert all(row["question_answered"] is False for row in approval["approved_diagnostic_questions"])


def test_ac_approved_decision_options_count_is_7(approval):
    assert len(approval["approved_decision_options"]) == 7
    assert all(row["approved_for_target_change"] is False for row in approval["approved_decision_options"])


def test_ad_approved_future_outputs_are_present(approval):
    assert [row["output_name"] for row in approval["approved_future_outputs"]] == service.APPROVED_FUTURE_OUTPUT_NAMES
    assert all(row["output_status"] == "AUTHORIZED_NOT_GENERATED" for row in approval["approved_future_outputs"])


def test_ae_per_ticker_approval_entries_count_is_12(approval):
    assert len(approval["per_ticker_approval_entries"]) == 12


def test_af_per_ticker_approval_digests_are_present(approval):
    assert all(len(row["per_ticker_label_objective_target_definition_review_approval_digest"]) == 64 for row in approval["per_ticker_approval_entries"])


def test_ag_next_chain_is_defined(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES


def test_ah_risk_controls_are_defined(approval):
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_ai_checklist_passes(approval):
    assert approval["approval_summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert approval["approval_summary"]["failed_checks"] == 0


def test_aj_approval_digest_is_deterministic(approval):
    assert service.label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(approval) == approval["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"]


def test_ak_per_ticker_approval_digests_are_deterministic(approval):
    for entry in approval["per_ticker_approval_entries"]:
        assert service.per_ticker_label_objective_target_definition_review_approval_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_label_objective_target_definition_review_approval_digest"]


def test_al_validator_accepts_valid_approval(approval):
    assert service.validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(approval)["blocker_count"] == 0


def test_am_validator_rejects_wrong_artifact_kind(approval): _reject(approval, "artifact_kind", "WRONG")
def test_an_validator_rejects_wrong_approval_status(approval): _reject(approval, "approval_status", "WRONG")
def test_ao_validator_rejects_wrong_scope(approval): _reject(approval, "approval_scope", "WRONG")
def test_ap_validator_rejects_selected_option_not_option_a(approval): _reject(approval, "selected_method_evidence_improvement_option", "OPTION_B")
def test_aq_validator_rejects_approval_false(approval): _reject(approval, "label_objective_target_definition_review_approved", False)
def test_ar_validator_rejects_authorization_false(approval): _reject(approval, "label_objective_target_definition_review_authorized", False)
def test_as_validator_rejects_review_executed_true(approval): _reject(approval, "label_objective_target_definition_review_executed", True)
def test_at_validator_rejects_label_regeneration_true(approval): _reject(approval, "label_regeneration_performed", True)
def test_au_validator_rejects_new_targets_created_true(approval): _reject(approval, "new_targets_created", True)
def test_av_validator_rejects_target_definition_change_authorized_true(approval): _reject(approval, "target_definition_change_authorized", True)
def test_aw_validator_rejects_predictive_usefulness_accepted(approval): _reject(approval, "predictive_usefulness", "accepted")
def test_ax_validator_rejects_runtime_authorized(approval): _reject(approval, "runtime_use", "AUTHORIZED")
def test_ay_validator_rejects_trade_recommendations_true(approval): _reject(approval, "trade_recommendations_generated", True)


def test_az_validator_rejects_wrong_operator_decision(approval):
    changed = deepcopy(approval); changed["operator_attestation"]["operator_decision"] = "WRONG"
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError):
        service.validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(changed)


def test_ba_validator_rejects_wrong_attestation_phrase(approval):
    changed = deepcopy(approval); changed["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError):
        service.validate_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(changed)


def test_bb_validator_rejects_missing_risk_controls(approval): _reject(approval, "risk_controls", None)


def test_bc_markdown_includes_required_sections(approval):
    markdown = service.build_label_objective_target_definition_review_approved_using_redesigned_evidence_markdown_v1(approval)
    for section in ("## Operator Attestation", "## Source Candidate Review", "## Bound Evidence",
                    "## Dataset and Universe", "## Approved Problem Basis", "## Approved Review Objective",
                    "## Approved Dimensions", "## Approved Label Family Review Plan",
                    "## Approved Diagnostic Questions", "## Approved Decision Options",
                    "## Approved Future Outputs", "## Per-Ticker Approval Entries", "## Next Chain",
                    "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
                    "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails"):
        assert section in markdown


def test_bd_writer_creates_canonical_json_without_overwrite(tmp_path, operator_attestation):
    receipt = service.write_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
        tmp_path, operator_attestation=operator_attestation)
    path = tmp_path / "label_objective_target_definition_review_approval_using_redesigned_evidence_v1.json"
    assert json.loads(path.read_text(encoding="utf-8"))["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_APPROVED_USING_REDESIGNED_EVIDENCE
    assert len(receipt["payload_sha256"]) == 64
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError):
        service.write_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
            tmp_path, operator_attestation=operator_attestation)


def test_be_attestation_mismatch_fails_closed(operator_attestation):
    changed = deepcopy(operator_attestation); changed["operator_confirms_meta_record_count"] = 1003
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewApprovalRedesignedEvidenceError):
        service.build_label_objective_target_definition_review_approved_using_redesigned_evidence_v1(
            operator_attestation=changed)
