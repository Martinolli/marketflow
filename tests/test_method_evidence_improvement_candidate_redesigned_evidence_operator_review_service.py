from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    method_evidence_improvement_candidate_redesigned_evidence_operator_review_service as service,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return service.build_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1()


def _rejected(review_package: dict, field: str, value) -> None:
    changed = deepcopy(review_package)
    changed[field] = value
    with pytest.raises(
        service.MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError
    ):
        service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
            changed
        )


def test_a_review_package_builds_offline(review_package):
    assert review_package["created_offline"] is True
    assert review_package["provider_requests_made_in_review"] is False


def test_b_artifact_kind_is_correct(review_package):
    assert review_package["artifact_kind"] == service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE


def test_c_review_status_is_correct(review_package):
    assert review_package["review_status"] == service.METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY


def test_d_reviewed_candidate_digest_matches_expected(review_package):
    assert review_package["source_candidate_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_e_candidate_checklist_has_zero_blockers(review_package):
    assert review_package["source_candidate_blocker_count"] == 0
    assert review_package["source_candidate_checklist_passed"] == 54


def test_f_candidate_digest_is_bound(review_package):
    assert review_package["method_evidence_improvement_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_g_readiness_review_digest_is_bound(review_package):
    assert review_package["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_h_reassessment_digest_is_bound(review_package):
    assert review_package["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_i_results_review_digest_is_bound(review_package):
    assert review_package["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_j_execution_digest_is_bound(review_package):
    assert review_package["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_k_matrix_digest_is_bound(review_package):
    assert review_package["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_l_feature_values_digest_is_bound(review_package):
    assert review_package["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_m_label_values_digest_is_bound(review_package):
    assert review_package["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_n_research_registry_digest_is_bound(review_package):
    assert review_package["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_o_records_digest_is_bound(review_package):
    assert review_package["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_p_universe_count_and_order_are_preserved(review_package):
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_q_meta_913_is_preserved(review_package):
    assert review_package["meta_record_count"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_r_source_readiness_decision_is_not_ready(review_package):
    assert review_package["source_readiness_decision"] == service.SOURCE_READINESS_DECISION


def test_s_additional_improvement_readiness_is_true(review_package):
    assert review_package["ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"] is True


def test_t_candidate_created_and_review_created_are_true(review_package):
    assert review_package["method_evidence_improvement_candidate_using_redesigned_evidence_created"] is True
    assert review_package["method_evidence_improvement_candidate_using_redesigned_evidence_review_created"] is True


def test_u_improvement_approval_execution_and_path_selection_are_false(review_package):
    assert review_package["method_evidence_improvement_approved"] is False
    assert review_package["method_evidence_improvement_authorized"] is False
    assert review_package["method_evidence_improvement_executed"] is False
    assert review_package["method_evidence_improvement_path_selected"] is False


def test_v_improved_evidence_planning_candidate_is_false(review_package):
    assert review_package["improved_evidence_planning_candidate_created"] is False


def test_w_predictive_usefulness_is_not_accepted(review_package):
    assert review_package["predictive_usefulness"] == "not accepted"


def test_x_acceptance_ready_and_recommended_are_false(review_package):
    assert review_package["predictive_usefulness_acceptance_ready"] is False
    assert review_package["predictive_usefulness_acceptance_recommended"] is False


def test_y_acceptance_candidate_is_false(review_package):
    assert review_package["predictive_usefulness_acceptance_candidate_created"] is False


def test_z_profitability_is_not_accepted(review_package):
    assert review_package["profitability"] == "not accepted"


def test_aa_runtime_is_not_authorized(review_package):
    assert review_package["runtime_use"] == "NOT_AUTHORIZED"
    assert review_package["strategy_use"] == "NOT_AUTHORIZED"


def test_ab_trade_recommendations_are_false(review_package):
    assert review_package["trade_recommendations_generated"] is False


def test_ac_problem_basis_is_reviewed(review_package):
    assert review_package["reviewed_problem_basis"] == service.PROBLEM_BASIS


def test_ad_improvement_objective_is_reviewed(review_package):
    assert review_package["reviewed_method_evidence_improvement_objective"] == service.candidate_service.METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE


def test_ae_improvement_themes_are_reviewed(review_package):
    assert [row["theme_id"] for row in review_package["reviewed_improvement_themes"]] == service.IMPROVEMENT_THEME_IDS
    assert all(row["theme_status"] == "PLANNED_NOT_EXECUTED" for row in review_package["reviewed_improvement_themes"])


def test_af_improvement_options_are_reviewed(review_package):
    assert [row["option_id"] for row in review_package["reviewed_improvement_options"]] == service.IMPROVEMENT_OPTION_IDS
    assert all(row["selected"] is False for row in review_package["reviewed_improvement_options"])


def test_ag_recommended_option_is_preserved(review_package):
    assert review_package["recommended_next_option"] == "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION"


def test_ah_diagnostic_questions_are_reviewed(review_package):
    assert [row["question"] for row in review_package["reviewed_diagnostic_questions"]] == service.DIAGNOSTIC_QUESTIONS
    assert all(row["status"] == "NOT_ANSWERED" for row in review_package["reviewed_diagnostic_questions"])


def test_ai_planned_outputs_are_not_generated(review_package):
    assert [row["output_name"] for row in review_package["reviewed_planned_outputs"]] == service.PLANNED_OUTPUT_NAMES
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in review_package["reviewed_planned_outputs"])


def test_aj_per_ticker_entries_count_is_12(review_package):
    assert len(review_package["per_ticker_review_entries"]) == 12


def test_ak_per_ticker_candidate_digests_are_present(review_package):
    assert all(len(row["per_ticker_method_evidence_improvement_candidate_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_al_per_ticker_review_digests_are_present(review_package):
    assert all(len(row["per_ticker_method_evidence_improvement_candidate_review_digest"]) == 64 for row in review_package["per_ticker_review_entries"])


def test_am_next_chain_is_reviewed(review_package):
    assert review_package["next_chain"] == service.NEXT_CHAIN
    assert review_package["next_gates"] == service.NEXT_GATES


def test_an_risk_controls_are_reviewed(review_package):
    assert review_package["risk_controls"] == service.RISK_CONTROLS


def test_ao_checklist_passes(review_package):
    assert review_package["review_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review_package["review_summary"]["failed_checks"] == 0


def test_ap_review_digest_is_deterministic(review_package):
    assert service.method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest_v1(review_package) == review_package["method_evidence_improvement_candidate_using_redesigned_evidence_review_package_digest"]


def test_aq_per_ticker_review_digests_are_deterministic(review_package):
    for entry in review_package["per_ticker_review_entries"]:
        assert service.per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_review_digest_v1(entry) == entry["per_ticker_method_evidence_improvement_candidate_review_digest"]


def test_ar_validator_accepts_valid_review(review_package):
    result = service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(review_package)
    assert result["status"] == "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID"


def test_as_validator_rejects_wrong_artifact_kind(review_package):
    _rejected(review_package, "artifact_kind", "WRONG")


def test_at_validator_rejects_wrong_status(review_package):
    _rejected(review_package, "review_status", "WRONG")


def test_au_validator_rejects_changed_candidate_digest(review_package):
    _rejected(review_package, "source_candidate_digest", "0" * 64)


def test_av_validator_rejects_candidate_blocker(review_package):
    _rejected(review_package, "source_candidate_blocker_count", 1)


def test_aw_validator_rejects_source_decision_not_not_ready(review_package):
    _rejected(review_package, "source_readiness_decision", "READY")


def test_ax_validator_rejects_approval_true(review_package):
    _rejected(review_package, "method_evidence_improvement_approved", True)


def test_ay_validator_rejects_path_selected_true(review_package):
    _rejected(review_package, "method_evidence_improvement_path_selected", True)


def test_az_validator_rejects_improved_evidence_candidate_true(review_package):
    _rejected(review_package, "improved_evidence_planning_candidate_created", True)


def test_ba_validator_rejects_predictive_usefulness_accepted(review_package):
    _rejected(review_package, "predictive_usefulness", "accepted")


def test_bb_validator_rejects_runtime_authorized(review_package):
    _rejected(review_package, "runtime_use", "AUTHORIZED")


def test_bc_validator_rejects_trade_recommendations_true(review_package):
    _rejected(review_package, "trade_recommendations_generated", True)


def test_bd_validator_rejects_predictive_evidence_rerun_true(review_package):
    _rejected(review_package, "predictive_evidence_execution_rerun_performed", True)


def test_be_validator_rejects_metric_recomputation_in_review_true(review_package):
    _rejected(review_package, "metric_recomputation_performed_in_review", True)


def test_bf_validator_rejects_model_training_in_review_true(review_package):
    _rejected(review_package, "model_training_performed_in_review", True)


def test_bg_validator_rejects_missing_improvement_options(review_package):
    _rejected(review_package, "reviewed_improvement_options", [])


def test_bh_validator_rejects_missing_next_chain(review_package):
    _rejected(review_package, "next_chain", [])


def test_bi_markdown_includes_required_sections(review_package):
    markdown = service.build_method_evidence_improvement_candidate_using_redesigned_evidence_review_markdown_v1(
        review_package
    )
    for section in (
        "Title", "Method / Evidence Improvement Candidate Review Using Redesigned Evidence",
        "Reviewed Candidate", "Source Readiness Review", "Bound Evidence", "Dataset and Universe",
        "Reviewed Problem Basis", "Reviewed Improvement Objective", "Reviewed Improvement Themes",
        "Reviewed Improvement Options", "Reviewed Diagnostic Questions", "Reviewed Planned Outputs",
        "Per-Ticker Review Entries", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_canonical_review_without_overwrite(tmp_path):
    result = service.write_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        tmp_path
    )
    path = Path(result["path"])
    written = json.loads(path.read_text(encoding="utf-8"))
    validation = service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
        written
    )
    assert validation["status"] == "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID"
    with pytest.raises(
        service.MethodEvidenceImprovementCandidateRedesignedEvidenceOperatorReviewError
    ):
        service.write_method_evidence_improvement_candidate_using_redesigned_evidence_review_package_v1(
            tmp_path
        )
