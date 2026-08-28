from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_tagging_release_strategy_operator_review_service as service,
)


@pytest.fixture
def review() -> dict:
    return service.build_marketflow_repository_tagging_release_strategy_operator_review_v1()


def test_review_builds_offline_without_rerunning_source_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.source_candidate_service,
        "build_marketflow_repository_tagging_release_strategy_candidate_v1",
        lambda *args, **kwargs: pytest.fail("source candidate must not be rerun"),
    )
    review = service.build_marketflow_repository_tagging_release_strategy_operator_review_v1()
    assert review["created_offline"] is True
    assert review["repository_tagging_release_strategy_operator_review_created"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tagging_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_inventory_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_archive_digest", service.EXPECTED_SOURCE_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_candidate_commit", service.EXPECTED_SOURCE_CANDIDATE_COMMIT),
    ],
)
def test_artifact_identity_and_required_source_bindings(
    review: dict, field: str, expected: object
) -> None:
    assert review[field] == expected


def test_complete_upstream_digest_chain_is_preserved(review: dict) -> None:
    assert len(review["source_evidence"]) == 57
    assert review["source_operator_selection_digest"] == service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
    assert review["source_closure_digest"] == service.EXPECTED_SOURCE_CLOSURE_DIGEST
    assert review["source_readiness_digest"] == service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
    assert review["source_reassessment_digest"] == service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
    assert review["source_results_review_digest"] == service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
    assert review["source_backtest_rows_digest"] == service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
    assert review["source_metric_report_digest"] == service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST


def test_source_repository_counts_are_bound(review: dict) -> None:
    assert (
        review["source_snapshot_local_branch_count"],
        review["source_snapshot_remote_branch_count"],
        review["source_snapshot_total_branch_ref_count"],
    ) == (290, 261, 551)
    assert (
        review["source_post_plan_push_live_local_branch_count"],
        review["source_post_plan_push_live_remote_branch_count"],
        review["source_post_plan_push_live_total_branch_ref_count"],
    ) == (290, 262, 552)
    assert (
        review["source_operator_review_live_local_branch_count"],
        review["source_operator_review_live_remote_branch_count"],
        review["source_operator_review_live_total_branch_ref_count"],
    ) == (291, 263, 554)
    assert (
        review["source_candidate_live_local_branch_count"],
        review["source_candidate_live_remote_branch_count"],
        review["source_candidate_live_total_branch_ref_count"],
    ) == (292, 264, 556)


def test_source_candidate_context_is_preserved(review: dict) -> None:
    assert review["source_tagging_candidate_status"] == service.source_candidate_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert review["source_existing_tag_count"] == 28
    assert review["source_candidate_namespace_tag_count"] == 0
    assert review["source_category_summary"] == service.SOURCE_CATEGORY_SUMMARY
    assert sum(row["count"] for row in review["source_category_summary"]) == 551
    assert review["source_terminal_chain"] == service.SOURCE_TERMINAL_CHAIN


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_candidate_created",
        "repository_tagging_release_strategy_candidate_ready_for_operator_review",
        "repository_tagging_release_strategy_operator_review_created",
        "repository_tagging_release_strategy_operator_review_ready",
        "tagging_packages_reviewed",
        "tagging_candidates_reviewed",
        "tagging_prerequisites_reviewed",
        "tagging_policy_reviewed",
    ],
)
def test_source_and_review_completion_flags_are_true(review: dict, field: str) -> None:
    assert review[field] is True


def test_reviewed_tagging_philosophy_is_planning_only(review: dict) -> None:
    assert review["reviewed_tagging_philosophy"] == service.source_candidate_service.TAGGING_PHILOSOPHY
    assert "Candidate-only reviewed" in review["reviewed_tagging_boundary"]
    assert review["reviewed_tagging_goal"] == service.source_candidate_service.TAGGING_GOAL
    assert review["tagging_philosophy_review_status"] == "REVIEWED_PLANNING_ONLY"


