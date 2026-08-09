from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_experiment_execution_results_review_service as review


def _boundary() -> dict[str, str]:
    return {
        "output_label": review.RESEARCH_ONLY_NON_ACTIONABLE,
        "runtime_use": review.NOT_AUTHORIZED,
        "strategy_use": review.NOT_AUTHORIZED,
        "paper_trading": review.NOT_AUTHORIZED,
        "broker_execution": review.NOT_AUTHORIZED,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
    }


def _payload(name: str) -> dict[str, Any]:
    payload: dict[str, Any] = {"report_name": name, **_boundary()}
    if name == "label_generation_report":
        payload.update(
            {
                "label_generation_performed": True,
                "labels_forward_looking_only": True,
                "datasets": [
                    {
                        "dataset_profile": "POSITION_SWING",
                        "row_count": 6,
                        "available_label_count": 5,
                        "unavailable_label_count": 1,
                    },
                    {
                        "dataset_profile": "SWING",
                        "row_count": 6,
                        "available_label_count": 5,
                        "unavailable_label_count": 1,
                    },
                ],
            }
        )
    elif name == "feature_matrix_manifest":
        payload.update(
            {
                "feature_matrix_generation_performed": True,
                "feature_names": review.execution.FEATURE_NAMES,
                "datasets": [
                    {"dataset_profile": "POSITION_SWING", "feature_count": 6, "feature_row_count": 6},
                    {"dataset_profile": "SWING", "feature_count": 6, "feature_row_count": 6},
                ],
            }
        )
    elif name == "walk_forward_configuration_report":
        payload.update(
            {
                "metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
                "walk_forward_validation_performed": True,
                "walk_forward_type": review.execution.SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT,
                "shuffle": False,
                "baselines": review.execution.BASELINES,
            }
        )
    elif name == "out_of_sample_split_report":
        payload.update(
            {
                "out_of_sample_evaluation_performed": True,
                "chronological": True,
                "shuffle": False,
            }
        )
    elif name == "baseline_comparison_report":
        payload.update(
            {
                "metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
                "baselines": review.execution.BASELINES,
                "results": {
                    "POSITION_SWING": {baseline: {"metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE} for baseline in review.execution.BASELINES},
                    "SWING": {baseline: {"metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE} for baseline in review.execution.BASELINES},
                },
            }
        )
    elif name == "signal_quality_metrics_report":
        payload.update(
            {
                "metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
                "predictive_usefulness_acceptance_ready": False,
                "profitability_acceptance_ready": False,
                "results": {
                    "POSITION_SWING": {baseline: {"metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE} for baseline in review.execution.BASELINES},
                    "SWING": {baseline: {"metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE} for baseline in review.execution.BASELINES},
                },
            }
        )
    elif name in {
        "stability_analysis_report",
        "false_positive_false_negative_report",
    }:
        payload["metrics_label"] = review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    elif name == "leakage_control_report":
        payload.update(
            {
                "leakage_control_status": "PASS",
                "controls": [{"control": "chronological_splits_only", "status": "PASS"}],
            }
        )
    elif name == "operator_review_summary":
        payload.update(
            {
                "metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
                "execution_status": review.execution.PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
                "execution_request_id": review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
                "generated_output_count": review.EXPECTED_OUTPUT_COUNT,
                "runtime_migration_active": False,
            }
        )
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _write_fixture_outputs(output_root: Path) -> None:
    digests: dict[str, str] = {}
    for name in review.EXPECTED_OUTPUT_NAMES:
        if name == "predictive_experiment_run_manifest":
            continue
        digests[name] = _write_json(output_root / f"{name}.json", _payload(name))
    manifest = {
        "report_name": "predictive_experiment_run_manifest",
        **_boundary(),
        "metrics_label": review.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "execution_request_id": review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID,
        "source_digests": {
            "predictive_experiment_execution_approval_digest": (
                review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
            ),
            "execution_candidate_digest": review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_DIGEST,
            "execution_candidate_review_package_digest": (
                review.EXPECTED_SOURCE_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
            ),
        },
        "output_digests": {**digests, "predictive_experiment_run_manifest": "self"},
    }
    _write_json(output_root / "predictive_experiment_run_manifest.json", manifest)


def _package(tmp_path: Path) -> dict[str, Any]:
    output_root = tmp_path / "predictive_outputs"
    _write_fixture_outputs(output_root)
    return review.build_predictive_experiment_execution_results_review_package_v1(
        output_root=output_root
    )


def _redigest(package: dict[str, Any]) -> dict[str, Any]:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(
        package["review_checklist"],
        review_status=package["review_status"],
    )
    package["predictive_experiment_execution_results_review_package_digest"] = (
        review.predictive_experiment_execution_results_review_package_digest_v1(package)
    )
    return package


def test_review_package_builds_offline_without_provider_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("predictive experiment execution must not be rerun")

    monkeypatch.setattr(review.execution, "execute_predictive_experiment_v1", fail_if_called)

    assert _package(tmp_path)["provider_requests_made_in_review"] is False


def test_artifact_kind_is_predictive_execution_results_review_package(tmp_path: Path):
    assert _package(tmp_path)["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE
    )


def test_review_status_is_ready_when_fixture_outputs_are_present(tmp_path: Path):
    assert _package(tmp_path)["review_status"] == (
        review.PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_READY
    )


def test_review_status_is_blocked_when_outputs_are_missing(tmp_path: Path):
    package = review.build_predictive_experiment_execution_results_review_package_v1(
        output_root=tmp_path / "missing"
    )

    assert package["review_status"] == (
        review.PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
    )
    assert package["output_file_inspection_performed"] is False


def test_execution_digest_is_bound(tmp_path: Path):
    assert _package(tmp_path)["source_execution_digest"] == review.EXPECTED_SOURCE_EXECUTION_DIGEST


def test_execution_request_id_is_bound(tmp_path: Path):
    assert _package(tmp_path)["source_execution_request_id"] == (
        review.EXPECTED_SOURCE_EXECUTION_REQUEST_ID
    )


def test_approval_digest_is_bound(tmp_path: Path):
    assert _package(tmp_path)["source_execution_approval_digest"] == (
        review.EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST
    )


def test_output_count_is_thirteen(tmp_path: Path):
    package = _package(tmp_path)

    assert package["expected_output_count"] == 13
    assert package["actual_output_count"] == 13


def test_all_outputs_are_labeled_research_only(tmp_path: Path):
    assert _package(tmp_path)["all_outputs_research_only_non_actionable"] is True


def test_metrics_are_labeled_research_only_not_performance_acceptance(tmp_path: Path):
    assert _package(tmp_path)["metrics_labeled_research_only_not_performance_acceptance"] is True


def test_label_generation_is_confirmed_true(tmp_path: Path):
    assert _package(tmp_path)["labels_generated"] is True


def test_feature_matrix_generation_is_confirmed_true(tmp_path: Path):
    assert _package(tmp_path)["feature_matrices_generated"] is True


def test_walk_forward_result_generation_is_confirmed_true(tmp_path: Path):
    assert _package(tmp_path)["walk_forward_result_generated"] is True


def test_oos_result_generation_is_confirmed_true(tmp_path: Path):
    assert _package(tmp_path)["out_of_sample_result_generated"] is True


def test_no_trade_recommendation_fields_exist(tmp_path: Path):
    assert _package(tmp_path)["trade_recommendations_present"] is False


def test_no_runtime_authorization_exists_in_outputs(tmp_path: Path):
    assert _package(tmp_path)["runtime_authorization_present_in_outputs"] is False


def test_no_strategy_authorization_exists_in_outputs(tmp_path: Path):
    assert _package(tmp_path)["strategy_authorization_present_in_outputs"] is False


def test_no_broker_authorization_exists_in_outputs(tmp_path: Path):
    assert _package(tmp_path)["broker_authorization_present_in_outputs"] is False


def test_predictive_usefulness_remains_not_accepted(tmp_path: Path):
    assert _package(tmp_path)["predictive_usefulness"] == "not accepted"


def test_predictive_usefulness_acceptance_ready_remains_false(tmp_path: Path):
    assert _package(tmp_path)["predictive_usefulness_acceptance_ready"] is False


def test_profitability_remains_not_accepted(tmp_path: Path):
    assert _package(tmp_path)["profitability"] == "not accepted"


def test_profitability_acceptance_ready_remains_false(tmp_path: Path):
    assert _package(tmp_path)["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "experiment_reexecution_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
    ],
)
def test_guardrail_boolean_fields_remain_false(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_authorization_fields_remain_not_authorized(tmp_path: Path, field: str):
    assert _package(tmp_path)[field] == review.NOT_AUTHORIZED


def test_checklist_contains_all_required_check_ids(tmp_path: Path):
    package = _package(tmp_path)

    assert [item["check_id"] for item in package["review_checklist"]] == review.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_valid_fixture_outputs(tmp_path: Path):
    package = _package(tmp_path)

    assert {item["status"] for item in package["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_and_failed_correctly(tmp_path: Path):
    package = _package(tmp_path)

    assert package["review_summary"]["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert package["review_summary"]["failed_checks"] == 0
    assert package["review_summary"]["blocker_count"] == 0


def test_review_package_digest_is_deterministic(tmp_path: Path):
    output_root = tmp_path / "predictive_outputs"
    _write_fixture_outputs(output_root)

    first = review.build_predictive_experiment_execution_results_review_package_v1(
        output_root=output_root
    )
    second = review.build_predictive_experiment_execution_results_review_package_v1(
        output_root=output_root
    )

    assert first["predictive_experiment_execution_results_review_package_digest"] == (
        second["predictive_experiment_execution_results_review_package_digest"]
    )


def test_validator_accepts_valid_review_package(tmp_path: Path):
    validation = review.validate_predictive_experiment_execution_results_review_package_v1(
        _package(tmp_path)
    )

    assert validation["status"] == "PREDICTIVE_EXPERIMENT_EXECUTION_RESULTS_REVIEW_PACKAGE_VALID"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("actual_output_count", 12),
        ("all_outputs_research_only_non_actionable", False),
        ("metrics_labeled_research_only_not_performance_acceptance", False),
        ("provider_requests_made_in_review", True),
        ("experiment_reexecution_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("profitability", "accepted"),
        ("runtime_migration_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_forbidden_or_inconsistent_values(
    tmp_path: Path,
    field: str,
    value: Any,
):
    package = deepcopy(_package(tmp_path))
    package[field] = value
    if field not in {
        "provider_requests_made_in_review",
        "experiment_reexecution_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness",
        "predictive_usefulness_acceptance_ready",
        "profitability",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_use",
        "strategy_use",
        "paper_trading",
        "broker_execution",
    }:
        _redigest(package)

    with pytest.raises(review.PredictiveExperimentExecutionResultsReviewError):
        review.validate_predictive_experiment_execution_results_review_package_v1(package)


def test_validator_rejects_missing_review_package_digest(tmp_path: Path):
    package = _package(tmp_path)
    package.pop("predictive_experiment_execution_results_review_package_digest")

    with pytest.raises(review.PredictiveExperimentExecutionResultsReviewError):
        review.validate_predictive_experiment_execution_results_review_package_v1(package)


def test_markdown_writer_includes_required_sections(tmp_path: Path):
    markdown = review.build_predictive_experiment_execution_results_review_markdown_v1(
        _package(tmp_path)
    )

    for section in [
        "## Title",
        "## Reviewed Predictive Experiment Execution",
        "## Output Summary",
        "## Label and Feature Matrix Summary",
        "## Walk-Forward / OOS Summary",
        "## Baseline and Metrics Summary",
        "## Leakage Controls Summary",
        "## Failure/Warning Inventory",
        "## Predictive/Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert section in markdown
