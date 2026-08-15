from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import feature_label_refinement_results_review_service as review


def _common() -> dict:
    return review.execution._common_output_fields()


def _execution_manifest() -> dict:
    return {
        **_common(),
        "artifact_kind": review.execution.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED,
        "schema_version": review.execution.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_EXECUTED_V1,
        "execution_status": review.execution.FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY,
        "feature_label_refinement_execution_digest": review.EXPECTED_EXECUTION_DIGEST,
        "source_evidence": {
            "feature_label_refinement_execution_approval_digest": review.EXPECTED_EXECUTION_APPROVAL_DIGEST,
            "feature_label_refinement_execution_candidate_review_package_digest": review.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
            "feature_label_refinement_execution_candidate_digest": review.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
            "feature_label_refinement_plan_approval_digest": review.EXPECTED_PLAN_APPROVAL_DIGEST,
            "research_registry_approval_digest": review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
            "canonical_dataset_freeze_digest": review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        },
        "registry_approved_dataset_metadata": deepcopy(
            review.execution.APPROVED_REGISTRY_METADATA
        ),
        "target_universe": list(review.EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(review.EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "refined_label_family_count": 7,
        "refined_feature_group_count": 9,
        "refined_feature_categories_generated": {
            f"category_{index}": [f"feature_{index}"] for index in range(11)
        },
        "refined_protocol_group_count": 6,
        "model_comparison_group_count": 5,
        "generated_output_count": 12,
        "generated_output_names": list(review.EXPECTED_OUTPUT_FILENAMES),
        "refined_walk_forward_summary": {
            "fold_count": 4,
            "evaluation_row_count": 3024,
            "performed": True,
        },
        "refined_metric_summary": {"model_count": 7, "performed": True},
        "model_comparison_summary": {
            "unavailable_model_family_count": 3,
            "performed": True,
        },
        "data_quality_summary": {
            "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        },
        "failure_count": 0,
        "warning_count": 1,
    }


def _fixture_payloads() -> dict[str, dict]:
    common = _common()
    return {
        "feature_label_refinement_execution_manifest.json": _execution_manifest(),
        "refined_label_generation_report.json": {
            **common,
            "coverage_entry_count": 84,
            "available_count": 82698,
            "unavailable_count": 924,
            "refined_label_generation_digest": (
                "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8"
            ),
        },
        "refined_feature_generation_report.json": {
            **common,
            "feature_matrix_row_count": 11946,
            "refined_feature_name_count": 19,
            "total_null_or_unavailable_count": 1128,
            "refined_feature_generation_digest": (
                "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00"
            ),
        },
        "refined_protocol_execution_report.json": {
            **common,
            "no_shuffle": True,
            "no_lookahead_leakage": True,
        },
        "refined_model_comparison_report.json": {
            **common,
            "model_comparison_group_count": 5,
            "deterministic_comparison_ids": [f"comparison_{index}" for index in range(7)],
        },
        "refined_walk_forward_report.json": {**common, "fold_count": 4},
        "refined_out_of_sample_report.json": {
            **common,
            "results": {
                "evaluation_row_count": 2988,
                "model_metrics": {
                    "low": {"accuracy": "0.119813"},
                    "middle": {"accuracy": "0.396252"},
                    "high": {"accuracy": "0.480924"},
                },
            },
        },
        "refined_metric_report.json": {**common, "performed": True},
        "refined_leakage_control_report.json": {
            **common,
            "leakage_control_status": "PASS",
            "failed_control_count": 0,
        },
        "per_ticker_refinement_execution_summary.json": {
            **common,
            "entries": [
                {
                    "ticker": ticker,
                    "canonical_record_count": review.EXPECTED_RECORD_COUNTS[ticker],
                    "meta_reduced_record_count_preserved": ticker == "META",
                }
                for ticker in review.EXPECTED_TARGET_UNIVERSE
            ],
        },
        "operator_review_summary.json": {**common, "failure_count": 0},
    }


def _write_fixture_outputs(root: Path) -> dict[str, str]:
    root.mkdir(parents=True)
    payloads = _fixture_payloads()
    digests: dict[str, str] = {}
    for filename, payload in payloads.items():
        data = canonical_json_bytes(payload)
        (root / filename).write_bytes(data)
        digests[filename] = sha256_bytes(data)
    manifest_name = "feature_label_refinement_execution_digest_manifest.json"
    entries = [
        (
            {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
            if filename == manifest_name
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": digests[filename],
            }
        )
        for filename in review.EXPECTED_OUTPUT_FILENAMES
    ]
    manifest = {
        **_common(),
        "report_name": manifest_name.removesuffix(".json"),
        "generated_output_count": 12,
        "output_digest_entries": entries,
        "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    }
    data = canonical_json_bytes(manifest)
    (root / manifest_name).write_bytes(data)
    digests[manifest_name] = sha256_bytes(data)
    return digests


@pytest.fixture(scope="module")
def output_bundle(tmp_path_factory):
    root = tmp_path_factory.mktemp("refinement_results") / "outputs"
    digests = _write_fixture_outputs(root)
    return root, digests


def _build(root: Path, digests: dict[str, str]) -> dict:
    with (
        patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests),
        patch.object(
            review.execution,
            "validate_feature_label_refinement_executed_v1",
            return_value={"status": review.execution.FEATURE_LABEL_REFINEMENT_EXECUTION_VALID},
        ),
    ):
        return review.build_feature_label_refinement_results_review_package_v1(
            output_root=root
        )


def _validate(package: dict, digests: dict[str, str]) -> dict:
    with patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests):
        return review.validate_feature_label_refinement_results_review_package_v1(
            package
        )


@pytest.fixture(scope="module")
def ready_package(output_bundle) -> dict:
    return _build(*output_bundle)


def test_review_builds_offline_without_provider_calls(
    output_bundle, monkeypatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = _build(*output_bundle)
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_blocks_when_outputs_are_missing(tmp_path) -> None:
    package = review.build_feature_label_refinement_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    assert package["feature_label_refinement_results_review_package_digest"] == (
        "NOT_CREATED"
    )
    assert package["feature_label_refinement_results_review_ready"] is False
    assert review.validate_feature_label_refinement_results_review_package_v1(
        package
    )["status"] == "FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_VALID"


def test_artifact_kind_status_and_schema(ready_package: dict) -> None:
    assert ready_package["artifact_kind"] == (
        review.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE
    )
    assert ready_package["review_status"] == (
        review.FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_PACKAGE_READY
    )
    assert ready_package["schema_version"] == (
        review.SCHEMA_VERSION_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_V1
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("source_feature_label_refinement_execution_digest", review.EXPECTED_EXECUTION_DIGEST),
        ("source_feature_label_refinement_execution_approval_digest", review.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("source_feature_label_refinement_execution_candidate_review_package_digest", review.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("source_research_registry_approval_digest", review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("source_canonical_dataset_freeze_digest", review.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("records_digest", review.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(
    ready_package: dict, field: str, expected: str
) -> None:
    assert ready_package[field] == expected


def test_target_universe_dataset_and_record_counts(ready_package: dict) -> None:
    assert ready_package["target_universe_count"] == 12
    assert ready_package["target_universe"] == review.EXPECTED_TARGET_UNIVERSE
    assert ready_package["total_canonical_record_count"] == 11946
    assert ready_package["meta_record_count"] == 913
    assert ready_package["non_meta_record_count"] == 1003
    assert ready_package["per_ticker_record_counts"] == review.EXPECTED_RECORD_COUNTS
    assert ready_package["registry_approved_dataset_metadata"] == (
        review.execution.APPROVED_REGISTRY_METADATA
    )


def test_outputs_and_local_digests_are_bound(
    ready_package: dict, output_bundle
) -> None:
    _root, digests = output_bundle
    assert ready_package["generated_output_count"] == 12
    assert ready_package["output_digests"] == digests
    assert len(ready_package["output_digest_bindings"]) == 12
    assert all(
        row["verification_status"] == review.PASS
        for row in ready_package["output_digest_bindings"]
    )
    assert ready_package["outputs_research_only_non_actionable"] is True
    assert ready_package["outputs_evidence_scope"] == (
        review.FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY
    )
    assert ready_package["digest_manifest_self_reference_policy"] == (
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    )


def test_refined_label_review_facts_are_bound(ready_package: dict) -> None:
    assert ready_package["refined_label_family_count"] == 7
    assert ready_package["refined_label_generation_review"] == {
        "coverage_entries": 84,
        "available_values": 82698,
        "unavailable_values": 924,
        "refined_label_generation_digest": (
            "04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8"
        ),
        "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
    }


def test_refined_feature_review_facts_are_bound(ready_package: dict) -> None:
    assert ready_package["refined_feature_group_count"] == 9
    assert ready_package["refined_feature_category_count"] == 11
    assert ready_package["refined_feature_field_count"] == 19
    assert ready_package["refined_feature_generation_review"] == {
        "feature_rows": 11946,
        "feature_fields": 19,
        "null_or_unavailable_values": 1128,
        "refined_feature_generation_digest": (
            "35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00"
        ),
        "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
    }


def test_protocol_walk_forward_oos_model_and_leakage_facts(
    ready_package: dict,
) -> None:
    assert ready_package["refined_protocol_group_count"] == 6
    assert ready_package["refined_protocol_review"] == {
        "chronological_splits": True,
        "one_session_embargo": True,
        "no_shuffle": True,
        "no_lookahead": True,
        "result_status": "RESULTS_AVAILABLE_RESEARCH_ONLY",
    }
    assert ready_package["refined_walk_forward_review"]["fold_count"] == 4
    assert ready_package["refined_walk_forward_review"]["evaluation_rows"] == 3024
    assert ready_package["refined_out_of_sample_review"]["evaluation_rows"] == 2988
    assert ready_package["refined_out_of_sample_review"]["accuracy_range"] == (
        "0.119813 to 0.480924"
    )
    assert ready_package["model_comparison_review"]["group_count"] == 5
    assert ready_package["model_comparison_review"][
        "deterministic_comparisons_evaluated"
    ] == 7
    assert ready_package["model_comparison_review"][
        "unavailable_model_family_requests"
    ] == 3
    assert ready_package["model_comparison_review"][
        "unavailable_model_family_status"
    ] == review.execution.NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE
    assert ready_package["refined_leakage_control_review"] == {
        "status": "PASS",
        "failed_controls": 0,
    }


def test_data_quality_and_per_ticker_review(ready_package: dict) -> None:
    assert ready_package["data_quality_review"] == {
        "status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "failure_count": 0,
        "warning_count": 1,
        "warning": "META_REDUCED_RECORD_COUNT_PRESERVED_EXACTLY_913",
    }
    entries = ready_package["per_ticker_results_review_entries"]
    assert [row["ticker"] for row in entries] == review.EXPECTED_TARGET_UNIVERSE
    assert [row["canonical_record_count"] for row in entries] == [
        review.EXPECTED_RECORD_COUNTS[ticker]
        for ticker in review.EXPECTED_TARGET_UNIVERSE
    ]


@pytest.mark.parametrize(
    "field",
    [
        "feature_label_refinement_execution_approved",
        "feature_label_refinement_execution_authorized",
        "feature_label_refinement_executed",
        "feature_label_refinement_results_created",
        "refined_label_generation_authorized",
        "refined_label_generation_performed",
        "refined_feature_generation_authorized",
        "refined_feature_generation_performed",
        "refined_walk_forward_validation_authorized",
        "refined_walk_forward_validation_performed",
        "refined_out_of_sample_evaluation_authorized",
        "refined_out_of_sample_evaluation_performed",
        "refined_metrics_recomputation_authorized",
        "refined_metrics_recomputation_performed",
        "model_comparison_authorized",
        "model_comparison_performed",
        "feature_label_refinement_results_review_created",
        "feature_label_refinement_results_review_ready",
        "feature_label_refinement_results_support_future_additional_predictive_evidence_planning",
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence",
        "refinement_results_support_future_additional_predictive_evidence_planning",
    ],
)
def test_execution_review_and_future_planning_states_are_true(
    ready_package: dict, field: str
) -> None:
    assert ready_package[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "feature_label_refinement_execution_rerun_performed",
        "refined_label_generation_rerun_performed",
        "refined_feature_generation_rerun_performed",
        "refined_walk_forward_validation_rerun_performed",
        "refined_out_of_sample_evaluation_rerun_performed",
        "refined_metrics_recomputation_rerun_performed",
        "model_comparison_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "refinement_results_create_additional_predictive_evidence_execution_candidate",
        "refinement_results_create_predictive_usefulness_acceptance",
        "refinement_results_create_profitability_acceptance",
        "refinement_results_create_runtime_authority",
        "refinement_results_create_trade_recommendations",
    ],
)
def test_review_reruns_and_downstream_authorities_remain_false(
    ready_package: dict, field: str
) -> None:
    assert ready_package[field] is False


def test_predictive_profitability_runtime_boundaries(ready_package: dict) -> None:
    assert ready_package["predictive_usefulness"] == review.NOT_ACCEPTED
    assert ready_package["profitability"] == review.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert ready_package[field] == review.NOT_AUTHORIZED


def test_limitations_next_gates_checklist_and_summary(ready_package: dict) -> None:
    assert ready_package["limitations"] == review.LIMITATIONS
    assert ready_package["next_gates"] == review.NEXT_GATES
    checklist = ready_package["review_checklist"]
    assert [row["check_id"] for row in checklist] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == review.PASS for row in checklist)
    assert all(row["severity"] == review.BLOCKER for row in checklist)
    assert ready_package["review_summary"] == {
        "total_checks": 80,
        "passed_checks": 80,
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_additional_predictive_evidence_execution_candidate_for_refined_evidence": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_review_package_digest_is_deterministic(output_bundle) -> None:
    first = _build(*output_bundle)
    second = _build(*output_bundle)
    assert first["feature_label_refinement_results_review_package_digest"] == second[
        "feature_label_refinement_results_review_package_digest"
    ]
    assert first["feature_label_refinement_results_review_package_digest"] == (
        review.feature_label_refinement_results_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_package(ready_package: dict, output_bundle) -> None:
    _root, digests = output_bundle
    assert _validate(deepcopy(ready_package), digests)["status"] == (
        review.FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_VALID
    )


@pytest.mark.parametrize(
    "path,bad_value",
    [
        (("artifact_kind",), "WRONG"),
        (("review_status",), "WRONG"),
        (("source_feature_label_refinement_execution_digest",), "0" * 64),
        (("source_feature_label_refinement_execution_approval_digest",), "0" * 64),
        (("target_universe",), ["MSFT"]),
        (("target_universe_count",), 11),
        (("total_canonical_record_count",), 11945),
        (("records_digest",), "0" * 64),
        (("meta_record_count",), 1003),
        (("per_ticker_record_counts", "MSFT"), 1002),
        (("generated_output_count",), 11),
        (("refined_label_family_count",), 6),
        (("refined_feature_group_count",), 8),
        (("refined_feature_field_count",), 18),
        (("refined_protocol_group_count",), 5),
        (("model_comparison_group_count",), 4),
        (("refined_label_generation_review", "refined_label_generation_digest"), "0" * 64),
        (("refined_feature_generation_review", "refined_feature_generation_digest"), "0" * 64),
        (("refined_walk_forward_review", "fold_count"), 3),
        (("refined_out_of_sample_review", "evaluation_rows"), 2987),
        (("refined_leakage_control_review", "status"), "FAIL"),
        (("refined_leakage_control_review", "failed_controls"), 1),
        (("provider_requests_made_in_review",), True),
        (("live_provider_transport_enabled_in_review",), True),
        (("market_data_acquisition_performed_in_review",), True),
        (("dataset_generation_performed_in_review",), True),
        (("canonical_dataset_regenerated_in_review",), True),
        (("feature_label_refinement_execution_rerun_performed",), True),
        (("refined_label_generation_rerun_performed",), True),
        (("refined_feature_generation_rerun_performed",), True),
        (("refined_metrics_recomputation_rerun_performed",), True),
        (("model_comparison_rerun_performed",), True),
        (("additional_predictive_evidence_execution_candidate_created",), True),
        (("new_strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness",), "accepted"),
        (("predictive_usefulness_acceptance_candidate_created",), True),
        (("profitability",), "accepted"),
        (("runtime_use",), "AUTHORIZED"),
        (("strategy_use",), "AUTHORIZED"),
        (("paper_trading",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("refinement_results_create_additional_predictive_evidence_execution_candidate",), True),
    ],
)
def test_validator_rejects_contract_mutations(
    ready_package: dict,
    output_bundle,
    path: tuple[str, ...],
    bad_value,
) -> None:
    _root, digests = output_bundle
    mutated = deepcopy(ready_package)
    target = mutated
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(review.FeatureLabelRefinementResultsReviewError):
        _validate(mutated, digests)


@pytest.mark.parametrize("field", ["limitations", "next_gates"])
def test_validator_rejects_missing_governance_lists(
    ready_package: dict, output_bundle, field: str
) -> None:
    _root, digests = output_bundle
    mutated = deepcopy(ready_package)
    mutated.pop(field)
    with pytest.raises(review.FeatureLabelRefinementResultsReviewError):
        _validate(mutated, digests)


def test_validator_rejects_missing_review_digest(
    ready_package: dict, output_bundle
) -> None:
    _root, digests = output_bundle
    mutated = deepcopy(ready_package)
    mutated.pop("feature_label_refinement_results_review_package_digest")
    with pytest.raises(review.FeatureLabelRefinementResultsReviewError):
        _validate(mutated, digests)


def test_changed_output_blocks_review(tmp_path) -> None:
    root = tmp_path / "outputs"
    digests = _write_fixture_outputs(root)
    (root / "refined_metric_report.json").write_text("{}", encoding="utf-8")
    with (
        patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests),
        patch.object(
            review.execution,
            "validate_feature_label_refinement_executed_v1",
            return_value={"status": review.execution.FEATURE_LABEL_REFINEMENT_EXECUTION_VALID},
        ),
    ):
        package = review.build_feature_label_refinement_results_review_package_v1(
            output_root=root
        )
    assert package["review_status"] == (
        review.FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )


def test_markdown_contains_required_sections(ready_package: dict, output_bundle) -> None:
    _root, digests = output_bundle
    with patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests):
        markdown = review.build_feature_label_refinement_results_review_markdown_v1(
            ready_package
        )
    for heading in (
        "Feature/Label Refinement Results Review Package",
        "Source Feature/Label Refinement Execution",
        "Registry-Approved Dataset Metadata",
        "Target Universe",
        "Refined Label Generation Review",
        "Refined Feature Generation Review",
        "Refined Protocol Review",
        "Refined Walk-Forward Review",
        "Refined OOS Review",
        "Refined Metrics Review",
        "Model Comparison Review",
        "Refined Leakage-Control Review",
        "Data Quality Review",
        "Output Digest Manifest",
        "Limitations",
        "Next Gates",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_uses_canonical_json_and_refuses_overwrite(
    tmp_path, output_bundle
) -> None:
    root, digests = output_bundle
    with (
        patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests),
        patch.object(
            review.execution,
            "validate_feature_label_refinement_executed_v1",
            return_value={"status": review.execution.FEATURE_LABEL_REFINEMENT_EXECUTION_VALID},
        ),
    ):
        receipt = review.write_feature_label_refinement_results_review_package_v1(
            tmp_path / "review", output_root=root
        )
        path = Path(receipt["path"])
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert path.read_bytes() == canonical_json_bytes(parsed)
        with pytest.raises(review.FeatureLabelRefinementResultsReviewError):
            review.write_feature_label_refinement_results_review_package_v1(
                tmp_path / "review", output_root=root
            )


@pytest.mark.parametrize("filename", ["../review.json", "review.txt"])
def test_writer_rejects_unsafe_filename(
    tmp_path, output_bundle, filename: str
) -> None:
    root, digests = output_bundle
    with (
        patch.object(review, "EXPECTED_OUTPUT_DIGESTS", digests),
        patch.object(
            review.execution,
            "validate_feature_label_refinement_executed_v1",
            return_value={"status": review.execution.FEATURE_LABEL_REFINEMENT_EXECUTION_VALID},
        ),
        pytest.raises(review.FeatureLabelRefinementResultsReviewError),
    ):
        review.write_feature_label_refinement_results_review_package_v1(
            tmp_path / "review", output_root=root, filename=filename
        )
