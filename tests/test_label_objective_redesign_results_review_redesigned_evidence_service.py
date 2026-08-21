from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import label_objective_redesign_execution_redesigned_evidence_service as execution
from marketflow.services import label_objective_redesign_results_review_redesigned_evidence_service as review


def _common() -> dict:
    return {
        "output_label": execution.OUTPUT_LABEL,
        "evidence_scope": execution.EVIDENCE_SCOPE,
        "dataset_name": execution.DATASET_NAME,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "trade_recommendations_generated": False,
        "research_only": True,
        "non_actionable": True,
    }


def _write_output_fixture(output_root) -> None:
    common = _common()
    per_ticker = [
        {"ticker": ticker, "historical_record_count": execution.EXPECTED_RECORD_COUNTS[ticker]}
        for ticker in execution.TARGET_UNIVERSE
    ]
    payloads = {
        "label_objective_redesign_execution_manifest.json": {
            **common,
            "artifact_kind": execution.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE,
            "execution_status": execution.LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
            "label_objective_redesign_execution_using_redesigned_evidence_digest": review.EXPECTED_EXECUTION_DIGEST,
            "output_digest_manifest_summary": {"binding_digest": review.EXPECTED_OUTPUT_BINDING_DIGEST},
            "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
            "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
            "target_universe": list(execution.TARGET_UNIVERSE), "target_universe_count": 12,
            "total_canonical_record_count": 11946, "meta_record_count": 913,
            "non_meta_record_count": 1003, "meta_reduced_record_count_preserved": True,
            "generated_output_count": 12, "generated_output_names": list(execution.OUTPUT_FILENAMES),
            "redesign_theme_count": 11, "redesign_option_count": 8,
            "label_family_impact_review_count": 10, "redesign_question_count": 10,
            "per_ticker_execution_entries": per_ticker,
        },
        "flat_class_and_majority_structure_redesign_report.json": {
            **common, "largest_aggregated_class": "FLAT", "largest_aggregated_class_count": 13600,
            "oos_evaluated_rows": 34848, "majority_accuracy": "0.58626033",
            "local_model_accuracy": "0.58626033",
        },
        "no_trade_abstain_objective_report.json": {
            **common, "flat_count": 13600, "no_trade_count": 1540,
            "selected_direction": execution.SELECTED_DIRECTION,
        },
        "material_move_target_definition_report.json": {
            **common, "source_global_threshold_5_session": "0.026556108631",
            "source_benchmark_relative_threshold_5_session": "0.02058653801",
            "new_target_definition_created": False,
        },
        "horizon_specific_target_design_report.json": {
            **common, "source_horizon_strategies": ["one", "five", "ten", "twenty", "multi"],
            "source_multi_horizon_values": [5, 10, 20],
        },
        "ticker_or_regime_split_target_report.json": {
            **common, "per_ticker_review_count": 12, "split_target_created": False,
            "regime_target_created": False,
        },
        "risk_adjusted_target_definition_report.json": {
            **common, "reviewed_families": [
                "volatility_adjusted_return", "drawdown_avoidance", "asymmetric_risk_reward"
            ], "risk_adjusted_target_created": False,
        },
        "label_family_impact_review_report.json": {
            **common, "label_family_impact_review_count": 10,
            "label_family_impact_review": [
                {"label_family": family, "regeneration_performed": False}
                for family in execution.LABEL_FAMILIES
            ],
        },
        "meta_target_limitation_review_report.json": {
            **common, "historical_record_count": 913, "meta_reduced_record_count_flag": True,
            "repair_or_inference_performed": False,
        },
        "acceptance_threshold_prerequisite_report.json": {
            **common, "cross_sectional_accuracy": "0.58935950",
            "cross_sectional_delta_vs_majority": "0.00309917",
            "cross_sectional_edge_materiality": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
            "acceptance_ready": False,
        },
        "operator_review_summary.json": {
            **common,
            "execution_status": execution.LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
            "next_task": "Optional Label Objective Redesign Results Review Using Redesigned Evidence v1",
        },
    }
    payload_bytes = {name: canonical_json_bytes(payload) for name, payload in payloads.items()}
    entries = [
        {"filename": name, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(payload_bytes[name])}
        for name in execution.OUTPUT_FILENAMES[:-1]
    ]
    entries.append({
        "filename": execution.OUTPUT_FILENAMES[-1],
        "digest_kind": execution.SELF_REFERENCE_POLICY,
        "sha256": None,
    })
    payloads["label_objective_redesign_digest_manifest.json"] = {
        **common, "output_digest_entries": entries,
        "self_reference_policy": execution.SELF_REFERENCE_POLICY,
        "output_manifest_binding_digest": review.EXPECTED_OUTPUT_BINDING_DIGEST,
        "execution_digest": review.EXPECTED_EXECUTION_DIGEST,
    }
    output_root.mkdir(parents=True)
    for filename in execution.OUTPUT_FILENAMES:
        (output_root / filename).write_bytes(canonical_json_bytes(payloads[filename]))


