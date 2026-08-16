from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_results_review_for_refined_evidence_service as review,
)


def _common(report_name: str) -> dict:
    return {
        "report_name": report_name,
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.EVIDENCE_SCOPE,
        "acceptance_evidence_status": "NOT_ACCEPTANCE_EVIDENCE",
        "profitability_evidence_status": "NOT_PROFITABILITY_EVIDENCE",
        "runtime_authority_status": "NOT_RUNTIME_AUTHORITY",
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "predictive_usefulness": review.NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": review.NOT_ACCEPTED,
        "automatic_stitching": False,
        "trade_recommendations_generated": False,
    }


def _source_evidence() -> dict:
    return {
        "additional_predictive_evidence_execution_approval_for_refined_evidence_digest": review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
        "feature_label_refinement_results_review_package_digest": review.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
        "feature_label_refinement_execution_digest": review.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
        "feature_label_refinement_execution_approval_digest": review.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": review.EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": review.EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        "research_registry_approval_digest": review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": review.EXPECTED_RECORDS_DIGEST,
    }


def _payload(filename: str) -> dict:
    payload = _common(filename.removesuffix(".json"))
    if filename == "refined_additional_predictive_evidence_execution_manifest.json":
        payload.update(
            {
                "artifact_kind": review.execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE,
                "execution_status": review.execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY,
                "additional_predictive_evidence_execution_for_refined_evidence_digest": review.EXPECTED_SOURCE_EXECUTION_DIGEST,
                "source_evidence": _source_evidence(),
                "registry_approved_dataset_metadata": deepcopy(
                    review.EXPECTED_REGISTRY_METADATA
                ),
                "target_universe": list(review.TARGET_UNIVERSE),
                "target_universe_count": 12,
                "total_canonical_record_count": 11946,
                "per_ticker_record_counts": dict(review.EXPECTED_RECORD_COUNTS),
                "records_digest": review.EXPECTED_RECORDS_DIGEST,
                "generated_output_count": 10,
                "additional_predictive_evidence_execution_for_refined_evidence_executed": True,
                "additional_predictive_evidence_results_for_refined_evidence_created": True,
                "refined_evidence_input_binding_performed": True,
                "refined_walk_forward_reassessment_performed": True,
                "refined_out_of_sample_reassessment_performed": True,
                "refined_baseline_model_comparison_reassessment_performed": True,
                "refined_calibration_stability_review_performed": True,
                "refined_leakage_quality_review_performed": True,
            }
        )
    elif filename == "refined_evidence_input_manifest.json":
        payload["input_binding_summary"] = {
            "binding_status": "BOUND_TO_REVIEWED_REFINED_EVIDENCE",
            "all_non_self_digests_verified": True,
            "records_digest_verified": True,
            "refined_label_generation_digest": review.EXPECTED_REFINED_LABEL_DIGEST,
            "refined_feature_generation_digest": review.EXPECTED_REFINED_FEATURE_DIGEST,
            "source_output_count": 12,
        }
    elif filename == "refined_label_feature_binding_manifest.json":
        payload.update(
            {
                "source_refined_label_generation_digest": review.EXPECTED_REFINED_LABEL_DIGEST,
                "source_refined_feature_generation_digest": review.EXPECTED_REFINED_FEATURE_DIGEST,
                "binding_summary": {
                    "label_family_count": 7,
                    "label_coverage_entries": 84,
                    "label_available_values": 82698,
                    "label_unavailable_values": 924,
                    "feature_group_count": 9,
                    "feature_category_count": 11,
                    "feature_field_count": 19,
                    "feature_rows": 11946,
                    "feature_null_or_unavailable_values": 1128,
                    "future_labels_used_as_features": False,
                    "features_current_or_historical_only": True,
                },
            }
        )
    elif filename == "refined_walk_forward_reassessment_report.json":
        payload.update(
            {
                "fold_count": 4,
                "evaluation_row_count": 3024,
                "walk_forward_policy": "EXPANDING_TRAINING_WITH_QUARTERLY_2024_VALIDATION_FOLDS",
                "fold_summaries": [{"fold_id": f"2024_Q{index}"} for index in range(1, 5)],
            }
        )
    elif filename == "refined_out_of_sample_reassessment_report.json":
        payload.update(
            {
                "evaluation_row_count": 2988,
                "accuracy_range": "0.119813 to 0.480924",
                "model_metrics": {"majority_class_baseline": {"accuracy": "0.480924"}},
            }
        )
    elif filename == "refined_baseline_model_comparison_report.json":
        payload.update(
            {
                "model_comparison_group_count": 5,
                "deterministic_comparison_ids": [f"comparison_{index}" for index in range(7)],
                "unavailable_model_family_requests": 3,
                "unavailable_model_family_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
                "model_comparison_is_acceptance_evidence": False,
            }
        )
    elif filename == "refined_calibration_stability_report.json":
        payload.update(
            {
                "review_status": "REVIEWED_FROM_EXISTING_REFINED_METRICS",
                "acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED",
                "metric_families": [f"metric_{index}" for index in range(6)],
            }
        )
    elif filename == "refined_leakage_quality_report.json":
        payload.update(
            {
                "protocol_group_count": 6,
                "chronological_splits": True,
                "one_session_embargo": True,
                "no_shuffle": True,
                "no_lookahead": True,
                "leakage_status": "PASS",
                "failed_leakage_controls": 0,
                "data_quality_summary": {
                    "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
                    "failure_count": 0,
                    "warning_count": 1,
                },
            }
        )
    return payload


