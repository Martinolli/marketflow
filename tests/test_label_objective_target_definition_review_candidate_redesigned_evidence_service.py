from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    label_objective_target_definition_review_candidate_redesigned_evidence_service as service,
)


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1()


def _reject(candidate: dict, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError):
        service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
            changed
        )


def test_a_candidate_builds_offline(candidate):
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False


def test_b_artifact_kind_is_correct(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE


def test_c_candidate_status_is_correct(candidate):
    assert candidate["candidate_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW


def test_d_path_selection_digest_is_bound(candidate):
    assert candidate["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == service.EXPECTED_PATH_SELECTION_DIGEST


def test_e_candidate_review_digest_is_bound(candidate):
    assert candidate["method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_f_candidate_digest_is_bound(candidate):
    assert candidate["method_evidence_improvement_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_g_readiness_review_digest_is_bound(candidate):
    assert candidate["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_h_reassessment_digest_is_bound(candidate):
    assert candidate["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_i_results_review_digest_is_bound(candidate):
    assert candidate["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_j_execution_digest_is_bound(candidate):
    assert candidate["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_k_matrix_digest_is_bound(candidate):
    assert candidate["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_l_feature_values_digest_is_bound(candidate):
    assert candidate["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_m_label_values_digest_is_bound(candidate):
    assert candidate["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_n_research_registry_digest_is_bound(candidate):
    assert candidate["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_o_records_digest_is_bound(candidate):
    assert candidate["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_p_universe_count_and_order_are_preserved(candidate):
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_q_meta_913_is_preserved(candidate):
    assert candidate["meta_record_count"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_r_selected_option_is_option_a(candidate):
    assert candidate["selected_method_evidence_improvement_option"] == service.SELECTED_OPTION


def test_s_ready_for_candidate_is_true(candidate):
    assert candidate["ready_for_label_objective_target_definition_review_candidate_using_redesigned_evidence"] is True


def test_t_candidate_created_and_ready_are_true(candidate):
    assert candidate["label_objective_target_definition_review_candidate_created"] is True
    assert candidate["label_objective_target_definition_review_candidate_using_redesigned_evidence_created"] is True
    assert candidate["label_objective_target_definition_review_candidate_using_redesigned_evidence_ready_for_operator_review"] is True


def test_u_review_approved_and_executed_are_false(candidate):
    assert candidate["label_objective_target_definition_review_approved"] is False
    assert candidate["label_objective_target_definition_review_authorized"] is False
    assert candidate["label_objective_target_definition_review_executed"] is False


def test_v_label_regeneration_is_false(candidate):
    assert candidate["redesigned_label_regeneration_performed"] is False
    assert all(row["label_regeneration_performed"] is False for row in candidate["current_label_family_review_plan"])


def test_w_new_targets_created_is_false(candidate):
    assert candidate["new_targets_created"] is False
    assert candidate["label_objective_redesign_candidate_created"] is False


def test_x_predictive_usefulness_is_not_accepted(candidate):
    assert candidate["predictive_usefulness"] == "not accepted"


def test_y_acceptance_ready_and_candidate_are_false(candidate):
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_z_profitability_is_not_accepted(candidate):
    assert candidate["profitability"] == "not accepted"


def test_aa_runtime_is_not_authorized(candidate):
    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"


def test_ab_trade_recommendations_are_false(candidate):
    assert candidate["trade_recommendations_generated"] is False


def test_ac_problem_basis_is_preserved(candidate):
    assert candidate["problem_basis"]["readiness_decision"] == service.READINESS_DECISION
    assert candidate["problem_basis"]["oos_cross_sectional_delta_vs_majority"] == "0.00309917"
    assert candidate["problem_basis"]["selected_option"] == service.SELECTED_OPTION


def test_ad_candidate_objective_is_defined(candidate):
    assert candidate["label_objective_target_definition_review_objective"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_OBJECTIVE
    assert candidate["label_objective_target_definition_review_scope"] == "CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"


def test_ae_review_dimensions_are_defined(candidate):
    assert [row["dimension_id"] for row in candidate["review_dimensions"]] == service.REVIEW_DIMENSION_IDS
    assert all(row["dimension_status"] == "PLANNED_NOT_EXECUTED" for row in candidate["review_dimensions"])


def test_af_label_family_review_plan_is_defined(candidate):
    assert [row["label_family"] for row in candidate["current_label_family_review_plan"]] == service.LABEL_FAMILY_IDS
    assert all(row["target_definition_change_authorized"] is False for row in candidate["current_label_family_review_plan"])


def test_ag_diagnostic_questions_are_defined(candidate):
    assert [row["question"] for row in candidate["diagnostic_questions"]] == service.DIAGNOSTIC_QUESTIONS
    assert all(row["question_status"] == "NOT_ANSWERED" for row in candidate["diagnostic_questions"])


def test_ah_decision_options_are_defined(candidate):
    assert [row["decision_option"] for row in candidate["decision_options_for_future_review"]] == service.DECISION_OPTION_IDS
    assert all(row["selected"] is False for row in candidate["decision_options_for_future_review"])


def test_ai_planned_outputs_are_not_generated(candidate):
    assert [row["output_name"] for row in candidate["planned_outputs"]] == service.PLANNED_OUTPUT_NAMES
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in candidate["planned_outputs"])


def test_aj_per_ticker_entries_count_is_12(candidate):
    assert len(candidate["per_ticker_candidate_entries"]) == 12


def test_ak_per_ticker_digests_are_present(candidate):
    assert all(len(row["per_ticker_label_objective_target_definition_review_candidate_digest"]) == 64 for row in candidate["per_ticker_candidate_entries"])


def test_al_next_chain_is_defined(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES


def test_am_risk_controls_are_defined(candidate):
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_an_checklist_passes(candidate):
    assert candidate["candidate_summary"]["passed_checks"] == len(service.CHECK_IDS)
    assert candidate["candidate_summary"]["failed_checks"] == 0


def test_ao_candidate_digest_is_deterministic(candidate):
    assert service.label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(candidate) == candidate["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"]


def test_ap_per_ticker_digests_are_deterministic(candidate):
    for entry in candidate["per_ticker_candidate_entries"]:
        assert service.per_ticker_label_objective_target_definition_review_candidate_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_label_objective_target_definition_review_candidate_digest"]


def test_aq_validator_accepts_valid_candidate(candidate):
    result = service.validate_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(candidate)
    assert result["blocker_count"] == 0


def test_ar_validator_rejects_wrong_artifact_kind(candidate):
    _reject(candidate, "artifact_kind", "WRONG")


def test_as_validator_rejects_wrong_status(candidate):
    _reject(candidate, "candidate_status", "WRONG")


def test_at_validator_rejects_selected_option_not_option_a(candidate):
    _reject(candidate, "selected_method_evidence_improvement_option", "OPTION_B")


def test_au_validator_rejects_candidate_created_false(candidate):
    _reject(candidate, "label_objective_target_definition_review_candidate_created", False)


def test_av_validator_rejects_review_approved_true(candidate):
    _reject(candidate, "label_objective_target_definition_review_approved", True)


def test_aw_validator_rejects_review_executed_true(candidate):
    _reject(candidate, "label_objective_target_definition_review_executed", True)


def test_ax_validator_rejects_label_regeneration_true(candidate):
    _reject(candidate, "redesigned_label_regeneration_performed", True)


def test_ay_validator_rejects_new_targets_created_true(candidate):
    _reject(candidate, "new_targets_created", True)


def test_az_validator_rejects_predictive_usefulness_accepted(candidate):
    _reject(candidate, "predictive_usefulness", "accepted")


def test_ba_validator_rejects_runtime_authorized(candidate):
    _reject(candidate, "runtime_use", "AUTHORIZED")


def test_bb_validator_rejects_trade_recommendations_true(candidate):
    _reject(candidate, "trade_recommendations_generated", True)


def test_bc_validator_rejects_predictive_evidence_rerun_true(candidate):
    _reject(candidate, "predictive_evidence_execution_rerun_performed", True)


def test_bd_validator_rejects_metric_recomputation_true(candidate):
    _reject(candidate, "metric_recomputation_performed_in_candidate", True)


def test_be_validator_rejects_model_training_true(candidate):
    _reject(candidate, "model_training_performed_in_candidate", True)


def test_bf_validator_rejects_missing_review_dimensions(candidate):
    _reject(candidate, "review_dimensions", None)


def test_bg_validator_rejects_missing_next_chain(candidate):
    _reject(candidate, "next_chain", None)


def test_bh_markdown_includes_required_sections(candidate):
    markdown = service.build_label_objective_target_definition_review_candidate_using_redesigned_evidence_markdown_v1(candidate)
    for section in (
        "## Title", "## Label Objective / Target Definition Review Candidate Using Redesigned Evidence",
        "## Source Path Selection", "## Bound Evidence", "## Dataset and Universe",
        "## Problem Basis", "## Candidate Objective", "## Review Dimensions",
        "## Current Label Family Review Plan", "## Diagnostic Questions", "## Decision Options",
        "## Planned Outputs", "## Per-Ticker Candidate Entries", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Predictive Usefulness Boundary",
        "## Profitability Boundary", "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    ):
        assert section in markdown


def test_bi_writer_creates_canonical_json_without_overwrite(tmp_path):
    receipt = service.write_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
        tmp_path
    )
    path = tmp_path / "label_objective_target_definition_review_candidate_using_redesigned_evidence_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_CANDIDATE_USING_REDESIGNED_EVIDENCE
    assert len(receipt["payload_sha256"]) == 64
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewCandidateRedesignedEvidenceError):
        service.write_label_objective_target_definition_review_candidate_using_redesigned_evidence_v1(
            tmp_path
        )
