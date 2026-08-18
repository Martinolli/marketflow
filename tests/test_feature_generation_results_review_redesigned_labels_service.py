from __future__ import annotations

from copy import deepcopy
import shutil

import pytest

from marketflow import services
from marketflow.services import feature_generation_execution_redesigned_labels_service as execution
from marketflow.services import feature_generation_results_review_redesigned_labels_service as review


@pytest.fixture(scope="module")
def reviewed(tmp_path_factory) -> tuple[dict, object]:
    output_root = tmp_path_factory.mktemp("feature_generation_results_review") / "outputs"
    artifact = execution.execute_feature_generation_using_redesigned_labels_v1(
        output_root=output_root,
        run_timestamp_utc="2026-08-18T17:06:43.758924Z",
    )
    assert artifact["feature_generation_execution_digest"] == review.EXPECTED_EXECUTION_DIGEST
    package = review.build_feature_generation_results_review_using_redesigned_labels_v1(
        output_root=output_root
    )
    return package, output_root


def test_review_package_builds_offline(reviewed, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    _, output_root = reviewed
    package = review.build_feature_generation_results_review_using_redesigned_labels_v1(
        output_root=output_root
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_blocks_when_output_root_is_missing(tmp_path) -> None:
    package = review.build_feature_generation_results_review_using_redesigned_labels_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["feature_generation_results_review_ready"] is False
    assert package["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is False
    assert package["blocker_count"] == 12


def test_review_blocks_when_output_digest_verification_fails(reviewed, tmp_path) -> None:
    _, output_root = reviewed
    copied_root = tmp_path / "outputs"
    shutil.copytree(output_root, copied_root)
    input_manifest = copied_root / "feature_generation_input_manifest.json"
    input_manifest.write_text(
        input_manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8"
    )
    package = review.build_feature_generation_results_review_using_redesigned_labels_v1(
        output_root=copied_root
    )
    assert package["review_status"] == review.FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS
    assert package["feature_generation_results_review_ready"] is False
    assert any(
        reason["failure_id"] == "digest_manifest_entry_mismatch"
        for reason in package["blocker_reasons"]
    )


def test_artifact_kind_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["artifact_kind"] == "FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS"


def test_review_status_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["review_status"] == "FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_feature_generation_execution_digest", review.EXPECTED_EXECUTION_DIGEST),
        ("source_feature_values_digest", review.EXPECTED_FEATURE_VALUES_DIGEST),
        ("source_feature_generation_approval_digest", execution.EXPECTED_APPROVAL_DIGEST),
        ("source_feature_generation_candidate_review_digest", execution.approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("source_feature_generation_candidate_digest", execution.approval_service.EXPECTED_CANDIDATE_DIGEST),
        ("source_feature_predictive_evidence_planning_approval_digest", execution.approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("source_redesigned_label_results_review_digest", execution.approval_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("source_redesigned_label_execution_digest", execution.approval_service.EXPECTED_EXECUTION_DIGEST),
        ("source_redesigned_label_approval_digest", execution.approval_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST),
        ("source_research_registry_approval_digest", execution.approval_service.EXPECTED_RESEARCH_REGISTRY_DIGEST),
        ("records_digest", execution.EXPECTED_RECORDS_DIGEST),
        ("label_values_digest", execution.EXPECTED_LABEL_VALUES_DIGEST),
    ],
)
def test_source_digest_is_bound(reviewed, field: str, expected: str) -> None:
    package, _ = reviewed
    assert package[field] == expected


def test_universe_count_and_order_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["target_universe_count"] == 12
    assert package["target_universe"] == execution.TARGET_UNIVERSE


def test_meta_913_is_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_generated_output_count_is_twelve(reviewed) -> None:
    package, _ = reviewed
    assert package["generated_output_count"] == 12
    assert package["generated_output_names"] == execution.OUTPUT_FILENAMES


def test_output_digests_are_bound(reviewed) -> None:
    package, _ = reviewed
    assert list(package["output_digests"]) == execution.OUTPUT_FILENAMES
    assert package["local_output_digest_count"] == 12
    assert package["recorded_file_digest_match_count"] == 11
    assert package["output_digest_mismatch_count"] == 0
    assert package["digest_manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"


def test_outputs_are_research_only_nonactionable(reviewed) -> None:
    package, _ = reviewed
    assert package["outputs_research_only_non_actionable"] is True
    assert package["outputs_evidence_scope"] == "FEATURE_GENERATION_USING_REDESIGNED_LABELS_RESEARCH_ONLY"


@pytest.mark.parametrize(
    "field",
    [
        "feature_values_review",
        "feature_family_coverage_review",
        "feature_group_generation_review",
        "feature_schema_contract_review",
        "feature_label_alignment_review",
        "feature_quality_review",
        "per_ticker_feature_summary_review",
        "meta_limitation_feature_handling_review",
    ],
)
def test_required_feature_output_is_verified(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field]["available"] is True
    assert package[field]["verified"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_family_count", 10),
        ("feature_group_count", 17),
        ("feature_schema_field_count", 16),
        ("feature_value_row_count", 203082),
        ("available_feature_value_count", 190848),
        ("unavailable_feature_value_count", 12234),
        ("non_meta_feature_rows_per_ticker", 17051),
        ("meta_feature_rows", 15521),
    ],
)
def test_exact_feature_output_fact(reviewed, field: str, expected: int) -> None:
    package, _ = reviewed
    assert package[field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("history_only_policy_preserved", True),
        ("future_label_values_used_as_features", False),
        ("label_values_used_as_features", False),
        ("forward_returns_used_as_features", False),
        ("threshold_values_used_as_numeric_predictors", False),
        ("baseline_error_context_computed_from_labels", False),
    ],
)
def test_feature_label_alignment_boundary(reviewed, field: str, expected: bool) -> None:
    package, _ = reviewed
    assert package["feature_label_alignment_review"][field] is expected


def test_baseline_error_context_is_unavailable_by_design(reviewed) -> None:
    package, _ = reviewed
    assert package["feature_quality_review"]["baseline_error_context_unavailable_by_design"] is True
    assert package["feature_quality_review"]["unavailable_feature_values_recorded"] is True


def test_results_review_created_and_ready_are_true(reviewed) -> None:
    package, _ = reviewed
    assert package["feature_generation_results_review_created"] is True
    assert package["feature_generation_results_review_ready"] is True


def test_ready_for_future_predictive_evidence_candidate_is_true(reviewed) -> None:
    package, _ = reviewed
    assert package["ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is True
    assert package["results_support_future_additional_predictive_evidence_execution_candidate_using_redesigned_labels"] is True


@pytest.mark.parametrize(
    "field",
    [
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "trade_recommendations_generated",
        "new_strategy_scoring_performed",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "redesigned_label_regeneration_performed",
        "feature_generation_rerun_performed",
        "feature_regeneration_performed",
    ],
)
def test_closed_action_remains_false(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] is False


def test_predictive_usefulness_remains_not_accepted(reviewed) -> None:
    package, _ = reviewed
    assert package["predictive_usefulness"] == "not accepted"
    assert package["predictive_usefulness_acceptance_ready"] is False
    assert package["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_remains_not_accepted(reviewed) -> None:
    package, _ = reviewed
    assert package["profitability"] == "not accepted"
    assert package["profitability_acceptance_ready"] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_and_trading_authority_remains_closed(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] == "NOT_AUTHORIZED"


def test_limitations_are_recorded(reviewed) -> None:
    package, _ = reviewed
    assert package["limitations"] == review.LIMITATIONS


def test_next_chain_and_gates_are_defined(reviewed) -> None:
    package, _ = reviewed
    assert package["next_chain"] == review.NEXT_CHAIN
    assert package["next_gates"] == review.NEXT_GATES


def test_risk_controls_are_defined(reviewed) -> None:
    package, _ = reviewed
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_checklist_passes(reviewed) -> None:
    package, _ = reviewed
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in package["review_checklist"])
    assert all(row["status"] == "PASS" for row in package["review_checklist"])
    assert package["review_summary"]["blocker_count"] == 0
    assert package["review_summary"]["passed_checks"] == len(review.REQUIRED_CHECK_IDS)


def test_review_digest_is_deterministic(reviewed) -> None:
    package, _ = reviewed
    first = review.feature_generation_results_review_using_redesigned_labels_digest_v1(package)
    second = review.feature_generation_results_review_using_redesigned_labels_digest_v1(deepcopy(package))
    assert first == second == package["feature_generation_results_review_using_redesigned_labels_digest"]


def test_validator_accepts_valid_package(reviewed) -> None:
    package, _ = reviewed
    result = review.validate_feature_generation_results_review_using_redesigned_labels_v1(deepcopy(package))
    assert result["status"] == "FEATURE_GENERATION_RESULTS_REVIEW_USING_REDESIGNED_LABELS_VALID"
    assert result["runtime_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_feature_generation_execution_digest", "0" * 64),
        ("source_feature_values_digest", "0" * 64),
        ("source_feature_generation_approval_digest", "0" * 64),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("label_values_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("generated_output_count", 11),
        ("feature_family_count", 9),
        ("feature_group_count", 16),
        ("feature_schema_field_count", 15),
        ("feature_value_row_count", 203081),
        ("available_feature_value_count", 190847),
        ("unavailable_feature_value_count", 12233),
        ("feature_values_digest", "0" * 64),
        ("feature_generation_results_review_ready", False),
        ("ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels", False),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_executed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("feature_generation_rerun_performed", True),
    ],
)
def test_validator_rejects_invalid_boundary(reviewed, field: str, value) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed[field] = value
    with pytest.raises(review.FeatureGenerationResultsReviewRedesignedLabelsError):
        review.validate_feature_generation_results_review_using_redesigned_labels_v1(changed)


@pytest.mark.parametrize("field", ["limitations", "next_chain", "risk_controls"])
def test_validator_rejects_missing_governance_section(reviewed, field: str) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop(field)
    with pytest.raises(review.FeatureGenerationResultsReviewRedesignedLabelsError):
        review.validate_feature_generation_results_review_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_review_digest(reviewed) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop("feature_generation_results_review_using_redesigned_labels_digest")
    with pytest.raises(review.FeatureGenerationResultsReviewRedesignedLabelsError):
        review.validate_feature_generation_results_review_using_redesigned_labels_v1(changed)


def test_markdown_includes_required_sections(reviewed) -> None:
    package, _ = reviewed
    markdown = review.build_feature_generation_results_review_using_redesigned_labels_markdown_v1(package)
    sections = [
        "Title", "Feature Generation Results Review Using Redesigned Labels", "Source Execution",
        "Dataset and Universe", "Source Redesigned Label Profile", "Generated Feature Outputs",
        "Feature Family Coverage Review", "Feature Group Review", "Feature Schema Contract Review",
        "Feature / Label Alignment Review", "Feature Quality Review", "Per-Ticker Feature Summary",
        "META Limitation Preservation Review", "Output Digest Manifest", "Limitations", "Next Chain",
        "Next Gates", "Risk Controls", "Predictive Evidence Boundary", "Predictive Usefulness Boundary",
        "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)


def test_writer_writes_one_package_without_overwrite(reviewed, tmp_path) -> None:
    _, output_root = reviewed
    result = review.write_feature_generation_results_review_using_redesigned_labels_v1(
        tmp_path, output_root=output_root
    )
    assert result["review_status"] == review.FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY
    assert (tmp_path / result["filename"]).is_file()
    with pytest.raises(review.FeatureGenerationResultsReviewRedesignedLabelsError):
        review.write_feature_generation_results_review_using_redesigned_labels_v1(
            tmp_path, output_root=output_root
        )


def test_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS == review.ARTIFACT_KIND_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS
    assert services.build_feature_generation_results_review_using_redesigned_labels_v1 is review.build_feature_generation_results_review_using_redesigned_labels_v1
    assert services.validate_feature_generation_results_review_using_redesigned_labels_v1 is review.validate_feature_generation_results_review_using_redesigned_labels_v1
