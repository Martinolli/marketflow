from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_state_branch_inventory_integration_plan_service as service,
)


def _ref(ref_name: str, commit: str, subject: str = "Inventory fixture") -> dict:
    if ref_name.startswith("refs/heads/"):
        ref_type = "LOCAL"
        short_name = ref_name.removeprefix("refs/heads/")
    else:
        ref_type = "REMOTE"
        short_name = ref_name.removeprefix("refs/remotes/")
    return {
        "ref_name": ref_name,
        "ref_type": ref_type,
        "short_name": short_name,
        "commit_sha": commit,
        "subject": subject,
        "committer_date": "2026-08-28T12:00:00+04:00",
        "symbolic_target": None,
    }


@pytest.fixture
def git_snapshot() -> dict:
    base = service.EXPECTED_INVENTORY_BASE_COMMIT
    main = service.EXPECTED_ORIGIN_MAIN_COMMIT
    refs = [
        _ref(f"refs/heads/{service.PLAN_BRANCH}", base),
        _ref(f"refs/heads/{service.TERMINAL_BRANCH}", base),
        _ref("refs/heads/feature/mystery-unclassified", "1" * 40),
        _ref("refs/heads/feature/broker-diagnostic-v1", "2" * 40),
        _ref("refs/heads/main", main),
        _ref(f"refs/remotes/origin/{service.TERMINAL_BRANCH}", base),
        _ref("refs/remotes/origin/feature/remote-only-misc-v1", "3" * 40),
        _ref("refs/remotes/origin/main", main),
    ]
    return {
        "repo_root_name": "marketflow",
        "current_branch": service.PLAN_BRANCH,
        "current_head_commit": base,
        "origin_main_commit": main,
        "main_commit_if_available": main,
        "working_tree_clean": True,
        "tracked_marketflow_files": [],
        "refs": refs,
    }


@pytest.fixture
def plan(git_snapshot: dict) -> dict:
    return service.build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        git_snapshot=git_snapshot
    )


def test_plan_builds_offline_from_deterministic_git_snapshot(
    git_snapshot: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        service.subprocess,
        "run",
        lambda *args, **kwargs: pytest.fail("subprocess must not run for supplied snapshot"),
    )
    plan = service.build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        git_snapshot=git_snapshot
    )
    assert plan["created_offline"] is True
    assert plan["branch_inventory_created"] is True


def test_plan_can_collect_using_only_read_only_git_commands(
    tmp_path: Path, git_snapshot: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".git").mkdir()
    calls: list[tuple[str, ...]] = []

    def fake_run_git(root: Path, *args: str, allow_failure: bool = False) -> str:
        calls.append(args)
        if args[:2] == ("branch", "--show-current"):
            return git_snapshot["current_branch"]
        if args[:2] == ("rev-parse", "HEAD"):
            return git_snapshot["current_head_commit"]
        if args[:2] == ("rev-parse", "origin/main"):
            return git_snapshot["origin_main_commit"]
        if args[:3] == ("rev-parse", "--verify", "main"):
            return git_snapshot["main_commit_if_available"]
        if args[0] in {"status", "ls-files"}:
            return ""
        if args[0] == "for-each-ref":
            return "\n".join(
                "\t".join(
                    [row["ref_name"], row["commit_sha"], row["committer_date"], row["subject"], ""]
                )
                for row in git_snapshot["refs"]
            )
        raise AssertionError(args)

    monkeypatch.setattr(service, "_run_git", fake_run_git)
    plan = service.build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        repo_root=tmp_path
    )
    assert plan["total_branch_ref_count"] == len(git_snapshot["refs"])
    assert {call[0] for call in calls} <= {
        "status", "branch", "for-each-ref", "rev-parse", "ls-files"
    }


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1),
        ("artifact_status", service.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY),
        ("plan_scope", service.REPOSITORY_STATE_AND_BRANCH_INVENTORY_PLANNING_ONLY_NOT_MERGE_NOT_DELETE_NOT_TAG_NOT_MAIN),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_archive_digest", service.EXPECTED_SOURCE_ARCHIVE_DIGEST),
        ("source_operator_selection_digest", service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST),
        ("source_closure_digest", service.EXPECTED_SOURCE_CLOSURE_DIGEST),
        ("source_acceptance_readiness_digest", service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST),
        ("source_reassessment_digest", service.EXPECTED_SOURCE_REASSESSMENT_DIGEST),
        ("source_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_backtest_rows_digest", service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST),
        ("source_metric_report_digest", service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
    ],
)
def test_artifact_identity_and_source_bindings(
    plan: dict, field: str, expected: object
) -> None:
    assert plan[field] == expected


def test_complete_source_evidence_and_dataset_context_are_preserved(plan: dict) -> None:
    assert len(plan["source_evidence"]) == 57
    assert plan["target_universe"] == service.TARGET_UNIVERSE
    assert plan["target_universe_count"] == 12
    assert plan["total_canonical_record_count"] == 11946
    assert plan["meta_record_count"] == 913
    assert plan["non_meta_record_count"] == 1003


