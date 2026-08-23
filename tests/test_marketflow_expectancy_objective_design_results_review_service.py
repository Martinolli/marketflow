from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    marketflow_expectancy_objective_design_execution_service as execution_service,
)
from marketflow.services import (
    marketflow_expectancy_objective_design_results_review_service as review_service,
)


@pytest.fixture(scope="module")
def source_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("expectancy-design-review-source") / "outputs"
    execution_service.execute_marketflow_expectancy_objective_design_v1(
        output_root=root,
        run_timestamp_utc="2026-08-23T01:00:00Z",
    )
    return root


@pytest.fixture(scope="module")
def review(source_root: Path) -> dict:
    return review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=source_root
    )


def _mutated(review: dict, field: str, value: object) -> dict:
    result = deepcopy(review)
    result[field] = value
    return result


def test_results_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["provider_requests_made_in_review"] is False
    assert review["objective_design_execution_rerun_performed"] is False


def test_results_review_blocks_when_output_root_missing(tmp_path: Path) -> None:
    review = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=tmp_path / "missing"
    )
    assert review["artifact_kind"] == (
        review_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED
    )
    assert review["review_status"] == (
        review_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    )
    assert review["expectancy_objective_design_results_review_created"] is False
    assert review["expectancy_objective_design_results_review_ready"] is False
    assert review["ready_for_objective_label_or_target_generation_candidate"] is False
    validation = review_service.validate_marketflow_expectancy_objective_design_results_review_v1(
        review
    )
    assert validation["status"].endswith("BLOCKED_VALID")


CORE_FIELDS = [
    (
        "artifact_kind",
        "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE",
    ),
    (
        "schema_version",
        "marketflow_expectancy_objective_design_results_review_v1",
    ),
    (
        "review_status",
        "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY",
    ),
    (
        "review_scope",
        "EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION",
    ),
    (
        "source_expectancy_objective_design_execution_digest",
        "ba9661d34b57dbd464b6ec559c5b3e48df5ff78847102aa16d2d9e45f076ec11",
    ),
    (
        "source_expectancy_objective_design_output_binding_digest",
        "3ee2acfb7461769fc054e1afb34e222302297b04d66a08b21fb411613e0585a4",
    ),
    (
        "source_expectancy_objective_approval_digest",
        "4ae9d4e81cc41b9578ac061574669d6fb11a45ed56871f4d05a02aacad165a1d",
    ),
    (
        "source_expectancy_objective_candidate_review_digest",
        "baac33f292d77d26eae6eacc4cffaa5cdabe17785cb2c090c053c82d1bfe551d",
    ),
    (
        "source_expectancy_objective_candidate_digest",
        "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17",
    ),
    ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
    ("dataset_name", "expanded_universe_canonical_dataset_v1"),
    ("source_profile", "RTH_FULL_SESSION_1D"),
    ("timeframe", "1d"),
    ("date_range_start", "2022-01-01"),
    ("date_range_end", "2025-12-31"),
    ("target_universe_count", 12),
    ("total_canonical_record_count", 11946),
    ("meta_record_count", 913),
    ("non_meta_record_count", 1003),
    ("generated_output_count", 11),
    ("expected_output_count", 11),
    ("observed_output_count", 11),
    ("output_digest_mismatch_count", 0),
    ("output_file_inspection_performed", True),
    (
        "digest_manifest_self_reference_policy",
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    ),
    ("expectancy_objective_selected", True),
    ("expectancy_objective_approved", True),
    ("ready_for_expectancy_objective_design_execution", True),
    ("expectancy_objective_design_executed", True),
    ("expectancy_objective_design_results_created", True),
    ("expectancy_objective_design_results_review_created", True),
    ("expectancy_objective_design_results_review_ready", True),
    ("ready_for_objective_label_or_target_generation_candidate", True),
    ("predictive_usefulness", "not accepted"),
    ("profitability", "not accepted"),
    ("runtime_use", "NOT_AUTHORIZED"),
    ("trade_recommendations_generated", False),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_required_core_field(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_bound_digest_chain_is_complete(review: dict) -> None:
    expected = {
        "source_strategy_charter_approval_digest",
        "source_strategy_charter_review_digest",
        "source_strategy_charter_digest",
        "source_final_archive_digest",
        "source_archive_digest",
        "source_selection_digest",
        "source_closure_digest",
        "source_readiness_digest",
        "source_reassessment_digest",
        "source_results_review_digest",
        "source_execution_digest",
        "source_output_binding_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "research_registry_approval_digest",
        "records_digest",
    }
    assert expected <= review["source_evidence_digests"].keys()
    assert all(
        len(review["source_evidence_digests"][field]) == 64 for field in expected
    )


def test_target_universe_order_is_preserved(review: dict) -> None:
    assert review["target_universe"] == [
        "MSFT",
        "NVDA",
        "AMZN",
        "GOOGL",
        "META",
        "TSLA",
        "JPM",
        "XOM",
        "JNJ",
        "WMT",
        "CAT",
        "LMT",
    ]


def test_output_files_and_local_hashes_are_verified(review: dict) -> None:
    rows = review["verified_output_files"]
    assert [row["filename"] for row in rows] == execution_service.OUTPUT_FILENAMES
    assert len(rows) == 11
    assert all(row["verified"] is True for row in rows)
    assert review["local_output_hashes"] == {
        row["filename"]: row["local_sha256"] for row in rows
    }
    assert all(len(digest) == 64 for digest in review["local_output_hashes"].values())


def test_digest_manifest_self_reference_policy_is_verified(review: dict) -> None:
    row = review["verified_output_files"][-1]
    assert row == {
        "filename": "expectancy_objective_design_digest_manifest.json",
        "local_sha256": review["local_output_hashes"][row["filename"]],
        "manifest_sha256": None,
        "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "verified": True,
    }


def test_objective_family_selection_report_is_reviewed(review: dict) -> None:
    assert len(review["reviewed_objective_family_selection_report"]) == 10
    assert review["design_output_review_statuses"][
        "objective_family_selection_report_review"
    ] == "REVIEWED_RESEARCH_ONLY"


@pytest.mark.parametrize(
    ("field", "count", "status_field"),
    [
        (
            "reviewed_expectancy_payoff_specification",
            7,
            "expectancy_payoff_specification_review",
        ),
        (
            "reviewed_abstention_support_specification",
            6,
            "abstention_support_specification_review",
        ),
        (
            "reviewed_material_move_specification",
            5,
            "material_move_specification_review",
        ),
    ],
)
def test_objective_specification_is_reviewed(
    review: dict, field: str, count: int, status_field: str
) -> None:
    assert len(review[field]["future_candidate_fields"]) == count
    assert review["design_output_review_statuses"][status_field] == (
        "REVIEWED_RESEARCH_ONLY"
    )
    assert review[field]["future_label_generation_authorized"] is False
    assert review[field]["future_target_creation_authorized"] is False


def test_label_generation_plan_is_reviewed_without_execution(review: dict) -> None:
    plan = review["reviewed_objective_label_generation_plan"]
    assert plan["plan_status"] == "PLANNED_NOT_EXECUTED"
    assert len(plan["planned_steps"]) == 10
    assert plan["label_generation_authorized"] is False
    assert plan["target_creation_authorized"] is False
    assert review["design_output_review_statuses"][
        "objective_label_generation_plan_review"
    ] == "REVIEWED_PLAN_ONLY_NOT_EXECUTED"


def test_validation_metric_plan_is_reviewed_without_computation(review: dict) -> None:
    metrics = review["reviewed_objective_validation_metric_plan"]
    assert set(metrics) == set(execution_service.VALIDATION_METRICS)
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in metrics.values())
    assert all(row["metric_computation_authorized"] is False for row in metrics.values())


def test_baseline_plan_is_reviewed_without_execution(review: dict) -> None:
    baselines = review["reviewed_objective_baseline_comparison_plan"]
    assert set(baselines) == set(execution_service.BASELINES)
    assert all(row["baseline_status"] == "PLANNED_NOT_EXECUTED" for row in baselines.values())
    assert all(row["backtest_authorized"] is False for row in baselines.values())


def test_per_ticker_review_and_digests_are_complete(review: dict) -> None:
    rows = review["per_ticker_objective_results_review"]
    assert len(rows) == 12
    assert [row["ticker"] for row in rows] == review["target_universe"]
    for row in rows:
        assert row[
            "per_ticker_expectancy_objective_design_results_review_digest"
        ] == review_service.per_ticker_expectancy_objective_design_results_review_digest_v1(
            row
        )
        assert row["label_generation_authorized"] is False
        assert row["runtime_use"] == "NOT_AUTHORIZED"
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["review_note"] == (
        "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW"
    )
    assert all(
        row["historical_record_count"] == 1003
        for row in rows
        if row["ticker"] != "META"
    )


CLOSED_FALSE_FIELDS = [
    "objective_label_or_target_generation_candidate_created",
    "objective_label_or_target_generation_approved",
    "objective_label_or_target_generation_performed",
    "expectancy_objective_generation_authorized",
    "expectancy_objective_generation_performed",
    "label_generation_authorized",
    "label_generation_performed",
    "new_targets_created",
    "target_definition_change_authorized",
    "target_definition_change_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
    "feature_label_matrix_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "new_strategy_scoring_performed",
    "predictive_usefulness_acceptance_candidate_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "trade_recommendations_generated",
    "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review",
    "objective_design_execution_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
]


@pytest.mark.parametrize("field", CLOSED_FALSE_FIELDS)
def test_authority_and_execution_boundary_remains_closed(
    review: dict, field: str
) -> None:
    assert review[field] is False


def test_next_chain_next_gates_and_risk_controls_are_exact(review: dict) -> None:
    assert review["next_chain"] == review_service.NEXT_CHAIN
    assert review["next_gates"] == review_service.NEXT_GATES
    assert review["risk_controls"] == review_service.RISK_CONTROLS
    assert len(review["next_chain"]) == 9
    assert len(review["next_gates"]) == 9
    assert len(review["risk_controls"]) == 24


def test_checklist_passes(review: dict) -> None:
    rows = review["review_checklist"]
    assert [row["check_id"] for row in rows] == review_service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in rows)
    assert review["review_summary"]["total_checks"] == len(rows) == 76
    assert review["review_summary"]["passed_checks"] == 76
    assert review["review_summary"]["failed_checks"] == 0
    assert review["review_summary"]["blocker_count"] == 0