def _write_json(path: Path, payload: dict) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _write_fixture_outputs(output_root: Path) -> None:
    manifest_name = "refined_execution_digest_manifest.json"
    digests: dict[str, str] = {}
    for filename in review.EXPECTED_OUTPUT_FILENAMES:
        if filename != manifest_name:
            digests[filename] = _write_json(output_root / filename, _payload(filename))
    entries = []
    for filename in review.EXPECTED_OUTPUT_FILENAMES:
        if filename == manifest_name:
            entries.append(
                {
                    "filename": filename,
                    "digest_kind": review.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                    "sha256": None,
                }
            )
        else:
            entries.append(
                {
                    "filename": filename,
                    "digest_kind": "FILE_SHA256",
                    "sha256": digests[filename],
                }
            )
    digest_manifest = _payload(manifest_name) | {
        "output_digest_entries": entries,
        "self_reference_policy": review.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "generated_output_count": 10,
    }
    _write_json(output_root / manifest_name, digest_manifest)


@pytest.fixture(scope="module")
def reviewed_run(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict]:
    root = tmp_path_factory.mktemp("refined-predictive-results")
    _write_fixture_outputs(root)
    package = review.build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=root
    )
    return root, package


def test_review_package_builds_offline_without_provider_calls(
    reviewed_run: tuple[Path, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _ = reviewed_run

    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=root
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path) -> None:
    package = review.build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    assert package["output_file_inspection_performed"] is False
    assert package["review_summary"]["blocker_count"] > 0
    assert package[
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence"
    ] is False


def test_digest_mismatch_blocks_review(tmp_path: Path) -> None:
    root = tmp_path / "tampered"
    _write_fixture_outputs(root)
    path = root / "refined_operator_review_summary.json"
    payload = _payload(path.name)
    payload["warning_count"] = 2
    _write_json(path, payload)
    package = review.build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=root
    )
    assert package["output_digest_manifest_summary"]["digest_mismatch_count"] == 1
    assert package["review_status"].endswith("BLOCKED_MISSING_OR_INVALID_OUTPUTS")


def test_review_artifact_status_and_source_chain(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE
    )
    assert package["review_status"] == (
        review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY
    )
    assert package[
        "source_additional_predictive_evidence_execution_for_refined_evidence_digest"
    ] == review.EXPECTED_SOURCE_EXECUTION_DIGEST
    assert package[
        "source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
    ] == review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
    assert package[
        "additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest"
    ] == review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST
    assert package["feature_label_refinement_results_review_package_digest"] == (
        review.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST
    )
    assert package["research_registry_approval_digest"] == (
        review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
    )


