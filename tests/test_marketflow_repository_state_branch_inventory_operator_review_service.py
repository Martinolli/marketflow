from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_state_branch_inventory_operator_review_service as service,
)


@pytest.fixture
def review() -> dict:
    return service.build_marketflow_repository_state_branch_inventory_operator_review_v1()


def test_review_builds_offline_without_rerunning_source_inventory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.inventory_plan,
        "build_marketflow_repository_state_branch_inventory_integration_plan_v1",
        lambda *args, **kwargs: pytest.fail("source inventory must not be rerun"),
    )
    review = service.build_marketflow_repository_state_branch_inventory_operator_review_v1()
    assert review["created_offline"] is True
    assert review["repository_inventory_operator_review_created"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_archive_digest", service.EXPECTED_SOURCE_ARCHIVE_DIGEST),
        ("source_operator_selection_digest", service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
    ],
)
def test_artifact_identity_and_required_source_bindings(
    review: dict, field: str, expected: object
) -> None:
    assert review[field] == expected


def test_complete_upstream_digest_chain_is_preserved(review: dict) -> None:
    assert len(review["source_evidence"]) == 57
    assert review["source_closure_digest"] == service.EXPECTED_SOURCE_CLOSURE_DIGEST
    assert review["source_readiness_digest"] == service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
    assert review["source_reassessment_digest"] == service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
    assert review["source_results_review_digest"] == service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
    assert review["source_backtest_rows_digest"] == service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
    assert review["source_metric_report_digest"] == service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST


def test_source_and_post_push_inventory_counts_are_bound(review: dict) -> None:
    assert (
        review["source_snapshot_local_branch_count"],
        review["source_snapshot_remote_branch_count"],
        review["source_snapshot_total_branch_ref_count"],
    ) == (290, 261, 551)
    assert (
        review["post_push_live_local_branch_count"],
        review["post_push_live_remote_branch_count"],
        review["post_push_live_total_branch_ref_count"],
    ) == (290, 262, 552)
    assert review["inventory_count_review_finding"] == (
        "INVENTORY_REVIEWED_WITH_EXPECTED_POST_PUSH_REMOTE_REF_DELTA"
    )
    assert review["inventory_count_delta_reason"] == (
        "CURRENT_INVENTORY_BRANCH_PUSH_ADDS_ONE_REMOTE_TRACKING_REF_AFTER_SOURCE_SNAPSHOT"
    )


