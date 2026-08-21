from copy import deepcopy

import pytest

from marketflow.services import label_objective_redesign_approval_redesigned_evidence_service as service


def _attestation():
    return service.build_label_objective_redesign_approval_using_redesigned_evidence_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-21T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE,
        operator_confirms_candidate_review_digest=service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        operator_confirms_candidate_digest=service.EXPECTED_CANDIDATE_DIGEST,
        operator_confirms_results_review_digest=service.SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"],
        operator_confirms_execution_digest=service.SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
        operator_confirms_records_digest=service.SOURCE_EVIDENCE["records_digest"],
        operator_confirms_target_universe=service.TARGET_UNIVERSE,
        operator_confirms_target_count=12,
        operator_confirms_meta_record_count=913,
        operator_confirms_non_meta_record_count=1003,
        operator_confirms_recommended_redesign_direction=service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        operator_confirms_selected_redesign_direction=service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION,
        operator_confirms_approval_scope_only=True,
        operator_confirms_redesign_authorized=True,
        operator_confirms_ready_for_redesign_execution=True,
        operator_confirms_no_redesign_execution=True,
        operator_confirms_no_label_regeneration=True,
        operator_confirms_no_new_targets=True,
        operator_confirms_no_target_definition_change_authorization=True,
        operator_confirms_no_threshold_horizon_refinement_candidate=True,
        operator_confirms_no_predictive_evidence_rerun=True,
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


@pytest.fixture
def attestation():
    return _attestation()


@pytest.fixture
def approval(attestation):
    return service.build_label_objective_redesign_approved_using_redesigned_evidence_v1(
        operator_attestation=attestation,
    )


def _reject(approval, field, value):
    changed = deepcopy(approval)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveRedesignApprovalRedesignedEvidenceError):
        service.validate_label_objective_redesign_approved_using_redesigned_evidence_v1(changed)


def test_a_attestation_builder_creates_required_fields(attestation):
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert attestation["operator_reference"] == "TEST_OPERATOR"


def test_b_approval_package_builds_offline(approval):
    assert approval["created_offline"] is True


