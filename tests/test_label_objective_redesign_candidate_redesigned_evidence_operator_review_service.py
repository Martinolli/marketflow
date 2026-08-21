from copy import deepcopy

import pytest

from marketflow.services import label_objective_redesign_candidate_redesigned_evidence_operator_review_service as service


@pytest.fixture
def review_package():
    return service.build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1()


def _reject(review_package, field, value):
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveRedesignCandidateRedesignedEvidenceOperatorReviewError):
        service.validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(changed)


def test_a_review_package_builds_offline(review_package):
    assert review_package["created_offline"] is True


def test_b_artifact_kind_is_correct(review_package):
    assert review_package["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE


def test_c_review_status_is_correct(review_package):
    assert review_package["review_status"] == service.LABEL_OBJECTIVE_REDESIGN_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY


def test_d_reviewed_candidate_digest_matches_expected(review_package):
    assert review_package["source_candidate_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_e_candidate_checklist_has_zero_blockers(review_package):
    assert review_package["source_candidate_blocker_count"] == 0
    assert review_package["source_candidate_checklist_passed"] == 69


def test_f_candidate_digest_is_bound(review_package):
    assert review_package["label_objective_redesign_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_g_results_review_digest_is_bound(review_package):
    key = "label_objective_target_definition_results_review_using_redesigned_evidence_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_h_execution_digest_is_bound(review_package):
    key = "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_i_output_binding_digest_is_bound(review_package):
    key = "label_objective_target_definition_review_output_binding_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_j_approval_digest_is_bound(review_package):
    key = "label_objective_target_definition_review_approval_using_redesigned_evidence_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_k_candidate_review_digest_is_bound(review_package):
    key = "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_l_path_selection_digest_is_bound(review_package):
    key = "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"
    assert review_package[key] == service.SOURCE_EVIDENCE[key]


def test_m_matrix_digest_is_bound(review_package):
    assert review_package["feature_label_matrix_digest"] == service.SOURCE_EVIDENCE["feature_label_matrix_digest"]


def test_n_feature_values_digest_is_bound(review_package):
    assert review_package["feature_values_digest"] == service.SOURCE_EVIDENCE["feature_values_digest"]


def test_o_label_values_digest_is_bound(review_package):
    assert review_package["redesigned_label_values_digest"] == service.SOURCE_EVIDENCE["redesigned_label_values_digest"]


def test_p_research_registry_digest_is_bound(review_package):
    assert review_package["research_registry_approval_digest"] == service.SOURCE_EVIDENCE["research_registry_approval_digest"]


def test_q_records_digest_is_bound(review_package):
    assert review_package["records_digest"] == service.SOURCE_EVIDENCE["records_digest"]


def test_r_universe_count_and_order_are_preserved(review_package):
    assert review_package["target_universe"] == service.TARGET_UNIVERSE
    assert review_package["target_universe_count"] == 12


def test_s_meta_913_is_preserved(review_package):
    assert review_package["meta_record_count"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_t_results_review_ready_is_true(review_package):
    assert review_package["label_objective_target_definition_results_review_ready"] is True


def test_u_ready_for_optional_redesign_refinement_is_true(review_package):
    assert review_package["ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence"] is True


def test_v_candidate_created_and_review_created_are_true(review_package):
    assert review_package["label_objective_redesign_candidate_created"] is True
    assert review_package["label_objective_redesign_candidate_using_redesigned_evidence_review_created"] is True


def test_w_redesign_approved_and_executed_are_false(review_package):
    assert review_package["label_objective_redesign_approved"] is False
    assert review_package["label_objective_redesign_executed"] is False


def test_x_recommended_direction_is_not_selected_for_approval(review_package):
    assert review_package["recommended_redesign_direction_selected_for_approval"] is False


def test_y_label_regeneration_is_false(review_package):
    assert review_package["label_regeneration_authorized"] is False
    assert review_package["label_regeneration_performed"] is False


def test_z_new_targets_created_is_false(review_package):
    assert review_package["new_targets_created"] is False


def test_aa_target_definition_change_authorized_is_false(review_package):
    assert review_package["target_definition_change_authorized"] is False


def test_ab_threshold_horizon_refinement_candidate_is_false(review_package):
    assert review_package["threshold_horizon_refinement_candidate_created"] is False


def test_ac_predictive_usefulness_is_not_accepted(review_package):
    assert review_package["predictive_usefulness"] == service.NOT_ACCEPTED


def test_ad_profitability_is_not_accepted(review_package):
    assert review_package["profitability"] == service.NOT_ACCEPTED


def test_ae_runtime_is_not_authorized(review_package):
    assert review_package["runtime_use"] == service.NOT_AUTHORIZED


def test_af_trade_recommendations_are_false(review_package):
    assert review_package["trade_recommendations_generated"] is False


def test_ag_candidate_basis_is_reviewed(review_package):
    assert review_package["reviewed_candidate_basis"] == service.CANDIDATE_BASIS


def test_ah_candidate_objective_is_reviewed(review_package):
    assert review_package["reviewed_label_objective_redesign_candidate_scope"] == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"


def test_ai_redesign_themes_are_reviewed(review_package):
    assert [row["theme"] for row in review_package["reviewed_redesign_themes"]] == service.REDESIGN_THEME_IDS


def test_aj_redesign_options_are_reviewed(review_package):
    assert [row["option"] for row in review_package["reviewed_redesign_options"]] == service.REDESIGN_OPTION_IDS
    assert all(row["selected"] is False for row in review_package["reviewed_redesign_options"])


def test_ak_recommended_redesign_direction_is_preserved(review_package):
    assert review_package["recommended_redesign_direction"] == service.RECOMMENDED_REDESIGN_DIRECTION


def test_al_label_family_impact_review_is_reviewed(review_package):
    assert [row["label_family"] for row in review_package["reviewed_label_family_impact_review"]] == service.LABEL_FAMILIES


def test_am_redesign_questions_are_reviewed(review_package):
    assert [row["question"] for row in review_package["reviewed_redesign_questions"]] == service.REDESIGN_QUESTIONS


def test_an_planned_outputs_are_not_generated(review_package):
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in review_package["reviewed_planned_outputs"])


def test_ao_per_ticker_entries_count_is_12(review_package):
    assert len(review_package["per_ticker_review_entries"]) == 12


def test_ap_per_ticker_candidate_digests_are_present(review_package):
    assert all(row["per_ticker_label_objective_redesign_candidate_digest"] for row in review_package["per_ticker_review_entries"])


def test_aq_per_ticker_review_digests_are_present(review_package):
    assert all(row["per_ticker_label_objective_redesign_candidate_review_digest"] for row in review_package["per_ticker_review_entries"])


def test_ar_next_chain_is_reviewed(review_package):
    assert review_package["next_chain"] == service.NEXT_CHAIN


def test_as_risk_controls_are_reviewed(review_package):
    assert review_package["risk_controls"] == service.RISK_CONTROLS


def test_at_checklist_passes(review_package):
    assert review_package["review_summary"]["passed_checks"] == 77
    assert review_package["review_summary"]["blocker_count"] == 0


def test_au_review_digest_is_deterministic(review_package):
    rebuilt = service.build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1()
    assert review_package["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"] == rebuilt["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"]


def test_av_per_ticker_review_digests_are_deterministic(review_package):
    rebuilt = service.build_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1()
    assert [row["per_ticker_label_objective_redesign_candidate_review_digest"] for row in review_package["per_ticker_review_entries"]] == [row["per_ticker_label_objective_redesign_candidate_review_digest"] for row in rebuilt["per_ticker_review_entries"]]


def test_aw_validator_accepts_valid_review(review_package):
    result = service.validate_label_objective_redesign_candidate_using_redesigned_evidence_review_package_v1(review_package)
    assert result["failed_checks"] == 0


def test_ax_validator_rejects_wrong_artifact_kind(review_package):
    _reject(review_package, "artifact_kind", "WRONG")


def test_ay_validator_rejects_wrong_status(review_package):
    _reject(review_package, "review_status", "WRONG")


def test_az_validator_rejects_changed_candidate_digest(review_package):
    _reject(review_package, "source_candidate_digest", "0" * 64)


def test_ba_validator_rejects_candidate_blocker(review_package):
    _reject(review_package, "source_candidate_blocker_count", 1)


def test_bb_validator_rejects_results_review_ready_false(review_package):
    _reject(review_package, "label_objective_target_definition_results_review_ready", False)


def test_bc_validator_rejects_redesign_approved_true(review_package):
    _reject(review_package, "label_objective_redesign_approved", True)


def test_bd_validator_rejects_redesign_executed_true(review_package):
    _reject(review_package, "label_objective_redesign_executed", True)


def test_be_validator_rejects_recommended_direction_selected_for_approval(review_package):
    _reject(review_package, "recommended_redesign_direction_selected_for_approval", True)


def test_bf_validator_rejects_label_regeneration_true(review_package):
    _reject(review_package, "label_regeneration_performed", True)


def test_bg_validator_rejects_new_targets_true(review_package):
    _reject(review_package, "new_targets_created", True)


def test_bh_validator_rejects_target_definition_change_authorized_true(review_package):
    _reject(review_package, "target_definition_change_authorized", True)


def test_bi_validator_rejects_threshold_horizon_candidate_true(review_package):
    _reject(review_package, "threshold_horizon_refinement_candidate_created", True)


def test_bj_validator_rejects_predictive_usefulness_accepted(review_package):
    _reject(review_package, "predictive_usefulness", "accepted")


def test_bk_validator_rejects_runtime_authorized(review_package):
    _reject(review_package, "runtime_use", "AUTHORIZED")


def test_bl_validator_rejects_trade_recommendations_true(review_package):
    _reject(review_package, "trade_recommendations_generated", True)


def test_bm_validator_rejects_predictive_evidence_rerun_true(review_package):
    _reject(review_package, "predictive_evidence_execution_rerun_performed", True)


def test_bn_validator_rejects_metric_recomputation_in_review_true(review_package):
    _reject(review_package, "metric_recomputation_performed_in_review", True)


def test_bo_validator_rejects_model_training_in_review_true(review_package):
    _reject(review_package, "model_training_performed_in_review", True)


def test_bp_validator_rejects_missing_redesign_options(review_package):
    _reject(review_package, "reviewed_redesign_options", [])


def test_bq_validator_rejects_missing_next_chain(review_package):
    _reject(review_package, "next_chain", [])


def test_br_markdown_includes_required_sections(review_package):
    markdown = service.build_label_objective_redesign_candidate_using_redesigned_evidence_review_markdown_v1(review_package)
    for section in (
        "## Title", "## Optional Label Objective Redesign Candidate Review Using Redesigned Evidence",
        "## Reviewed Candidate", "## Source Results Review", "## Bound Evidence",
        "## Dataset and Universe", "## Reviewed Candidate Basis", "## Reviewed Candidate Objective",
        "## Reviewed Redesign Themes", "## Reviewed Redesign Options",
        "## Reviewed Label Family Impact Review", "## Reviewed Redesign Questions",
        "## Reviewed Planned Outputs", "## Per-Ticker Review Entries", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown
