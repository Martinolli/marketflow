from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    additional_predictive_evidence_results_review_improved_evidence_service as service,
)


def _source_ticker_entries() -> list[dict]:
    return [
        {"ticker": ticker, "historical_record_count": service.EXPECTED_RECORD_COUNTS[ticker]}
        for ticker in service.TARGET_UNIVERSE
    ]


def _verification() -> dict:
    return {
        "observed_output_count": 13,
        "output_digest_mismatch_count": 0,
        "local_output_hashes": {
            filename: str(index).zfill(64)
            for index, filename in enumerate(service.EXPECTED_OUTPUT_FILENAMES, start=1)
        },
        "output_digest_manifest": [
            {
                "filename": filename,
                "local_sha256": str(index).zfill(64),
                "recorded_sha256": None if index == 13 else str(index).zfill(64),
                "digest_kind": (
                    "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
                    if index == 13
                    else "FILE_SHA256"
                ),
                "digest_match": True,
            }
            for index, filename in enumerate(service.EXPECTED_OUTPUT_FILENAMES, start=1)
        ],
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "verified_sections": {
            "execution_manifest": True,
            "source_binding_manifest": True,
            "improved_label_schema_binding_report": True,
            "improved_feature_label_matrix_report": True,
            "walk_forward_results": True,
            "oos_results": True,
            "baseline_model_comparison": True,
            "metric_family_results": True,
            "calibration_stability_report": True,
            "leakage_quality_control_report": True,
            "per_ticker_meta_review": True,
            "operator_results_review_summary": True,
        },
        "per_ticker_results_review_entries": service._build_per_ticker_entries(
            _source_ticker_entries()
        ),
        "optional_model_statuses": {
            "tree": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            "ensemble": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        },
        "walk_forward_stability": {},
        "oos_method_metrics": {},
        "metric_families": [f"metric-{index}" for index in range(10)],
        "source_outputs_unchanged": True,
    }


def _build_ready(
    monkeypatch: pytest.MonkeyPatch, output_root: Path
) -> dict:
    monkeypatch.setattr(service, "_verify_outputs", lambda _root: _verification())
    return service.build_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        output_root=output_root
    )


@pytest.fixture
def review_package(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    return _build_ready(monkeypatch, tmp_path / "source")


def test_results_review_builds_offline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    package = _build_ready(monkeypatch, tmp_path / "source")
    assert package["created_offline"] is True
    assert package["output_file_inspection_performed"] is True
    assert package["additional_predictive_evidence_results_review_ready"] is True


def test_results_review_blocks_when_output_root_is_missing(tmp_path: Path) -> None:
    package = service.build_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == (
        service.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_IMPROVED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS
    )
    assert package["output_file_inspection_performed"] is False
    assert package["additional_predictive_evidence_results_review_ready"] is False
    assert package["ready_for_predictive_usefulness_reassessment_using_improved_evidence"] is False
    assert service.validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        package
    )["blocked"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (
            "artifact_kind",
            service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE,
        ),
        (
            "review_status",
            service.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY,
        ),
        ("source_execution_digest", service.EXPECTED_EXECUTION_DIGEST),
        ("source_output_binding_digest", service.EXPECTED_OUTPUT_BINDING_DIGEST),
        ("source_approval_digest", service.EXPECTED_APPROVAL_DIGEST),
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
            service.execution.SOURCE_EVIDENCE[
                "improved_evidence_planning_results_review_using_redesigned_evidence_digest"
            ],
        ),
        ("feature_label_matrix_digest", service.EXPECTED_MATRIX_DIGEST),
        ("feature_values_digest", service.EXPECTED_FEATURE_VALUES_DIGEST),
        ("redesigned_label_values_digest", service.EXPECTED_LABEL_VALUES_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
        ("target_universe", service.TARGET_UNIVERSE),
        ("target_universe_count", 12),
        ("meta_record_count", 913),
        ("selected_redesign_direction", service.SELECTED_DIRECTION),
        ("generated_output_count", 13),
        ("observed_output_count", 13),
        ("output_digest_mismatch_count", 0),
        ("outputs_research_only_non_actionable", True),
        ("output_file_inspection_performed", True),
        ("additional_predictive_evidence_results_review_created", True),
        ("additional_predictive_evidence_results_review_ready", True),
        ("ready_for_predictive_usefulness_reassessment_using_improved_evidence", True),
        ("predictive_usefulness_reassessment_using_improved_evidence_created", False),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", False),
        ("label_regeneration_performed", False),
        ("new_targets_created", False),
        ("target_definition_change_authorized", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("metric_recomputation_performed_in_review", False),
        ("model_training_performed_in_review", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("matrix_row_count", 143352),
        ("evaluable_matrix_row_count", 142200),
        ("unavailable_target_count", 1152),
        ("cross_sectional_delta_vs_majority", "0.00309917"),
        ("majority_accuracy", "0.58626033"),
        ("local_model_accuracy", "0.58626033"),
        ("leakage_control_passed", True),
        ("leakage_failed_control_count", 0),
        ("meta_reduced_record_count_preserved", True),
        ("results_review_classification", "COMPLETED_RESEARCH_ONLY"),
        ("reassessment_readiness", "READY_FOR_FUTURE_REASSESSMENT_ONLY"),
    ],
)
def test_results_review_contract_fields(
    review_package: dict, field: str, expected: object
) -> None:
    assert review_package[field] == expected


@pytest.mark.parametrize("field", service.FALSE_AUTHORITY_FIELDS)
def test_closed_authority_fields_remain_false(review_package: dict, field: str) -> None:
    assert review_package[field] is False


@pytest.mark.parametrize(
    "section",
    [
        "execution_manifest",
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
    ],
)
def test_each_source_section_is_verified(review_package: dict, section: str) -> None:
    assert review_package["verified_sections"][section] is True


def test_output_digests_and_local_hashes_are_bound(review_package: dict) -> None:
    assert len(review_package["local_output_hashes"]) == 13
    assert len(review_package["output_digest_manifest"]) == 13
    assert all(row["digest_match"] is True for row in review_package["output_digest_manifest"])
    assert review_package["digest_manifest_self_reference_policy"] == (
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    )


def test_per_ticker_entries_preserve_order_meta_and_digests(review_package: dict) -> None:
    entries = review_package["per_ticker_results_review_entries"]
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert len(entries) == 12
    assert service._per_ticker_digests_valid(entries) is True
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["review_note"] == (
        "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_IMPROVED_EVIDENCE"
    )


def test_limitations_next_chain_next_gates_and_risk_controls_are_exact(
    review_package: dict,
) -> None:
    assert review_package["limitations"] == service.LIMITATIONS
    assert review_package["next_chain"] == service.NEXT_CHAIN
    assert review_package["next_gates"] == service.NEXT_GATES
    assert review_package["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(review_package: dict) -> None:
    checklist = review_package["review_checklist"]
    summary = review_package["review_summary"]
    assert len(checklist) == 95
    assert all(row["status"] == "PASS" for row in checklist)
    assert summary["total_checks"] == 95
    assert summary["passed_checks"] == 95
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_validator_accepts_valid_package(review_package: dict) -> None:
    result = service.validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        review_package
    )
    assert result["valid"] is True
    assert result["blocked"] is False
    assert result["passed_checks"] == 95


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_execution_digest", "0" * 64),
        ("source_output_binding_digest", "0" * 64),
        ("source_approval_digest", "0" * 64),
        ("selected_redesign_direction", "WRONG"),
        ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("generated_output_count", 12),
        ("output_digest_mismatch_count", 1),
        ("additional_predictive_evidence_results_review_ready", False),
        ("predictive_usefulness_reassessment_using_improved_evidence_created", True),
        ("predictive_usefulness_acceptance_readiness_using_improved_evidence_created", True),
        ("label_regeneration_authorized", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("target_definition_change_performed", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("metric_recomputation_performed_in_review", True),
        ("model_training_performed_in_review", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("additional_predictive_evidence_execution_rerun_performed", True),
        ("limitations", []),
        ("next_chain", []),
        ("risk_controls", []),
        (
            "additional_predictive_evidence_results_review_using_improved_evidence_digest",
            None,
        ),
    ],
)
def test_validator_rejects_invalid_contract_field(
    review_package: dict, field: str, invalid_value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid[field] = invalid_value
    with pytest.raises(service.AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError):
        service.validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_digest(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_results_review_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_results_review_digest"
    )
    with pytest.raises(service.AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError):
        service.validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
            invalid
        )


def test_review_digest_is_deterministic_and_output_location_independent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    first = _build_ready(monkeypatch, tmp_path / "first")
    second = _build_ready(monkeypatch, tmp_path / "second")
    assert first[
        "additional_predictive_evidence_results_review_using_improved_evidence_digest"
    ] == second[
        "additional_predictive_evidence_results_review_using_improved_evidence_digest"
    ]


def test_writer_writes_once_without_overwrite(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(service, "_verify_outputs", lambda _root: _verification())
    result = service.write_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        tmp_path / "review", output_root=tmp_path / "source"
    )
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert payload["review_status"] == (
        service.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY
    )
    with pytest.raises(service.AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError):
        service.write_additional_predictive_evidence_results_review_using_improved_evidence_v1(
            tmp_path / "review", output_root=tmp_path / "source"
        )


def test_markdown_includes_required_sections(review_package: dict) -> None:
    markdown = service.build_additional_predictive_evidence_results_review_using_improved_evidence_markdown_v1(
        review_package
    )
    sections = [
        "Title",
        "Optional Additional Predictive Evidence Results Review Using Improved Evidence",
        "Source Execution",
        "Bound Evidence",
        "Dataset and Universe",
        "Output Verification",
        "Selected Redesign Direction",
        "Source Binding Review",
        "Improved Label Schema Binding Review",
        "Improved Feature-Label Matrix Report Review",
        "Walk-Forward Results Review",
        "OOS Results Review",
        "Baseline and Model Comparison Review",
        "Metric Family Results Review",
        "Calibration and Stability Review",
        "Leakage and Quality Controls Review",
        "Per-Ticker and META Review",
        "Review Classification",
        "Limitations",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)
