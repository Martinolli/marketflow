from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import additional_predictive_evidence_results_review_service as review


def _common(report_name: str) -> dict:
    return {
        "report_name": report_name,
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": review.EVIDENCE_SCOPE,
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


def _baseline_payload(accuracy: str) -> dict:
    return {
        "classification_metrics": {"accuracy": accuracy, "evaluated_count": 2988},
        "trade_recommendation": False,
        "buy_hold_reference_only": False,
    }


def _payload(filename: str) -> dict:
    report_name = filename.removesuffix(".json")
    payload = _common(report_name)
    if filename == "additional_predictive_evidence_execution_manifest.json":
        payload.update(
            {
                "artifact_kind": review.execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED,
                "execution_status": review.execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY,
                "additional_predictive_evidence_execution_digest": review.EXPECTED_SOURCE_EXECUTION_DIGEST,
                "source_evidence": {
                    "additional_predictive_evidence_execution_approval_digest": review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
                    "additional_predictive_evidence_execution_candidate_review_package_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST,
                    "additional_predictive_evidence_execution_candidate_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
                    "research_registry_approval_digest": review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
                    "canonical_dataset_freeze_digest": review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
                    "canonical_dataset_generation_digest": review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
                    "records_digest": review.EXPECTED_RECORDS_DIGEST,
                },
                "registry_approved_dataset_metadata": deepcopy(
                    review.execution.APPROVED_REGISTRY_METADATA
                ),
                "target_universe": review.TARGET_UNIVERSE,
                "target_universe_count": 12,
                "total_canonical_record_count": 11946,
                "per_ticker_record_counts": review.EXPECTED_RECORD_COUNTS,
                "records_digest": review.EXPECTED_RECORDS_DIGEST,
                "metric_family_count": 9,
                "generated_output_count": 15,
                "label_coverage_summary": {
                    "available_count": 82854,
                    "unavailable_count": 768,
                },
            }
        )
    elif filename == "label_generation_manifest.json":
        payload.update(
            {
                "label_family_count": 7,
                "label_generation_digest": review.EXPECTED_LABEL_GENERATION_DIGEST,
                "label_coverage": [{"coverage_id": index} for index in range(84)],
            }
        )
    elif filename == "feature_matrix_manifest.json":
        payload.update(
            {
                "feature_family_count": 10,
                "feature_count": 22,
                "feature_matrix_row_count": 11946,
                "feature_matrix_digest": review.EXPECTED_FEATURE_GENERATION_DIGEST,
            }
        )
    elif filename == "feature_quality_report.json":
        payload.update(
            {
                "feature_coverage": [{"coverage_id": index} for index in range(120)],
                "total_null_counts_by_feature": {"rolling_features": 1428},
                "future_label_values_used_as_features": False,
            }
        )
    elif filename == "walk_forward_results_report.json":
        payload.update(
            {
                "fold_count": 4,
                "shuffle": False,
                "folds": [
                    {
                        "fold_id": item["fold_id"],
                        "evaluation_count": item["evaluation_count"],
                        "baselines": {
                            "majority_class_baseline": _baseline_payload(
                                item["majority_accuracy"]
                            )
                        },
                    }
                    for item in review.EXPECTED_WALK_FORWARD_FOLDS
                ],
            }
        )
    elif filename == "out_of_sample_results_report.json":
        payload["results"] = {
            "out_of_sample_window": "2025",
            "overall": {
                "evaluation_count": 2988,
                "baselines": {
                    name: _baseline_payload(accuracy)
                    for name, accuracy in review.EXPECTED_OOS_BASELINE_ACCURACIES.items()
                },
            },
        }
    elif filename == "baseline_comparison_report.json":
        payload.update(
            {
                "baseline_count": 6,
                "out_of_sample_comparison": {
                    name: {"accuracy": accuracy}
                    for name, accuracy in review.EXPECTED_OOS_BASELINE_ACCURACIES.items()
                },
            }
        )
    elif filename == "calibration_report.json":
        payload["calibration_metrics"] = {
            "out_of_sample_brier_score": "0.24875351",
            "out_of_sample_count": 2988,
        }
    elif filename == "stability_analysis_report.json":
        payload["stability_metrics"] = {
            name: {"acceptance_conclusion": "NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED"}
            for name in review.EXPECTED_OOS_BASELINE_ACCURACIES
        }
    elif filename == "leakage_control_report.json":
        payload.update({"leakage_control_status": "PASS", "failed_control_count": 0})
    elif filename == "data_quality_report.json":
        payload.update(
            {
                "quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
                "failure_count": 0,
                "warning_count": 1,
                "warnings": ["META reduced record count preserved"],
                "meta_reduced_record_count_preserved": True,
            }
        )
    return payload


def _write_json(path: Path, payload: dict) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _write_fixture_outputs(output_root: Path) -> None:
    digests: dict[str, str] = {}
    for filename in review.EXPECTED_OUTPUT_FILENAMES:
        if filename == "execution_digest_manifest.json":
            continue
        digests[filename] = _write_json(output_root / filename, _payload(filename))
    digest_entries = []
    for filename in review.EXPECTED_OUTPUT_FILENAMES:
        if filename == "execution_digest_manifest.json":
            digest_entries.append(
                {
                    "filename": filename,
                    "digest_kind": review.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                    "sha256": None,
                }
            )
        else:
            digest_entries.append(
                {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": digests[filename]}
            )
    manifest = _common("execution_digest_manifest") | {
        "output_digest_entries": digest_entries,
        "self_reference_policy": review.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "generated_output_count": 15,
    }
    _write_json(output_root / "execution_digest_manifest.json", manifest)


@pytest.fixture(scope="module")
def reviewed_run(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict]:
    root = tmp_path_factory.mktemp("additional-predictive-results")
    _write_fixture_outputs(root)
    package = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=root
    )
    return root, package


def _redigest(package: dict) -> dict:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(
        package["review_checklist"], review_status=package["review_status"]
    )
    package["additional_predictive_evidence_results_review_package_digest"] = (
        review.additional_predictive_evidence_results_review_package_digest_v1(package)
    )
    return package


def test_review_package_builds_offline_without_provider_calls(
    reviewed_run: tuple[Path, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _ = reviewed_run

    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=root
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path) -> None:
    package = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert (
        package["review_status"]
        == review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    assert package["output_file_inspection_performed"] is False
    assert package["additional_predictive_evidence_results_review_created"] is False
    assert package["review_summary"]["blocker_count"] > 0


def test_review_status_is_blocked_for_invalid_json(
    tmp_path: Path,
) -> None:
    root = tmp_path / "outputs"
    _write_fixture_outputs(root)
    (root / "operator_review_summary.json").write_text("not-json", encoding="utf-8")
    package = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=root
    )
    assert package["invalid_output_count"] == 1
    assert package["review_summary"]["blocker_count"] > 0
    assert package["review_status"].endswith("BLOCKED_MISSING_OR_INVALID_OUTPUTS")


def test_review_status_is_blocked_for_digest_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _write_fixture_outputs(root)
    _write_json(root / "operator_review_summary.json", _common("tampered"))
    package = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=root
    )
    assert package["output_digest_manifest_summary"]["digest_mismatch_count"] == 1
    assert package["review_status"].endswith("BLOCKED_MISSING_OR_INVALID_OUTPUTS")


def test_artifact_kind_and_ready_status(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["artifact_kind"] == review.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE
    assert package["review_status"] == review.ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY


def test_all_output_digests_are_bound(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    summary = package["output_digest_manifest_summary"]
    assert len(package["output_file_digests"]) == 15
    assert summary["verified_non_self_digest_count"] == 14
    assert summary["digest_mismatch_count"] == 0
    assert summary["self_reference_valid"] is True
    assert len(package["output_file_digests"]["execution_digest_manifest.json"]) == 64


def test_result_review_summaries_bind_executed_facts(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["label_coverage_entries"] == 84
    assert package["feature_coverage_entries"] == 120
    assert package["walk_forward_review"]["folds"] == review.EXPECTED_WALK_FORWARD_FOLDS
    assert package["baseline_comparison_review"]["baseline_accuracies"] == review.EXPECTED_OOS_BASELINE_ACCURACIES
    assert package["oos_up_vs_not_up_brier_score"] == "0.24875351"
    assert package["leakage_status"] == "PASS"


def test_review_preserves_meta_limitation(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert package["meta_record_count"] == 913
    assert package["non_meta_record_counts_1003_preserved"] is True
    assert package["meta_reduced_record_count_preserved"] is True
    assert package["data_quality_review"]["warning_count"] == 1


def test_checklist_and_summary_are_complete(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == review.PASS for row in package["review_checklist"])
    assert package["review_summary"] == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_predictive_usefulness_reassessment_candidate": True,
        "ready_for_predictive_usefulness_acceptance": False,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_review_digest_is_deterministic(reviewed_run: tuple[Path, dict]) -> None:
    root, first = reviewed_run
    second = review.build_additional_predictive_evidence_results_review_package_v1(
        output_root=root
    )
    assert second == first
    assert len(first["additional_predictive_evidence_results_review_package_digest"]) == 64


def test_validator_accepts_valid_package(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    validation = review.validate_additional_predictive_evidence_results_review_package_v1(
        package
    )
    assert validation["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID"
    assert validation["ready_for_predictive_usefulness_reassessment_candidate"] is True
    assert validation["ready_for_predictive_usefulness_acceptance"] is False


EXPECTED_PACKAGE_FIELDS = [
    ("source_additional_predictive_evidence_execution_digest", review.EXPECTED_SOURCE_EXECUTION_DIGEST),
    ("source_additional_predictive_evidence_execution_approval_digest", review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST),
    ("source_additional_predictive_evidence_execution_candidate_review_package_digest", review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_DIGEST),
    ("research_registry_approval_digest", review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
    ("canonical_dataset_freeze_digest", review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
    ("canonical_dataset_generation_digest", review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
    ("records_digest", review.EXPECTED_RECORDS_DIGEST),
    ("target_universe", review.TARGET_UNIVERSE),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("generated_output_count", 15),
    ("label_family_count", 7),
    ("feature_family_count", 10),
    ("metric_family_count", 9),
    ("baseline_count", 6),
    ("label_generation_digest", review.EXPECTED_LABEL_GENERATION_DIGEST),
    ("feature_generation_digest", review.EXPECTED_FEATURE_GENERATION_DIGEST),
    ("label_available_values", 82854),
    ("label_unavailable_values", 768),
    ("feature_field_count", 22),
    ("feature_rows", 11946),
    ("expected_rolling_window_null_count", 1428),
    ("future_labels_used_as_features", False),
    ("walk_forward_fold_count", 4),
    ("walk_forward_no_shuffle", True),
    ("oos_evaluation_rows", 2988),
    ("leakage_status", "PASS"),
    ("failed_leakage_controls", 0),
    ("provider_requests_made_in_review", False),
    ("live_provider_transport_enabled_in_review", False),
    ("market_data_acquisition_performed_in_review", False),
    ("dataset_generation_performed_in_review", False),
    ("canonical_dataset_regenerated_in_review", False),
    ("predictive_execution_rerun_performed", False),
    ("label_generation_rerun_performed", False),
    ("feature_matrix_rerun_performed", False),
    ("walk_forward_validation_rerun_performed", False),
    ("out_of_sample_evaluation_rerun_performed", False),
    ("baseline_comparison_rerun_performed", False),
    ("metrics_recomputation_performed", False),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True),
    ("label_generation_performed", True),
    ("feature_matrix_generation_performed", True),
    ("walk_forward_validation_performed", True),
    ("out_of_sample_evaluation_performed", True),
    ("baseline_comparison_performed", True),
    ("signal_quality_metrics_performed", True),
    ("stability_analysis_performed", True),
    ("leakage_control_review_performed", True),
    ("predictive_experiment_rerun_performed", True),
    ("new_strategy_scoring_performed", False),
    ("trade_recommendations_generated", False),
    ("predictive_usefulness", review.NOT_ACCEPTED),
    ("predictive_usefulness_acceptance_candidate_created", False),
    ("profitability", review.NOT_ACCEPTED),
    ("runtime_migration_approved", False),
    ("runtime_use", review.NOT_AUTHORIZED),
    ("strategy_use", review.NOT_AUTHORIZED),
    ("paper_trading", review.NOT_AUTHORIZED),
    ("broker_execution", review.NOT_AUTHORIZED),
    ("automatic_stitching", False),
    ("additional_predictive_evidence_results_support_future_reassessment_planning", True),
    ("additional_predictive_evidence_results_create_predictive_usefulness_acceptance", False),
    ("additional_predictive_evidence_results_create_profitability_acceptance", False),
    ("additional_predictive_evidence_results_create_runtime_authority", False),
]


@pytest.mark.parametrize(("field", "expected"), EXPECTED_PACKAGE_FIELDS)
def test_review_package_expected_field(
    reviewed_run: tuple[Path, dict], field: str, expected: object
) -> None:
    _, package = reviewed_run
    assert package[field] == expected


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("review_status", "WRONG"),
    ("source_additional_predictive_evidence_execution_digest", "0" * 64),
    ("source_additional_predictive_evidence_execution_approval_digest", "0" * 64),
    ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
    ("target_universe_count", 11),
    ("total_canonical_record_count", 11945),
    ("records_digest", "0" * 64),
    ("meta_record_count", 914),
    ("generated_output_count", 14),
    ("label_family_count", 6),
    ("feature_family_count", 9),
    ("metric_family_count", 8),
    ("baseline_count", 5),
    ("leakage_status", "FAIL"),
    ("failed_leakage_controls", 1),
    ("provider_requests_made_in_review", True),
    ("live_provider_transport_enabled_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("dataset_generation_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
    ("predictive_execution_rerun_performed", True),
    ("label_generation_rerun_performed", True),
    ("feature_matrix_rerun_performed", True),
    ("walk_forward_validation_rerun_performed", True),
    ("out_of_sample_evaluation_rerun_performed", True),
    ("baseline_comparison_rerun_performed", True),
    ("metrics_recomputation_performed", True),
    ("new_strategy_scoring_performed", True),
    ("trade_recommendations_generated", True),
    ("predictive_usefulness", "accepted"),
    ("predictive_usefulness_acceptance_candidate_created", True),
    ("profitability", "accepted"),
    ("runtime_migration_approved", True),
    ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"),
    ("automatic_stitching", True),
    ("additional_predictive_evidence_results_create_predictive_usefulness_acceptance", True),
    ("additional_predictive_evidence_results_create_profitability_acceptance", True),
    ("additional_predictive_evidence_results_create_runtime_authority", True),
]


@pytest.mark.parametrize(("field", "value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_invalid_field(
    reviewed_run: tuple[Path, dict], field: str, value: object
) -> None:
    _, source = reviewed_run
    package = deepcopy(source)
    package[field] = value
    _redigest(package)
    with pytest.raises(review.AdditionalPredictiveEvidenceResultsReviewError):
        review.validate_additional_predictive_evidence_results_review_package_v1(package)


@pytest.mark.parametrize("field", ["limitations", "next_gates"])
def test_validator_rejects_missing_governance_list(
    reviewed_run: tuple[Path, dict], field: str
) -> None:
    _, source = reviewed_run
    package = deepcopy(source)
    package.pop(field)
    _redigest(package)
    with pytest.raises(review.AdditionalPredictiveEvidenceResultsReviewError):
        review.validate_additional_predictive_evidence_results_review_package_v1(package)


def test_validator_rejects_missing_digest(reviewed_run: tuple[Path, dict]) -> None:
    _, source = reviewed_run
    package = deepcopy(source)
    package.pop("additional_predictive_evidence_results_review_package_digest")
    with pytest.raises(review.AdditionalPredictiveEvidenceResultsReviewError):
        review.validate_additional_predictive_evidence_results_review_package_v1(package)


MARKDOWN_SECTIONS = [
    "Title",
    "Additional Predictive Evidence Results Review Package",
    "Source Predictive Evidence Execution",
    "Registry-Approved Dataset Metadata",
    "Target Universe",
    "Label Generation Review",
    "Feature Generation Review",
    "Walk-Forward Validation Review",
    "Out-of-Sample Evaluation Review",
    "Baseline Comparison Review",
    "Metric and Calibration Review",
    "Stability Review",
    "Leakage-Control Review",
    "Data Quality Review",
    "Output Digest Manifest",
    "Limitations",
    "Next Gates",
    "Predictive Usefulness Boundary",
    "Profitability Boundary",
    "Runtime Boundary",
    "Checklist Summary",
    "Guardrails",
]


@pytest.mark.parametrize("section", MARKDOWN_SECTIONS)
def test_markdown_contains_required_section(
    reviewed_run: tuple[Path, dict], section: str
) -> None:
    _, package = reviewed_run
    markdown = review.build_additional_predictive_evidence_results_review_markdown_v1(
        package
    )
    assert f"## {section}" in markdown


def test_writer_writes_canonical_json_once(
    reviewed_run: tuple[Path, dict], tmp_path: Path
) -> None:
    root, package = reviewed_run
    result = review.write_additional_predictive_evidence_results_review_package_v1(
        tmp_path, output_root=root
    )
    path = Path(result["path"])
    assert path.read_bytes() == canonical_json_bytes(package)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    with pytest.raises(review.AdditionalPredictiveEvidenceResultsReviewError):
        review.write_additional_predictive_evidence_results_review_package_v1(
            tmp_path, output_root=root
        )


@pytest.mark.parametrize("filename", ["review.txt", "../review.json", "folder/review.json"])
def test_writer_rejects_invalid_filename(
    reviewed_run: tuple[Path, dict], tmp_path: Path, filename: str
) -> None:
    root, _ = reviewed_run
    with pytest.raises(review.AdditionalPredictiveEvidenceResultsReviewError):
        review.write_additional_predictive_evidence_results_review_package_v1(
            tmp_path, output_root=root, filename=filename
        )


def test_review_contains_no_forbidden_artifact_names(reviewed_run: tuple[Path, dict]) -> None:
    _, package = reviewed_run
    rendered = json.dumps(package, sort_keys=True)
    for forbidden in (
        "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE\"",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE\"",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS\"",
    ):
        assert forbidden not in rendered