def test_repository_commits_and_current_branch_are_bound(plan: dict) -> None:
    assert plan["current_branch"] == service.PLAN_BRANCH
    assert plan["current_head_commit"] == service.EXPECTED_INVENTORY_BASE_COMMIT
    assert plan["origin_main_commit"] == service.EXPECTED_ORIGIN_MAIN_COMMIT
    assert plan["main_commit_if_available"] == service.EXPECTED_ORIGIN_MAIN_COMMIT
    assert plan["main_modified"] is False
    assert plan["working_tree_clean"] is True


def test_inventory_counts_are_recorded(plan: dict) -> None:
    assert plan["local_branch_count"] == 5
    assert plan["remote_branch_count"] == 3
    assert plan["total_branch_ref_count"] == 8
    assert len(plan["branch_inventory"]) == 8


def test_origin_main_and_terminal_branches_are_protected(plan: dict) -> None:
    origin_main = next(row for row in plan["branch_inventory"] if row["is_origin_main"])
    terminal = [row for row in plan["branch_inventory"] if row["is_terminal_archive_branch"]]
    assert origin_main["category"] == service.CATEGORY_MAIN_PROTECTED
    assert origin_main["suggested_disposition"] == "PROTECT_DO_NOT_TOUCH"
    assert len(terminal) == 2
    assert all(row["suggested_disposition"] == "KEEP_TERMINAL_EVIDENCE" for row in terminal)


@pytest.mark.parametrize(
    "field",
    [
        "git_merge_performed", "git_rebase_performed", "git_branch_delete_performed",
        "git_remote_delete_performed", "git_tag_created", "git_main_push_performed",
        "git_force_push_performed", "git_remote_prune_performed",
    ],
)
def test_no_git_integration_or_cleanup_action_is_performed(plan: dict, field: str) -> None:
    assert plan[field] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_inventory",
        "market_data_acquisition_performed_in_inventory",
        "dataset_generation_performed_in_inventory",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_no_provider_data_metric_training_or_scoring_action_is_performed(
    plan: dict, field: str
) -> None:
    assert plan[field] is False


def test_authority_boundaries_remain_closed(plan: dict) -> None:
    assert plan["predictive_usefulness"] == "not accepted"
    assert plan["predictive_usefulness_accepted"] is False
    assert plan["profitability"] == "not accepted"
    assert plan["profitability_accepted"] is False
    assert plan["runtime_use"] == "NOT_AUTHORIZED"
    assert plan["strategy_use"] == "NOT_AUTHORIZED"
    assert plan["paper_trading"] == "NOT_AUTHORIZED"
    assert plan["broker_execution"] == "NOT_AUTHORIZED"


def test_branch_categories_and_role_flags_are_assigned(plan: dict) -> None:
    assert all(row["category"].startswith("CATEGORY_") for row in plan["branch_inventory"])
    assert sum(row["ref_count"] for row in plan["branch_category_summary"]) == 8
    broker = next(row for row in plan["branch_inventory"] if "broker-diagnostic" in row["short_name"])
    assert broker["is_ibkr_or_broker_branch"] is True
    assert broker["category"] == service.CATEGORY_IBKR_OR_BROKER_CHAIN


def test_unknown_branches_require_operator_review(plan: dict) -> None:
    unknown = next(row for row in plan["branch_inventory"] if row["short_name"] == "feature/mystery-unclassified")
    assert unknown["is_unknown_category"] is False
    assert unknown["category"] == service.CATEGORY_OTHER_FEATURE_BRANCH
    assert unknown["suggested_disposition"] == "CANDIDATE_FOR_FUTURE_ARCHIVE_AFTER_OPERATOR_CONFIRMATION"
    remote_only = next(row for row in plan["branch_inventory"] if row["short_name"] == "origin/feature/remote-only-misc-v1")
    assert remote_only["category"] == service.CATEGORY_OTHER_FEATURE_BRANCH
    assert remote_only["suggested_disposition"] == "CANDIDATE_FOR_FUTURE_ARCHIVE_AFTER_OPERATOR_CONFIRMATION"


def test_unknown_non_feature_branch_is_never_touched(git_snapshot: dict) -> None:
    mutated = deepcopy(git_snapshot)
    mutated["refs"].append(_ref("refs/heads/unclassified-root-branch", "4" * 40))
    plan = service.build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        git_snapshot=mutated
    )
    unknown = next(row for row in plan["branch_inventory"] if row["short_name"] == "unclassified-root-branch")
    assert unknown["category"] == service.CATEGORY_UNKNOWN_REQUIRES_OPERATOR_REVIEW
    assert unknown["suggested_disposition"] == "UNKNOWN_DO_NOT_TOUCH"


def test_chain_summaries_include_terminal_and_required_chains(plan: dict) -> None:
    assert len(plan["chain_summaries"]) == 10
    terminal = plan["chain_summaries"][0]
    assert terminal["chain_status"] == "TERMINAL_ARCHIVED_NOT_READY"
    assert terminal["terminal_branch_if_known"] == service.TERMINAL_BRANCH
    assert terminal["terminal_commit_if_known"] == service.EXPECTED_INVENTORY_BASE_COMMIT
    assert terminal["recommended_next_action"] == "NONE_FOR_CURRENT_ARCHIVED_PATH"
    assert terminal["merge_readiness"] == "NOT_EVALUATED_BY_THIS_TASK"
    assert terminal["delete_readiness"] == "NOT_AUTHORIZED_BY_THIS_TASK"
    assert terminal["archive_readiness"] == "PLANNING_ONLY"


def test_integration_phases_and_policy_are_conservative(plan: dict) -> None:
    assert plan["integration_phases"] == service.INTEGRATION_PHASES
    assert len(plan["integration_phases"]) == 6
    assert plan["integration_phases"][0]["status"] == "COMPLETED_BY_THIS_ARTIFACT"
    assert all(row["status"] == "FUTURE_NOT_STARTED" for row in plan["integration_phases"][1:])
    assert plan["recommended_policy"] == "INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG"
    assert plan["recommended_immediate_next_task"] == "MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1"


def test_risk_controls_and_marketflow_tracking_guard_are_exact(plan: dict) -> None:
    assert plan["risk_controls"] == service.RISK_CONTROLS
    assert len(plan["risk_controls"]) == 29
    assert plan["tracked_marketflow_file_count"] == 0
    assert plan["tracked_marketflow_files"] == []
    assert plan["no_tracked_marketflow_files"] is True


def test_checklist_passes(plan: dict) -> None:
    assert plan["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 45
    assert plan["summary"]["passed_checks"] == 45
    assert plan["summary"]["failed_checks"] == 0
    assert plan["summary"]["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in plan["checklist"])


def test_plan_digest_is_deterministic(plan: dict, git_snapshot: dict) -> None:
    rebuilt = service.build_marketflow_repository_state_branch_inventory_integration_plan_v1(
        git_snapshot=git_snapshot
    )
    assert rebuilt["marketflow_repository_state_branch_inventory_integration_plan_digest"] == plan["marketflow_repository_state_branch_inventory_integration_plan_digest"]


def test_validator_accepts_valid_plan(plan: dict) -> None:
    result = service.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(plan)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_INTEGRATION_PLAN_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("artifact_status", "WRONG"),
        ("plan_scope", "WRONG"),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", ""),
        ("current_head_commit", ""),
        ("integration_plan_created", False),
        ("git_merge_performed", True),
        ("git_rebase_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_tag_created", True),
        ("git_main_push_performed", True),
        ("git_force_push_performed", True),
        ("git_remote_prune_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_inventory", True),
        ("market_data_acquisition_performed_in_inventory", True),
        ("dataset_generation_performed_in_inventory", True),
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
    plan: dict, field: str, value: object
) -> None:
    mutated = deepcopy(plan)
    mutated[field] = value
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryIntegrationPlanError):
        service.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(mutated)


@pytest.mark.parametrize("field", ["branch_inventory", "integration_phases", "risk_controls"])
def test_validator_rejects_missing_required_structures(plan: dict, field: str) -> None:
    mutated = deepcopy(plan)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryIntegrationPlanError):
        service.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(mutated)


def test_validator_rejects_changed_branch_classification(plan: dict) -> None:
    mutated = deepcopy(plan)
    mutated["branch_inventory"][0]["category"] = "CATEGORY_WRONG"
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryIntegrationPlanError):
        service.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(mutated)


def test_validator_rejects_missing_plan_digest(plan: dict) -> None:
    mutated = deepcopy(plan)
    mutated.pop("marketflow_repository_state_branch_inventory_integration_plan_digest")
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryIntegrationPlanError):
        service.validate_marketflow_repository_state_branch_inventory_integration_plan_v1(mutated)


def test_markdown_includes_required_sections(plan: dict) -> None:
    markdown = service.build_marketflow_repository_state_branch_inventory_integration_plan_markdown_v1(plan)
    for heading in (
        "Title", "MarketFlow Repository State, Branch Inventory, and Integration Plan v1",
        "Source Final Archive Summary", "Repository State", "Branch Inventory Summary",
        "Branch Category Summary", "Terminal Evidence Chains", "Expectancy Lab Archive Chain",
        "Integration Plan", "Recommended Policy", "Protected Branches",
        "Branches Requiring Operator Review", "Future Cleanup Considerations",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(
    tmp_path: Path, git_snapshot: dict
) -> None:
    result = service.write_marketflow_repository_state_branch_inventory_integration_plan_v1(
        tmp_path, git_snapshot=git_snapshot
    )
    path = tmp_path / "marketflow_repository_state_branch_inventory_integration_plan_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["marketflow_repository_state_branch_inventory_integration_plan_digest"] == result["marketflow_repository_state_branch_inventory_integration_plan_digest"]
    with pytest.raises(service.MarketFlowRepositoryStateBranchInventoryIntegrationPlanError):
        service.write_marketflow_repository_state_branch_inventory_integration_plan_v1(
            tmp_path, git_snapshot=git_snapshot
        )