def _build(monkeypatch: pytest.MonkeyPatch, output_root) -> dict:
    monkeypatch.setattr(
        execution,
        "validate_label_objective_redesign_executed_using_redesigned_evidence_v1",
        lambda _artifact: {"status": "VALID"},
    )
    return review.build_label_objective_redesign_results_review_using_redesigned_evidence_v1(
        output_root=output_root
    )


@pytest.fixture
def reviewed(tmp_path, monkeypatch: pytest.MonkeyPatch):
    output_root = tmp_path / "outputs"
    _write_output_fixture(output_root)
    return _build(monkeypatch, output_root), output_root


def test_results_review_builds_offline(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    output_root = tmp_path / "outputs"
    _write_output_fixture(output_root)
    package = _build(monkeypatch, output_root)
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_results_review_blocks_when_output_root_is_missing(tmp_path) -> None:
    package = review.build_label_objective_redesign_results_review_using_redesigned_evidence_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS"
    )
    assert package["output_file_inspection_performed"] is False
    assert package["label_objective_redesign_results_review_ready"] is False
    assert package["ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"] is False
    assert package["blocker_count"] == 12


def test_artifact_kind_schema_and_status_are_exact(reviewed) -> None:
    package, _ = reviewed
    assert package["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE"
    assert package["schema_version"] == "label_objective_redesign_results_review_using_redesigned_evidence_v1"
    assert package["review_status"] == "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY"


@pytest.mark.parametrize(("field", "expected"), list(review._source_evidence().items()))
def test_all_source_evidence_is_bound(reviewed, field: str, expected: str) -> None:
    package, _ = reviewed
    assert package["source_evidence"][field] == expected


def test_source_execution_output_binding_and_approval_digests_are_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["source_execution_digest"] == review.EXPECTED_EXECUTION_DIGEST
    assert package["source_output_binding_digest"] == review.EXPECTED_OUTPUT_BINDING_DIGEST
    assert package["source_approval_digest"] == review.EXPECTED_APPROVAL_DIGEST


def test_dataset_universe_and_meta_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["target_universe"] == execution.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_selected_direction_is_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["selected_label_objective_redesign_direction"] == execution.SELECTED_DIRECTION


def test_all_outputs_are_bound_and_verified(reviewed) -> None:
    package, _ = reviewed
    assert package["expected_output_count"] == 12
    assert package["observed_output_count"] == 12
    assert package["generated_output_count"] == 12
    assert package["generated_output_names"] == execution.OUTPUT_FILENAMES
    assert len(package["local_output_hashes"]) == 12
    assert package["output_digest_mismatch_count"] == 0
    assert package["non_self_output_digest_match_count"] == 11
    assert package["digest_manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert package["outputs_research_only_non_actionable"] is True


@pytest.mark.parametrize(
    "field",
    [
        "redesign_execution_manifest_review", "flat_class_majority_structure_review",
        "no_trade_abstain_objective_review", "material_move_target_definition_review",
        "horizon_specific_target_review", "ticker_or_regime_split_target_review",
        "risk_adjusted_target_review", "label_family_impact_results_review",
        "meta_target_limitation_results_review", "acceptance_threshold_prerequisite_results_review",
        "operator_summary_review",
    ],
)
def test_each_required_output_review_is_verified(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field]["available"] is True
    assert package[field]["verified"] is True


def test_results_review_created_ready_and_future_candidate_ready_are_true(reviewed) -> None:
    package, _ = reviewed
    assert package["label_objective_redesign_results_review_created"] is True
    assert package["label_objective_redesign_results_review_ready"] is True
    assert package["ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"] is True


@pytest.mark.parametrize(
    "field",
    [
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "threshold_horizon_refinement_candidate_created", "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "label_objective_redesign_execution_rerun_performed", "metric_recomputation_performed_in_review",
        "model_training_performed_in_review",
    ],
)
def test_closed_authority_and_rerun_fields_remain_false(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_remain_not_authorized(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] == "NOT_AUTHORIZED"


def test_predictive_usefulness_and_profitability_are_not_accepted(reviewed) -> None:
    package, _ = reviewed
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"


def test_review_facts_are_preserved(reviewed) -> None:
    package, _ = reviewed
    flat = package["flat_class_majority_structure_review"]
    assert flat["largest_aggregated_class"] == "FLAT"
    assert flat["largest_aggregated_class_count"] == 13600
    assert flat["oos_evaluated_rows"] == 34848
    assert flat["majority_accuracy"] == flat["local_model_accuracy"] == "0.58626033"
    assert package["no_trade_abstain_objective_review"]["no_trade_count"] == 1540
    threshold = package["acceptance_threshold_prerequisite_results_review"]
    assert threshold["cross_sectional_delta_vs_majority"] == "0.00309917"
    assert threshold["cross_sectional_edge_materiality"] == "SMALL_NOT_ACCEPTANCE_EVIDENCE"


def test_review_classification_is_conservative(reviewed) -> None:
    package, _ = reviewed
    classification = package["review_classification"]
    assert classification["results_review_classification"] == "COMPLETED_RESEARCH_ONLY"
    assert classification["selected_direction_analysis_status"] == "REVIEWED_RESEARCH_ONLY"
    assert classification["redesign_decision_review"] == "NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED"
    assert classification["improved_evidence_planning_candidate_readiness"] == (
        "OPTIONAL_FUTURE_CANDIDATE_REQUIRES_OPERATOR_SELECTION"
    )


def test_meta_limitation_is_preserved(reviewed) -> None:
    package, _ = reviewed
    meta = package["meta_target_limitation_results_review"]
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["repair_or_inference_performed"] is False


def test_per_ticker_entries_and_digests_are_complete(reviewed) -> None:
    package, _ = reviewed
    rows = package["per_ticker_results_review_entries"]
    assert [row["ticker"] for row in rows] == execution.TARGET_UNIVERSE
    assert len(rows) == 12
    assert all(len(row["per_ticker_label_objective_redesign_results_review_digest"]) == 64 for row in rows)
    assert rows[4]["review_note"] == "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW"


def test_limitations_next_chain_gates_and_controls_are_exact(reviewed) -> None:
    package, _ = reviewed
    assert package["limitations"] == review.LIMITATIONS
    assert package["next_chain"] == review.NEXT_CHAIN
    assert package["next_gates"] == review.NEXT_GATES
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_checklist_passes(reviewed) -> None:
    package, _ = reviewed
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in package["review_checklist"])
    assert package["review_summary"] == {
        "total_checks": 84, "passed_checks": 84, "failed_checks": 0, "blocker_count": 0,
        "results_review_ready": True,
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence": True,
        "label_regeneration_performed": False, "new_targets_created": False,
        "target_definition_change_authorized": False,
        "improved_evidence_planning_candidate_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False, "trade_recommendations_generated": False,
    }


def test_review_digest_is_deterministic_and_output_location_independent(tmp_path, monkeypatch) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    _write_output_fixture(first_root)
    _write_output_fixture(second_root)
    first = _build(monkeypatch, first_root)
    second = _build(monkeypatch, second_root)
    assert first["label_objective_redesign_results_review_using_redesigned_evidence_digest"] == second[
        "label_objective_redesign_results_review_using_redesigned_evidence_digest"
    ]


def test_validator_accepts_valid_package(reviewed) -> None:
    package, _ = reviewed
    result = review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1(package)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_USING_REDESIGNED_EVIDENCE_VALID"


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"),
        ("source_execution_digest", "0" * 64), ("source_output_binding_digest", "0" * 64),
        ("source_approval_digest", "0" * 64),
        ("selected_label_objective_redesign_direction", "WRONG"),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))), ("target_universe_count", 11),
        ("records_digest", "0" * 64), ("meta_record_count", 1003),
        ("generated_output_count", 11), ("output_digest_mismatch_count", 1),
        ("label_objective_redesign_results_review_ready", False),
        ("label_regeneration_authorized", True), ("label_regeneration_performed", True),
        ("new_targets_created", True), ("target_definition_change_authorized", True),
        ("target_definition_change_performed", True),
        ("improved_evidence_planning_candidate_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True), ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("label_objective_redesign_execution_rerun_performed", True),
        ("metric_recomputation_performed_in_review", True),
        ("model_training_performed_in_review", True),
    ],
)
def test_validator_rejects_invalid_contract_fields(reviewed, field: str, bad_value) -> None:
    package, _ = reviewed
    invalid = deepcopy(package)
    invalid[field] = bad_value
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewRedesignedEvidenceError):
        review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1(invalid)