def test_registry_universe_and_record_counts_are_bound(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["records_digest"] == review.EXPECTED_RECORDS_DIGEST
    assert package["meta_record_count"] == 913
    assert package["non_meta_record_count"] == 1003
    assert all(
        count == (913 if ticker == "META" else 1003)
        for ticker, count in package["per_ticker_record_counts"].items()
    )


def test_output_digests_and_boundaries_are_verified(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["generated_output_count"] == 10
    assert len(package["output_file_digests"]) == 10
    assert package["output_digest_manifest_summary"]["verified_non_self_digest_count"] == 9
    assert package["output_digest_manifest_summary"]["digest_mismatch_count"] == 0
    assert package["output_digest_manifest_summary"]["self_reference_valid"] is True
    assert package["outputs_research_only_non_actionable"] is True
    assert package["outputs_not_acceptance_evidence"] is True
    assert package["outputs_not_profitability_evidence"] is True
    assert package["outputs_not_runtime_authority"] is True


def test_refined_label_feature_and_protocol_facts(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["refined_label_family_count"] == 7
    assert package["refined_label_available_values"] == 82698
    assert package["refined_label_unavailable_values"] == 924
    assert package["refined_label_generation_digest"] == review.EXPECTED_REFINED_LABEL_DIGEST
    assert package["refined_feature_group_count"] == 9
    assert package["refined_feature_category_count"] == 11
    assert package["refined_feature_field_count"] == 19
    assert package["refined_feature_rows"] == 11946
    assert package["refined_feature_null_or_unavailable_values"] == 1128
    assert package["refined_feature_generation_digest"] == review.EXPECTED_REFINED_FEATURE_DIGEST
    assert package["refined_protocol_group_count"] == 6
    assert package["chronological_splits"] is True
    assert package["one_session_embargo"] is True
    assert package["no_shuffle"] is True
    assert package["no_lookahead"] is True


def test_refined_reassessment_and_model_facts(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["refined_walk_forward_fold_count"] == 4
    assert package["refined_walk_forward_evaluation_rows"] == 3024
    assert package["refined_oos_evaluation_rows"] == 2988
    assert package["refined_oos_accuracy_range"] == "0.119813 to 0.480924"
    assert package["model_comparison_group_count"] == 5
    assert package["deterministic_comparisons_evaluated"] == 7
    assert package["unavailable_model_family_requests"] == 3
    assert package["unavailable_model_family_status"] == (
        "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    )
    assert package["refined_leakage_status"] == "PASS"
    assert package["failed_leakage_controls"] == 0
    assert package["data_quality_status"] == "PASS_WITH_PRESERVED_SOURCE_LIMITATION"


@pytest.mark.parametrize(
    "field, expected",
    [
        ("provider_requests_made_in_review", False),
        ("live_provider_transport_enabled_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("canonical_dataset_regenerated_in_review", False),
        ("feature_label_refinement_execution_rerun_performed", False),
        ("refined_label_generation_rerun_performed", False),
        ("refined_feature_generation_rerun_performed", False),
        ("refined_walk_forward_reassessment_rerun_performed", False),
        ("refined_out_of_sample_reassessment_rerun_performed", False),
        ("refined_metrics_recomputation_performed", False),
        ("refined_model_comparison_rerun_performed", False),
        ("additional_predictive_evidence_execution_for_refined_evidence_rerun_performed", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created", False),
    ],
)
def test_review_does_not_rerun_or_create_prohibited_work(
    reviewed_run: tuple[Path, dict], field: str, expected: bool
) -> None:
    _, package = reviewed_run
    assert package[field] is expected


@pytest.mark.parametrize(
    "field, expected",
    [
        ("predictive_usefulness", review.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", review.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", review.NOT_AUTHORIZED),
        ("strategy_use", review.NOT_AUTHORIZED),
        ("paper_trading", review.NOT_AUTHORIZED),
        ("broker_execution", review.NOT_AUTHORIZED),
        ("automatic_stitching", False),
        ("results_create_predictive_usefulness_reassessment_review", False),
        ("results_create_predictive_usefulness_acceptance", False),
        ("results_create_profitability_acceptance", False),
        ("results_create_runtime_authority", False),
    ],
)
def test_acceptance_and_runtime_boundaries_remain_closed(
    reviewed_run: tuple[Path, dict], field: str, expected: object
) -> None:
    _, package = reviewed_run
    assert package[field] == expected


def test_results_support_only_future_reassessment_review_rerun(
    reviewed_run: tuple[Path, dict],
) -> None:
    _, package = reviewed_run
    assert package[
        "results_support_predictive_usefulness_reassessment_rerun_using_refined_evidence"
    ] is True
    assert package[
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence"
    ] is True
    assert package["predictive_usefulness_reassessment_review_created"] is False


def test_checklist_and_summary_are_complete(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert [item["check_id"] for item in package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert all(item["status"] == "PASS" for item in package["review_checklist"])
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0


def test_review_package_digest_is_deterministic(reviewed_run: tuple[Path, dict]) -> None:
    root, first = reviewed_run
    second = review.build_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        output_root=root
    )
    assert second == first
    assert second[
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    ] == review.additional_predictive_evidence_results_review_for_refined_evidence_package_digest_v1(
        second
    )


def test_validator_accepts_valid_package(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    validation = review.validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        package
    )
    assert validation["blocker_count"] == 0
    assert validation[
        "ready_for_predictive_usefulness_reassessment_review_rerun_using_refined_evidence"
    ] is True


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_additional_predictive_evidence_execution_for_refined_evidence_digest", "0" * 64),
        ("source_additional_predictive_evidence_execution_approval_for_refined_evidence_digest", "0" * 64),
        ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("per_ticker_record_counts", review.EXPECTED_RECORD_COUNTS | {"META": 914}),
        ("generated_output_count", 9),
        ("refined_label_family_count", 6),
        ("refined_feature_group_count", 8),
        ("refined_feature_field_count", 18),
        ("model_comparison_group_count", 4),
        ("refined_leakage_status", "FAIL"),
        ("failed_leakage_controls", 1),
        ("provider_requests_made_in_review", True),
        ("additional_predictive_evidence_execution_for_refined_evidence_rerun_performed", True),
        ("refined_label_generation_rerun_performed", True),
        ("refined_feature_generation_rerun_performed", True),
        ("refined_metrics_recomputation_performed", True),
        ("refined_model_comparison_rerun_performed", True),
        ("predictive_usefulness_reassessment_review_rerun_using_refined_evidence_created", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("results_create_predictive_usefulness_reassessment_review", True),
        ("results_create_predictive_usefulness_acceptance", True),
        ("limitations", []),
        ("next_gates", []),
    ],
)
def test_validator_rejects_invalid_or_authorizing_mutation(
    reviewed_run: tuple[Path, dict], field: str, invalid_value: object
) -> None:
    _, package = reviewed_run
    invalid = deepcopy(package)
    invalid[field] = invalid_value
    with pytest.raises(
        review.AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError
    ):
        review.validate_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
            invalid
        )


def test_markdown_contains_required_sections(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    markdown = review.build_additional_predictive_evidence_results_review_for_refined_evidence_markdown_v1(
        package
    )
    for section in (
        "# MarketFlow Additional Predictive Evidence Results Review for Refined Evidence",
        "## Source Refined-Evidence Execution",
        "## Source Feature/Label Refinement Results Review",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Refined Evidence Input Binding Review",
        "## Refined Walk-Forward Reassessment Review",
        "## Refined OOS Reassessment Review",
        "## Refined Baseline and Model Comparison Review",
        "## Refined Calibration and Stability Review",
        "## Refined Leakage and Quality Review",
        "## Output Digest Manifest",
        "## Limitations",
        "## Next Gates",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert section in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(
    reviewed_run: tuple[Path, dict], tmp_path: Path
) -> None:
    root, package = reviewed_run
    result = review.write_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
        tmp_path, output_root=root
    )
    path = Path(result["path"])
    assert path.is_file()
    assert result[
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    ] == package[
        "additional_predictive_evidence_results_review_for_refined_evidence_package_digest"
    ]
    with pytest.raises(
        review.AdditionalPredictiveEvidenceResultsReviewForRefinedEvidenceError
    ):
        review.write_additional_predictive_evidence_results_review_for_refined_evidence_package_v1(
            tmp_path, output_root=root
        )