@pytest.mark.parametrize(
    "field",
    [
        "repository_inventory_operator_review_created",
        "repository_inventory_operator_review_ready",
        "inventory_review_completed",
        "inventory_categories_reviewed",
        "integration_phases_reviewed",
        "recommended_policy_reviewed",
        "ready_for_repository_tagging_release_strategy_candidate",
    ],
)
def test_review_completion_flags_are_true(review: dict, field: str) -> None:
    assert review[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_candidate_created",
        "repository_merge_strategy_candidate_created",
        "repository_cleanup_candidate_created",
        "repository_cleanup_approved",
        "repository_cleanup_executed",
        "merge_approval_created",
        "delete_approval_created",
        "tag_approval_created",
        "git_merge_performed",
        "git_rebase_performed",
        "git_branch_delete_performed",
        "git_remote_delete_performed",
        "git_tag_created",
        "git_main_push_performed",
        "git_force_push_performed",
        "git_remote_prune_performed",
        "origin_main_modified_by_this_task",
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


def test_main_origin_main_and_marketflow_outputs_are_protected(review: dict) -> None:
    assert review["main_protection_reviewed"] is True
    assert review["origin_main_commit"] == service.EXPECTED_ORIGIN_MAIN_COMMIT
    assert review["origin_main_modified_by_this_task"] is False
    assert review["tracked_marketflow_file_count"] == 0
    assert review["no_tracked_marketflow_files"] is True


def test_authority_boundaries_remain_closed(review: dict) -> None:
    assert review["predictive_usefulness"] == "not accepted"
    assert review["predictive_usefulness_accepted"] is False
    assert review["profitability"] == "not accepted"
    assert review["profitability_accepted"] is False
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"


def test_category_review_is_complete_and_exact(review: dict) -> None:
    assert review["category_reviews"] == service.CATEGORY_REVIEWS
    assert len(review["category_reviews"]) == 11
    assert sum(row["source_count"] for row in review["category_reviews"]) == 551


def test_terminal_chain_is_reviewed_without_immediate_action(review: dict) -> None:
    terminal = review["terminal_chain_review"]
    assert terminal["chain_id"] == "CHAIN_EXPECTANCY_LAB_PREDICTIVE_USEFULNESS_PATH"
    assert terminal["chain_status"] == "TERMINAL_ARCHIVED_NOT_READY"
    assert terminal["review_status"] == "REVIEWED_TERMINAL_NO_IMMEDIATE_ACTION"
    assert terminal["recommended_next_action"] == "NONE_FOR_CURRENT_ARCHIVED_PATH"
    assert terminal["merge_readiness"] == "NOT_EVALUATED_BY_THIS_REVIEW"
    assert terminal["delete_readiness"] == "NOT_AUTHORIZED_BY_THIS_REVIEW"


def test_other_chains_are_reviewed_as_planning_only(review: dict) -> None:
    assert review["other_chain_reviews"] == service.OTHER_CHAIN_REVIEWS
    assert len(review["other_chain_reviews"]) == 9
    assert all(row["review_status"] == "REVIEWED_PLANNING_ONLY" for row in review["other_chain_reviews"])
    assert all(row["merge_readiness"] == "NOT_EVALUATED_BY_THIS_REVIEW" for row in review["other_chain_reviews"])
    assert all(row["delete_readiness"] == "NOT_AUTHORIZED_BY_THIS_REVIEW" for row in review["other_chain_reviews"])


def test_integration_phases_are_reviewed_and_only_phase_two_is_ready(review: dict) -> None:
    assert review["integration_phase_reviews"] == service.INTEGRATION_PHASE_REVIEWS
    assert len(review["integration_phase_reviews"]) == 6
    assert review["integration_phase_reviews"][0]["review_status"] == "REVIEWED_COMPLETE"
    assert review["integration_phase_reviews"][1]["review_status"] == "COMPLETED_BY_THIS_ARTIFACT"
    assert [row["phase_number"] for row in review["integration_phase_reviews"] if row["next_candidate_ready"]] == [2]


def test_policy_and_recommendation_are_review_only(review: dict) -> None:
    assert review["reviewed_policy"] == "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG"
    assert review["policy_review_status"] == "REVIEWED_ACCEPTED_FOR_PLANNING"
    assert review["recommended_next_task"] == "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1"
    assert review["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["recommended_action"] == "CREATE_TAGGING_RELEASE_STRATEGY_CANDIDATE_PLANNING_ONLY"
    assert review["merge_or_delete_now_recommended"] is False
    assert review["main_push_now_recommended"] is False
    assert review["tag_now_recommended"] is False
    assert review["cleanup_now_recommended"] is False


def test_next_chain_and_gates_are_complete(review: dict) -> None:
    assert review["next_chain"] == service.NEXT_CHAIN
    assert len(review["next_chain"]) == 7
    assert review["next_gates"] == service.NEXT_GATES
    assert len(review["next_gates"]) == 8


def test_risk_controls_and_checklist_are_complete(review: dict) -> None:
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(review["risk_controls"]) == 29
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 56
    assert review["summary"]["passed_checks"] == 56
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert all(
        set(row) == {"check_id", "status", "expected", "actual", "severity", "message"}
        for row in review["checklist"]
    )


def test_review_digest_is_deterministic(review: dict) -> None:
    rebuilt = service.build_marketflow_repository_state_branch_inventory_operator_review_v1()
    digest = review["marketflow_repository_state_branch_inventory_operator_review_digest"]
    assert rebuilt["marketflow_repository_state_branch_inventory_operator_review_digest"] == digest
    assert service.marketflow_repository_state_branch_inventory_operator_review_digest_v1(review) == digest


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_VALID
    assert result["passed_checks"] == 56
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_inventory_plan_digest", "0" * 64),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", ""),
        ("repository_inventory_operator_review_created", False),
        ("repository_inventory_operator_review_ready", False),
        ("recommended_policy_reviewed", False),
        ("ready_for_repository_tagging_release_strategy_candidate", False),
        ("repository_tagging_release_strategy_candidate_created", True),
        ("repository_merge_strategy_candidate_created", True),
        ("repository_cleanup_candidate_created", True),
        ("git_merge_performed", True),
        ("git_rebase_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_tag_created", True),
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
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryOperatorReviewError):
        service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(mutated)


@pytest.mark.parametrize(
    "field", ["category_reviews", "integration_phase_reviews", "risk_controls"]
)
def test_validator_rejects_missing_required_structures(review: dict, field: str) -> None:
    mutated = deepcopy(review)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryOperatorReviewError):
        service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(mutated)


def test_validator_rejects_missing_review_digest(review: dict) -> None:
    mutated = deepcopy(review)
    mutated.pop("marketflow_repository_state_branch_inventory_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryOperatorReviewError):
        service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(mutated)


def test_source_plan_must_be_an_object() -> None:
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryOperatorReviewError):
        service.build_marketflow_repository_state_branch_inventory_operator_review_v1(
            source_plan=[]  # type: ignore[arg-type]
        )


def test_markdown_includes_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_state_branch_inventory_operator_review_markdown_v1(review)
    for heading in (
        "Title",
        "MarketFlow Repository State Branch Inventory Operator Review v1",
        "Source Inventory Plan",
        "Repository State Review",
        "Inventory Count Review",
        "Category Review",
        "Terminal Expectancy Lab Chain Review",
        "Other Chain Reviews",
        "Integration Phase Review",
        "Policy Review",
        "Recommended Next Task",
        "Protected Branches",
        "Branches Requiring Operator Review",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(
    tmp_path: Path,
) -> None:
    result = service.write_marketflow_repository_state_branch_inventory_operator_review_v1(
        tmp_path
    )
    path = tmp_path / "marketflow_repository_state_branch_inventory_operator_review_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    digest = payload["marketflow_repository_state_branch_inventory_operator_review_digest"]
    assert digest == result["marketflow_repository_state_branch_inventory_operator_review_digest"]
    service.validate_marketflow_repository_state_branch_inventory_operator_review_v1(payload)
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryOperatorReviewError):
        service.write_marketflow_repository_state_branch_inventory_operator_review_v1(tmp_path)
