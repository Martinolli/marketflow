from __future__ import annotations

from copy import deepcopy
import subprocess

import pytest

from marketflow.services import marketflow_repository_tagging_execution_service as service


RUN_TIMESTAMP = "2026-08-23T00:00:00Z"


@pytest.fixture
def execution() -> dict:
    return service.execute_marketflow_repository_tagging_v1(
        run_timestamp_utc=RUN_TIMESTAMP,
        execute_git_operations=False,
    )


def _git(repo, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def _temporary_repo_with_targets(tmp_path, monkeypatch: pytest.MonkeyPatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "MarketFlow Test")
    _git(repo, "config", "user.email", "marketflow-test@example.invalid")
    commits = []
    for index in range(4):
        path = repo / f"target-{index}.txt"
        path.write_text(f"target {index}\n", encoding="utf-8")
        _git(repo, "add", path.name)
        _git(repo, "commit", "-q", "-m", f"target {index}")
        commits.append(_git(repo, "rev-parse", "HEAD"))
    specs = deepcopy(service.APPROVED_TERMINAL_TAGS)
    for spec, commit in zip(specs, commits):
        spec["target_commit"] = commit
    monkeypatch.setattr(service, "APPROVED_TERMINAL_TAGS", specs)
    return repo, commits


def test_fixture_execution_is_deterministic_and_does_not_call_git(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service,
        "_run_git",
        lambda *args, **kwargs: pytest.fail("fixture mode must not call Git"),
    )
    first = service.execute_marketflow_repository_tagging_v1(
        run_timestamp_utc=RUN_TIMESTAMP, execute_git_operations=False
    )
    second = service.execute_marketflow_repository_tagging_v1(
        run_timestamp_utc=RUN_TIMESTAMP, execute_git_operations=False
    )
    assert first == second
    assert first["deterministic_fixture_mode"] is True


def test_actual_tag_creation_is_isolated_to_temporary_repository(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, commits = _temporary_repo_with_targets(tmp_path, monkeypatch)
    result = service.execute_marketflow_repository_tagging_v1(
        repo_root=repo,
        run_timestamp_utc=RUN_TIMESTAMP,
    )
    assert result["created_terminal_tag_count"] == 4
    assert result["existing_matching_terminal_tag_count"] == 0
    assert result["tag_count_summary"]["tag_count_before_execution"] == 0
    assert result["tag_count_summary"]["tag_count_after_execution"] == 4
    for record, commit in zip(result["terminal_tag_execution_records"], commits):
        assert _git(repo, "cat-file", "-t", record["tag_object_sha"]) == "tag"
        assert _git(repo, "rev-parse", f"{record['tag_name']}^{{commit}}") == commit


def test_matching_annotated_tags_are_not_recreated(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, _ = _temporary_repo_with_targets(tmp_path, monkeypatch)
    first = service.execute_marketflow_repository_tagging_v1(
        repo_root=repo, run_timestamp_utc=RUN_TIMESTAMP
    )
    second = service.execute_marketflow_repository_tagging_v1(
        repo_root=repo, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert first["created_terminal_tag_count"] == 4
    assert second["created_terminal_tag_count"] == 0
    assert second["existing_matching_terminal_tag_count"] == 4
    assert all(row["tag_status"] == service.TAG_STATUS_EXISTING for row in second["terminal_tag_execution_records"])


def test_lightweight_existing_tag_blocks_before_other_creation(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, commits = _temporary_repo_with_targets(tmp_path, monkeypatch)
    _git(repo, "tag", service.APPROVED_TERMINAL_TAG_NAMES[0], commits[0])
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionBlockedError) as caught:
        service.execute_marketflow_repository_tagging_v1(
            repo_root=repo, run_timestamp_utc=RUN_TIMESTAMP
        )
    assert caught.value.blocked_artifact["artifact_kind"] == service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_BLOCKED
    assert caught.value.blocked_artifact["created_tag_names_before_block"] == []
    assert len(_git(repo, "for-each-ref", "--format=%(refname)", "refs/tags").splitlines()) == 1


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1),
        ("execution_status", service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED),
        ("execution_scope", service.REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("selected_tagging_package", service.SELECTED_TAGGING_PACKAGE),
        ("source_tagging_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_approval_commit", service.EXPECTED_SOURCE_APPROVAL_COMMIT),
    ],
)
def test_artifact_identity_and_source_bindings(
    execution: dict, field: str, expected: object
) -> None:
    assert execution[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_selected",
        "repository_tagging_release_strategy_approved",
        "repository_tagging_release_strategy_authorized",
        "repository_tagging_release_strategy_executed",
        "repository_tags_created",
        "git_tag_created",
        "local_annotated_tags_created",
        "ready_for_repository_tagging_execution_results_review",
    ],
)
def test_execution_completion_flags_are_true(execution: dict, field: str) -> None:
    assert execution[field] is True


def test_four_terminal_tags_have_exact_names_targets_and_annotated_objects(
    execution: dict,
) -> None:
    rows = execution["terminal_tag_execution_records"]
    assert execution["approved_terminal_tag_count"] == len(rows) == 4
    assert execution["created_terminal_tag_count"] + execution["existing_matching_terminal_tag_count"] == 4
    assert [row["tag_name"] for row in rows] == service.APPROVED_TERMINAL_TAG_NAMES
    assert [row["target_commit"] for row in rows] == [row["target_commit"] for row in service.APPROVED_TERMINAL_TAGS]
    assert all(row["tag_type"] == "ANNOTATED" for row in rows)
    assert all(len(row["tag_object_sha"]) == 40 for row in rows)


@pytest.mark.parametrize(
    ("tag_name", "target_commit"),
    [
        ("marketflow/expectancy-lab/final-archive-not-ready/v1", "0be55dc8a65a586368c192d6bc13302b9830a0b4"),
        ("marketflow/expectancy-lab/archive-record-not-ready/v1", "e2fcfb792ad14db8a2de69556c291529fda47a8e"),
        ("marketflow/expectancy-lab/operator-selection-option-a/v1", "15c4fae495f88b54e30380f3d8b4aa54989fad39"),
        ("marketflow/expectancy-lab/readiness-not-ready/v1", "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0"),
    ],
)
def test_exact_terminal_tag_target(execution: dict, tag_name: str, target_commit: str) -> None:
    row = next(item for item in execution["terminal_tag_execution_records"] if item["tag_name"] == tag_name)
    assert row["target_commit"] == target_commit
    assert row["tag_target_commit_verified"] is True


def test_tag_messages_preserve_all_authority_boundaries(execution: dict) -> None:
    for row in execution["terminal_tag_execution_records"]:
        message = row["tag_message"]
        assert "Predictive usefulness: NOT_ACCEPTED" in message
        assert "Profitability: NOT_ACCEPTED" in message
        assert "Runtime: NOT_AUTHORIZED" in message
        assert "Trading/Broker: NOT_AUTHORIZED" in message
        assert "No trade recommendation is created by this tag." in message
        assert row["source_digest"] in message
        assert row["tag_message_verified"] is True


@pytest.mark.parametrize(
    "field",
    [
        "repository_tags_pushed",
        "git_tag_push_performed",
        "git_merge_performed",
        "git_rebase_performed",
        "git_branch_delete_performed",
        "git_remote_delete_performed",
        "git_main_push_performed",
        "git_force_push_performed",
        "git_remote_prune_performed",
        "origin_main_modified_by_this_task",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ],
)
def test_forbidden_actions_remain_false(execution: dict, field: str) -> None:
    assert execution[field] is False


def test_authority_strings_remain_closed(execution: dict) -> None:
    assert execution["predictive_usefulness"] == service.NOT_ACCEPTED
    assert execution["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert execution[field] == service.NOT_AUTHORIZED


def test_tag_counts_next_chain_and_controls(execution: dict) -> None:
    assert execution["tag_count_summary"] == {
        "tag_count_before_execution": 28,
        "candidate_namespace_tag_count_before_execution": 0,
        "approved_terminal_tag_count": 4,
        "created_terminal_tag_count": 4,
        "existing_matching_terminal_tag_count": 0,
        "tag_count_after_execution": 32,
        "candidate_namespace_tag_count_after_execution": 4,
        "tag_count_observation_note": "Observed expected 28/0 before and 32/4 after local tag creation.",
    }
    assert execution["next_chain"] == service.NEXT_CHAIN
    assert execution["next_gates"] == service.NEXT_GATES
    assert execution["risk_controls"] == service.RISK_CONTROLS
    assert len(service.NEXT_CHAIN) == 6
    assert len(service.NEXT_GATES) == 7
    assert len(service.RISK_CONTROLS) == 35


def test_checklist_passes(execution: dict) -> None:
    assert [row["check_id"] for row in execution["checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(execution["checklist"]) == 54
    assert all(row["status"] == service.PASS for row in execution["checklist"])
    assert execution["summary"]["passed_checks"] == 54
    assert execution["summary"]["failed_checks"] == 0
    assert execution["summary"]["blocker_count"] == 0


def test_execution_and_manifest_digests_are_deterministic(execution: dict) -> None:
    rebuilt = service.execute_marketflow_repository_tagging_v1(
        run_timestamp_utc=RUN_TIMESTAMP, execute_git_operations=False
    )
    assert rebuilt["marketflow_repository_tagging_execution_digest"] == execution["marketflow_repository_tagging_execution_digest"]
    assert rebuilt["marketflow_repository_tagging_execution_tag_manifest_digest"] == execution["marketflow_repository_tagging_execution_tag_manifest_digest"]
    assert service.marketflow_repository_tagging_execution_digest_v1(execution) == execution["marketflow_repository_tagging_execution_digest"]
    assert service.marketflow_repository_tagging_execution_tag_manifest_digest_v1(execution) == execution["marketflow_repository_tagging_execution_tag_manifest_digest"]


def test_validator_accepts_valid_execution(execution: dict) -> None:
    result = service.validate_marketflow_repository_tagging_execution_v1(execution)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_VALID
    assert result["passed_checks"] == 54
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("execution_scope", "WRONG"),
        ("selected_tagging_package", "WRONG"),
        ("source_tagging_approval_digest", "0" * 64),
        ("source_operator_review_digest", "0" * 64),
        ("source_candidate_digest", "0" * 64),
        ("source_inventory_plan_digest", "0" * 64),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tagging_release_strategy_authorized", False),
        ("repository_tagging_release_strategy_executed", False),
        ("repository_tags_created", False),
        ("local_annotated_tags_created", False),
        ("approved_terminal_tag_count", 3),
        ("terminal_tag_execution_records", []),
        ("repository_tags_pushed", True),
        ("git_tag_push_performed", True),
        ("git_merge_performed", True),
        ("git_rebase_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_main_push_performed", True),
        ("git_force_push_performed", True),
        ("git_remote_prune_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_execution", True),
        ("market_data_acquisition_performed_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness_accepted", True),
        ("profitability_accepted", True),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_top_level_contract_mutations(
    execution: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(execution)
    mutated[field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionError):
        service.validate_marketflow_repository_tagging_execution_v1(mutated)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("target_commit", "0" * 40),
        ("tag_type", "LIGHTWEIGHT"),
        ("tag_object_sha", "WRONG"),
        ("tag_target_commit_verified", False),
        ("tag_message_verified", False),
        ("tag_created", False),
        ("tag_pushed", True),
        ("runtime_authority_created", True),
        ("predictive_usefulness_accepted", True),
        ("profitability_accepted", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_terminal_tag_mutations(
    execution: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(execution)
    mutated["terminal_tag_execution_records"][0][field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionError):
        service.validate_marketflow_repository_tagging_execution_v1(mutated)


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_tagging_execution_digest",
        "marketflow_repository_tagging_execution_tag_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(execution: dict, field: str) -> None:
    mutated = deepcopy(execution)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionError):
        service.validate_marketflow_repository_tagging_execution_v1(mutated)


def test_markdown_contains_required_sections(execution: dict) -> None:
    markdown = service.build_marketflow_repository_tagging_execution_markdown_v1(execution)
    for section in (
        "Title",
        "MarketFlow Repository Tagging Execution v1",
        "Source Approval",
        "Bound Evidence",
        "Repository Context",
        "Execution Scope",
        "Created Local Annotated Tags",
        "Tag Count Summary",
        "Tag Messages",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown
