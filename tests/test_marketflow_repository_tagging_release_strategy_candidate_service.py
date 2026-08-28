from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_tagging_release_strategy_candidate_service as service,
)


@pytest.fixture
def candidate() -> dict:
    return service.build_marketflow_repository_tagging_release_strategy_candidate_v1()


def test_candidate_builds_offline_without_rerunning_source_review(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.source_review_service,
        "build_marketflow_repository_state_branch_inventory_operator_review_v1",
        lambda *args, **kwargs: pytest.fail("source operator review must not be rerun"),
    )
    candidate = service.build_marketflow_repository_tagging_release_strategy_candidate_v1()
    assert candidate["created_offline"] is True
    assert candidate["repository_tagging_release_strategy_candidate_created"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_inventory_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_archive_digest", service.EXPECTED_SOURCE_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_operator_review_commit", service.EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT),
    ],
)
def test_artifact_identity_and_required_source_bindings(
    candidate: dict, field: str, expected: object
) -> None:
    assert candidate[field] == expected


def test_complete_upstream_digest_chain_is_preserved(candidate: dict) -> None:
    assert len(candidate["source_evidence"]) == 57
    assert candidate["source_operator_selection_digest"] == service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
    assert candidate["source_closure_digest"] == service.EXPECTED_SOURCE_CLOSURE_DIGEST
    assert candidate["source_readiness_digest"] == service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
    assert candidate["source_reassessment_digest"] == service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
    assert candidate["source_results_review_digest"] == service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
    assert candidate["source_backtest_rows_digest"] == service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
    assert candidate["source_metric_report_digest"] == service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST


def test_source_repository_counts_are_bound(candidate: dict) -> None:
    assert (
        candidate["source_snapshot_local_branch_count"],
        candidate["source_snapshot_remote_branch_count"],
        candidate["source_snapshot_total_branch_ref_count"],
    ) == (290, 261, 551)
    assert (
        candidate["source_post_plan_push_live_local_branch_count"],
        candidate["source_post_plan_push_live_remote_branch_count"],
        candidate["source_post_plan_push_live_total_branch_ref_count"],
    ) == (290, 262, 552)
    assert (
        candidate["source_operator_review_live_local_branch_count"],
        candidate["source_operator_review_live_remote_branch_count"],
        candidate["source_operator_review_live_total_branch_ref_count"],
    ) == (291, 263, 554)


@pytest.mark.parametrize(
    "field",
    [
        "source_operator_review_ready",
        "repository_tagging_release_strategy_candidate_created",
        "repository_tagging_release_strategy_candidate_ready_for_operator_review",
        "ready_for_repository_tagging_release_strategy_operator_review",
    ],
)
def test_source_and_candidate_readiness_flags_are_true(candidate: dict, field: str) -> None:
    assert candidate[field] is True


def test_tagging_philosophy_is_governance_only(candidate: dict) -> None:
    assert candidate["tagging_philosophy"] == service.TAGGING_PHILOSOPHY
    assert candidate["tagging_boundary"] == service.TAGGING_BOUNDARY
    assert candidate["tagging_goal"] == service.TAGGING_GOAL
    assert "no tag is created" in candidate["tagging_boundary"]
    assert "trading authority" in candidate["tagging_goal"]


def test_recommended_package_is_terminal_archive_tags(candidate: dict) -> None:
    assert candidate["recommended_tagging_package"] == service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert "narrowest" in candidate["recommendation_reason"]


def test_four_tagging_packages_are_present_and_unselected(candidate: dict) -> None:
    assert candidate["tagging_packages"] == service.TAGGING_PACKAGES
    assert len(candidate["tagging_packages"]) == 4
    assert all(row["selected"] is False for row in candidate["tagging_packages"])
    assert all(row["approved"] is False for row in candidate["tagging_packages"])
    assert all(row["executed"] is False for row in candidate["tagging_packages"])
    assert all(row["tags_created"] is False for row in candidate["tagging_packages"])


