from __future__ import annotations

from copy import deepcopy
import hashlib
import json

import pytest

from marketflow.services import (
    marketflow_expectancy_objective_design_execution_service as execution_service,
)


FIXED_TIMESTAMP = "2026-08-23T01:00:00Z"


@pytest.fixture(scope="module")
def executed_bundle(tmp_path_factory):
    root = tmp_path_factory.mktemp("expectancy-objective-design")
    artifact = execution_service.execute_marketflow_expectancy_objective_design_v1(
        output_root=root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    return artifact, root


@pytest.fixture(scope="module")
def artifact(executed_bundle) -> dict:
    return executed_bundle[0]


def test_design_execution_builds_offline_and_writes_exact_outputs(
    executed_bundle,
) -> None:
    artifact, root = executed_bundle
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert sorted(path.name for path in root.iterdir()) == sorted(
        execution_service.OUTPUT_FILENAMES
    )
    assert all(path.is_file() for path in root.iterdir())


def test_output_root_must_be_empty(executed_bundle) -> None:
    _, root = executed_bundle
    with pytest.raises(
        execution_service.MarketFlowExpectancyObjectiveDesignExecutionError
    ):
        execution_service.execute_marketflow_expectancy_objective_design_v1(
            output_root=root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED"),
        ("execution_status", "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY"),
        ("execution_scope", "EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION"),
        ("selected_objective_path", "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"),
        ("source_expectancy_objective_approval_digest", "4ae9d4e81cc41b9578ac061574669d6fb11a45ed56871f4d05a02aacad165a1d"),
        ("source_expectancy_objective_candidate_review_digest", "baac33f292d77d26eae6eacc4cffaa5cdabe17785cb2c090c053c82d1bfe551d"),
        ("source_expectancy_objective_candidate_digest", "9b241ab1be15921384d97d75a11ac7858065d041c0b8a02144e97c3e3ed3bc17"),
        ("source_strategy_charter_approval_digest", "ea6c77007c4827fbdd4015425bc92af40eb59b08daba3d5c2e41090df0762b92"),
        ("feature_label_matrix_digest", "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"),
        ("feature_values_digest", "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"),
        ("redesigned_label_values_digest", "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"),
        ("records_digest", "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"),
        ("expectancy_objective_selected", True),
        ("expectancy_objective_approved", True),
        ("ready_for_expectancy_objective_design_execution", True),
        ("expectancy_objective_design_execution_authorized", True),
        ("expectancy_objective_design_executed", True),
        ("expectancy_objective_design_results_created", True),
        ("generated_output_count", 11),
        ("label_generation_authorized", False),
        ("label_generation_performed", False),
        ("new_targets_created", False),
        ("target_definition_change_authorized", False),
        ("feature_generation_authorized", False),
        ("feature_generation_performed", False),
        ("feature_label_matrix_created", False),
        ("backtest_execution_authorized", False),
        ("model_training_authorized", False),
        ("metric_computation_authorized", False),
        ("strategy_scoring_performed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("trade_recommendations_generated", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("canonical_dataset_regenerated_in_execution", False),
    ],
)
def test_required_top_level_values(
    artifact: dict,
    field: str,
    expected: object,
) -> None:
    assert artifact[field] == expected


def test_universe_order_counts_and_meta_limitation_are_preserved(
    artifact: dict,
) -> None:
    assert artifact["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]
    assert artifact["target_universe_count"] == 12
    assert artifact["total_canonical_record_count"] == 11946
    assert artifact["meta_record_count"] == 913
    assert artifact["non_meta_record_count"] == 1003
    assert artifact["meta_reduced_record_count_preserved"] is True


def test_design_philosophy_is_research_only(artifact: dict) -> None:
    assert artifact["objective_design_philosophy"].startswith(
        "Translate the approved expectancy/payoff objective path"
    )
    assert artifact["objective_design_primary_goal"].startswith(
        "Define how future labels or targets may represent positive expectancy"
    )
    assert artifact["objective_design_boundary"].startswith("Design-only")


def test_objective_family_selection_report_has_all_roles(artifact: dict) -> None:
    rows = artifact["objective_family_selection_report"]
    assert len(rows) == 10
    assert rows["OBJECTIVE_EXPECTANCY_POSITIVE_SETUP"]["design_role"] == (
        "PRIMARY_EXPECTANCY_CORE"
    )
    assert rows["OBJECTIVE_NO_TRADE_ABSTAIN_ZONE"]["design_role"] == (
        "SUPPORTING_ABSTENTION_FILTER"
    )
    assert rows["OBJECTIVE_ABSORPTION_REVERSAL_SETUP"]["design_role"] == (
        "CONTEXTUAL_SETUP_CLASS"
    )
    assert all(row["design_status"] == "DESIGNED_RESEARCH_ONLY" for row in rows.values())
    assert all(row["label_generation_authorized"] is False for row in rows.values())


@pytest.mark.parametrize(
    ("field", "cluster", "candidate_count"),
    [
        ("expectancy_payoff_objective_specification", "CLUSTER_EXPECTANCY_AND_PAYOFF", 7),
        ("abstention_support_objective_specification", "CLUSTER_ABSTENTION_AND_NO_TRADE", 6),
        ("material_move_objective_specification", "CLUSTER_TREND_QUALITY_AND_MATERIAL_MOVE", 5),
    ],
)
def test_objective_specifications_are_designed_not_generated(
    artifact: dict,
    field: str,
    cluster: str,
    candidate_count: int,
) -> None:
    specification = artifact[field]
    assert specification["specification_status"] == (
        "DESIGNED_RESEARCH_ONLY_NOT_GENERATED"
    )
    assert specification["objective_cluster"] == cluster
    assert specification["objective_path"] == (
        "EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT"
    )
    assert len(specification["future_candidate_fields"]) == candidate_count
    assert specification["future_label_generation_authorized"] is False
    assert specification["future_target_creation_authorized"] is False


def test_label_generation_plan_exists_without_generation(artifact: dict) -> None:
    plan = artifact["objective_label_generation_plan"]
    assert plan["plan_status"] == "PLANNED_NOT_EXECUTED"
    assert plan["label_generation_authorized"] is False
    assert plan["target_creation_authorized"] is False
    assert plan["requires_separate_candidate"] is True
    assert plan["requires_operator_review"] is True
    assert plan["requires_approval_before_generation"] is True
    assert len(plan["planned_steps"]) == 10


def test_validation_metric_plan_has_14_uncomputed_metrics(artifact: dict) -> None:
    rows = artifact["objective_validation_metric_plan"]
    assert list(rows) == execution_service.VALIDATION_METRICS
    assert len(rows) == 14
    assert all(row["metric_status"] == "PLANNED_NOT_COMPUTED" for row in rows.values())
    assert all(row["metric_computation_authorized"] is False for row in rows.values())


def test_baseline_plan_has_7_unexecuted_baselines(artifact: dict) -> None:
    rows = artifact["objective_baseline_comparison_plan"]
    assert list(rows) == execution_service.BASELINES
    assert len(rows) == 7
    assert all(row["baseline_status"] == "PLANNED_NOT_EXECUTED" for row in rows.values())
    assert all(row["backtest_authorized"] is False for row in rows.values())


def test_per_ticker_review_and_digests_are_complete(artifact: dict) -> None:
    rows = artifact["per_ticker_objective_review"]
    assert len(rows) == 12
    assert all(
        row["per_ticker_expectancy_objective_design_digest"]
        == execution_service.per_ticker_expectancy_objective_design_digest_v1(row)
        for row in rows
    )
    meta = next(row for row in rows if row["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert meta["design_note"] == (
        "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION"
    )


def test_every_output_has_research_only_guardrails(executed_bundle) -> None:
    _, root = executed_bundle
    for filename in execution_service.OUTPUT_FILENAMES:
        payload = json.loads((root / filename).read_text(encoding="utf-8"))
        if filename == "expectancy_objective_design_manifest.json":
            assert payload["research_only"] is True
        else:
            assert payload["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
            assert payload["evidence_scope"] == (
                "EXPECTANCY_OBJECTIVE_DESIGN_RESEARCH_ONLY"
            )
        assert payload["label_generation_authorized"] is False
        assert payload["new_targets_created"] is False
        assert payload["feature_generation_authorized"] is False
        assert payload["backtest_execution_authorized"] is False
        assert payload["metric_computation_authorized"] is False
        assert payload["predictive_usefulness"] == "not accepted"
        assert payload["profitability"] == "not accepted"
        assert payload["runtime_use"] == "NOT_AUTHORIZED"


def test_output_digest_manifest_covers_all_outputs(executed_bundle) -> None:
    artifact, root = executed_bundle
    manifest = json.loads(
        (root / "expectancy_objective_design_digest_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    entries = manifest["output_digest_entries"]
    assert [entry["filename"] for entry in entries] == execution_service.OUTPUT_FILENAMES
    assert manifest["generated_output_count"] == 11
    assert manifest["self_reference_policy"] == (
        "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    )
    for entry in entries:
        if entry["filename"] == "expectancy_objective_design_digest_manifest.json":
            assert entry["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
            assert entry["sha256"] is None
        else:
            data = (root / entry["filename"]).read_bytes()
            assert entry["digest_kind"] == "FILE_SHA256"
            assert entry["sha256"] == hashlib.sha256(data).hexdigest()
    assert manifest["expectancy_objective_design_output_binding_digest"] == (
        artifact["expectancy_objective_design_output_binding_digest"]
    )


def test_next_chain_gates_and_risk_controls_are_exact(artifact: dict) -> None:
    assert len(artifact["next_chain"]) == 7
    assert len(artifact["next_gates"]) == 9
    assert len(artifact["risk_controls"]) == 23
    assert "design_execution_does_not_generate_labels" in artifact["risk_controls"]
    assert "all_outputs_research_only" in artifact["risk_controls"]


def test_checklist_passes_and_summary_is_research_only(artifact: dict) -> None:
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    summary = artifact["execution_summary"]
    assert summary["total_checks"] == len(artifact["execution_checklist"])
    assert summary["passed_checks"] == summary["total_checks"]
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["generated_output_count"] == 11
    assert summary["label_generation_performed"] is False
    assert summary["runtime_authorized"] is False


def test_execution_binding_and_per_ticker_digests_are_deterministic(
    artifact: dict,
    tmp_path,
) -> None:
    again = execution_service.execute_marketflow_expectancy_objective_design_v1(
        output_root=tmp_path / "again",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["marketflow_expectancy_objective_design_execution_digest"] == (
        again["marketflow_expectancy_objective_design_execution_digest"]
    )
    assert artifact["expectancy_objective_design_output_binding_digest"] == (
        again["expectancy_objective_design_output_binding_digest"]
    )
    assert artifact["marketflow_expectancy_objective_design_execution_digest"] == (
        execution_service.marketflow_expectancy_objective_design_execution_digest_v1(
            artifact
        )
    )
    assert artifact["expectancy_objective_design_output_binding_digest"] == (
        execution_service.expectancy_objective_design_output_binding_digest_v1(
            artifact
        )
    )
    assert [
        row["per_ticker_expectancy_objective_design_digest"]
        for row in artifact["per_ticker_objective_review"]
    ] == [
        row["per_ticker_expectancy_objective_design_digest"]
        for row in again["per_ticker_objective_review"]
    ]


def test_validator_accepts_valid_artifact(artifact: dict) -> None:
    result = execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
        artifact
    )
    assert result["status"] == (
        "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_VALID"
    )
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_objective_path", "WRONG"),
        ("source_expectancy_objective_approval_digest", "0" * 64),
        ("source_expectancy_objective_candidate_review_digest", "0" * 64),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("expectancy_objective_selected", False),
        ("expectancy_objective_approved", False),
        ("ready_for_expectancy_objective_design_execution", False),
        ("expectancy_objective_design_execution_authorized", False),
        ("expectancy_objective_design_executed", False),
        ("expectancy_objective_design_results_created", False),
        ("generated_output_count", 10),
        ("label_generation_authorized", True),
        ("label_generation_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("feature_generation_authorized", True),
        ("feature_label_matrix_created", True),
        ("backtest_execution_authorized", True),
        ("model_training_authorized", True),
        ("metric_computation_authorized", True),
        ("strategy_scoring_performed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_execution", True),
        ("market_data_acquisition_performed_in_execution", True),
        ("canonical_dataset_regenerated_in_execution", True),
        ("objective_design_philosophy", ""),
        ("objective_family_selection_report", {}),
        ("expectancy_payoff_objective_specification", {}),
        ("abstention_support_objective_specification", {}),
        ("material_move_objective_specification", {}),
        ("objective_label_generation_plan", {}),
        ("objective_validation_metric_plan", {}),
        ("objective_baseline_comparison_plan", {}),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_mutated_artifact(
    artifact: dict,
    field: str,
    bad_value: object,
) -> None:
    mutated = deepcopy(artifact)
    mutated[field] = bad_value
    with pytest.raises(
        execution_service.MarketFlowExpectancyObjectiveDesignExecutionError
    ):
        execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
            mutated
        )


def test_validator_rejects_missing_execution_digest(artifact: dict) -> None:
    mutated = deepcopy(artifact)
    mutated.pop("marketflow_expectancy_objective_design_execution_digest")
    with pytest.raises(
        execution_service.MarketFlowExpectancyObjectiveDesignExecutionError
    ):
        execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
            mutated
        )


def test_validator_rejects_missing_output_binding_digest(artifact: dict) -> None:
    mutated = deepcopy(artifact)
    mutated.pop("expectancy_objective_design_output_binding_digest")
    with pytest.raises(
        execution_service.MarketFlowExpectancyObjectiveDesignExecutionError
    ):
        execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
            mutated
        )


def test_validator_rejects_missing_per_ticker_digest(artifact: dict) -> None:
    mutated = deepcopy(artifact)
    mutated["per_ticker_objective_review"][0].pop(
        "per_ticker_expectancy_objective_design_digest"
    )
    with pytest.raises(
        execution_service.MarketFlowExpectancyObjectiveDesignExecutionError
    ):
        execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
            mutated
        )


def test_markdown_includes_all_required_sections(artifact: dict) -> None:
    markdown = execution_service.build_marketflow_expectancy_objective_design_execution_markdown_v1(
        artifact
    )
    required_sections = [
        "Title",
        "Expectancy Objective Design Execution v1",
        "Source Expectancy Objective Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Execution Scope",
        "Selected Objective Path",
        "Design Philosophy",
        "Objective Family Selection Report",
        "Expectancy Payoff Objective Specification",
        "Abstention Support Objective Specification",
        "Material Move Objective Specification",
        "Objective Label Generation Plan",
        "Validation Metric Plan",
        "Baseline Comparison Plan",
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
    assert all(f"## {section}" in markdown for section in required_sections)
