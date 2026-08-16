from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    additional_predictive_evidence_execution_for_refined_evidence_service as execution,
)


FIXED_TIMESTAMP = "2026-08-16T16:00:00Z"


def _source_reports() -> dict:
    model_metrics = {
        name: {"accuracy": accuracy, "evaluated_count": 2988}
        for name, accuracy in (
            ("majority_class_baseline", "0.480924"),
            ("previous_direction_baseline", "0.404953"),
            ("zero_return_baseline", "0.119813"),
            ("ticker_cross_sectional_baseline", "0.396252"),
            ("refined_relative_strength_signal", "0.396252"),
            ("refined_vpa_signal", "0.233266"),
            ("refined_combined_simple_signal", "0.382195"),
        )
    }
    folds = [
        {
            "fold_id": f"2024_Q{index}",
            "training_row_count": 5000 + index,
            "evaluation_row_count": rows,
            "embargo_sessions": 1,
            "shuffle": False,
            "model_metrics": model_metrics,
        }
        for index, rows in enumerate((732, 756, 768, 768), start=1)
    ]
    group_results = [
        {"group_id": f"group_{index}", "execution_status": status}
        for index, status in enumerate(
            (
                "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
                "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
                "EVALUATED_RESEARCH_ONLY",
                "EVALUATED_RESEARCH_ONLY",
                "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            )
        )
    ]
    return {
        "feature_label_refinement_execution_manifest": {
            "data_quality_summary": {
                "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
                "failure_count": 0,
                "warning_count": 1,
            }
        },
        "refined_label_generation_report": {
            "refined_label_family_count": 7,
            "coverage_entry_count": 84,
            "available_count": 82698,
            "unavailable_count": 924,
            "refined_label_generation_digest": execution.EXPECTED_REFINED_LABEL_DIGEST,
        },
        "refined_feature_generation_report": {
            "refined_feature_group_count": 9,
            "refined_feature_name_count": 19,
            "feature_matrix_row_count": 11946,
            "total_null_or_unavailable_count": 1128,
            "refined_feature_generation_digest": execution.EXPECTED_REFINED_FEATURE_DIGEST,
            "features_use_current_and_historical_information_only": True,
            "future_label_values_used_as_features": False,
        },
        "refined_protocol_execution_report": {
            "refined_protocol_group_count": 6,
            "no_shuffle": True,
            "no_lookahead_leakage": True,
        },
        "refined_walk_forward_report": {
            "fold_count": 4,
            "walk_forward_policy": "EXPANDING_TRAINING_WITH_QUARTERLY_2024_VALIDATION_FOLDS",
            "folds": folds,
        },
        "refined_out_of_sample_report": {
            "out_of_sample_window": {"start": "2025-01-01", "end": "2025-12-31"}
        },
        "refined_model_comparison_report": {
            "model_comparison_group_count": 5,
            "deterministic_comparison_ids": list(model_metrics),
            "group_execution_results": group_results,
            "out_of_sample_model_metrics": model_metrics,
            "model_comparison_is_acceptance_evidence": False,
        },
        "refined_metric_report": {
            "metric_families": ["classification", "calibration", "stability"],
            "walk_forward_fold_metrics": {fold["fold_id"]: model_metrics for fold in folds},
            "out_of_sample_model_metrics": model_metrics,
            "acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE",
        },
        "refined_leakage_control_report": {
            "leakage_control_status": "PASS",
            "failed_control_count": 0,
            "controls": [{"control": "no_lookahead", "status": "PASS"}],
        },
        "feature_label_refinement_execution_digest_manifest": {
            "output_digest_entries": [
                {
                    "filename": filename,
                    "digest_kind": (
                        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
                        if filename == "feature_label_refinement_execution_digest_manifest.json"
                        else "FILE_SHA256"
                    ),
                    "sha256": None if filename == "feature_label_refinement_execution_digest_manifest.json" else "a" * 64,
                }
                for filename in execution.REQUIRED_SOURCE_FILENAMES
            ]
        },
    }


def _verification() -> dict:
    return {
        "source_root": "fixture",
        "canonical_source_root": "fixture-canonical",
        "source_refinement_output_count": 12,
        "required_source_files": list(execution.REQUIRED_SOURCE_FILENAMES),
        "all_non_self_digest_manifest_entries_match": True,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(execution.EXPECTED_RECORD_COUNTS),
    }


def _execute(output_root: Path) -> dict:
    with patch.object(
        execution,
        "_verify_refined_sources",
        return_value=(_verification(), _source_reports(), []),
    ):
        return execution.execute_additional_predictive_evidence_for_refined_evidence_v1(
            source_root=output_root.parent / "source",
            canonical_source_root=output_root.parent / "canonical",
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


@pytest.fixture(scope="module")
def executed_bundle(tmp_path_factory):
    root = tmp_path_factory.mktemp("additional_predictive_refined_execution")
    artifact = _execute(root / "outputs")
    return artifact, root / "outputs"


@pytest.fixture(scope="module")
def executed(executed_bundle):
    return executed_bundle[0]


def test_execution_builds_offline_without_provider_calls(tmp_path, monkeypatch):
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _execute(tmp_path / "outputs")
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False


def test_execution_blocks_when_refined_source_is_missing(tmp_path):
    artifact = execution.execute_additional_predictive_evidence_for_refined_evidence_v1(
        source_root=tmp_path / "missing-refined",
        canonical_source_root=tmp_path / "missing-canonical",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED
    assert artifact["execution_status"] == execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_REFINED_EVIDENCE
    assert artifact["additional_predictive_evidence_execution_for_refined_evidence_digest"] == "NOT_CREATED"
    assert artifact["additional_predictive_evidence_execution_for_refined_evidence_executed"] is False
    assert artifact["additional_predictive_evidence_results_for_refined_evidence_created"] is False
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "outputs").exists()


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE),
        ("execution_status", execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY),
        ("target_universe_count", 12),
        ("target_universe", execution.TARGET_UNIVERSE),
        ("total_canonical_record_count", 11946),
        ("records_digest", execution.EXPECTED_RECORDS_DIGEST),
        ("meta_record_count", 913),
        ("non_meta_record_count", 1003),
        ("refined_label_family_count", 7),
        ("refined_feature_group_count", 9),
        ("refined_feature_field_count", 19),
        ("refined_protocol_group_count", 6),
        ("model_comparison_group_count", 5),
        ("generated_output_count", 10),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_executed_artifact_fields(executed, field, expected):
    assert executed[field] == expected


@pytest.mark.parametrize("field", execution.TRUE_EXECUTION_FIELDS)
def test_required_execution_state_is_true(executed, field):
    assert executed[field] is True


@pytest.mark.parametrize("field", execution.FALSE_GUARDRAIL_FIELDS)
def test_guardrail_state_is_false(executed, field):
    assert executed[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_execution_approval_for_refined_evidence_digest", execution.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest", execution.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest", execution.EXPECTED_CANDIDATE_DIGEST),
        ("feature_label_refinement_results_review_package_digest", execution.EXPECTED_REFINEMENT_RESULTS_REVIEW_DIGEST),
        ("feature_label_refinement_execution_digest", execution.EXPECTED_REFINEMENT_EXECUTION_DIGEST),
        ("feature_label_refinement_execution_approval_digest", execution.EXPECTED_REFINEMENT_EXECUTION_APPROVAL_DIGEST),
        ("research_registry_approval_digest", execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", execution.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(executed, field, expected):
    assert executed["source_evidence"][field] == expected


def test_refined_reassessment_summaries(executed):
    assert executed["refined_evidence_input_binding_summary"]["binding_status"] == "BOUND_REVIEWED_REFINED_EVIDENCE"
    assert executed["refined_label_feature_binding_summary"]["binding_status"] == "BOUND_NOT_REGENERATED"
    assert executed["refined_walk_forward_reassessment_summary"]["fold_count"] == 4
    assert executed["refined_walk_forward_reassessment_summary"]["evaluation_row_count"] == 3024
    assert executed["refined_out_of_sample_reassessment_summary"]["evaluation_row_count"] == 2988
    assert executed["refined_out_of_sample_reassessment_summary"]["accuracy_range"] == "0.119813 to 0.480924"
    assert executed["refined_baseline_model_comparison_summary"]["unavailable_model_family_requests"] == 3
    assert executed["refined_leakage_quality_summary"]["leakage_status"] == "PASS"
    assert executed["data_quality_summary"]["status"] == "PASS_WITH_PRESERVED_SOURCE_LIMITATION"


def test_all_outputs_and_digest_manifest_are_written(executed_bundle):
    _, output_root = executed_bundle
    assert sorted(path.name for path in output_root.iterdir()) == sorted(execution.OUTPUT_FILENAMES)
    manifest = json.loads((output_root / "refined_execution_digest_manifest.json").read_text(encoding="utf-8"))
    assert manifest["generated_output_count"] == 10
    assert [entry["filename"] for entry in manifest["output_digest_entries"]] == execution.OUTPUT_FILENAMES
    for entry in manifest["output_digest_entries"]:
        if entry["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            assert entry["filename"] == "refined_execution_digest_manifest.json"
            assert entry["sha256"] is None
        else:
            assert entry["sha256"] == sha256_file(output_root / entry["filename"])


def test_every_output_is_research_only_and_non_actionable(executed_bundle):
    _, output_root = executed_bundle
    for path in output_root.glob("*.json"):
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
        assert report["evidence_scope"] == execution.EVIDENCE_SCOPE
        assert report["predictive_usefulness"] == "not accepted"
        assert report["profitability"] == "not accepted"
        assert report["acceptance_evidence_status"] == "NOT_ACCEPTANCE_EVIDENCE"
        assert report["profitability_evidence_status"] == "NOT_PROFITABILITY_EVIDENCE"
        assert report["runtime_authority_status"] == "NOT_RUNTIME_AUTHORITY"


def test_validator_accepts_valid_executed_artifact(executed):
    result = execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(executed)
    assert result["status"] == execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE_VALID
    assert result["generated_output_count"] == 10


@pytest.mark.parametrize(
    ("field", "wrong"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("target_universe_count", 11),
        ("target_universe", ["META"]),
        ("total_canonical_record_count", 11945),
        ("records_digest", "WRONG"),
        ("meta_record_count", 1003),
        ("non_meta_record_count", 913),
        ("refined_label_family_count", 6),
        ("refined_feature_group_count", 8),
        ("refined_feature_field_count", 18),
        ("refined_protocol_group_count", 5),
        ("model_comparison_group_count", 4),
        ("refined_leakage_status", "FAIL"),
        ("generated_output_count", 9),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_wrong_contract_value(executed, field, wrong):
    mutated = deepcopy(executed)
    mutated[field] = wrong
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
        execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(mutated)


@pytest.mark.parametrize("field", execution.TRUE_EXECUTION_FIELDS)
def test_validator_rejects_required_execution_false(executed, field):
    mutated = deepcopy(executed)
    mutated[field] = False
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
        execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(mutated)


@pytest.mark.parametrize("field", execution.FALSE_GUARDRAIL_FIELDS)
def test_validator_rejects_guardrail_true(executed, field):
    mutated = deepcopy(executed)
    mutated[field] = True
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
        execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(mutated)


def test_validator_rejects_missing_or_changed_approval_digest(executed):
    for value in (None, "WRONG"):
        mutated = deepcopy(executed)
        mutated["source_evidence"]["additional_predictive_evidence_execution_approval_for_refined_evidence_digest"] = value
        with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
            execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(mutated)


def test_validator_rejects_missing_execution_digest(executed):
    mutated = deepcopy(executed)
    mutated.pop("additional_predictive_evidence_execution_for_refined_evidence_digest")
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
        execution.validate_additional_predictive_evidence_executed_for_refined_evidence_v1(mutated)


def test_execution_digest_is_deterministic_for_fixed_inputs(tmp_path):
    first = _execute(tmp_path / "first")
    second = _execute(tmp_path / "second")
    assert first["additional_predictive_evidence_execution_for_refined_evidence_digest"] == second["additional_predictive_evidence_execution_for_refined_evidence_digest"]


def test_markdown_includes_required_sections(executed):
    markdown = execution.build_additional_predictive_evidence_execution_for_refined_evidence_status_markdown_v1(executed)
    for section in (
        "Additional Predictive Evidence Execution for Refined Evidence",
        "Source Execution Approval",
        "Source Feature/Label Refinement Results Review",
        "Registry-Approved Dataset Metadata",
        "Target Universe",
        "Refined Evidence Input Binding",
        "Refined Label/Feature Binding Summary",
        "Refined Walk-Forward Reassessment",
        "Refined OOS Reassessment",
        "Refined Baseline and Model Comparison Reassessment",
        "Refined Calibration and Stability Review",
        "Refined Leakage and Quality Review",
        "Output Digest Manifest",
        "Execution Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_execution_refuses_to_overwrite_outputs(tmp_path):
    output_root = tmp_path / "outputs"
    _execute(output_root)
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionForRefinedEvidenceError):
        _execute(output_root)