@pytest.mark.parametrize(
    ("tag_name", "target_branch", "target_commit"),
    [
        (
            "marketflow/expectancy-lab/final-archive-not-ready/v1",
            "feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1",
            "0be55dc8a65a586368c192d6bc13302b9830a0b4",
        ),
        (
            "marketflow/expectancy-lab/archive-record-not-ready/v1",
            "feature/marketflow-predictive-usefulness-acceptance-path-archive-record-expectancy-lab-evidence-v1",
            "e2fcfb792ad14db8a2de69556c291529fda47a8e",
        ),
        (
            "marketflow/expectancy-lab/operator-selection-option-a/v1",
            "feature/marketflow-operator-method-or-closure-selection-expectancy-lab-evidence-v1",
            "15c4fae495f88b54e30380f3d8b4aa54989fad39",
        ),
        (
            "marketflow/expectancy-lab/readiness-not-ready/v1",
            "feature/marketflow-predictive-usefulness-acceptance-readiness-review-expectancy-lab-evidence-v1",
            "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0",
        ),
    ],
)
def test_required_terminal_tag_candidates_have_exact_targets(
    candidate: dict, tag_name: str, target_branch: str, target_commit: str
) -> None:
    definition = next(
        row for row in candidate["candidate_tag_definitions"] if row["tag_name"] == tag_name
    )
    assert definition["tag_target_branch"] == target_branch
    assert definition["tag_target_commit"] == target_commit
    assert definition["tag_status"] == "CANDIDATE_TAG_NOT_CREATED"
    assert definition["tag_created"] is False
    assert definition["tag_pushed"] is False


def test_all_fourteen_candidate_tag_definitions_are_non_authorizing(candidate: dict) -> None:
    definitions = candidate["candidate_tag_definitions"]
    assert definitions == service.CANDIDATE_TAG_DEFINITIONS
    assert len(definitions) == 14
    assert all(row["tag_type"] == "ANNOTATED_TAG_RECOMMENDED" for row in definitions)
    assert all(row["operator_approval_required"] is True for row in definitions)
    assert all(row["main_push_required"] is False for row in definitions)
    assert all(row["runtime_authority_created"] is False for row in definitions)
    assert all(row["predictive_usefulness_accepted"] is False for row in definitions)
    assert all(row["profitability_accepted"] is False for row in definitions)


def test_unbound_governance_targets_require_operator_selection(candidate: dict) -> None:
    definitions = {
        row["tag_name"]: row for row in candidate["candidate_tag_definitions"]
    }
    for tag_name in service.GOVERNANCE_TAG_NAMES:
        assert definitions[tag_name]["tag_target_branch"] == service.REQUIRES_OPERATOR_SELECTION
        assert definitions[tag_name]["tag_target_commit"] == service.NOT_BOUND_BY_THIS_CANDIDATE


def test_tagging_prerequisites_are_complete(candidate: dict) -> None:
    assert candidate["tagging_prerequisites"] == service.TAGGING_PREREQUISITES
    assert len(candidate["tagging_prerequisites"]) == 10
    assert all(candidate["tagging_prerequisites"].values())


def test_future_tag_message_template_has_all_authority_boundaries(candidate: dict) -> None:
    template = candidate["future_tag_message_template"]
    assert template == service.FUTURE_TAG_MESSAGE_TEMPLATE
    for text in (
        "Predictive usefulness: NOT_ACCEPTED",
        "Profitability: NOT_ACCEPTED",
        "Runtime: NOT_AUTHORIZED",
        "Trading/Broker: NOT_AUTHORIZED",
        "No trade recommendation is created by this tag.",
    ):
        assert text in template


def test_tagging_non_goals_are_complete(candidate: dict) -> None:
    assert candidate["tagging_non_goals"] == service.TAGGING_NON_GOALS
    assert len(candidate["tagging_non_goals"]) == 12


def test_per_chain_tagging_summary_is_complete(candidate: dict) -> None:
    summaries = candidate["per_chain_tagging_candidate_summary"]
    assert summaries == service.PER_CHAIN_TAGGING_CANDIDATE_SUMMARY
    assert len(summaries) == 9
    assert summaries[0]["candidate_tags"] == service.TERMINAL_TAG_NAMES
    assert all(row["tags_created"] is False for row in summaries)
    assert all(row["approval_required"] is True for row in summaries)
    assert all(row["operator_review_required"] is True for row in summaries)
    assert all(row["merge_required"] is False for row in summaries)
    assert all(row["main_push_required"] is False for row in summaries)


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_selected",
        "repository_tagging_release_strategy_approved",
        "repository_tagging_release_strategy_authorized",
        "repository_tagging_release_strategy_executed",
        "git_tag_created",
        "git_tag_push_performed",
        "git_merge_performed",
        "git_rebase_performed",
        "git_branch_delete_performed",
        "git_remote_delete_performed",
        "git_main_push_performed",
        "git_force_push_performed",
        "git_remote_prune_performed",
        "origin_main_modified_by_this_task",
        "repository_merge_strategy_candidate_created",
        "repository_cleanup_candidate_created",
        "repository_cleanup_executed",
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_selection_execution_provider_and_research_actions_remain_false(
    candidate: dict, field: str
) -> None:
    assert candidate[field] is False