def test_c_artifact_kind_is_correct(approval):
    assert approval["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE


def test_d_approval_status_is_correct(approval):
    assert approval["approval_status"] == service.LABEL_OBJECTIVE_REDESIGN_APPROVED_USING_REDESIGNED_EVIDENCE


def test_e_approval_scope_is_correct(approval):
    assert approval["approval_scope"] == service.LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY


def test_f_candidate_review_digest_is_bound(approval):
    assert approval["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_g_candidate_digest_is_bound(approval):
    assert approval["label_objective_redesign_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_h_results_review_digest_is_bound(approval):
    key = "label_objective_target_definition_results_review_using_redesigned_evidence_digest"
    assert approval[key] == service.SOURCE_EVIDENCE[key]


def test_i_execution_digest_is_bound(approval):
    key = "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
    assert approval[key] == service.SOURCE_EVIDENCE[key]


def test_j_output_binding_digest_is_bound(approval):
    key = "label_objective_target_definition_review_output_binding_digest"
    assert approval[key] == service.SOURCE_EVIDENCE[key]


def test_k_records_digest_is_bound(approval):
    assert approval["records_digest"] == service.SOURCE_EVIDENCE["records_digest"]


def test_l_universe_count_and_order_are_preserved(approval):
    assert approval["target_universe"] == service.TARGET_UNIVERSE
    assert approval["target_universe_count"] == 12


def test_m_meta_913_is_preserved(approval):
    assert approval["meta_record_count"] == 913
    assert approval["meta_reduced_record_count_preserved"] is True


def test_n_selected_redesign_direction_is_expected(approval):
    assert approval["selected_label_objective_redesign_direction"] == service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION


def test_o_approval_authorization_and_ready_are_true(approval):
    assert approval["label_objective_redesign_approved"] is True
    assert approval["label_objective_redesign_authorized"] is True
    assert approval["ready_for_label_objective_redesign_execution_using_redesigned_evidence"] is True


def test_p_redesign_executed_is_false(approval):
    assert approval["label_objective_redesign_executed"] is False


def test_q_label_regeneration_remains_false(approval):
    assert approval["label_regeneration_authorized"] is False
    assert approval["label_regeneration_performed"] is False


def test_r_new_targets_created_remains_false(approval):
    assert approval["new_targets_created"] is False


def test_s_target_definition_change_authorized_remains_false(approval):
    assert approval["target_definition_change_authorized"] is False


def test_t_threshold_horizon_refinement_candidate_is_false(approval):
    assert approval["threshold_horizon_refinement_candidate_created"] is False


def test_u_predictive_usefulness_is_not_accepted(approval):
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED


def test_v_acceptance_ready_and_candidate_are_false(approval):
    assert approval["predictive_usefulness_acceptance_ready"] is False
    assert approval["predictive_usefulness_acceptance_candidate_created"] is False


def test_w_profitability_is_not_accepted(approval):
    assert approval["profitability"] == service.NOT_ACCEPTED


def test_x_runtime_is_not_authorized(approval):
    assert approval["runtime_use"] == service.NOT_AUTHORIZED


def test_y_trade_recommendations_are_false(approval):
    assert approval["trade_recommendations_generated"] is False


def test_z_approved_candidate_basis_is_preserved(approval):
    assert approval["approved_candidate_basis"] == service.CANDIDATE_BASIS


def test_aa_redesign_objective_is_defined(approval):
    assert approval["label_objective_redesign_scope"] == service.LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY
    assert approval["label_objective_redesign_mode"] == "AUTHORIZED_NOT_EXECUTED"


def test_ab_only_recommended_option_is_selected(approval):
    selected = [row["redesign_option"] for row in approval["approved_redesign_options"] if row["selected_for_approval"]]
    assert selected == [service.SELECTED_LABEL_OBJECTIVE_REDESIGN_DIRECTION]


def test_ac_approved_redesign_themes_count_is_11(approval):
    assert len(approval["approved_redesign_themes"]) == 11


def test_ad_approved_label_family_impact_review_count_is_10(approval):
    assert len(approval["approved_label_family_impact_review"]) == 10


def test_ae_approved_redesign_questions_count_is_10(approval):
    assert len(approval["approved_redesign_questions"]) == 10


def test_af_approved_future_outputs_are_present(approval):
    assert [row["output_name"] for row in approval["approved_future_outputs"]] == service.APPROVED_FUTURE_OUTPUT_NAMES
    assert all(row["output_status"] == "AUTHORIZED_NOT_GENERATED" for row in approval["approved_future_outputs"])


def test_ag_per_ticker_approval_entries_count_is_12(approval):
    assert len(approval["per_ticker_approval_entries"]) == 12


def test_ah_per_ticker_approval_digests_are_present(approval):
    assert all(row["per_ticker_label_objective_redesign_approval_digest"] for row in approval["per_ticker_approval_entries"])


def test_ai_next_chain_is_defined(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN


def test_aj_risk_controls_are_defined(approval):
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_ak_checklist_passes(approval):
    assert approval["approval_summary"]["passed_checks"] == 76
    assert approval["approval_summary"]["blocker_count"] == 0


def test_al_approval_digest_is_deterministic(approval):
    rebuilt = service.build_label_objective_redesign_approved_using_redesigned_evidence_v1(operator_attestation=_attestation())
    assert approval["label_objective_redesign_approval_using_redesigned_evidence_digest"] == rebuilt["label_objective_redesign_approval_using_redesigned_evidence_digest"]


def test_am_per_ticker_approval_digests_are_deterministic(approval):
    rebuilt = service.build_label_objective_redesign_approved_using_redesigned_evidence_v1(operator_attestation=_attestation())
    assert [row["per_ticker_label_objective_redesign_approval_digest"] for row in approval["per_ticker_approval_entries"]] == [row["per_ticker_label_objective_redesign_approval_digest"] for row in rebuilt["per_ticker_approval_entries"]]


def test_an_validator_accepts_valid_approval(approval):
    result = service.validate_label_objective_redesign_approved_using_redesigned_evidence_v1(approval)
    assert result["failed_checks"] == 0


def test_ao_validator_rejects_wrong_artifact_kind(approval):
    _reject(approval, "artifact_kind", "WRONG")


def test_ap_validator_rejects_wrong_approval_status(approval):
    _reject(approval, "approval_status", "WRONG")


def test_aq_validator_rejects_wrong_scope(approval):
    _reject(approval, "approval_scope", "WRONG")


def test_ar_validator_rejects_wrong_selected_redesign_direction(approval):
    _reject(approval, "selected_label_objective_redesign_direction", "WRONG")


def test_as_validator_rejects_approval_false(approval):
    _reject(approval, "label_objective_redesign_approved", False)


def test_at_validator_rejects_authorization_false(approval):
    _reject(approval, "label_objective_redesign_authorized", False)


def test_au_validator_rejects_redesign_executed_true(approval):
    _reject(approval, "label_objective_redesign_executed", True)


def test_av_validator_rejects_label_regeneration_true(approval):
    _reject(approval, "label_regeneration_performed", True)


def test_aw_validator_rejects_new_targets_true(approval):
    _reject(approval, "new_targets_created", True)


def test_ax_validator_rejects_target_definition_change_authorized_true(approval):
    _reject(approval, "target_definition_change_authorized", True)


def test_ay_validator_rejects_threshold_horizon_candidate_true(approval):
    _reject(approval, "threshold_horizon_refinement_candidate_created", True)


def test_az_validator_rejects_predictive_usefulness_accepted(approval):
    _reject(approval, "predictive_usefulness", "accepted")


def test_ba_validator_rejects_runtime_authorized(approval):
    _reject(approval, "runtime_use", "AUTHORIZED")


def test_bb_validator_rejects_trade_recommendations_true(approval):
    _reject(approval, "trade_recommendations_generated", True)


def test_bc_validator_rejects_wrong_operator_decision(approval):
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_decision"] = "WRONG"
    with pytest.raises(service.LabelObjectiveRedesignApprovalRedesignedEvidenceError):
        service.validate_label_objective_redesign_approved_using_redesigned_evidence_v1(changed)


def test_bd_validator_rejects_wrong_attestation_phrase(approval):
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(service.LabelObjectiveRedesignApprovalRedesignedEvidenceError):
        service.validate_label_objective_redesign_approved_using_redesigned_evidence_v1(changed)


def test_be_validator_rejects_missing_risk_controls(approval):
    _reject(approval, "risk_controls", [])


def test_bf_markdown_includes_required_sections(approval):
    markdown = service.build_label_objective_redesign_approved_using_redesigned_evidence_markdown_v1(approval)
    for section in (
        "## Title", "## Optional Label Objective Redesign Approval Using Redesigned Evidence",
        "## Operator Attestation", "## Source Candidate Review", "## Bound Evidence",
        "## Dataset and Universe", "## Approved Candidate Basis", "## Approved Redesign Objective",
        "## Selected Redesign Direction", "## Approved Redesign Themes",
        "## Approved Label Family Impact Review", "## Approved Redesign Questions",
        "## Approved Future Outputs", "## Per-Ticker Approval Entries", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown
