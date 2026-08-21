import json
from copy import deepcopy

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    label_objective_target_definition_results_review_redesigned_evidence_service as service,
)


def _common():
    return {
        "output_label": service.OUTPUT_LABEL, "evidence_scope": service.EVIDENCE_SCOPE,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False, "predictive_usefulness": service.NOT_ACCEPTED,
        "profitability": service.NOT_ACCEPTED, "runtime_use": service.NOT_AUTHORIZED,
        "strategy_use": service.NOT_AUTHORIZED, "paper_trading": service.NOT_AUTHORIZED,
        "broker_execution": service.NOT_AUTHORIZED, "trade_recommendations_generated": False,
    }


@pytest.fixture
def output_root(tmp_path):
    root = tmp_path / "execution-output"
    root.mkdir()
    common = _common()
    ticker_rows = [{
        "ticker": ticker, "historical_record_count": count,
        "majority_baseline_accuracy": "0.53099174" if ticker == "META" else "0.58626033",
        "cross_sectional_accuracy": "0.51997245" if ticker == "META" else "0.58935950",
        "local_model_accuracy": "0.53099174" if ticker == "META" else "0.58626033",
    } for ticker, count in service.EXPECTED_RECORD_COUNTS.items()]
    execution_manifest = {
        **common, "artifact_kind": service.SOURCE_EXECUTION_ARTIFACT_KIND,
        "execution_status": service.SOURCE_EXECUTION_STATUS,
        "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": service.EXPECTED_SOURCE_EXECUTION_DIGEST,
        "output_digest_manifest_summary": {"binding_digest": service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST},
        "per_ticker_execution_entries": ticker_rows,
    }
    payloads = {
        "label_objective_target_definition_review_execution_manifest.json": execution_manifest,
        "current_label_family_objective_map.json": {**common, "label_family_objective_map": [{"label_family": f"FAMILY_{i}"} for i in range(10)]},
        "target_definition_vs_majority_structure_report.json": {**common, "majority_structure_risk": "PRESENT_REQUIRES_RESULTS_REVIEW", "majority_class": "FLAT", "majority_class_count": 13600, "evaluated_class_count": 34848},
        "cross_sectional_edge_materiality_report.json": {**common, "cross_sectional_edge_materiality": "SMALL_NOT_ACCEPTANCE_EVIDENCE", "oos_cross_sectional_delta_vs_majority": "0.00309917", "oos_local_model_delta_vs_majority": 0},
        "horizon_noise_review_report.json": {**common, "horizon_noise_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW"},
        "threshold_materiality_review_report.json": {**common, "threshold_materiality_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW"},
        "class_balance_target_distribution_report.json": {**common, "class_balance_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW", "source_label_value_row_count": 143352, "source_available_label_value_count": 142200, "source_unavailable_label_value_count": 1152},
        "per_ticker_target_behavior_report.json": {**common, "per_ticker_execution_entries": ticker_rows},
        "meta_target_behavior_report.json": {**common, "meta_target_behavior_review": {**ticker_rows[4], "execution_note": "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION"}},
        "target_decision_options_report.json": {**common, "decision_options_review": [{"decision_option": f"OPTION_{i}"} for i in range(7)], "diagnostic_question_results": [{"question": f"QUESTION_{i}"} for i in range(10)]},
        "operator_review_summary.json": {**common, "execution_status": service.SOURCE_EXECUTION_STATUS},
    }
    encoded = {name: canonical_json_bytes(payload) for name, payload in payloads.items()}
    entries = [
        ({"filename": name, "digest_kind": service.SELF_REFERENCE_POLICY, "sha256": None}
         if name == "label_objective_target_definition_review_digest_manifest.json"
         else {"filename": name, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(encoded[name])})
        for name in service.OUTPUT_FILENAMES
    ]
    manifest = {
        **common, "output_digest_entries": entries,
        "self_reference_policy": service.SELF_REFERENCE_POLICY,
        "output_manifest_binding_digest": service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "execution_digest": service.EXPECTED_SOURCE_EXECUTION_DIGEST,
    }
    encoded["label_objective_target_definition_review_digest_manifest.json"] = canonical_json_bytes(manifest)
    for name in service.OUTPUT_FILENAMES:
        (root / name).write_bytes(encoded[name])
    return root


@pytest.fixture
def package(output_root):
    return service.build_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
        output_root=output_root)


def _reject(package, field, value):
    changed = deepcopy(package)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError):
        service.validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(changed)


def test_a_results_review_builds_offline(package):
    assert package["created_offline"] is True


def test_b_results_review_blocks_when_output_root_is_missing(tmp_path):
    package = service.build_label_objective_target_definition_results_review_using_redesigned_evidence_v1(output_root=tmp_path / "missing")
    assert package["review_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS
    assert package["label_objective_target_definition_results_review_ready"] is False


def test_c_artifact_kind_is_correct(package):
    assert package["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE


def test_d_review_status_is_correct(package):
    assert package["review_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY


def test_e_source_execution_digest_is_bound(package):
    assert package["source_execution_digest"] == service.EXPECTED_SOURCE_EXECUTION_DIGEST


def test_f_source_output_binding_digest_is_bound(package):
    assert package["source_output_binding_digest"] == service.EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST


def test_g_source_approval_digest_is_bound(package):
    assert package["source_approval_digest"] == service.EXPECTED_SOURCE_APPROVAL_DIGEST


def test_h_candidate_review_digest_is_bound(package):
    assert package["source_evidence"]["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"] == service.execution.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_i_candidate_digest_is_bound(package):
    assert package["source_evidence"]["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] == service.execution.EXPECTED_CANDIDATE_DIGEST


def test_j_path_selection_digest_is_bound(package):
    assert package["source_evidence"]["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == service.execution.EXPECTED_PATH_SELECTION_DIGEST


def test_k_matrix_digest_is_bound(package):
    assert package["source_evidence"]["feature_label_matrix_digest"] == service.execution.EXPECTED_MATRIX_DIGEST


def test_l_feature_values_digest_is_bound(package):
    assert package["source_evidence"]["feature_values_digest"] == service.execution.EXPECTED_FEATURE_VALUES_DIGEST


def test_m_label_values_digest_is_bound(package):
    assert package["source_evidence"]["redesigned_label_values_digest"] == service.execution.EXPECTED_LABEL_VALUES_DIGEST


def test_n_research_registry_digest_is_bound(package):
    assert package["source_evidence"]["research_registry_approval_digest"] == service.execution.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_o_records_digest_is_bound(package):
    assert package["records_digest"] == service.execution.EXPECTED_RECORDS_DIGEST


def test_p_universe_count_and_order_are_preserved(package):
    assert package["target_universe"] == service.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12


def test_q_meta_913_is_preserved(package):
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_r_generated_output_count_is_12(package):
    assert package["generated_output_count"] == 12


def test_s_output_digests_are_bound(package):
    assert len(package["output_verification"]["local_output_hashes"]) == 12


def test_t_output_digest_mismatch_count_is_zero(package):
    assert package["output_verification"]["output_digest_mismatch_count"] == 0


def test_u_outputs_are_research_only_non_actionable(package):
    assert package["output_verification"]["all_outputs_research_only_non_actionable"] is True


def test_v_execution_manifest_is_verified(package):
    assert package["execution_manifest_verified"] is True


def test_w_label_family_objective_map_is_verified(package):
    assert package["label_family_objective_map_verified"] is True


def test_x_majority_structure_report_is_verified(package):
    assert package["majority_structure_report_verified"] is True


def test_y_cross_sectional_edge_report_is_verified(package):
    assert package["cross_sectional_edge_report_verified"] is True


def test_z_horizon_noise_report_is_verified(package):
    assert package["horizon_noise_report_verified"] is True


def test_aa_threshold_materiality_report_is_verified(package):
    assert package["threshold_materiality_report_verified"] is True


def test_ab_class_balance_report_is_verified(package):
    assert package["class_balance_report_verified"] is True


def test_ac_per_ticker_behavior_report_is_verified(package):
    assert package["per_ticker_behavior_report_verified"] is True


def test_ad_meta_behavior_report_is_verified(package):
    assert package["meta_behavior_report_verified"] is True


def test_ae_decision_options_report_is_verified(package):
    assert package["decision_options_report_verified"] is True


def test_af_operator_summary_is_verified(package):
    assert package["operator_summary_verified"] is True


def test_ag_results_review_created_and_ready_are_true(package):
    assert package["label_objective_target_definition_results_review_created"] is True
    assert package["label_objective_target_definition_results_review_ready"] is True


def test_ah_ready_for_optional_redesign_or_refinement_candidate_is_true(package):
    assert package["ready_for_optional_label_objective_redesign_or_threshold_horizon_refinement_candidate_using_redesigned_evidence"] is True


def test_ai_label_regeneration_is_false(package):
    assert package["label_regeneration_authorized"] is False
    assert package["label_regeneration_performed"] is False


def test_aj_new_targets_created_is_false(package):
    assert package["new_targets_created"] is False


def test_ak_target_definition_change_authorized_is_false(package):
    assert package["target_definition_change_authorized"] is False


def test_al_redesign_and_refinement_candidates_are_false(package):
    assert package["label_objective_redesign_candidate_created"] is False
    assert package["threshold_horizon_refinement_candidate_created"] is False


def test_am_predictive_usefulness_remains_not_accepted(package):
    assert package["predictive_usefulness"] == service.NOT_ACCEPTED


def test_an_profitability_remains_not_accepted(package):
    assert package["profitability"] == service.NOT_ACCEPTED


def test_ao_runtime_remains_not_authorized(package):
    assert package["runtime_use"] == service.NOT_AUTHORIZED


def test_ap_trade_recommendations_remain_false(package):
    assert package["trade_recommendations_generated"] is False


def test_aq_majority_structure_risk_is_preserved(package):
    assert package["result_review_classification"]["majority_structure_review"] == "PRESENT_REQUIRES_OPERATOR_REVIEW"


def test_ar_small_cross_sectional_edge_is_preserved(package):
    assert package["result_review_classification"]["cross_sectional_edge_materiality_review"] == "SMALL_NOT_ACCEPTANCE_EVIDENCE"


def test_as_local_model_equivalence_is_preserved(package):
    assert package["result_review_classification"]["local_model_equivalence_review"] == "MATCHES_MAJORITY_BASELINE"


def test_at_meta_limitation_is_preserved(package):
    meta = package["per_ticker_results_review_entries"][4]
    assert meta["review_note"] == "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW"


def test_au_per_ticker_entries_count_is_12(package):
    assert len(package["per_ticker_results_review_entries"]) == 12


def test_av_per_ticker_digests_are_present(package):
    assert all(len(row["per_ticker_label_objective_target_definition_results_review_digest"]) == 64 for row in package["per_ticker_results_review_entries"])


def test_aw_no_review_execution_rerun_in_results_review(package):
    assert package["label_objective_target_definition_review_execution_rerun_performed"] is False


def test_ax_no_metric_recomputation_in_review(package):
    assert package["metric_recomputation_performed_in_review"] is False


def test_ay_no_model_training_in_review(package):
    assert package["model_training_performed_in_review"] is False


def test_az_limitations_are_recorded(package):
    assert package["limitations"] == service.LIMITATIONS


def test_ba_next_chain_is_defined(package):
    assert package["next_chain"] == service.NEXT_CHAIN


def test_bb_risk_controls_are_defined(package):
    assert package["risk_controls"] == service.RISK_CONTROLS


def test_bc_checklist_passes(package):
    assert package["checklist_summary"]["total_checks"] == 78
    assert package["checklist_summary"]["passed_checks"] == 78
    assert package["checklist_summary"]["failed_checks"] == 0


def test_bd_review_digest_is_deterministic(package):
    first = service.label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(package)
    second = service.label_objective_target_definition_results_review_using_redesigned_evidence_digest_v1(deepcopy(package))
    assert first == second == package["label_objective_target_definition_results_review_using_redesigned_evidence_digest"]


def test_be_validator_accepts_valid_package(package):
    validation = service.validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(package)
    assert validation["status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID


def test_bf_validator_rejects_wrong_artifact_kind(package):
    _reject(package, "artifact_kind", "WRONG")


def test_bg_validator_rejects_wrong_status(package):
    _reject(package, "review_status", "WRONG")


def test_bh_validator_rejects_changed_execution_digest(package):
    _reject(package, "source_execution_digest", "0" * 64)


def test_bi_validator_rejects_output_mismatch_count_nonzero(package):
    changed = deepcopy(package)
    changed["output_verification"]["output_digest_mismatch_count"] = 1
    with pytest.raises(service.LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError):
        service.validate_label_objective_target_definition_results_review_using_redesigned_evidence_v1(changed)


def test_bj_validator_rejects_label_regeneration_true(package):
    _reject(package, "label_regeneration_performed", True)


def test_bk_validator_rejects_new_targets_true(package):
    _reject(package, "new_targets_created", True)


def test_bl_validator_rejects_target_definition_change_authorized_true(package):
    _reject(package, "target_definition_change_authorized", True)


def test_bm_validator_rejects_redesign_candidate_true(package):
    _reject(package, "label_objective_redesign_candidate_created", True)


def test_bn_validator_rejects_predictive_usefulness_accepted(package):
    _reject(package, "predictive_usefulness", "accepted")


def test_bo_validator_rejects_runtime_authorized(package):
    _reject(package, "runtime_use", "AUTHORIZED")


def test_bp_validator_rejects_trade_recommendations_true(package):
    _reject(package, "trade_recommendations_generated", True)


def test_bq_validator_rejects_missing_limitations(package):
    _reject(package, "limitations", [])


def test_br_validator_rejects_missing_next_chain(package):
    _reject(package, "next_chain", [])


def test_bs_markdown_includes_required_sections(package):
    markdown = service.build_label_objective_target_definition_results_review_using_redesigned_evidence_markdown_v1(package)
    sections = (
        "## Title", "## Label Objective / Target Definition Results Review Using Redesigned Evidence",
        "## Source Execution", "## Bound Evidence", "## Dataset and Universe", "## Output Verification",
        "## Reviewed Problem Basis", "## Label Family Objective Map Review", "## Majority Structure Review",
        "## Cross-Sectional Edge Materiality Review", "## Horizon and Threshold Review",
        "## Class Balance and Target Distribution Review", "## Per-Ticker Target Behavior Review",
        "## META Target Behavior Review", "## Decision Options Review", "## Review Classification",
        "## Limitations", "## Next Chain", "## Next Gates", "## Risk Controls",
        "## Predictive Usefulness Boundary", "## Profitability Boundary", "## Runtime Boundary",
        "## Checklist Summary", "## Guardrails",
    )
    assert all(section in markdown for section in sections)


def test_bt_writer_creates_canonical_package_without_overwrite(package, output_root, tmp_path):
    destination = tmp_path / "review-package"
    receipt = service.write_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
        destination, output_root=output_root)
    assert len(receipt["payload_sha256"]) == 64
    with pytest.raises(service.LabelObjectiveTargetDefinitionResultsReviewRedesignedEvidenceError):
        service.write_label_objective_target_definition_results_review_using_redesigned_evidence_v1(
            destination, output_root=output_root)