@pytest.mark.parametrize("field", ["limitations", "next_chain", "risk_controls"])
def test_validator_rejects_missing_governance_sections(reviewed, field: str) -> None:
    package, _ = reviewed
    invalid = deepcopy(package)
    invalid.pop(field)
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewRedesignedEvidenceError):
        review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_review_digest(reviewed) -> None:
    package, _ = reviewed
    invalid = deepcopy(package)
    invalid.pop("label_objective_redesign_results_review_using_redesigned_evidence_digest")
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewRedesignedEvidenceError):
        review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(reviewed) -> None:
    package, _ = reviewed
    invalid = deepcopy(package)
    invalid["per_ticker_results_review_entries"][0].pop(
        "per_ticker_label_objective_redesign_results_review_digest"
    )
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewRedesignedEvidenceError):
        review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1(invalid)


def test_markdown_includes_required_sections(reviewed) -> None:
    package, _ = reviewed
    markdown = review.build_label_objective_redesign_results_review_using_redesigned_evidence_markdown_v1(package)
    headings = [
        "Title", "Optional Label Objective Redesign Results Review Using Redesigned Evidence",
        "Source Execution", "Bound Evidence", "Dataset and Universe", "Output Verification",
        "Selected Redesign Direction", "FLAT Class and Majority Structure Review",
        "No-Trade / Abstain Objective Review", "Material-Move Target Definition Review",
        "Horizon-Specific Target Review", "Ticker or Regime Split Target Review",
        "Risk-Adjusted Target Review", "Label Family Impact Review", "META Target Limitation Review",
        "Acceptance Threshold Prerequisite Review", "Review Classification", "Limitations",
        "Next Chain", "Next Gates", "Risk Controls", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in headings)


