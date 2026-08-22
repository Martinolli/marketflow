from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    additional_predictive_evidence_execution_improved_evidence_service as service,
)


FIXED_TIMESTAMP = "2026-08-22T16:00:00Z"


def _summaries() -> dict:
    return {
        "walk_forward_status": "COMPUTED_RESEARCH_ONLY",
        "oos_status": "COMPUTED_RESEARCH_ONLY",
        "baseline_model_comparison_status": "COMPUTED_RESEARCH_ONLY",
        "metric_family_status": "COMPUTED_RESEARCH_ONLY",
        "calibration_stability_status": "COMPUTED_RESEARCH_ONLY",
        "leakage_quality_control_status": "PASS_RESEARCH_ONLY",
        "per_ticker_meta_review_status": "COMPLETED_RESEARCH_ONLY",
        "per_ticker_execution_entries": service._per_ticker_entries([]),
        "oos_method_metrics": {},
        "walk_forward_stability": {},
        "leakage_control_count": 8,
        "leakage_failed_control_count": 0,
        "feature_label_matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152,
        "feature_input_names": ["offline_fixture_feature"],
        "metric_recomputation_performed": True,
        "model_training_performed": True,
    }


def _verification() -> dict:
    return {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": True,
        "all_required_source_bindings_match": True,
        "source_files_unchanged": True,
        "source_file_count": 21,
        "source_paths": {"fixture": "fixture.json"},
        "source_file_sha256": {"fixture": "f" * 64},
    }


def _artifact(tmp_path: Path) -> dict:
    return service._build_executed_artifact(
        run_timestamp_utc=FIXED_TIMESTAMP,
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        prior_predictive_evidence_root=tmp_path / "prior",
        improved_planning_root=tmp_path / "planning",
        output_root=tmp_path / "output",
        verification=_verification(),
        summaries=_summaries(),
    )


@pytest.fixture
def artifact(tmp_path: Path) -> dict:
    return _artifact(tmp_path)


def _reports() -> dict[str, dict]:
    names = {
        "source_binding_manifest",
        "improved_label_schema_binding_report",
        "improved_feature_label_matrix_report",
        "walk_forward_results",
        "oos_results",
        "baseline_model_comparison",
        "metric_family_results",
        "calibration_stability_report",
        "leakage_quality_control_report",
        "per_ticker_meta_review",
        "operator_results_review_summary",
    }
    return {name: {"report_name": name, "research_only": True} for name in names}


def test_execution_builds_offline_and_writes_exact_output_set(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(service, "_verify_sources", lambda **_kwargs: (_verification(), []))
    monkeypatch.setattr(service, "_sha256_file", lambda _path: "f" * 64)
    monkeypatch.setattr(
        service, "_build_report_payloads", lambda **_kwargs: (_reports(), _summaries())
    )
    output_root = tmp_path / "output"
    result = service.execute_additional_predictive_evidence_using_improved_evidence_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        prior_predictive_evidence_root=tmp_path / "prior",
        improved_planning_root=tmp_path / "planning",
        output_root=output_root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert result["additional_predictive_evidence_executed"] is True
    assert sorted(path.name for path in output_root.iterdir()) == sorted(
        service.OUTPUT_FILENAMES
    )


def test_execution_blocks_without_required_sources_and_writes_nothing(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "output"
    result = service.execute_additional_predictive_evidence_using_improved_evidence_v1(
        canonical_root=tmp_path / "missing-canonical",
        label_root=tmp_path / "missing-labels",
        feature_root=tmp_path / "missing-features",
        prior_predictive_evidence_root=tmp_path / "missing-prior",
        improved_planning_root=tmp_path / "missing-planning",
        output_root=output_root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert result["artifact_kind"] == (
        service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_IMPROVED_EVIDENCE
    )
    assert result["execution_status"] == (
        service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE
    )
    assert result["additional_predictive_evidence_executed"] is False
    assert result["additional_predictive_evidence_results_created"] is False
    assert result["generated_output_count"] == 0
    assert not output_root.exists()


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        ),
        (
            "execution_status",
            service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        ),
        (
            "additional_predictive_evidence_execution_approval_using_improved_evidence_digest",
            service.EXPECTED_APPROVAL_DIGEST,
        ),
        (
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest",
            service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        ),
        (
            "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest",
            service.EXPECTED_CANDIDATE_DIGEST,
        ),
        (
            "improved_evidence_planning_results_review_using_redesigned_evidence_digest",
            service.approval_service.BOUND_DIGESTS[
                "improved_evidence_planning_results_review_using_redesigned_evidence_digest"
            ],
        ),
        (
            "improved_evidence_planning_execution_using_redesigned_evidence_digest",
            service.EXPECTED_PLANNING_EXECUTION_DIGEST,
        ),
        (
            "improved_evidence_planning_output_binding_digest",
            service.EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST,
        ),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        (
            "research_registry_approval_digest",
            service.approval_service.BOUND_DIGESTS["research_registry_approval_digest"],
        ),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
        ("target_universe", service.TARGET_UNIVERSE),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
        ("additional_predictive_evidence_execution_approved", True),
        ("additional_predictive_evidence_execution_authorized", True),
        (
            "ready_for_additional_predictive_evidence_execution_using_improved_evidence",
            True,
        ),
        ("additional_predictive_evidence_executed", True),
        ("additional_predictive_evidence_results_created", True),
        ("selected_redesign_direction", service.SELECTED_DIRECTION),
        ("generated_output_count", 13),
        ("planned_source_input_count", 15),
        ("execution_activity_count", 12),
        ("model_family_count", 9),
        ("metric_family_count", 10),
        ("label_regeneration_performed", False),
        ("new_targets_created", False),
        ("target_definition_change_authorized", False),
        ("feature_generation_performed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("additional_predictive_evidence_execution_classification", "COMPLETED_RESEARCH_ONLY"),
        ("label_schema_binding_status", "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION"),
        (
            "improved_feature_label_matrix_status",
            "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX",
        ),
        ("walk_forward_status", "COMPUTED_RESEARCH_ONLY"),
        ("oos_status", "COMPUTED_RESEARCH_ONLY"),
        ("metric_family_status", "COMPUTED_RESEARCH_ONLY"),
        ("leakage_quality_control_status", "PASS_RESEARCH_ONLY"),
        ("digest_manifest_created", True),
        ("source_files_unchanged", True),
    ],
)
def test_artifact_contract_fields(artifact: dict, field: str, expected: object) -> None:
    assert artifact[field] == expected


@pytest.mark.parametrize("field", service.FALSE_GUARDRAIL_FIELDS)
def test_all_source_mutation_and_authority_guardrails_remain_false(
    artifact: dict, field: str
) -> None:
    assert artifact[field] is False


def test_per_ticker_entries_preserve_order_counts_and_digests(artifact: dict) -> None:
    entries = artifact["per_ticker_execution_entries"]
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert len(entries) == 12
    assert all(
        entry["per_ticker_additional_predictive_evidence_execution_digest"]
        == service.per_ticker_additional_predictive_evidence_execution_using_improved_evidence_digest_v1(
            entry
        )
        for entry in entries
    )
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True


def test_validator_accepts_valid_artifact(artifact: dict) -> None:
    result = service.validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
        artifact
    )
    assert result["valid"] is True
    assert result["generated_output_count"] == 13


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        (
            "additional_predictive_evidence_execution_approval_using_improved_evidence_digest",
            None,
        ),
        ("additional_predictive_evidence_execution_approved", False),
        ("additional_predictive_evidence_execution_authorized", False),
        (
            "ready_for_additional_predictive_evidence_execution_using_improved_evidence",
            False,
        ),
        ("additional_predictive_evidence_executed", False),
        ("additional_predictive_evidence_results_created", False),
        ("generated_output_count", 12),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("selected_redesign_direction", "WRONG"),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("feature_generation_performed", True),
        ("canonical_dataset_regenerated_in_execution", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_execution", True),
        ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("redesigned_label_regeneration_performed", True),
        ("feature_regeneration_performed", True),
        ("additional_predictive_evidence_execution_digest", None),
        ("output_digest_manifest_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_field(
    artifact: dict, field: str, invalid_value: object
) -> None:
    invalid = deepcopy(artifact)
    invalid[field] = invalid_value
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionImprovedEvidenceError):
        service.validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(artifact: dict) -> None:
    invalid = deepcopy(artifact)
    invalid["per_ticker_execution_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_execution_digest"
    )
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionImprovedEvidenceError):
        service.validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
            invalid
        )


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_sources(
    tmp_path: Path,
) -> None:
    first = _artifact(tmp_path / "first")
    second = _artifact(tmp_path / "second")
    assert first["additional_predictive_evidence_execution_digest"] == second[
        "additional_predictive_evidence_execution_digest"
    ]


def test_markdown_includes_all_required_sections(artifact: dict) -> None:
    markdown = service.build_additional_predictive_evidence_execution_status_markdown_v1(
        artifact
    )
    required_sections = [
        "Title",
        "Optional Additional Predictive Evidence Execution Using Improved Evidence",
        "Source Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Policy",
        "Selected Redesign Direction",
        "Source Binding",
        "Improved Label Schema Binding",
        "Improved Feature-Label Matrix Report",
        "Walk-Forward Results",
        "OOS Results",
        "Baseline and Model Comparison",
        "Metric Family Results",
        "Calibration and Stability",
        "Leakage and Quality Controls",
        "Per-Ticker and META Review",
        "Output Digest Manifest",
        "Authority Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in required_sections)
