from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import predictive_usefulness_reassessment_redesigned_evidence_service as service


@pytest.fixture(scope="module")
def reassessment() -> dict:
    return service.build_predictive_usefulness_reassessment_using_redesigned_evidence_v1()


def _rejected(reassessment: dict, field: str, value) -> None:
    changed = deepcopy(reassessment)
    changed[field] = value
    with pytest.raises(service.PredictiveUsefulnessReassessmentRedesignedEvidenceError):
        service.validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(changed)


def test_a_reassessment_builds_offline(reassessment):
    assert reassessment["created_offline"] is True


def test_b_artifact_kind_is_correct(reassessment):
    assert reassessment["artifact_kind"] == service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE


def test_c_reassessment_status_is_correct(reassessment):
    assert reassessment["reassessment_status"] == service.PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY


def test_d_results_review_digest_is_bound(reassessment):
    assert reassessment["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] == service.EXPECTED_RESULTS_REVIEW_DIGEST


def test_e_execution_digest_is_bound(reassessment):
    assert reassessment["additional_predictive_evidence_execution_using_redesigned_labels_digest"] == service.EXPECTED_EXECUTION_DIGEST


def test_f_matrix_digest_is_bound(reassessment):
    assert reassessment["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_g_feature_values_digest_is_bound(reassessment):
    assert reassessment["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_h_label_values_digest_is_bound(reassessment):
    assert reassessment["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_i_research_registry_digest_is_bound(reassessment):
    assert reassessment["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_j_records_digest_is_bound(reassessment):
    assert reassessment["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_k_universe_count_and_order_are_preserved(reassessment):
    assert reassessment["target_universe_count"] == 12
    assert reassessment["target_universe"] == service.EXPECTED_TARGET_UNIVERSE


def test_l_meta_913_is_preserved(reassessment):
    assert reassessment["meta_record_count"] == 913
    assert reassessment["meta_reduced_record_count_preserved"] is True


def test_m_source_results_review_ready_is_true(reassessment):
    assert reassessment["additional_predictive_evidence_results_review_ready"] is True


def test_n_ready_for_reassessment_is_true(reassessment):
    assert reassessment["ready_for_predictive_usefulness_reassessment_using_redesigned_evidence"] is True


def test_o_reassessment_created_and_ready_are_true(reassessment):
    assert reassessment["predictive_usefulness_reassessment_created"] is True
    assert reassessment["predictive_usefulness_reassessment_ready"] is True


def test_p_ready_for_acceptance_readiness_review_is_true(reassessment):
    assert reassessment["ready_for_predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence"] is True


def test_q_acceptance_readiness_review_created_is_false(reassessment):
    assert reassessment["predictive_usefulness_acceptance_readiness_review_created"] is False


def test_r_acceptance_candidate_created_is_false(reassessment):
    assert reassessment["predictive_usefulness_acceptance_candidate_created"] is False


def test_s_predictive_usefulness_is_not_accepted(reassessment):
    assert reassessment["predictive_usefulness"] == "not accepted"


def test_t_profitability_is_not_accepted(reassessment):
    assert reassessment["profitability"] == "not accepted"


def test_u_runtime_is_not_authorized(reassessment):
    assert reassessment["runtime_use"] == "NOT_AUTHORIZED"


def test_v_trade_recommendations_are_false(reassessment):
    assert reassessment["trade_recommendations_generated"] is False


def test_w_oos_cross_sectional_delta_is_preserved(reassessment):
    assert reassessment["oos_cross_sectional_delta_vs_majority"] == "0.00309917"


def test_x_local_model_delta_is_preserved(reassessment):
    assert reassessment["oos_local_model_delta_vs_majority"] == "0.00000000"


def test_y_leakage_pass_is_preserved(reassessment):
    assert reassessment["leakage_control_status"] == "PASS"
    assert reassessment["leakage_failed_control_count"] == 0


def test_z_optional_model_unavailability_is_recorded(reassessment):
    assert reassessment["optional_tree_family_status"] == "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    assert reassessment["optional_ensemble_family_status"] == "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"


def test_aa_domains_are_defined(reassessment):
    assert list(reassessment["reassessment_domains"]) == list(service.DOMAIN_INTERPRETATIONS)
    assert len(reassessment["reassessment_domains"]) == 17


def test_ab_conservative_classification_is_present(reassessment):
    assert reassessment["reassessment_classification"] == "COMPLETED_RESEARCH_ONLY"
    assert reassessment["predictive_signal_classification"] == "WEAK_TO_MODEST_MIXED"


def test_ac_acceptance_recommendation_is_do_not_accept(reassessment):
    assert reassessment["acceptance_recommendation"] == "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE"


def test_ad_per_ticker_entries_count_is_12(reassessment):
    assert len(reassessment["per_ticker_reassessment_entries"]) == 12


def test_ae_per_ticker_digests_are_present(reassessment):
    assert all(len(row["per_ticker_predictive_usefulness_reassessment_digest"]) == 64 for row in reassessment["per_ticker_reassessment_entries"])


def test_af_next_chain_is_defined(reassessment):
    assert reassessment["next_chain"] == service.NEXT_CHAIN


def test_ag_risk_controls_are_defined(reassessment):
    assert reassessment["risk_controls"] == service.RISK_CONTROLS


def test_ah_checklist_passes(reassessment):
    assert reassessment["reassessment_summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert reassessment["reassessment_summary"]["failed_checks"] == 0


def test_ai_reassessment_digest_is_deterministic(reassessment):
    assert service.predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(reassessment) == reassessment["predictive_usefulness_reassessment_using_redesigned_evidence_digest"]


def test_aj_per_ticker_digests_are_deterministic(reassessment):
    for entry in reassessment["per_ticker_reassessment_entries"]:
        assert service.per_ticker_predictive_usefulness_reassessment_using_redesigned_evidence_digest_v1(entry) == entry["per_ticker_predictive_usefulness_reassessment_digest"]


def test_ak_validator_accepts_valid_reassessment(reassessment):
    result = service.validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(reassessment)
    assert result["status"] == "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_VALID"


def test_al_validator_rejects_wrong_artifact_kind(reassessment):
    _rejected(reassessment, "artifact_kind", "WRONG")


def test_am_validator_rejects_wrong_status(reassessment):
    _rejected(reassessment, "reassessment_status", "WRONG")


def test_an_validator_rejects_source_results_review_ready_false(reassessment):
    _rejected(reassessment, "additional_predictive_evidence_results_review_ready", False)


def test_ao_validator_rejects_reassessment_created_false(reassessment):
    _rejected(reassessment, "predictive_usefulness_reassessment_created", False)


def test_ap_validator_rejects_acceptance_readiness_review_created_true(reassessment):
    _rejected(reassessment, "predictive_usefulness_acceptance_readiness_review_created", True)


def test_aq_validator_rejects_acceptance_candidate_true(reassessment):
    _rejected(reassessment, "predictive_usefulness_acceptance_candidate_created", True)


def test_ar_validator_rejects_predictive_usefulness_accepted(reassessment):
    _rejected(reassessment, "predictive_usefulness", "accepted")


def test_as_validator_rejects_runtime_authorized(reassessment):
    _rejected(reassessment, "runtime_use", "AUTHORIZED")


def test_at_validator_rejects_trade_recommendations_true(reassessment):
    _rejected(reassessment, "trade_recommendations_generated", True)


def test_au_validator_rejects_predictive_evidence_rerun_true(reassessment):
    _rejected(reassessment, "predictive_evidence_execution_rerun_performed", True)


def test_av_validator_rejects_metric_recomputation_in_reassessment_true(reassessment):
    _rejected(reassessment, "metric_recomputation_performed_in_reassessment", True)


def test_aw_validator_rejects_model_training_in_reassessment_true(reassessment):
    _rejected(reassessment, "model_training_performed_in_reassessment", True)


def test_ax_validator_rejects_missing_domains(reassessment):
    _rejected(reassessment, "reassessment_domains", {})


def test_ay_validator_rejects_missing_next_chain(reassessment):
    _rejected(reassessment, "next_chain", [])


def test_az_markdown_includes_required_sections(reassessment):
    markdown = service.build_predictive_usefulness_reassessment_using_redesigned_evidence_markdown_v1(reassessment)
    for section in (
        "Predictive Usefulness Reassessment Using Redesigned Evidence", "Source Results Review",
        "Bound Evidence", "Dataset and Universe", "Evidence Summary", "Reassessment Domains",
        "Reassessment Classification", "Per-Ticker Reassessment Entries", "Next Chain",
        "Next Gates", "Risk Controls", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_creates_package_without_overwrite(tmp_path):
    result = service.write_predictive_usefulness_reassessment_using_redesigned_evidence_v1(tmp_path)
    path = Path(result["path"])
    assert path.is_file()
    written = json.loads(path.read_text(encoding="utf-8"))
    assert service.validate_predictive_usefulness_reassessment_using_redesigned_evidence_v1(written)["status"] == "PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_VALID"
    with pytest.raises(service.PredictiveUsefulnessReassessmentRedesignedEvidenceError):
        service.write_predictive_usefulness_reassessment_using_redesigned_evidence_v1(tmp_path)
