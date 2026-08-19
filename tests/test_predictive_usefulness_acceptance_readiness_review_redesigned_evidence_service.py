from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import predictive_usefulness_acceptance_readiness_review_redesigned_evidence_service as service


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1()


def _rejected(review: dict, field: str, value) -> None:
    changed = deepcopy(review)
    changed[field] = value
    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError):
        service.validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(changed)


def test_a_readiness_review_builds_offline(review):
    assert review["created_offline"] is True


def test_b_artifact_kind_is_correct(review):
    assert review["artifact_kind"] == service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE


def test_c_review_status_is_correct(review):
    assert review["review_status"] == service.PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED


def test_d_reassessment_digest_is_bound(review):
    assert review["predictive_usefulness_reassessment_using_redesigned_evidence_digest"] == service.EXPECTED_REASSESSMENT_DIGEST


def test_e_results_review_digest_is_bound(review):
    assert review["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_f_execution_digest_is_bound(review):
    assert review["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_g_matrix_digest_is_bound(review):
    assert review["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_h_feature_values_digest_is_bound(review):
    assert review["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_i_label_values_digest_is_bound(review):
    assert review["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_j_research_registry_digest_is_bound(review):
    assert review["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_k_records_digest_is_bound(review):
    assert review["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_l_universe_count_and_order_are_preserved(review):
    assert review["target_universe_count"] == 12
    assert review["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_m_meta_913_is_preserved(review):
    assert review["meta_record_count"] == 913
    assert review["meta_reduced_record_count_preserved"] is True


def test_n_source_reassessment_ready_is_true(review):
    assert review["predictive_usefulness_reassessment_ready"] is True


def test_o_ready_for_readiness_review_is_true(review):
    assert review["ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence"] is True


def test_p_readiness_review_created_and_completed_are_true(review):
    assert review["predictive_usefulness_acceptance_readiness_review_created"] is True
    assert review["predictive_usefulness_acceptance_readiness_review_completed"] is True


def test_q_decision_is_not_ready(review):
    assert review["readiness_decision"] == service.PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE


def test_r_acceptance_ready_is_false(review):
    assert review["predictive_usefulness_acceptance_ready"] is False


def test_s_acceptance_recommended_is_false(review):
    assert review["predictive_usefulness_acceptance_recommended"] is False


def test_t_acceptance_candidate_created_is_false(review):
    assert review["predictive_usefulness_acceptance_candidate_created"] is False


def test_u_predictive_usefulness_is_not_accepted(review):
    assert review["predictive_usefulness"] == "not accepted"


def test_v_profitability_is_not_accepted(review):
    assert review["profitability"] == "not accepted"


def test_w_runtime_is_not_authorized(review):
    assert review["runtime_use"] == "NOT_AUTHORIZED"


def test_x_trade_recommendations_are_false(review):
    assert review["trade_recommendations_generated"] is False


def test_y_evidence_integrity_passes(review):
    assert review["readiness_criteria"]["evidence_integrity_pass"]["criterion_status"] == "PASS"


def test_z_leakage_passes(review):
    assert review["leakage_readiness"] == "PASS"


def test_aa_cross_sectional_edge_is_not_material(review):
    assert review["readiness_criteria"]["oos_cross_sectional_edge_materiality"]["criterion_status"] == "FAIL_OR_NOT_MET"


def test_ab_local_model_outperformance_is_not_material(review):
    assert review["readiness_criteria"]["local_model_outperformance_materiality"]["criterion_status"] == "FAIL_OR_NOT_MET"


def test_ac_stability_is_not_ready(review):
    assert review["stability_readiness"] == "NOT_READY"


def test_ad_baseline_outperformance_is_not_ready(review):
    assert review["baseline_outperformance_readiness"] == "NOT_READY"


def test_ae_optional_model_coverage_is_not_sufficient(review):
    assert review["readiness_criteria"]["optional_model_coverage_sufficiency"]["criterion_status"] == "FAIL_OR_NOT_MET"


def test_af_calibration_requires_review(review):
    assert review["calibration_readiness"] == "REQUIRES_OPERATOR_REVIEW"


def test_ag_additional_improvement_readiness_is_true(review):
    assert review["ready_for_additional_method_or_evidence_improvement_using_redesigned_evidence"] is True


def test_ah_per_ticker_entries_count_is_12(review):
    assert len(review["per_ticker_readiness_entries"]) == 12


def test_ai_per_ticker_digests_are_present(review):
    assert all(len(row["per_ticker_acceptance_readiness_digest"]) == 64 for row in review["per_ticker_readiness_entries"])


def test_aj_next_chain_is_defined(review):
    assert review["next_chain"] == service.NEXT_CHAIN


def test_ak_risk_controls_are_defined(review):
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_al_checklist_passes(review):
    assert review["readiness_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["readiness_summary"]["failed_checks"] == 0


def test_am_readiness_digest_is_deterministic(review):
    assert service.predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(review) == review["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"]


def test_an_per_ticker_digests_are_deterministic(review):
    for entry in review["per_ticker_readiness_entries"]:
        assert service.per_ticker_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_acceptance_readiness_digest"]


def test_ao_validator_accepts_valid_readiness_review(review):
    result = service.validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(review)
    assert result["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID"


def test_ap_validator_rejects_wrong_artifact_kind(review):
    _rejected(review, "artifact_kind", "WRONG")


def test_aq_validator_rejects_wrong_status(review):
    _rejected(review, "review_status", "WRONG")


def test_ar_validator_rejects_source_reassessment_ready_false(review):
    _rejected(review, "predictive_usefulness_reassessment_ready", False)


def test_as_validator_rejects_wrong_readiness_decision(review):
    _rejected(review, "readiness_decision", "READY")


def test_at_validator_rejects_acceptance_ready_true(review):
    _rejected(review, "predictive_usefulness_acceptance_ready", True)


def test_au_validator_rejects_acceptance_candidate_true(review):
    _rejected(review, "predictive_usefulness_acceptance_candidate_created", True)


def test_av_validator_rejects_predictive_usefulness_accepted(review):
    _rejected(review, "predictive_usefulness", "accepted")


def test_aw_validator_rejects_runtime_authorized(review):
    _rejected(review, "runtime_use", "AUTHORIZED")


def test_ax_validator_rejects_trade_recommendations_true(review):
    _rejected(review, "trade_recommendations_generated", True)


def test_ay_validator_rejects_predictive_evidence_rerun_true(review):
    _rejected(review, "predictive_evidence_execution_rerun_performed", True)


def test_az_validator_rejects_metric_recomputation_in_review_true(review):
    _rejected(review, "metric_recomputation_performed_in_review", True)


def test_ba_validator_rejects_model_training_in_review_true(review):
    _rejected(review, "model_training_performed_in_review", True)


def test_bb_validator_rejects_missing_criteria(review):
    _rejected(review, "readiness_criteria", {})


def test_bc_validator_rejects_missing_next_chain(review):
    _rejected(review, "next_chain", [])


def test_bd_markdown_includes_required_sections(review):
    markdown = service.build_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_markdown_v1(review)
    for section in (
        "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence",
        "Source Reassessment", "Bound Evidence", "Dataset and Universe", "Evidence Summary",
        "Readiness Criteria", "Readiness Findings", "Readiness Decision",
        "Per-Ticker Readiness Entries", "Next Chain", "Next Gates", "Risk Controls",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_canonical_package_without_overwrite(tmp_path):
    result = service.write_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(tmp_path)
    path = Path(result["path"])
    written = json.loads(path.read_text(encoding="utf-8"))
    assert service.validate_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(written)["status"] == "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID"
    with pytest.raises(service.PredictiveUsefulnessAcceptanceReadinessReviewRedesignedEvidenceError):
        service.write_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_v1(tmp_path)
