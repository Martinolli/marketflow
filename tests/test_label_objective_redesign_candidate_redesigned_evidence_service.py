from copy import deepcopy

import pytest

from marketflow.services import label_objective_redesign_candidate_redesigned_evidence_service as service


@pytest.fixture
def candidate():
    return service.build_label_objective_redesign_candidate_using_redesigned_evidence_v1()


def _reject(candidate, field, value):
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveRedesignCandidateRedesignedEvidenceError):
        service.validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(changed)


def test_a_candidate_builds_offline(candidate):
    assert candidate["created_offline"] is True


def test_b_artifact_kind_is_correct(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE


def test_c_candidate_status_is_correct(candidate):
    assert candidate["candidate_status"] == service.LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW


def test_d_results_review_digest_is_bound(candidate):
    assert candidate["source_results_review_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_e_execution_digest_is_bound(candidate):
    assert candidate["source_evidence"]["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"] == service.SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"]


def test_f_output_binding_digest_is_bound(candidate):
    assert candidate["source_evidence"]["label_objective_target_definition_review_output_binding_digest"] == service.SOURCE_EVIDENCE["label_objective_target_definition_review_output_binding_digest"]


def test_g_approval_digest_is_bound(candidate):
    assert candidate["source_evidence"]["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"] == service.SOURCE_EVIDENCE["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"]


def test_h_candidate_review_digest_is_bound(candidate):
    key = "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"
    assert candidate["source_evidence"][key] == service.SOURCE_EVIDENCE[key]


def test_i_path_selection_digest_is_bound(candidate):
    key = "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"
    assert candidate["source_evidence"][key] == service.SOURCE_EVIDENCE[key]


def test_j_matrix_digest_is_bound(candidate):
    assert candidate["source_evidence"]["feature_label_matrix_digest"] == service.SOURCE_EVIDENCE["feature_label_matrix_digest"]


def test_k_feature_values_digest_is_bound(candidate):
    assert candidate["source_evidence"]["feature_values_digest"] == service.SOURCE_EVIDENCE["feature_values_digest"]


def test_l_label_values_digest_is_bound(candidate):
    assert candidate["source_evidence"]["redesigned_label_values_digest"] == service.SOURCE_EVIDENCE["redesigned_label_values_digest"]


def test_m_research_registry_digest_is_bound(candidate):
    assert candidate["source_evidence"]["research_registry_approval_digest"] == service.SOURCE_EVIDENCE["research_registry_approval_digest"]


def test_n_records_digest_is_bound(candidate):
    assert candidate["records_digest"] == service.SOURCE_EVIDENCE["records_digest"]


def test_o_universe_count_and_order_are_preserved(candidate):
    assert candidate["target_universe"] == service.TARGET_UNIVERSE
    assert candidate["target_universe_count"] == 12


def test_p_meta_913_is_preserved(candidate):
    assert candidate["meta_record_count"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_q_results_review_ready_is_true(candidate):
    assert candidate["label_objective_target_definition_results_review_ready"] is True


def test_r_ready_for_optional_redesign_refinement_is_true(candidate):
    assert candidate["ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence"] is True


def test_s_redesign_candidate_created_and_ready_are_true(candidate):
    assert candidate["label_objective_redesign_candidate_created"] is True
    assert candidate["label_objective_redesign_candidate_using_redesigned_evidence_ready_for_operator_review"] is True


def test_t_redesign_approved_and_executed_are_false(candidate):
    assert candidate["label_objective_redesign_approved"] is False
    assert candidate["label_objective_redesign_executed"] is False


def test_u_label_regeneration_is_false(candidate):
    assert candidate["label_regeneration_authorized"] is False
    assert candidate["label_regeneration_performed"] is False


def test_v_new_targets_created_is_false(candidate):
    assert candidate["new_targets_created"] is False


def test_w_target_definition_change_authorized_is_false(candidate):
    assert candidate["target_definition_change_authorized"] is False


def test_x_threshold_horizon_refinement_candidate_is_false(candidate):
    assert candidate["threshold_horizon_refinement_candidate_created"] is False


def test_y_predictive_usefulness_is_not_accepted(candidate):
    assert candidate["predictive_usefulness"] == service.NOT_ACCEPTED


def test_z_profitability_is_not_accepted(candidate):
    assert candidate["profitability"] == service.NOT_ACCEPTED


def test_aa_runtime_is_not_authorized(candidate):
    assert candidate["runtime_use"] == service.NOT_AUTHORIZED


def test_ab_trade_recommendations_are_false(candidate):
    assert candidate["trade_recommendations_generated"] is False


def test_ac_candidate_basis_is_preserved(candidate):
    assert candidate["candidate_basis"] == service.CANDIDATE_BASIS


def test_ad_candidate_objective_is_defined(candidate):
    assert candidate["label_objective_redesign_candidate_scope"] == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
    assert candidate["label_objective_redesign_candidate_mode"] == "PLANNED_NOT_EXECUTED"
    assert candidate["label_objective_redesign_candidate_authority_status"] == service.NOT_AUTHORIZED


def test_ae_redesign_themes_are_defined(candidate):
    assert [item["theme"] for item in candidate["redesign_themes"]] == service.REDESIGN_THEME_IDS


def test_af_redesign_options_are_defined(candidate):
    assert [item["option"] for item in candidate["redesign_options"]] == service.REDESIGN_OPTION_IDS
    assert all(item["selected"] is False for item in candidate["redesign_options"])


def test_ag_recommended_redesign_direction_is_defined(candidate):
    assert candidate["recommended_redesign_direction"] == service.RECOMMENDED_REDESIGN_DIRECTION


def test_ah_label_family_impact_review_is_defined(candidate):
    assert [item["label_family"] for item in candidate["current_label_family_impact_review"]] == service.LABEL_FAMILIES


def test_ai_redesign_questions_are_defined(candidate):
    assert [item["question"] for item in candidate["planned_redesign_questions"]] == service.REDESIGN_QUESTIONS


def test_aj_planned_outputs_are_not_generated(candidate):
    assert all(item["output_status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])


def test_ak_per_ticker_entries_count_is_12(candidate):
    assert len(candidate["per_ticker_candidate_entries"]) == 12


def test_al_per_ticker_digests_are_present(candidate):
    assert all(item["per_ticker_label_objective_redesign_candidate_digest"] for item in candidate["per_ticker_candidate_entries"])


def test_am_next_chain_is_defined(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN


def test_an_risk_controls_are_defined(candidate):
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_ao_checklist_passes(candidate):
    assert candidate["summary"]["passed_checks"] == candidate["summary"]["total_checks"]
    assert candidate["summary"]["blocker_count"] == 0


def test_ap_candidate_digest_is_deterministic(candidate):
    rebuilt = service.build_label_objective_redesign_candidate_using_redesigned_evidence_v1()
    assert candidate["label_objective_redesign_candidate_using_redesigned_evidence_digest"] == rebuilt["label_objective_redesign_candidate_using_redesigned_evidence_digest"]


def test_aq_per_ticker_digests_are_deterministic(candidate):
    rebuilt = service.build_label_objective_redesign_candidate_using_redesigned_evidence_v1()
    assert [item["per_ticker_label_objective_redesign_candidate_digest"] for item in candidate["per_ticker_candidate_entries"]] == [item["per_ticker_label_objective_redesign_candidate_digest"] for item in rebuilt["per_ticker_candidate_entries"]]


def test_ar_validator_accepts_valid_candidate(candidate):
    result = service.validate_label_objective_redesign_candidate_using_redesigned_evidence_v1(candidate)
    assert result["failure_count"] == 0


def test_as_validator_rejects_wrong_artifact_kind(candidate):
    _reject(candidate, "artifact_kind", "WRONG")


def test_at_validator_rejects_wrong_status(candidate):
    _reject(candidate, "candidate_status", "WRONG")


def test_au_validator_rejects_results_review_ready_false(candidate):
    _reject(candidate, "label_objective_target_definition_results_review_ready", False)


def test_av_validator_rejects_candidate_created_false(candidate):
    _reject(candidate, "label_objective_redesign_candidate_created", False)


def test_aw_validator_rejects_redesign_approved_true(candidate):
    _reject(candidate, "label_objective_redesign_approved", True)


def test_ax_validator_rejects_redesign_executed_true(candidate):
    _reject(candidate, "label_objective_redesign_executed", True)


def test_ay_validator_rejects_label_regeneration_true(candidate):
    _reject(candidate, "label_regeneration_performed", True)


def test_az_validator_rejects_new_targets_true(candidate):
    _reject(candidate, "new_targets_created", True)


def test_ba_validator_rejects_target_definition_change_authorized_true(candidate):
    _reject(candidate, "target_definition_change_authorized", True)


def test_bb_validator_rejects_threshold_horizon_candidate_true(candidate):
    _reject(candidate, "threshold_horizon_refinement_candidate_created", True)


def test_bc_validator_rejects_predictive_usefulness_accepted(candidate):
    _reject(candidate, "predictive_usefulness", "accepted")


def test_bd_validator_rejects_runtime_authorized(candidate):
    _reject(candidate, "runtime_use", "AUTHORIZED")


def test_be_validator_rejects_trade_recommendations_true(candidate):
    _reject(candidate, "trade_recommendations_generated", True)


def test_bf_validator_rejects_predictive_evidence_rerun_true(candidate):
    _reject(candidate, "predictive_evidence_execution_rerun_performed", True)


def test_bg_validator_rejects_metric_recomputation_in_candidate_true(candidate):
    _reject(candidate, "metric_recomputation_performed_in_candidate", True)


def test_bh_validator_rejects_model_training_in_candidate_true(candidate):
    _reject(candidate, "model_training_performed_in_candidate", True)


def test_bi_validator_rejects_missing_redesign_options(candidate):
    _reject(candidate, "redesign_options", [])


def test_bj_validator_rejects_missing_next_chain(candidate):
    _reject(candidate, "next_chain", [])


def test_bk_markdown_includes_required_sections(candidate):
    markdown = service.build_label_objective_redesign_candidate_using_redesigned_evidence_markdown_v1(candidate)
    for section in (
        "# Optional Label Objective Redesign Candidate Using Redesigned Evidence",
        "## Source Results Review", "## Bound Evidence", "## Dataset and Universe",
        "## Candidate Basis", "## Candidate Objective", "## Redesign Themes",
        "## Redesign Options", "## Current Label Family Impact Review",
        "## Planned Redesign Questions", "## Planned Outputs", "## Per-Ticker Candidate Entries",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown
