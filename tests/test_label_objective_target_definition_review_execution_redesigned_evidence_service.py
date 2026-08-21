import json
from copy import deepcopy

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    label_objective_target_definition_review_execution_redesigned_evidence_service as service,
)


FIXED_TIMESTAMP = "2026-08-21T12:00:00Z"


def _write_json(path, payload):
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


@pytest.fixture
def source_bundle(tmp_path, monkeypatch):
    roots = {name: tmp_path / name for name in ("canonical", "label", "feature", "predictive")}
    for root in roots.values():
        root.mkdir()
    raw_files = {
        "canonical": (roots["canonical"] / "canonical_dataset_records.jsonl", b"canonical-records\n"),
        "labels": (roots["label"] / "redesigned_label_values.jsonl", b"redesigned-labels\n"),
        "features": (roots["feature"] / "feature_values.jsonl", b"feature-values\n"),
        "matrix": (roots["predictive"] / "feature_label_matrix.jsonl", b"feature-label-matrix\n"),
    }
    for path, data in raw_files.values():
        path.write_bytes(data)
    monkeypatch.setattr(service, "EXPECTED_RECORDS_DIGEST", sha256_file(raw_files["canonical"][0]))
    monkeypatch.setattr(service, "EXPECTED_LABEL_VALUES_DIGEST", sha256_file(raw_files["labels"][0]))
    monkeypatch.setattr(service, "EXPECTED_FEATURE_VALUES_DIGEST", sha256_file(raw_files["features"][0]))
    monkeypatch.setattr(service, "EXPECTED_MATRIX_DIGEST", sha256_file(raw_files["matrix"][0]))
    common = {"dataset_name": service.DATASET_NAME, "records_digest": service.EXPECTED_RECORDS_DIGEST}
    label_summary = [{
        "ticker": ticker, "historical_record_count": count,
        "available_label_value_count": count * 12 - 96,
        "unavailable_label_value_count": 96,
    } for ticker, count in service.EXPECTED_RECORD_COUNTS.items()]
    metrics = {
        "BASELINE_MAJORITY_CLASS": {"accuracy": "0.58626033"},
        "BASELINE_TICKER_CROSS_SECTIONAL": {"accuracy": "0.58935950"},
        "MODEL_FAMILY_REGULARIZED_LINEAR": {"accuracy": "0.58626033"},
    }
    reports = {
        roots["label"] / "redesigned_label_family_coverage_report.json": {
            **common, "label_family_count": 10, "label_families": list(service.LABEL_FAMILIES),
        },
        roots["label"] / "redesigned_threshold_generation_report.json": {
            **common, "threshold_strategies": ["global", "per_ticker"],
            "global_threshold_5_session": "0.026556108631",
            "benchmark_relative_threshold_5_session": "0.02058653801",
        },
        roots["label"] / "redesigned_horizon_generation_report.json": {
            **common, "horizon_strategies": ["one", "five", "ten", "twenty"],
            "multi_horizon_values": [5, 10, 20], "horizon_label_row_counts": {"1": 11946},
        },
        roots["label"] / "redesigned_label_availability_report.json": {
            **common, "label_value_row_count": 143352,
            "available_label_value_count": 142200, "unavailable_label_value_count": 1152,
        },
        roots["label"] / "per_ticker_redesigned_label_summary.json": {
            **common, "per_ticker_label_summary": label_summary,
        },
        roots["predictive"] / "baseline_model_comparison_results.json": {
            **common, "oos_method_metrics": metrics,
        },
        roots["predictive"] / "metric_family_results.json": {
            **common,
            "baseline_outperformance_delta": {
                "BASELINE_MAJORITY_CLASS": "0.00000000",
                "BASELINE_TICKER_CROSS_SECTIONAL": "0.00309917",
                "MODEL_FAMILY_REGULARIZED_LINEAR": "0.00000000",
            },
            "class_balance": {"FLAT": 13600, "UP": 6227, "DOWN": 4336},
        },
        roots["predictive"] / "calibration_stability_report.json": {
            **common, "calibration_status": "RESEARCH_ONLY_HARD_CLASS_CALIBRATION_SUMMARY",
        },
        roots["predictive"] / "per_ticker_cross_sectional_review.json": {
            **common, "per_ticker_entries": [{
                "ticker": ticker, "oos_method_metrics": metrics,
            } for ticker in service.TARGET_UNIVERSE],
        },
    }
    for path, payload in reports.items():
        _write_json(path, payload)
    return {**roots, "output": tmp_path / "output", "raw_files": raw_files}


@pytest.fixture
def artifact(source_bundle):
    return service.execute_label_objective_target_definition_review_using_redesigned_evidence_v1(
        canonical_root=source_bundle["canonical"], label_root=source_bundle["label"],
        feature_root=source_bundle["feature"], predictive_evidence_root=source_bundle["predictive"],
        output_root=source_bundle["output"], run_timestamp_utc=FIXED_TIMESTAMP,
    )


def _reject(artifact, field, value):
    changed = deepcopy(artifact)
    changed[field] = value
    with pytest.raises(service.LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError):
        service.validate_label_objective_target_definition_review_executed_using_redesigned_evidence_v1(changed)


def test_a_execution_builds_offline(artifact):
    assert artifact["created_offline"] is True


def test_b_execution_blocks_if_required_source_root_is_missing(tmp_path):
    artifact = service.execute_label_objective_target_definition_review_using_redesigned_evidence_v1(
        canonical_root=tmp_path / "missing-canonical", label_root=tmp_path / "missing-label",
        feature_root=tmp_path / "missing-feature", predictive_evidence_root=tmp_path / "missing-predictive",
        output_root=tmp_path / "output", run_timestamp_utc=FIXED_TIMESTAMP)
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "output").exists()


def test_c_artifact_kind_is_correct(artifact):
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE


def test_d_execution_status_is_correct(artifact):
    assert artifact["execution_status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY


def test_e_approval_digest_is_bound(artifact):
    assert artifact["source_evidence"]["label_objective_target_definition_review_approval_using_redesigned_evidence_digest"] == service.EXPECTED_APPROVAL_DIGEST


def test_f_candidate_review_digest_is_bound(artifact):
    assert artifact["source_evidence"]["label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_g_candidate_digest_is_bound(artifact):
    assert artifact["source_evidence"]["label_objective_target_definition_review_candidate_using_redesigned_evidence_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_h_path_selection_digest_is_bound(artifact):
    assert artifact["source_evidence"]["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"] == service.EXPECTED_PATH_SELECTION_DIGEST


def test_i_readiness_digest_is_bound(artifact):
    assert artifact["source_evidence"]["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"] == service.EXPECTED_READINESS_REVIEW_DIGEST


def test_j_matrix_digest_is_bound(artifact):
    assert artifact["source_evidence"]["feature_label_matrix_digest"] == service.EXPECTED_MATRIX_DIGEST


def test_k_feature_values_digest_is_bound(artifact):
    assert artifact["source_evidence"]["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_l_label_values_digest_is_bound(artifact):
    assert artifact["source_evidence"]["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_m_research_registry_digest_is_bound(artifact):
    assert artifact["source_evidence"]["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_DIGEST


def test_n_records_digest_is_bound(artifact):
    assert artifact["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_o_universe_count_and_order_are_preserved(artifact):
    assert artifact["target_universe"] == service.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12


def test_p_meta_913_is_preserved(artifact):
    assert artifact["meta_record_count"] == 913
    assert artifact["meta_reduced_record_count_preserved"] is True


def test_q_review_approved_authorized_and_ready_are_true(artifact):
    assert artifact["label_objective_target_definition_review_approved"] is True
    assert artifact["label_objective_target_definition_review_authorized"] is True
    assert artifact["ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence"] is True


def test_r_review_executed_and_results_created_are_true(artifact):
    assert artifact["label_objective_target_definition_review_executed"] is True
    assert artifact["label_objective_target_definition_review_results_created"] is True


def test_s_generated_output_count_is_12(artifact, source_bundle):
    assert artifact["generated_output_count"] == 12
    assert len(list(source_bundle["output"].iterdir())) == 12


def test_t_review_dimensions_count_is_12(artifact):
    assert artifact["review_dimension_count"] == len(artifact["review_dimensions"]) == 12


def test_u_label_family_review_count_is_10(artifact):
    assert artifact["label_family_review_count"] == len(artifact["label_family_objective_map"]) == 10


def test_v_diagnostic_question_count_is_10(artifact):
    assert artifact["diagnostic_question_count"] == len(artifact["diagnostic_question_results"]) == 10


def test_w_decision_option_count_is_7(artifact):
    assert artifact["decision_option_count"] == len(artifact["decision_options_review"]) == 7


def test_x_label_regeneration_is_false(artifact):
    assert artifact["label_regeneration_authorized"] is False
    assert artifact["label_regeneration_performed"] is False


def test_y_new_targets_created_is_false(artifact):
    assert artifact["new_targets_created"] is False


def test_z_target_definition_change_authorized_is_false(artifact):
    assert artifact["target_definition_change_authorized"] is False


def test_aa_target_definition_change_performed_is_false(artifact):
    assert artifact["target_definition_change_performed"] is False


def test_ab_no_redesign_or_refinement_candidate_is_created(artifact):
    assert artifact["label_objective_redesign_candidate_created"] is False
    assert artifact["threshold_horizon_refinement_candidate_created"] is False


def test_ac_predictive_usefulness_is_not_accepted(artifact):
    assert artifact["predictive_usefulness"] == "not accepted"


def test_ad_profitability_is_not_accepted(artifact):
    assert artifact["profitability"] == "not accepted"


def test_ae_runtime_is_not_authorized(artifact):
    assert artifact["runtime_use"] == "NOT_AUTHORIZED"


def test_af_trade_recommendations_are_false(artifact):
    assert artifact["trade_recommendations_generated"] is False


def test_ag_review_result_classification_is_conservative(artifact):
    assert artifact["review_result_classification"]["cross_sectional_edge_materiality"] == "SMALL_NOT_ACCEPTANCE_EVIDENCE"


def test_ah_decision_recommendation_does_not_authorize_target_change(artifact):
    assert artifact["review_result_classification"]["target_decision_recommendation"] == "NO_TARGET_CHANGE_AUTHORIZED_BY_THIS_EXECUTION"


def test_ai_per_ticker_execution_entries_count_is_12(artifact):
    assert len(artifact["per_ticker_execution_entries"]) == 12


def test_aj_per_ticker_execution_digests_are_present(artifact):
    assert all(len(row["per_ticker_label_objective_target_definition_review_execution_digest"]) == 64 for row in artifact["per_ticker_execution_entries"])


def test_ak_output_digest_manifest_is_created(artifact, source_bundle):
    path = source_bundle["output"] / "label_objective_target_definition_review_digest_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert len(manifest["output_digest_entries"]) == 12
    assert manifest["self_reference_policy"] == service.SELF_REFERENCE_POLICY


def test_al_source_hashes_remain_bound(artifact, source_bundle):
    assert artifact["source_verification"]["source_files_unchanged"] is True
    assert sha256_file(source_bundle["raw_files"]["matrix"][0]) == service.EXPECTED_MATRIX_DIGEST


def test_am_validator_accepts_valid_artifact(artifact):
    validation = service.validate_label_objective_target_definition_review_executed_using_redesigned_evidence_v1(artifact)
    assert validation["status"] == service.LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID


def test_an_validator_rejects_wrong_artifact_kind(artifact):
    _reject(artifact, "artifact_kind", "WRONG")


def test_ao_validator_rejects_wrong_execution_status(artifact):
    _reject(artifact, "execution_status", "WRONG")


def test_ap_validator_rejects_approval_false(artifact):
    _reject(artifact, "label_objective_target_definition_review_approved", False)


def test_aq_validator_rejects_review_executed_false(artifact):
    _reject(artifact, "label_objective_target_definition_review_executed", False)


def test_ar_validator_rejects_label_regeneration_true(artifact):
    _reject(artifact, "label_regeneration_performed", True)


def test_as_validator_rejects_new_targets_true(artifact):
    _reject(artifact, "new_targets_created", True)


def test_at_validator_rejects_target_definition_change_authorized_true(artifact):
    _reject(artifact, "target_definition_change_authorized", True)


def test_au_validator_rejects_predictive_usefulness_accepted(artifact):
    _reject(artifact, "predictive_usefulness", "accepted")


def test_av_validator_rejects_runtime_authorized(artifact):
    _reject(artifact, "runtime_use", "AUTHORIZED")


def test_aw_validator_rejects_trade_recommendations_true(artifact):
    _reject(artifact, "trade_recommendations_generated", True)


def test_ax_validator_rejects_predictive_evidence_rerun_true(artifact):
    _reject(artifact, "predictive_evidence_execution_rerun_performed", True)


def test_ay_validator_rejects_metric_recomputation_true(artifact):
    _reject(artifact, "metric_recomputation_performed_in_execution", True)


def test_az_validator_rejects_model_training_true(artifact):
    _reject(artifact, "model_training_performed_in_execution", True)


def test_ba_execution_digest_is_deterministic_for_fixed_timestamp_and_source(artifact):
    first = service.label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(artifact)
    second = service.label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(deepcopy(artifact))
    assert first == second == artifact["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"]


def test_bb_markdown_includes_required_sections(artifact):
    markdown = service.build_label_objective_target_definition_review_execution_status_markdown_v1(artifact)
    sections = (
        "## Title", "## Label Objective / Target Definition Review Execution Using Redesigned Evidence",
        "## Source Approval", "## Bound Evidence", "## Dataset and Universe",
        "## Review Execution Policy", "## Reviewed Problem Basis", "## Review Dimensions",
        "## Label Family Objective Map", "## Majority Structure Review",
        "## Cross-Sectional Edge Materiality Review", "## Horizon and Threshold Review",
        "## Class Balance and Target Distribution Review", "## Per-Ticker Target Behavior Review",
        "## META Target Behavior Review", "## Decision Options Review", "## Output Digest Manifest",
        "## Authority Boundary", "## Predictive Usefulness Boundary", "## Profitability Boundary",
        "## Runtime Boundary", "## Checklist Summary", "## Guardrails",
    )
    assert all(section in markdown for section in sections)
