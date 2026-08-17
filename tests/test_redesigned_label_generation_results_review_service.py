from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal
import json
from unittest.mock import patch

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import redesigned_label_generation_execution_service as execution
from marketflow.services import redesigned_label_generation_results_review_service as review


FIXED_TIMESTAMP = "2026-08-17T12:00:00Z"


def _business_dates(count: int) -> list[str]:
    result: list[str] = []
    current = date(2022, 1, 3)
    while len(result) < count:
        if current.weekday() < 5:
            result.append(current.isoformat())
        current += timedelta(days=1)
    return result


def _records() -> list[dict]:
    dates = _business_dates(1003)
    rows: list[dict] = []
    for ticker_index, ticker in enumerate(execution.TARGET_UNIVERSE, start=1):
        ticker_dates = dates[90:] if ticker == "META" else dates
        for index, value in enumerate(ticker_dates):
            close = Decimal(100 + ticker_index * 7) * (Decimal("1.0004") ** index)
            close += Decimal((index % 11) - 5) / Decimal(100)
            rows.append({"ticker": ticker, "date": value, "close": str(close)})
    return rows


def _canonical_verification() -> dict:
    return {
        "source_root": "isolated/canonical",
        "required_source_file_count": 9,
        "required_source_files": list(execution.CANONICAL_SOURCE_FILENAMES),
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "total_record_count_actual": 11946,
        "per_ticker_record_counts_actual": deepcopy(execution.EXPECTED_RECORD_COUNTS),
    }


def _design_verification() -> dict:
    return {
        "design_root": "isolated/design",
        "required_design_source_file_count": 8,
        "required_design_source_files": list(execution.DESIGN_SOURCE_FILENAMES),
        "label_objective_redesign_execution_digest": execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST,
        "source_label_objective_redesign_output_count": 8,
        "source_label_objective_redesign_output_status": "REVIEWED_AND_VERIFIED",
        "design_source_digests": [],
    }