def test_writer_round_trip_and_no_overwrite(reviewed, tmp_path, monkeypatch) -> None:
    package, output_root = reviewed
    monkeypatch.setattr(
        execution,
        "validate_label_objective_redesign_executed_using_redesigned_evidence_v1",
        lambda _artifact: {"status": "VALID"},
    )
    receipt = review.write_label_objective_redesign_results_review_using_redesigned_evidence_v1(
        tmp_path / "review", output_root=output_root
    )
    written = json.loads((tmp_path / "review" / receipt["filename"]).read_text(encoding="utf-8"))
    assert written == package
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewRedesignedEvidenceError):
        review.write_label_objective_redesign_results_review_using_redesigned_evidence_v1(
            tmp_path / "review", output_root=output_root
        )


def test_public_exports_are_available() -> None:
    import marketflow.services as services

    assert services.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE == (
        review.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE
    )
    assert services.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY == (
        review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY
    )
    assert services.build_label_objective_redesign_results_review_using_redesigned_evidence_v1 is (
        review.build_label_objective_redesign_results_review_using_redesigned_evidence_v1
    )
    assert services.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1 is (
        review.validate_label_objective_redesign_results_review_using_redesigned_evidence_v1
    )
    assert services.write_label_objective_redesign_results_review_using_redesigned_evidence_v1 is (
        review.write_label_objective_redesign_results_review_using_redesigned_evidence_v1
    )