def test_review_and_per_ticker_digests_are_deterministic(
    source_root: Path, review: dict
) -> None:
    again = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=source_root
    )
    assert again[
        "marketflow_expectancy_objective_design_results_review_digest"
    ] == review["marketflow_expectancy_objective_design_results_review_digest"]
    assert [
        row["per_ticker_expectancy_objective_design_results_review_digest"]
        for row in again["per_ticker_objective_results_review"]
    ] == [
        row["per_ticker_expectancy_objective_design_results_review_digest"]
        for row in review["per_ticker_objective_results_review"]
    ]


def test_review_digest_is_output_location_independent(
    source_root: Path, tmp_path: Path, review: dict
) -> None:
    second_root = tmp_path / "second-source"
    shutil.copytree(source_root, second_root)
    second = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=second_root
    )
    assert second[
        "marketflow_expectancy_objective_design_results_review_digest"
    ] == review["marketflow_expectancy_objective_design_results_review_digest"]


def test_validator_accepts_valid_review(review: dict) -> None:
    validation = review_service.validate_marketflow_expectancy_objective_design_results_review_v1(
        deepcopy(review)
    )
    assert validation["status"] == (
        "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_VALID"
    )
    assert validation["total_checks"] == 76


INVALID_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("review_status", "WRONG"),
    ("review_scope", "WRONG"),
    ("source_expectancy_objective_design_execution_digest", "0" * 64),
    ("source_expectancy_objective_design_output_binding_digest", "0" * 64),
    ("source_expectancy_objective_approval_digest", "0" * 64),
    ("selected_objective_path", "WRONG"),
    ("target_universe", ["MSFT"]),
    ("target_universe_count", 11),
    ("records_digest", "0" * 64),
    ("meta_record_count", 1003),
    ("expected_output_count", 10),
    ("observed_output_count", 10),
    ("output_digest_mismatch_count", 1),
    ("output_file_inspection_performed", False),
    ("expectancy_objective_design_results_review_created", False),
    ("expectancy_objective_design_results_review_ready", False),
    ("ready_for_objective_label_or_target_generation_candidate", False),
    ("objective_label_or_target_generation_candidate_created", True),
    ("label_generation_authorized", True),
    ("label_generation_performed", True),
    ("new_targets_created", True),
    ("target_definition_change_authorized", True),
    ("feature_generation_authorized", True),
    ("feature_label_matrix_created", True),
    ("backtest_execution_authorized", True),
    ("backtest_execution_performed", True),
    ("model_training_authorized", True),
    ("model_training_performed", True),
    ("metric_computation_authorized", True),
    ("metric_computation_performed", True),
    ("strategy_scoring_performed", True),
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
    ("objective_design_execution_rerun_performed", True),
    ("output_verification", None),
    ("reviewed_objective_family_selection_report", {}),
    ("reviewed_expectancy_payoff_specification", {}),
    ("reviewed_objective_label_generation_plan", {}),
    ("reviewed_objective_validation_metric_plan", {}),
    ("reviewed_objective_baseline_comparison_plan", {}),
    ("risk_controls", []),
    ("marketflow_expectancy_objective_design_results_review_digest", None),
]