def _execute(output_root) -> dict:
    source_result = (
        _canonical_verification(),
        _design_verification(),
        _records(),
        [],
    )
    with patch.object(execution, "_load_and_verify_sources", return_value=source_result):
        return execution.execute_redesigned_label_generation_v1(
            canonical_root=output_root.parent / "canonical",
            design_root=output_root.parent / "design",
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


@pytest.fixture(scope="module")
def reviewed(tmp_path_factory):
    output_root = tmp_path_factory.mktemp("redesigned_label_results_review") / "outputs"
    artifact = _execute(output_root)
    fixture_execution_digest = artifact["redesigned_label_generation_execution_digest"]
    fixture_digest = sha256_file(output_root / "redesigned_label_values.jsonl")
    threshold_payload = json.loads(
        (output_root / "redesigned_threshold_generation_report.json").read_text(
            encoding="utf-8"
        )
    )
    original_execution_digest = review.EXPECTED_EXECUTION_DIGEST
    original_source_execution_digest = review.SOURCE_EVIDENCE[
        "redesigned_label_generation_execution_digest"
    ]
    original_digest = review.EXPECTED_LABEL_VALUES_DIGEST
    original_source_digest = review.SOURCE_EVIDENCE["label_values_digest"]
    original_global_threshold = review.GLOBAL_FIVE_SESSION_THRESHOLD
    original_benchmark_threshold = review.BENCHMARK_RELATIVE_THRESHOLD
    review.EXPECTED_EXECUTION_DIGEST = fixture_execution_digest
    review.SOURCE_EVIDENCE[
        "redesigned_label_generation_execution_digest"
    ] = fixture_execution_digest
    review.EXPECTED_LABEL_VALUES_DIGEST = fixture_digest
    review.SOURCE_EVIDENCE["label_values_digest"] = fixture_digest
    review.GLOBAL_FIVE_SESSION_THRESHOLD = threshold_payload[
        "global_threshold_5_session"
    ]
    review.BENCHMARK_RELATIVE_THRESHOLD = threshold_payload[
        "benchmark_relative_threshold_5_session"
    ]
    try:
        package = review.build_redesigned_label_generation_results_review_package_v1(
            output_root=output_root
        )
        yield package, output_root
    finally:
        review.EXPECTED_EXECUTION_DIGEST = original_execution_digest
        review.SOURCE_EVIDENCE[
            "redesigned_label_generation_execution_digest"
        ] = original_source_execution_digest
        review.EXPECTED_LABEL_VALUES_DIGEST = original_digest
        review.SOURCE_EVIDENCE["label_values_digest"] = original_source_digest
        review.GLOBAL_FIVE_SESSION_THRESHOLD = original_global_threshold
        review.BENCHMARK_RELATIVE_THRESHOLD = original_benchmark_threshold


def test_review_package_builds_offline(reviewed, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    _, output_root = reviewed
    package = review.build_redesigned_label_generation_results_review_package_v1(
        output_root=output_root
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_blocks_when_output_root_is_missing(tmp_path) -> None:
    package = review.build_redesigned_label_generation_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["redesigned_label_generation_results_review_ready"] is False
    assert package["ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"] is False
    assert package["blocker_count"] == 11


def test_artifact_kind_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE"


def test_review_status_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["review_status"] == "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_PACKAGE_READY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_redesigned_label_generation_execution_digest", None),
        ("source_redesigned_label_generation_approval_digest", execution.EXPECTED_REDESIGNED_LABEL_GENERATION_APPROVAL_DIGEST),
        ("source_redesigned_label_generation_candidate_review_package_digest", execution.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("source_redesigned_label_generation_candidate_digest", execution.EXPECTED_CANDIDATE_DIGEST),
        ("source_label_objective_redesign_results_review_package_digest", execution.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST),
        ("source_label_objective_redesign_execution_digest", execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST),
        ("source_operator_method_path_selection_digest", execution.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST),
        ("source_research_registry_approval_digest", execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", execution.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_digest_is_bound(reviewed, field: str, expected: str) -> None:
    package, _ = reviewed
    if expected is None:
        expected = review.EXPECTED_EXECUTION_DIGEST
    assert package[field] == expected


def test_label_values_digest_is_bound(reviewed) -> None:
    package, output_root = reviewed
    assert package["label_values_digest"] == sha256_file(output_root / "redesigned_label_values.jsonl")


def test_universe_count_and_order_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["target_universe_count"] == 12
    assert package["target_universe"] == execution.TARGET_UNIVERSE


def test_meta_913_is_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_generated_output_count_is_eleven(reviewed) -> None:
    package, _ = reviewed
    assert package["generated_output_count"] == 11
    assert package["generated_output_names"] == execution.OUTPUT_FILENAMES


def test_output_digests_are_bound(reviewed) -> None:
    package, _ = reviewed
    assert list(package["output_digests"]) == execution.OUTPUT_FILENAMES
    assert package["local_output_digest_count"] == 11
    assert package["recorded_file_digest_match_count"] == 9
    assert package["output_digest_mismatch_count"] == 0


def test_outputs_are_research_only_nonactionable(reviewed) -> None:
    package, _ = reviewed
    assert package["outputs_research_only_non_actionable"] is True
    assert package["outputs_evidence_scope"] == "REDESIGNED_LABEL_GENERATION_RESEARCH_ONLY"


@pytest.mark.parametrize(
    "field",
    [
        "label_values_review",
        "label_family_coverage_review",
        "threshold_strategy_review",
        "horizon_strategy_review",
        "label_availability_review",
        "per_ticker_redesigned_label_summary_review",
        "meta_limitation_preservation_review",
    ],
)
def test_required_label_output_is_verified(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field]["available"] is True
    assert package[field]["verified"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("label_family_count", 10),
        ("threshold_strategy_count", 7),
        ("horizon_strategy_count", 5),
        ("label_value_row_count", 143352),
        ("available_label_value_count", 142200),
        ("unavailable_label_value_count", 1152),
        ("label_family_coverage_entries", 144),
    ],
)
def test_exact_label_output_fact(reviewed, field: str, expected: int) -> None:
    package, _ = reviewed
    assert package[field] == expected


def test_global_threshold_is_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["global_five_session_threshold"] == review.GLOBAL_FIVE_SESSION_THRESHOLD


def test_benchmark_relative_threshold_is_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["benchmark_relative_threshold"] == review.BENCHMARK_RELATIVE_THRESHOLD


def test_class_balance_is_descriptive_only(reviewed) -> None:
    package, _ = reviewed
    assert package["class_balance_output_descriptive_only"] is True


def test_threshold_optimization_is_false(reviewed) -> None:
    package, _ = reviewed
    assert package["threshold_optimization_performed"] is False


def test_forward_tail_unavailable_labels_are_null(reviewed) -> None:
    package, _ = reviewed
    assert package["label_values_review"]["forward_tail_unavailable_labels_null"] is True
    assert package["label_availability_review"]["forward_tail_unavailable_value"] is None


def test_meta_label_summary_is_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["meta_label_rows"] == 10956
    assert package["meta_available_labels"] == 10860
    assert package["meta_unavailable_labels"] == 96
    assert package["meta_source_record_count"] == 913


def test_results_review_created_and_ready_are_true(reviewed) -> None:
    package, _ = reviewed
    assert package["redesigned_label_generation_results_review_created"] is True
    assert package["redesigned_label_generation_results_review_ready"] is True


def test_ready_for_future_planning_candidate_is_true(reviewed) -> None:
    package, _ = reviewed
    assert package["ready_for_feature_or_predictive_evidence_planning_candidate_using_redesigned_labels"] is True


@pytest.mark.parametrize(
    "field",
    [
        "feature_or_predictive_evidence_planning_candidate_using_redesigned_labels_created",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "trade_recommendations_generated",
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "redesigned_label_generation_execution_rerun_performed",
    ],
)
def test_closed_action_remains_false(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] is False


def test_predictive_usefulness_remains_not_accepted(reviewed) -> None:
    package, _ = reviewed
    assert package["predictive_usefulness"] == "not accepted"


def test_profitability_remains_not_accepted(reviewed) -> None:
    package, _ = reviewed
    assert package["profitability"] == "not accepted"


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
    assert all(row["status"] == "PASS" for row in package["review_checklist"])
    assert package["review_summary"]["blocker_count"] == 0
    assert package["review_summary"]["passed_checks"] == len(review.REQUIRED_CHECK_IDS)


def test_review_digest_is_deterministic(reviewed) -> None:
    package, _ = reviewed
    first = review.redesigned_label_generation_results_review_package_digest_v1(package)
    second = review.redesigned_label_generation_results_review_package_digest_v1(deepcopy(package))
    assert first == second == package["redesigned_label_generation_results_review_package_digest"]


def test_validator_accepts_valid_package(reviewed) -> None:
    package, _ = reviewed
    validation = review.validate_redesigned_label_generation_results_review_package_v1(deepcopy(package))
    assert validation["status"] == "REDESIGNED_LABEL_GENERATION_RESULTS_REVIEW_VALID"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_redesigned_label_generation_execution_digest", "0" * 64),
        ("generated_output_count", 10),
        ("label_value_row_count", 143351),
        ("label_values_digest", "0" * 64),
        ("feature_generation_performed", True),
        ("predictive_usefulness", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_invalid_boundary(reviewed, field: str, value) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed[field] = value
    with pytest.raises(review.RedesignedLabelGenerationResultsReviewError):
        review.validate_redesigned_label_generation_results_review_package_v1(changed)


@pytest.mark.parametrize("field", ["limitations", "next_chain", "risk_controls"])
def test_validator_rejects_missing_governance_section(reviewed, field: str) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop(field)
    with pytest.raises(review.RedesignedLabelGenerationResultsReviewError):
        review.validate_redesigned_label_generation_results_review_package_v1(changed)


def test_validator_rejects_missing_review_digest(reviewed) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop("redesigned_label_generation_results_review_package_digest")
    with pytest.raises(review.RedesignedLabelGenerationResultsReviewError):
        review.validate_redesigned_label_generation_results_review_package_v1(changed)


def test_markdown_includes_required_sections(reviewed) -> None:
    package, _ = reviewed
    markdown = review.build_redesigned_label_generation_results_review_markdown_v1(package)
    sections = [
        "Title",
        "Redesigned Label Generation Results Review",
        "Source Execution",
        "Dataset and Universe",
        "Generated Label Outputs",
        "Label Family Coverage Review",
        "Threshold Strategy Review",
        "Horizon Strategy Review",
        "Label Availability Review",
        "Per-Ticker Label Summary",
        "META Limitation Preservation Review",
        "Output Digest Manifest",
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
    for section in sections:
        assert f"## {section}" in markdown


def test_writer_writes_canonical_package_once(reviewed, tmp_path) -> None:
    package, output_root = reviewed
    result = review.write_redesigned_label_generation_results_review_package_v1(
        tmp_path, output_root=output_root
    )
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == package
    with pytest.raises(review.RedesignedLabelGenerationResultsReviewError):
        review.write_redesigned_label_generation_results_review_package_v1(
            tmp_path, output_root=output_root
        )


def test_service_exports_are_available() -> None:
    assert services.build_redesigned_label_generation_results_review_package_v1 is review.build_redesigned_label_generation_results_review_package_v1
    assert services.validate_redesigned_label_generation_results_review_package_v1 is review.validate_redesigned_label_generation_results_review_package_v1
    assert services.build_redesigned_label_generation_results_review_markdown_v1 is review.build_redesigned_label_generation_results_review_markdown_v1
    assert services.write_redesigned_label_generation_results_review_package_v1 is review.write_redesigned_label_generation_results_review_package_v1
