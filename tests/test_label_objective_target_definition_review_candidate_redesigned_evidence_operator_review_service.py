from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    label_objective_target_definition_review_candidate_redesigned_evidence_operator_review_service as service,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1()


def _reject(review_package: dict, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError):
        service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
            changed
        )


def test_a_review_package_builds_offline(review_package):
    assert review_package["created_offline"] is True
    assert review_package["provider_requests_made_in_review"] is False


def test_b_artifact_kind_is_correct(review_package):
    assert review_package["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE


def test_c_review_status_is_correct(review_package):
    assert review_package["review_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY


def test_d_reviewed_candidate_digest_matches_expected(review_package):
    assert review_package["source_candidate_digest"] == service.EXPECTED_SOURCE_CANDIDATE_DIGEST


def test_e_candidate_checklist_has_zero_blockers(review_package):
    assert review_package["source_candidate_checklist_total"] == 56
    assert review_package["source_candidate_checklist_passed"] == 56
    assert review_package["source_candidate_blocker_count"] == 0


def test_f_candidate_digest_is_bound(review_package):
    assert review_package["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_SOURCE_CANDIDATE_DIGEST


def test_g_path_selection_digest_is_bound(review_package):
    assert review_package["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == service.EXPECTED_PATH_SELECTION_DIGEST


def test_h_candidate_review_digest_is_bound(review_package):
    assert review_package["method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_i_readiness_review_digest_is_bound(review_package):
    assert review_package["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_j_reassessment_digest_is_bound(review_package):
    assert review_package["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_k_results_review_digest_is_bound(review_package):
    assert review_package["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_l_execution_digest_is_bound(review_package):
    assert review_package["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_m_matrix_digest_is_bound(review_package):
    assert review_package["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_n_feature_values_digest_is_bound(review_package):
    assert review_package["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_o_label_values_digest_is_bound(review_package):
    assert review_package["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_p_research_registry_digest_is_bound(review_package):
    assert review_package["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_q_records_digest_is_bound(review_package):
    assert review_package["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_r_universe_count_and_order_are_preserved(review_package):
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_s_meta_913_is_preserved(review_package):
    assert review_package["meta_record_count"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_t_selected_option_is_option_a(review_package):
    assert review_package["selected_method_evidence_improvement_option"] == service.SELECTED_OPTION


def test_u_candidate_created_and_review_created_are_true(review_package):
    assert review_package["label_objective_target_definition_review_candidate_using_redesigned_evidence_created"] is True
    assert review_package["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_created"] is True


def test_v_review_approved_and_executed_are_false(review_package):
    assert review_package["label_objective_target_definition_review_approved"] is False
    assert review_package["label_objective_target_definition_review_authorized"] is False
    assert review_package["label_objective_target_definition_review_executed"] is False


def test_w_label_regeneration_is_false(review_package):
    assert review_package["label_regeneration_authorized"] is False
    assert review_package["label_regeneration_performed"] is False
    assert review_package["redesigned_label_regeneration_performed"] is False


def test_x_new_targets_created_is_false(review_package):
    assert review_package["new_targets_created"] is False


def test_y_target_definition_change_authorized_is_false(review_package):
    assert review_package["target_definition_change_authorized"] is False
    assert all(row["target_definition_change_authorized"] is False for row in review_package["reviewed_label_family_review_plan"])


def test_z_predictive_usefulness_is_not_accepted(review_package):
    assert review_package["predictive_usefulness"] == "not accepted"


def test_aa_acceptance_ready_and_candidate_are_false(review_package):
    assert review_package["predictive_usefulness_acceptance_ready"] is False
    assert review_package["predictive_usefulness_acceptance_candidate_created"] is False


def test_ab_profitability_is_not_accepted(review_package):
    assert review_package["profitability"] == "not accepted"


def test_ac_runtime_is_not_authorized(review_package):
    assert review_package["runtime_use"] == "NOT_AUTHORIZED"
    assert review_package["strategy_use"] == "NOT_AUTHORIZED"


def test_ad_trade_recommendations_are_false(review_package):
    assert review_package["trade_recommendations_generated"] is False


def test_ae_problem_basis_is_reviewed(review_package):
    assert review_package["reviewed_problem_basis"] == service.candidate_service._base_candidate()["problem_basis"]


def test_af_candidate_objective_is_reviewed(review_package):
    assert review_package["reviewed_label_objective_target_definition_review_objective"] == service.candidate_service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE
    assert review_package["reviewed_label_objective_target_definition_review_scope"] == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"


def test_ag_review_dimensions_are_reviewed(review_package):
    assert [row["dimension_id"] for row in review_package["reviewed_dimensions"]] == service.REVIEW_DIMENSION_IDS
    assert all(row["dimension_status"] == "PLANNED_NOT_EXECUTED" for row in review_package["reviewed_dimensions"])


def test_ah_label_family_review_plan_is_reviewed(review_package):
    assert [row["label_family"] for row in review_package["reviewed_label_family_review_plan"]] == service.LABEL_FAMILY_IDS


def test_ai_diagnostic_questions_are_reviewed(review_package):
    assert [row["question"] for row in review_package["reviewed_diagnostic_questions"]] == service.DIAGNOSTIC_QUESTIONS
    assert all(row["question_status"] == "NOT_ANSWERED" for row in review_package["reviewed_diagnostic_questions"])


def test_aj_decision_options_are_reviewed(review_package):
    assert [row["decision_option"] for row in review_package["reviewed_decision_options"]] == service.DECISION_OPTION_IDS
    assert all(row["selected"] is False for row in review_package["reviewed_decision_options"])


def test_ak_planned_outputs_are_not_generated(review_package):
    assert [row["output_name"] for row in review_package["reviewed_planned_outputs"]] == service.PLANNED_OUTPUT_NAMES
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in review_package["reviewed_planned_outputs"])


def test_al_per_ticker_entries_count_is_12(review_package):
    assert len(review_package["per_ticker_review_entries"]) == 12


def test_am_per_ticker_candidate_digests_are_present(review_package):
    assert all(len(row["per_ticker_label_objective_target_definition_review_candidate_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_an_per_ticker_review_digests_are_present(review_package):
    assert all(len(row["per_ticker_label_objective_target_definition_review_candidate_review_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_ao_next_chain_is_reviewed(review_package):
    assert review_package["next_chain"] == service.NEXT_CHAIN
    assert review_package["next_gates"] == service.NEXT_GATES


def test_ap_risk_controls_are_reviewed(review_package):
    assert review_package["risk_controls"] == service.RISK_CONTROLS


def test_aq_checklist_passes(review_package):
    assert review_package["review_summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert review_package["review_summary"]["failed_checks"] == 0


def test_ar_review_digest_is_deterministic(review_package):
    assert service.label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest_v1(review_package) == review_package["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"]


def test_as_per_ticker_review_digests_are_deterministic(review_package):
    for entry in review_package["per_ticker_review_entries"]:
        assert service.per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_digest_v1(entry) == entry["per_ticker_label_objective_target_definition_review_candidate_review_digest"]


def test_at_validator_accepts_valid_review(review_package):
    result = service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(review_package)
    assert result["blocker_count"] == 0


def test_au_validator_rejects_wrong_artifact_kind(review_package):
    _reject(review_package, "artifact_kind", "WRONG")


def test_av_validator_rejects_wrong_status(review_package):
    _reject(review_package, "review_status", "WRONG")


def test_aw_validator_rejects_changed_candidate_digest(review_package):
    _reject(review_package, "source_candidate_digest", "0" * 64)


def test_ax_validator_rejects_candidate_blocker(review_package):
    _reject(review_package, "source_candidate_blocker_count", 1)


def test_ay_validator_rejects_selected_option_not_option_a(review_package):
    _reject(review_package, "selected_method_evidence_improvement_option", "OPTION_B")


def test_az_validator_rejects_review_approved_true(review_package):
    _reject(review_package, "label_objective_target_definition_review_approved", True)


def test_ba_validator_rejects_review_executed_true(review_package):
    _reject(review_package, "label_objective_target_definition_review_executed", True)


def test_bb_validator_rejects_label_regeneration_true(review_package):
    _reject(review_package, "label_regeneration_performed", True)


def test_bc_validator_rejects_new_targets_created_true(review_package):
    _reject(review_package, "new_targets_created", True)


def test_bd_validator_rejects_predictive_usefulness_accepted(review_package):
    _reject(review_package, "predictive_usefulness", "accepted")


def test_be_validator_rejects_runtime_authorized(review_package):
    _reject(review_package, "runtime_use", "AUTHORIZED")


def test_bf_validator_rejects_trade_recommendations_true(review_package):
    _reject(review_package, "trade_recommendations_generated", True)


def test_bg_validator_rejects_predictive_evidence_rerun_true(review_package):
    _reject(review_package, "predictive_evidence_execution_rerun_performed", True)


def test_bh_validator_rejects_metric_recomputation_true(review_package):
    _reject(review_package, "metric_recomputation_performed_in_review", True)


def test_bi_validator_rejects_model_training_true(review_package):
    _reject(review_package, "model_training_performed_in_review", True)


def test_bj_validator_rejects_missing_review_dimensions(review_package):
    _reject(review_package, "reviewed_dimensions", None)


def test_bk_validator_rejects_missing_next_chain(review_package):
    _reject(review_package, "next_chain", None)


def test_bl_markdown_includes_required_sections(review_package):
    markdown = service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_markdown_v1(review_package)
    for section in (
        "## Title", "## Label Objective / Target Definition Review Candidate Review Using Redesigned Evidence",
        "## Reviewed Candidate", "## Source Path Selection", "## Bound Evidence",
        "## Dataset and Universe", "## Reviewed Problem Basis", "## Reviewed Candidate Objective",
        "## Reviewed Dimensions", "## Reviewed Label Family Review Plan",
        "## Reviewed Diagnostic Questions", "## Reviewed Decision Options",
        "## Reviewed Planned Outputs", "## Per-Ticker Review Entries", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_bm_writer_creates_canonical_json_without_overwrite(tmp_path):
    receipt = service.write_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
        tmp_path
    )
    path = tmp_path / "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE
    assert len(receipt["payload_sha256"]) == 64
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceOperatorReviewError):
        service.write_label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_v1(
            tmp_path
        )