@pytest.mark.parametrize(("field", "value"), INVALID_MUTATIONS)
def test_validator_rejects_invalid_review_field(
    review: dict, field: str, value: object
) -> None:
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveDesignResultsReviewError
    ):
        review_service.validate_marketflow_expectancy_objective_design_results_review_v1(
            _mutated(review, field, value)
        )


def test_validator_rejects_missing_per_ticker_digest(review: dict) -> None:
    mutated = deepcopy(review)
    mutated["per_ticker_objective_results_review"][0].pop(
        "per_ticker_expectancy_objective_design_results_review_digest"
    )
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveDesignResultsReviewError
    ):
        review_service.validate_marketflow_expectancy_objective_design_results_review_v1(
            mutated
        )


def test_builder_blocks_on_missing_source_output(
    source_root: Path, tmp_path: Path
) -> None:
    root = tmp_path / "missing-file"
    shutil.copytree(source_root, root)
    (root / "operator_summary.json").unlink()
    review = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=root
    )
    assert review["review_status"].endswith("MISSING_OR_INVALID_OUTPUTS")
    assert "filename set mismatch" in review["blocked_reason"]


def test_builder_blocks_on_digest_mismatch(source_root: Path, tmp_path: Path) -> None:
    root = tmp_path / "digest-mismatch"
    shutil.copytree(source_root, root)
    path = root / "operator_summary.json"
    path.write_bytes(path.read_bytes() + b" ")
    review = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=root
    )
    assert review["review_status"].endswith("MISSING_OR_INVALID_OUTPUTS")
    assert "digest mismatch" in review["blocked_reason"]


def test_builder_blocks_on_forbidden_payload_even_with_updated_manifest(
    source_root: Path, tmp_path: Path
) -> None:
    root = tmp_path / "forbidden-payload"
    shutil.copytree(source_root, root)
    report_path = root / "operator_summary.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["raw_provider_payloads"] = [{"secret": "forbidden"}]
    report_bytes = canonical_json_bytes(report)
    report_path.write_bytes(report_bytes)
    manifest_path = root / "expectancy_objective_design_digest_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    row = next(
        item
        for item in manifest["output_digest_entries"]
        if item["filename"] == "operator_summary.json"
    )
    row["sha256"] = sha256_bytes(report_bytes)
    manifest_path.write_bytes(canonical_json_bytes(manifest))
    review = review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=root
    )
    assert review["review_status"].endswith("MISSING_OR_INVALID_OUTPUTS")
    assert "API-key or provider-payload material" in review["blocked_reason"]


def test_builder_does_not_modify_source_outputs(source_root: Path) -> None:
    before = {
        path.name: sha256_bytes(path.read_bytes()) for path in source_root.iterdir()
    }
    review_service.build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=source_root
    )
    after = {
        path.name: sha256_bytes(path.read_bytes()) for path in source_root.iterdir()
    }
    assert after == before


def test_writer_uses_canonical_json_and_refuses_overwrite(
    source_root: Path, tmp_path: Path
) -> None:
    result = review_service.write_marketflow_expectancy_objective_design_results_review_v1(
        tmp_path,
        output_root=source_root,
    )
    path = Path(result["path"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() == canonical_json_bytes(payload)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    with pytest.raises(
        review_service.MarketFlowExpectancyObjectiveDesignResultsReviewError
    ):
        review_service.write_marketflow_expectancy_objective_design_results_review_v1(
            tmp_path,
            output_root=source_root,
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = review_service.build_marketflow_expectancy_objective_design_results_review_markdown_v1(
        review
    )
    sections = [
        "Title",
        "Expectancy Objective Design Results Review v1",
        "Source Design Execution",
        "Bound Evidence",
        "Dataset and Universe",
        "Output Verification",
        "Selected Objective Path",
        "Design Philosophy Review",
        "Objective Family Selection Report Review",
        "Expectancy Payoff Specification Review",
        "Abstention Support Specification Review",
        "Material Move Specification Review",
        "Label Generation Plan Boundary",
        "Validation Metric Plan Boundary",
        "Baseline Comparison Plan Boundary",
        "Per-Ticker Objective Review",
        "Output Digest Manifest",
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
    assert "not accepted" in markdown
    assert "NOT_AUTHORIZED" in markdown
