from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import additional_predictive_evidence_results_review_redesigned_labels_service as service


@pytest.fixture(scope="module")
def package() -> dict:
    return service.build_additional_predictive_evidence_results_review_using_redesigned_labels_v1()


def _rejected(package: dict, field: str, value) -> None:
    changed = deepcopy(package)
    changed[field] = value
    with pytest.raises(service.AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError):
        service.validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(changed)


def test_a_review_package_builds_offline(package):
    assert package["created_offline"] is True


def test_b_review_blocks_when_output_root_is_missing(tmp_path):
    blocked = service.build_additional_predictive_evidence_results_review_using_redesigned_labels_v1(output_root=tmp_path / "missing")
    assert blocked["review_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS
    assert blocked["additional_predictive_evidence_results_review_ready"] is False


def test_c_artifact_kind_is_correct(package):
    assert package["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS


def test_d_review_status_is_correct(package):
    assert package["review_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY


def test_e_source_execution_digest_is_bound(package):
    assert package["source_additional_predictive_evidence_execution_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_f_matrix_digest_is_bound(package):
    assert package["source_feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_g_source_approval_digest_is_bound(package):
    assert package["source_additional_predictive_evidence_execution_approval_digest"] == service.EXPECTED_APPROVAL_DIGEST


def test_h_candidate_review_digest_is_bound(package):
    assert package["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_i_feature_values_digest_is_bound(package):
    assert package["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_j_redesigned_label_values_digest_is_bound(package):
    assert package["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_k_research_registry_digest_is_bound(package):
    assert package["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_l_records_digest_is_bound(package):
    assert package["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_m_universe_count_and_order_are_preserved(package):
    assert package["target_universe_count"] == 12
    assert package["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_n_meta_913_is_preserved(package):
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_o_generated_output_count_is_13(package):
    assert package["generated_output_count"] == 13


def test_p_output_digests_are_bound(package):
    assert len(package["output_digest_manifest"]) == 13
    assert all(row["digest_match"] for row in package["output_digest_manifest"])


def test_q_outputs_are_research_only_non_actionable(package):
    assert package["outputs_research_only_non_actionable"] is True


def test_r_feature_label_matrix_is_verified(package):
    assert package["verified_sections"]["feature_label_matrix"] is True


def test_s_matrix_row_count_is_143352(package):
    assert package["feature_label_matrix_row_count"] == 143352


def test_t_evaluable_matrix_row_count_is_142200(package):
    assert package["evaluable_matrix_row_count"] == 142200


def test_u_unavailable_target_count_is_1152(package):
    assert package["unavailable_target_matrix_row_count"] == 1152


def test_v_walk_forward_results_are_verified(package):
    assert package["verified_sections"]["walk_forward_results"] is True


def test_w_walk_forward_fold_count_is_4(package):
    assert package["walk_forward_fold_count"] == 4


def test_x_oos_holdout_results_are_verified(package):
    assert package["verified_sections"]["oos_holdout_results"] is True


def test_y_oos_year_is_2025(package):
    assert package["oos_holdout_year"] == 2025


def test_z_oos_evaluated_rows_are_34848(package):
    assert package["oos_evaluated_rows"] == 34848


def test_aa_baseline_model_comparison_is_verified(package):
    assert package["verified_sections"]["baseline_model_comparison"] is True


def test_ab_metric_family_results_are_verified(package):
    assert package["verified_sections"]["metric_family_results"] is True


def test_ac_metric_family_count_is_10(package):
    assert package["metric_family_count"] == 10


def test_ad_calibration_stability_report_is_verified(package):
    assert package["verified_sections"]["calibration_stability_report"] is True


def test_ae_leakage_control_status_is_pass(package):
    assert package["leakage_control_status"] == "PASS"


def test_af_leakage_failed_controls_are_zero(package):
    assert package["leakage_failed_control_count"] == 0


def test_ag_per_ticker_review_is_verified(package):
    assert len(package["per_ticker_cross_sectional_review"]) == 12


def test_ah_cross_sectional_delta_is_bound(package):
    assert package["oos_cross_sectional_delta_vs_majority"] == "0.00309917"


def test_ai_local_model_delta_is_bound(package):
    assert package["oos_local_model_delta_vs_majority"] == "0.00000000"


def test_aj_optional_model_unavailability_is_recorded(package):
    assert list(package["optional_model_statuses"].values()).count("NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE") == 2


def test_ak_results_review_created_and_ready_are_true(package):
    assert package["additional_predictive_evidence_results_review_created"] is True
    assert package["additional_predictive_evidence_results_review_ready"] is True


def test_al_ready_for_predictive_usefulness_reassessment_is_true(package):
    assert package["ready_for_predictive_usefulness_reassessment_using_redesigned_evidence"] is True


def test_am_predictive_usefulness_reassessment_created_is_false(package):
    assert package["predictive_usefulness_reassessment_review_created"] is False


def test_an_predictive_usefulness_remains_not_accepted(package):
    assert package["predictive_usefulness"] == "not accepted"


def test_ao_profitability_remains_not_accepted(package):
    assert package["profitability"] == "not accepted"


def test_ap_runtime_remains_not_authorized(package):
    assert package["runtime_use"] == "NOT_AUTHORIZED"


def test_aq_trade_recommendations_remain_false(package):
    assert package["trade_recommendations_generated"] is False


def test_ar_no_predictive_evidence_rerun_in_review(package):
    assert package["predictive_evidence_execution_rerun_performed"] is False


def test_as_no_metric_recomputation_in_review(package):
    assert package["metric_recomputation_performed_in_review"] is False


def test_at_no_model_training_in_review(package):
    assert package["model_training_performed_in_review"] is False


def test_au_limitations_are_recorded(package):
    assert package["limitations"] == service.LIMITATIONS


def test_av_next_chain_is_defined(package):
    assert package["next_chain"] == service.NEXT_CHAIN


def test_aw_risk_controls_are_defined(package):
    assert package["risk_controls"] == service.RISK_CONTROLS


def test_ax_checklist_passes(package):
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)


def test_ay_review_digest_is_deterministic(package):
    assert service.additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(package) == package["additional_predictive_evidence_results_review_using_redesigned_labels_digest"]


def test_az_validator_accepts_valid_package(package):
    result = service.validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(package)
    assert result["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_VALID"


def test_ba_validator_rejects_wrong_artifact_kind(package):
    _rejected(package, "artifact_kind", "WRONG")


def test_bb_validator_rejects_wrong_status(package):
    _rejected(package, "review_status", "WRONG")


def test_bc_validator_rejects_changed_execution_digest(package):
    _rejected(package, "source_additional_predictive_evidence_execution_digest", "0" * 64)


def test_bd_validator_rejects_changed_matrix_digest(package):
    _rejected(package, "source_feature_label_matrix_digest", "0" * 64)


def test_be_validator_rejects_generated_output_count_mismatch(package):
    _rejected(package, "generated_output_count", 12)


def test_bf_validator_rejects_matrix_row_count_mismatch(package):
    _rejected(package, "feature_label_matrix_row_count", 1)


def test_bg_validator_rejects_leakage_failure(package):
    _rejected(package, "leakage_control_status", "FAIL")


def test_bh_validator_rejects_reassessment_created_true(package):
    _rejected(package, "predictive_usefulness_reassessment_review_created", True)


def test_bi_validator_rejects_predictive_usefulness_accepted(package):
    _rejected(package, "predictive_usefulness", "accepted")


def test_bj_validator_rejects_runtime_authorized(package):
    _rejected(package, "runtime_use", "AUTHORIZED")


def test_bk_validator_rejects_trade_recommendations_true(package):
    _rejected(package, "trade_recommendations_generated", True)


def test_bl_validator_rejects_missing_limitations(package):
    _rejected(package, "limitations", [])


def test_bm_validator_rejects_missing_next_chain(package):
    _rejected(package, "next_chain", [])


def test_bn_markdown_includes_required_sections(package):
    markdown = service.build_additional_predictive_evidence_results_review_using_redesigned_labels_markdown_v1(package)
    for section in (
        "Source Execution", "Dataset and Universe", "Feature / Label Matrix Review",
        "Walk-Forward Review", "OOS Holdout Review", "Output Digest Manifest",
        "Review Interpretation", "Limitations", "Next Chain", "Next Gates",
        "Risk Controls", "Predictive Usefulness Boundary", "Profitability Boundary",
        "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_canonical_package_without_overwrite(package, tmp_path):
    result = service.write_additional_predictive_evidence_results_review_using_redesigned_labels_v1(tmp_path)
    assert Path(result["path"]).is_file()
    with pytest.raises(service.AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError):
        service.write_additional_predictive_evidence_results_review_using_redesigned_labels_v1(tmp_path)