def test_four_tagging_packages_are_reviewed_not_selected(review: dict) -> None:
    packages = review["reviewed_tagging_packages"]
    assert packages == service.REVIEWED_TAGGING_PACKAGES
    assert len(packages) == 4
    assert packages[0]["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)
    assert all(row["tags_created"] is False for row in packages)


def test_recommended_package_is_reviewed_but_not_selected(review: dict) -> None:
    assert review["recommended_tagging_package"] == service.source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS
    assert review["recommended_package_review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["repository_tagging_release_strategy_selected"] is False


def test_fourteen_candidate_tags_are_reviewed(review: dict) -> None:
    tags = review["reviewed_candidate_tag_definitions"]
    assert tags == service.REVIEWED_CANDIDATE_TAG_DEFINITIONS
    assert review["reviewed_candidate_tag_count"] == len(tags) == 14
    assert review["terminal_candidate_tag_count"] == 4
    assert review["governance_candidate_tag_count"] == 7
    assert review["protection_candidate_tag_count"] == 3
    assert all(row["review_status"] == "REVIEWED_CANDIDATE_TAG_NOT_CREATED" for row in tags)
    assert all(row["tag_created"] is False for row in tags)
    assert all(row["tag_pushed"] is False for row in tags)


@pytest.mark.parametrize(
    ("tag_name", "target_commit"),
    [
        ("marketflow/expectancy-lab/final-archive-not-ready/v1", "0be55dc8a65a586368c192d6bc13302b9830a0b4"),
        ("marketflow/expectancy-lab/archive-record-not-ready/v1", "e2fcfb792ad14db8a2de69556c291529fda47a8e"),
        ("marketflow/expectancy-lab/operator-selection-option-a/v1", "15c4fae495f88b54e30380f3d8b4aa54989fad39"),
        ("marketflow/expectancy-lab/readiness-not-ready/v1", "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0"),
    ],
)
def test_terminal_tags_are_reviewed_with_exact_commits(
    review: dict, tag_name: str, target_commit: str
) -> None:
    row = next(
        item for item in review["reviewed_candidate_tag_definitions"]
        if item["tag_name"] == tag_name
    )
    assert row["tag_target_commit"] == target_commit
    assert row["source_tag_status"] == "CANDIDATE_TAG_NOT_CREATED"
    assert row["operator_approval_required"] is True


def test_governance_tags_remain_unbound_for_operator_selection(review: dict) -> None:
    rows = {row["tag_name"]: row for row in review["reviewed_candidate_tag_definitions"]}
    for tag_name in service.source_candidate_service.GOVERNANCE_TAG_NAMES:
        assert rows[tag_name]["tag_target_branch"] == service.source_candidate_service.REQUIRES_OPERATOR_SELECTION
        assert rows[tag_name]["tag_target_commit"] == service.source_candidate_service.NOT_BOUND_BY_THIS_CANDIDATE


def test_all_prerequisites_are_reviewed_not_executed(review: dict) -> None:
    prerequisites = review["reviewed_prerequisites"]
    assert prerequisites == service.REVIEWED_PREREQUISITES
    assert len(prerequisites) == 10
    assert all(row["required"] is True for row in prerequisites)
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_TAGGING" for row in prerequisites)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in prerequisites)


def test_tag_message_template_review_preserves_all_boundaries(review: dict) -> None:
    template_review = review["reviewed_tag_message_template"]
    assert template_review == service.REVIEWED_TAG_MESSAGE_TEMPLATE
    assert template_review["template_review_status"] == "REVIEWED_PLANNING_ONLY"
    assert all(
        template_review[field] is True
        for field in (
            "tag_message_template_present",
            "tag_message_includes_not_accepted_usefulness",
            "tag_message_includes_not_accepted_profitability",
            "tag_message_includes_runtime_not_authorized",
            "tag_message_includes_trading_not_authorized",
            "tag_message_includes_no_trade_recommendation",
        )
    )


def test_all_non_goals_remain_active(review: dict) -> None:
    assert review["reviewed_tagging_non_goals"] == service.REVIEWED_TAGGING_NON_GOALS
    assert len(review["reviewed_tagging_non_goals"]) == 12
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_tagging_non_goals"])


def test_per_chain_review_is_complete_and_planning_only(review: dict) -> None:
    rows = review["per_chain_tagging_review_summary"]
    assert rows == service.PER_CHAIN_TAGGING_REVIEW_SUMMARY
    assert len(rows) == 9
    assert all(row["review_status"] == "REVIEWED_PLANNING_ONLY" for row in rows)
    assert all(row["tags_created"] is False for row in rows)
    assert all(row["approval_required"] is True for row in rows)
    assert all(row["operator_review_required"] is True for row in rows)
    assert all(row["merge_required"] is False for row in rows)
    assert all(row["main_push_required"] is False for row in rows)


def test_recommendation_requires_optional_selection_and_approval(review: dict) -> None:
    assert review["recommended_next_task"] == "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1_IF_SELECTED"
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["recommended_action"] == "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_TAGGING"
    assert review["ready_for_repository_tagging_release_strategy_approval"] is False
    assert "no package has been selected or approved" in review["recommendation_reason"]


@pytest.mark.parametrize(
    "field",
    [
        "ready_for_repository_tagging_release_strategy_approval",
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
        "provider_requests_made_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_approval_execution_provider_and_research_actions_remain_false(
    review: dict, field: str
) -> None:
    assert review[field] is False


def test_authority_boundaries_remain_closed(review: dict) -> None:
    assert review["predictive_usefulness"] == "not accepted"
    assert review["predictive_usefulness_accepted"] is False
    assert review["profitability"] == "not accepted"
    assert review["profitability_accepted"] is False
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_defined(review: dict) -> None:
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 6
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 7


def test_risk_controls_and_marketflow_tracking_guard_are_exact(review: dict) -> None:
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 32
    assert review["tracked_marketflow_file_count"] == 0
    assert review["no_tracked_marketflow_files"] is True


def test_checklist_passes(review: dict) -> None:
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 62
    assert review["summary"]["passed_checks"] == 62
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert review["summary"]["recommended_package_selected"] is False
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in review["checklist"]
    )


def test_review_digest_is_deterministic(review: dict) -> None:
    rebuilt = service.build_marketflow_repository_tagging_release_strategy_operator_review_v1()
    digest = review["marketflow_repository_tagging_release_strategy_operator_review_digest"]
    assert rebuilt["marketflow_repository_tagging_release_strategy_operator_review_digest"] == digest
    assert service.marketflow_repository_tagging_release_strategy_operator_review_digest_v1(review) == digest


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_VALID
    assert result["passed_checks"] == 62
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_tagging_candidate_digest", "0" * 64),
        ("source_inventory_operator_review_digest", "0" * 64),
        ("source_inventory_plan_digest", "0" * 64),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", ""),
        ("repository_tagging_release_strategy_operator_review_created", False),
        ("repository_tagging_release_strategy_operator_review_ready", False),
        ("tagging_packages_reviewed", False),
        ("tagging_candidates_reviewed", False),
        ("tagging_prerequisites_reviewed", False),
        ("ready_for_repository_tagging_release_strategy_approval", True),
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
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
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
    review: dict, field: str, value: object
) -> None:
    mutated = deepcopy(review)
    mutated[field] = value
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError):
        service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(mutated)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_tagging_packages",
        "reviewed_candidate_tag_definitions",
        "reviewed_prerequisites",
        "reviewed_tagging_non_goals",
        "per_chain_tagging_review_summary",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_required_structures(review: dict, field: str) -> None:
    mutated = deepcopy(review)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError):
        service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(mutated)


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    mutated = deepcopy(review)
    mutated.pop("marketflow_repository_tagging_release_strategy_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError):
        service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(mutated)


def test_source_candidate_must_be_an_object() -> None:
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError):
        service.build_marketflow_repository_tagging_release_strategy_operator_review_v1(
            source_candidate=[]  # type: ignore[arg-type]
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_tagging_release_strategy_operator_review_markdown_v1(review)
    for heading in (
        "Title",
        "MarketFlow Repository Tagging / Release Strategy Operator Review v1",
        "Source Tagging Candidate",
        "Bound Evidence",
        "Repository Context",
        "Review Scope",
        "Reviewed Tagging Philosophy",
        "Reviewed Tagging Packages",
        "Reviewed Candidate Tags",
        "Reviewed Prerequisites",
        "Reviewed Tag Message Template",
        "Reviewed Non-Goals",
        "Per-Chain Review Summary",
        "Recommendation",
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
    result = service.write_marketflow_repository_tagging_release_strategy_operator_review_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_tagging_release_strategy_operator_review_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    digest = payload["marketflow_repository_tagging_release_strategy_operator_review_digest"]
    assert digest == result["marketflow_repository_tagging_release_strategy_operator_review_digest"]
    service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(payload)
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyOperatorReviewError):
        service.write_marketflow_repository_tagging_release_strategy_operator_review_v1(tmp_path)
