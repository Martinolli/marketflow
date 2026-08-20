from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import method_evidence_improvement_candidate_redesigned_evidence_service as service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_method_evidence_improvement_candidate_using_redesigned_evidence_v1()


def _rejected(candidate: dict, field: str, value) -> None:
    changed = deepcopy(candidate)
    changed[field] = value
    with pytest.raises(service.MethodEvidenceImprovementCandidateRedesignedEvidenceError):
        service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(changed)


def test_a_candidate_builds_offline(candidate):
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made_in_candidate"] is False


def test_b_artifact_kind_is_correct(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND_METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE


def test_c_candidate_status_is_correct(candidate):
    assert candidate["candidate_status"] == service.METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW


def test_d_readiness_review_digest_is_bound(candidate):
    assert candidate["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_e_reassessment_digest_is_bound(candidate):
    assert candidate["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_f_results_review_digest_is_bound(candidate):
    assert candidate["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_g_execution_digest_is_bound(candidate):
    assert candidate["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_h_matrix_digest_is_bound(candidate):
    assert candidate["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_i_feature_values_digest_is_bound(candidate):
    assert candidate["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_j_label_values_digest_is_bound(candidate):
    assert candidate["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_k_research_registry_digest_is_bound(candidate):
    assert candidate["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_l_records_digest_is_bound(candidate):
    assert candidate["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_m_universe_count_and_order_are_preserved(candidate):
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_n_meta_913_is_preserved(candidate):
    assert candidate["meta_record_count"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_o_source_readiness_decision_is_not_ready(candidate):
    assert candidate["source_readiness_decision"] == service.SOURCE_READINESS_DECISION


def test_p_additional_improvement_readiness_is_true(candidate):
    assert candidate["ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"] is True


def test_q_candidate_created_and_ready_are_true(candidate):
    assert candidate["method_evidence_improvement_candidate_using_redesigned_evidence_created"] is True
    assert candidate["method_evidence_improvement_candidate_using_redesigned_evidence_ready_for_operator_review"] is True


def test_r_improvement_approval_and_execution_are_false(candidate):
    assert candidate["method_evidence_improvement_approved"] is False
    assert candidate["method_evidence_improvement_authorized"] is False
    assert candidate["method_evidence_improvement_executed"] is False


def test_s_improved_evidence_planning_candidate_is_false(candidate):
    assert candidate["improved_evidence_planning_candidate_created"] is False


def test_t_predictive_usefulness_is_not_accepted(candidate):
    assert candidate["predictive_usefulness"] == "not accepted"


def test_u_acceptance_ready_and_recommended_are_false(candidate):
    assert candidate["predictive_usefulness_acceptance_ready"] is False
    assert candidate["predictive_usefulness_acceptance_recommended"] is False


def test_v_acceptance_candidate_is_false(candidate):
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_w_profitability_is_not_accepted(candidate):
    assert candidate["profitability"] == "not accepted"


def test_x_runtime_is_not_authorized(candidate):
    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"


def test_y_trade_recommendations_are_false(candidate):
    assert candidate["trade_recommendations_generated"] is False


def test_z_problem_basis_is_preserved(candidate):
    assert candidate["problem_basis"] == service.PROBLEM_BASIS


def test_aa_improvement_objective_is_defined(candidate):
    assert candidate["method_evidence_improvement_objective"] == service.METHOD_EVIDENCE_IMPROVEMENT_OBJECTIVE


def test_ab_improvement_themes_are_defined(candidate):
    assert [row["theme_id"] for row in candidate["improvement_themes"]] == service.IMPROVEMENT_THEME_IDS
    assert all(row["theme_status"] == "PLANNED_NOT_EXECUTED" for row in candidate["improvement_themes"])


def test_ac_improvement_options_are_defined(candidate):
    assert [row["option_id"] for row in candidate["improvement_options"]] == service.IMPROVEMENT_OPTION_IDS
    assert all(row["selected"] is False for row in candidate["improvement_options"])


def test_ad_recommended_option_is_option_a(candidate):
    assert candidate["recommended_next_option"] == "OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION"


def test_ae_diagnostic_questions_are_defined(candidate):
    assert [row["question"] for row in candidate["planned_diagnostic_questions"]] == service.DIAGNOSTIC_QUESTIONS
    assert all(row["status"] == "NOT_ANSWERED" for row in candidate["planned_diagnostic_questions"])


def test_af_planned_outputs_are_not_generated(candidate):
    assert [row["output_name"] for row in candidate["planned_outputs"]] == service.PLANNED_OUTPUT_NAMES
    assert all(row["output_status"] == "PLANNED_NOT_GENERATED" for row in candidate["planned_outputs"])


def test_ag_per_ticker_entries_count_is_12(candidate):
    assert len(candidate["per_ticker_improvement_candidate_entries"]) == 12


def test_ah_per_ticker_digests_are_present(candidate):
    assert all(len(row["per_ticker_method_evidence_improvement_candidate_digest"]) == 64 for row in candidate["per_ticker_improvement_candidate_entries"])


def test_ai_next_chain_is_defined(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES


def test_aj_risk_controls_are_defined(candidate):
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_ak_checklist_passes(candidate):
    assert candidate["candidate_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["candidate_summary"]["failed_checks"] == 0


def test_al_candidate_digest_is_deterministic(candidate):
    assert service.method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(candidate) == candidate["method_evidence_improvement_candidate_using_redesigned_evidence_digest"]


def test_am_per_ticker_digests_are_deterministic(candidate):
    for entry in candidate["per_ticker_improvement_candidate_entries"]:
        assert service.per_ticker_method_evidence_improvement_candidate_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_method_evidence_improvement_candidate_digest"]


def test_an_validator_accepts_valid_candidate(candidate):
    result = service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(candidate)
    assert result["status"] == "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID"


def test_ao_validator_rejects_wrong_artifact_kind(candidate):
    _rejected(candidate, "artifact_kind", "WRONG")


def test_ap_validator_rejects_wrong_status(candidate):
    _rejected(candidate, "candidate_status", "WRONG")


def test_aq_validator_rejects_source_decision_not_not_ready(candidate):
    _rejected(candidate, "source_readiness_decision", "READY")


def test_ar_validator_rejects_additional_improvement_ready_false(candidate):
    _rejected(candidate, "ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence", False)


def test_as_validator_rejects_approval_true(candidate):
    _rejected(candidate, "method_evidence_improvement_approved", True)


def test_at_validator_rejects_improved_evidence_candidate_true(candidate):
    _rejected(candidate, "improved_evidence_planning_candidate_created", True)


def test_au_validator_rejects_predictive_usefulness_accepted(candidate):
    _rejected(candidate, "predictive_usefulness", "accepted")


def test_av_validator_rejects_acceptance_ready_true(candidate):
    _rejected(candidate, "predictive_usefulness_acceptance_ready", True)


def test_aw_validator_rejects_runtime_authorized(candidate):
    _rejected(candidate, "runtime_use", "AUTHORIZED")


def test_ax_validator_rejects_trade_recommendations_true(candidate):
    _rejected(candidate, "trade_recommendations_generated", True)


def test_ay_validator_rejects_predictive_evidence_rerun_true(candidate):
    _rejected(candidate, "predictive_evidence_execution_rerun_performed", True)


def test_az_validator_rejects_metric_recomputation_in_candidate_true(candidate):
    _rejected(candidate, "metric_recomputation_performed_in_candidate", True)


def test_ba_validator_rejects_model_training_in_candidate_true(candidate):
    _rejected(candidate, "model_training_performed_in_candidate", True)


def test_bb_validator_rejects_missing_improvement_options(candidate):
    _rejected(candidate, "improvement_options", [])


def test_bc_validator_rejects_missing_next_chain(candidate):
    _rejected(candidate, "next_chain", [])


def test_bd_markdown_includes_required_sections(candidate):
    markdown = service.build_method_evidence_improvement_candidate_using_redesigned_evidence_markdown_v1(candidate)
    for section in (
        "Title", "Method / Evidence Improvement Candidate Using Redesigned Evidence",
        "Source Readiness Review", "Bound Evidence", "Dataset and Universe", "Problem Basis",
        "Improvement Objective", "Improvement Themes", "Improvement Options", "Diagnostic Questions",
        "Planned Outputs", "Per-Ticker Candidate Entries", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_canonical_package_without_overwrite(tmp_path):
    result = service.write_method_evidence_improvement_candidate_using_redesigned_evidence_v1(tmp_path)
    path = Path(result["path"])
    written = json.loads(path.read_text(encoding="utf-8"))
    validation = service.validate_method_evidence_improvement_candidate_using_redesigned_evidence_v1(written)
    assert validation["status"] == "METHOD_EVIDENCE_IMPROVEMENT_CANDIDATE_USING_REDESIGNED_EVIDENCE_VALID"
    with pytest.raises(service.MethodEvidenceImprovementCandidateRedesignedEvidenceError):
        service.write_method_evidence_improvement_candidate_using_redesigned_evidence_v1(tmp_path)