def test_authority_boundaries_remain_closed(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_accepted"] is False
    assert candidate["profitability"] == "not accepted"
    assert candidate["profitability_accepted"] is False
    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"
    assert candidate["paper_trading"] == "NOT_AUTHORIZED"
    assert candidate["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_defined(candidate: dict) -> None:
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert len(candidate["next_chain"]) == 6
    assert candidate["next_gates"] == service.NEXT_GATES
    assert len(candidate["next_gates"]) == 8
    assert candidate["recommended_next_task"] == (
        "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1"
    )


def test_risk_controls_and_marketflow_tracking_guard_are_exact(candidate: dict) -> None:
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 30
    assert candidate["tracked_marketflow_file_count"] == 0
    assert candidate["no_tracked_marketflow_files"] is True


def test_checklist_passes(candidate: dict) -> None:
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 55
    assert candidate["summary"]["passed_checks"] == 55
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0
    assert candidate["summary"]["candidate_tag_count"] == 14
    assert all(row["status"] == service.PASS for row in candidate["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in candidate["checklist"]
    )


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    rebuilt = service.build_marketflow_repository_tagging_release_strategy_candidate_v1()
    digest = candidate["marketflow_repository_tagging_release_strategy_candidate_digest"]
    assert rebuilt["marketflow_repository_tagging_release_strategy_candidate_digest"] == digest
    assert service.marketflow_repository_tagging_release_strategy_candidate_digest_v1(candidate) == digest


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_VALID
    assert result["passed_checks"] == 55
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_inventory_operator_review_digest", "0" * 64),
        ("source_inventory_plan_digest", "0" * 64),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", ""),
        ("repository_tagging_release_strategy_candidate_created", False),
        ("repository_tagging_release_strategy_candidate_ready_for_operator_review", False),
        ("recommended_tagging_package", ""),
        ("repository_tagging_release_strategy_selected", True),
        ("repository_tagging_release_strategy_approved", True),
        ("repository_tagging_release_strategy_authorized", True),
        ("repository_tagging_release_strategy_executed", True),
        ("git_tag_created", True),
        ("git_tag_push_performed", True),
        ("git_merge_performed", True),
        ("git_rebase_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_main_push_performed", True),
        ("git_force_push_performed", True),
        ("git_remote_prune_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness_accepted", True),
        ("profitability_accepted", True),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_invalid_top_level_values(
    candidate: dict, field: str, value: object
) -> None:
    mutated = deepcopy(candidate)
    mutated[field] = value
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(mutated)


@pytest.mark.parametrize(
    "field",
    [
        "candidate_tag_definitions",
        "tagging_packages",
        "tagging_prerequisites",
        "per_chain_tagging_candidate_summary",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_structures(candidate: dict, field: str) -> None:
    mutated = deepcopy(candidate)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(mutated)


def test_validator_rejects_missing_terminal_tag(candidate: dict) -> None:
    mutated = deepcopy(candidate)
    mutated["candidate_tag_definitions"].pop(0)
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(mutated)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    mutated = deepcopy(candidate)
    mutated.pop("marketflow_repository_tagging_release_strategy_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(mutated)


def test_source_review_must_be_an_object() -> None:
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.build_marketflow_repository_tagging_release_strategy_candidate_v1(
            source_review=[]  # type: ignore[arg-type]
        )


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = service.build_marketflow_repository_tagging_release_strategy_candidate_markdown_v1(candidate)
    for heading in (
        "Title",
        "MarketFlow Repository Tagging / Release Strategy Candidate v1",
        "Source Inventory Operator Review",
        "Bound Evidence",
        "Repository Context",
        "Candidate Scope",
        "Tagging Philosophy",
        "Recommended Tagging Package",
        "Candidate Tag Packages",
        "Candidate Tag Definitions",
        "Tagging Prerequisites",
        "Future Tag Message Template",
        "Tagging Non-Goals",
        "Per-Chain Tagging Summary",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(
    tmp_path: Path,
) -> None:
    result = service.write_marketflow_repository_tagging_release_strategy_candidate_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_tagging_release_strategy_candidate_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    digest = payload["marketflow_repository_tagging_release_strategy_candidate_digest"]
    assert digest == result["marketflow_repository_tagging_release_strategy_candidate_digest"]
    service.validate_marketflow_repository_tagging_release_strategy_candidate_v1(payload)
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyCandidateError):
        service.write_marketflow_repository_tagging_release_strategy_candidate_v1(tmp_path)
