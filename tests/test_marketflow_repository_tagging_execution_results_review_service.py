from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from marketflow.services import (
    marketflow_repository_tagging_execution_results_review_service as service,
)


@pytest.fixture
def git_snapshot() -> dict:
    return service.deterministic_marketflow_repository_tagging_execution_results_review_snapshot_v1()


@pytest.fixture
def review(git_snapshot: dict) -> dict:
    return service.build_marketflow_repository_tagging_execution_results_review_v1(
        git_snapshot=git_snapshot
    )


def test_review_builds_offline_from_deterministic_git_snapshot(
    monkeypatch: pytest.MonkeyPatch, git_snapshot: dict
) -> None:
    monkeypatch.setattr(
        service,
        "_collect_git_snapshot",
        lambda *args, **kwargs: pytest.fail("provided snapshot must avoid Git inspection"),
    )
    result = service.build_marketflow_repository_tagging_execution_results_review_v1(
        git_snapshot=git_snapshot
    )
    assert result["created_offline"] is True
    assert result["local_tags_reviewed"] is True


def test_review_collects_snapshot_with_read_only_git_commands(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path.resolve()
    calls: list[tuple[str, ...]] = []
    expected_by_name = {row["tag_name"]: row for row in service.EXPECTED_TAGS}

    def fake_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        assert repo_root == repo
        calls.append(args)
        stdout = ""
        if args == ("rev-parse", "--show-toplevel"):
            stdout = str(repo)
        elif args == ("for-each-ref", "--format=%(refname)", "refs/tags"):
            refs = [f"refs/tags/existing/{index}" for index in range(28)]
            refs.extend(f"refs/tags/{name}" for name in service.APPROVED_TERMINAL_TAG_NAMES)
            stdout = "\n".join(refs)
        elif args == (
            "for-each-ref",
            "--format=%(refname)",
            "refs/tags/marketflow/expectancy-lab/",
        ):
            stdout = "\n".join(
                f"refs/tags/{name}" for name in service.APPROVED_TERMINAL_TAG_NAMES
            )
        elif args == (
            "ls-remote",
            "--tags",
            "origin",
            "marketflow/expectancy-lab/*",
        ):
            stdout = ""
        elif args == ("ls-files", "--", ".marketflow"):
            stdout = ""
        elif args == ("rev-parse", "origin/main"):
            stdout = service.EXPECTED_ORIGIN_MAIN_COMMIT
        elif args[0] == "cat-file" and args[1] == "-t":
            stdout = "tag"
        elif args[0] == "rev-parse" and args[1].startswith("refs/tags/"):
            token = args[1].removeprefix("refs/tags/")
            peeled = token.endswith("^{commit}")
            name = token.removesuffix("^{commit}")
            row = expected_by_name[name]
            stdout = row["target_commit"] if peeled else row["tag_object_sha"]
        elif (
            args[0] == "for-each-ref"
            and args[1] == "--format=%(contents)"
            and args[2].startswith("refs/tags/")
        ):
            name = args[2].removeprefix("refs/tags/")
            stdout = expected_by_name[name]["tag_message"] + "\n"
        else:
            pytest.fail(f"unexpected Git command: {args}")
        return subprocess.CompletedProcess(["git", *args], 0, stdout=stdout, stderr="")

    monkeypatch.setattr(service, "_run_git", fake_git)
    result = service.build_marketflow_repository_tagging_execution_results_review_v1(
        repo_root=repo
    )
    assert result["verified_terminal_tag_count"] == 4
    assert result["tag_count_review"]["remote_approved_tag_count"] == 0
    allowed = {"rev-parse", "for-each-ref", "cat-file", "ls-remote", "ls-files"}
    assert calls
    assert all(args[0] in allowed for args in calls)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_READY),
        ("review_scope", service.REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tagging_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_tag_manifest_digest", service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST),
        ("source_tagging_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_execution_commit", service.EXPECTED_SOURCE_EXECUTION_COMMIT),
    ],
)
def test_artifact_identity_and_source_bindings(
    review: dict, field: str, expected: object
) -> None:
    assert review[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_execution_results_review_created",
        "repository_tagging_execution_results_review_ready",
        "local_tags_reviewed",
        "tag_messages_reviewed",
        "tag_targets_reviewed",
        "tag_objects_reviewed",
        "ready_for_repository_tag_push_strategy_candidate",
    ],
)
def test_review_completion_flags_are_true(review: dict, field: str) -> None:
    assert review[field] is True


def test_execution_status_is_bound(review: dict) -> None:
    assert review["source_tagging_execution_artifact_kind"] == service.source_execution_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_EXECUTED
    assert review["source_tagging_execution_status"] == service.source_execution_service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTED_LOCAL_TAGS_CREATED
    assert review["source_tagging_execution_scope"] == service.source_execution_service.REPOSITORY_TAGGING_EXECUTION_ONLY_LOCAL_TAGS_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN


def test_four_exact_local_annotated_tags_are_verified(review: dict) -> None:
    rows = review["tag_review_records"]
    assert review["approved_terminal_tag_count"] == 4
    assert review["verified_terminal_tag_count"] == len(rows) == 4
    assert [row["tag_name"] for row in rows] == service.APPROVED_TERMINAL_TAG_NAMES
    assert all(row["tag_type_observed"] == "ANNOTATED" for row in rows)
    assert all(row["review_status"] == "VERIFIED_LOCAL_ANNOTATED_TAG_NOT_PUSHED" for row in rows)


@pytest.mark.parametrize(
    ("tag_name", "target_commit", "object_sha"),
    [
        ("marketflow/expectancy-lab/final-archive-not-ready/v1", "0be55dc8a65a586368c192d6bc13302b9830a0b4", "c349f647fa06ef7eeeaba5addfaa1486592e4130"),
        ("marketflow/expectancy-lab/archive-record-not-ready/v1", "e2fcfb792ad14db8a2de69556c291529fda47a8e", "4321312337d93a147b66ef16948a0802cc6c3e2e"),
        ("marketflow/expectancy-lab/operator-selection-option-a/v1", "15c4fae495f88b54e30380f3d8b4aa54989fad39", "1056c5e3217197270327da6e4a01182295fcd4d0"),
        ("marketflow/expectancy-lab/readiness-not-ready/v1", "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0", "728ce5b883480ea0d0f952ff881274fbf110a7b8"),
    ],
)
def test_tag_targets_and_object_shas_match(
    review: dict, tag_name: str, target_commit: str, object_sha: str
) -> None:
    row = next(item for item in review["tag_review_records"] if item["tag_name"] == tag_name)
    assert row["expected_target_commit"] == row["observed_target_commit"] == target_commit
    assert row["expected_tag_object_sha"] == row["observed_tag_object_sha"] == object_sha
    assert row["tag_target_commit_verified"] is True
    assert row["tag_object_sha_verified"] is True


def test_tag_messages_and_remote_absence_are_verified(review: dict) -> None:
    assert all(review["tag_message_review"].values())
    for row in review["tag_review_records"]:
        assert row["tag_message_verified"] is True
        assert row["tag_remote_ref_exists"] is False
        assert row["tag_pushed"] is False
        assert all(boundary in row["tag_message"] for boundary in service.MESSAGE_BOUNDARIES)


def test_tag_count_review_matches_execution_and_live_snapshot(review: dict) -> None:
    assert review["tag_count_review"] == {
        "tag_count_before_execution_from_source": 28,
        "candidate_namespace_tag_count_before_execution_from_source": 0,
        "tag_count_after_execution_from_source": 32,
        "candidate_namespace_tag_count_after_execution_from_source": 4,
        "observed_tag_count_at_review": 32,
        "observed_candidate_namespace_tag_count_at_review": 4,
        "approved_terminal_tag_count": 4,
        "verified_terminal_tag_count": 4,
        "extra_candidate_namespace_tag_count": 0,
        "remote_approved_tag_count": 0,
        "tag_count_observation_note": "Observed source execution totals exactly: 32 local tags and 4 approved namespace tags.",
    }


@pytest.mark.parametrize(
    "field",
    [
        "repository_tag_push_strategy_candidate_created",
        "repository_tags_pushed",
        "git_tag_push_performed",
        "additional_tags_created",
        "tags_modified",
        "tags_deleted",
        "git_merge_performed",
        "git_rebase_performed",
        "git_branch_delete_performed",
        "git_remote_delete_performed",
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
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ],
)
def test_forbidden_actions_remain_false(review: dict, field: str) -> None:
    assert review[field] is False


def test_authority_strings_remain_closed(review: dict) -> None:
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_defined(review: dict) -> None:
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert len(service.NEXT_CHAIN) == 5
    assert len(service.NEXT_GATES) == 8
    assert len(service.RISK_CONTROLS) == 35


def test_checklist_and_summary_pass(review: dict) -> None:
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(review["checklist"]) == 62
    assert all(row["status"] == service.PASS for row in review["checklist"])
    assert review["summary"]["passed_checks"] == 62
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_and_tag_manifest_digests_are_deterministic(
    git_snapshot: dict, review: dict
) -> None:
    rebuilt = service.build_marketflow_repository_tagging_execution_results_review_v1(
        git_snapshot=git_snapshot
    )
    assert rebuilt["marketflow_repository_tagging_execution_results_review_digest"] == review["marketflow_repository_tagging_execution_results_review_digest"]
    assert rebuilt["marketflow_repository_tagging_execution_results_review_tag_manifest_digest"] == review["marketflow_repository_tagging_execution_results_review_tag_manifest_digest"]
    assert service.marketflow_repository_tagging_execution_results_review_digest_v1(review) == review["marketflow_repository_tagging_execution_results_review_digest"]
    assert service.marketflow_repository_tagging_execution_results_review_tag_manifest_digest_v1(review) == review["marketflow_repository_tagging_execution_results_review_tag_manifest_digest"]


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_repository_tagging_execution_results_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_VALID
    assert result["passed_checks"] == 62
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_tagging_execution_digest", "0" * 64),
        ("source_tag_manifest_digest", "0" * 64),
        ("source_tagging_approval_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tagging_execution_results_review_created", False),
        ("repository_tagging_execution_results_review_ready", False),
        ("local_tags_reviewed", False),
        ("tag_messages_reviewed", False),
        ("tag_targets_reviewed", False),
        ("tag_objects_reviewed", False),
        ("ready_for_repository_tag_push_strategy_candidate", False),
        ("repository_tag_push_strategy_candidate_created", True),
        ("verified_terminal_tag_count", 3),
        ("repository_tags_pushed", True),
        ("git_tag_push_performed", True),
        ("additional_tags_created", True),
        ("tags_modified", True),
        ("tags_deleted", True),
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
        ("risk_controls", []),
    ],
)
def test_validator_rejects_top_level_contract_mutations(
    review: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(review)
    mutated[field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewError):
        service.validate_marketflow_repository_tagging_execution_results_review_v1(mutated)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("tag_name", "WRONG"),
        ("observed_target_commit", "0" * 40),
        ("observed_tag_object_sha", "0" * 40),
        ("tag_type_observed", "LIGHTWEIGHT"),
        ("tag_target_commit_verified", False),
        ("tag_object_sha_verified", False),
        ("tag_message", "boundary missing"),
        ("tag_message_verified", False),
        ("tag_remote_ref_exists", True),
        ("tag_pushed", True),
        ("tag_modified", True),
        ("tag_deleted", True),
    ],
)
def test_validator_rejects_tag_review_mutations(
    review: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(review)
    mutated["tag_review_records"][0][field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewError):
        service.validate_marketflow_repository_tagging_execution_results_review_v1(mutated)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("verified_terminal_tag_count", 3),
        ("remote_approved_tag_count", 1),
        ("extra_candidate_namespace_tag_count", 1),
    ],
)
def test_validator_rejects_tag_count_mutations(
    review: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(review)
    mutated["tag_count_review"][field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewError):
        service.validate_marketflow_repository_tagging_execution_results_review_v1(mutated)


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_tagging_execution_results_review_digest",
        "marketflow_repository_tagging_execution_results_review_tag_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(review: dict, field: str) -> None:
    mutated = deepcopy(review)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewError):
        service.validate_marketflow_repository_tagging_execution_results_review_v1(mutated)


@pytest.mark.parametrize(
    ("path", "invalid"),
    [
        (("tags", 0, "tag_object_type"), "commit"),
        (("tags", 0, "target_commit"), "0" * 40),
        (("tags", 0, "tag_object_sha"), "0" * 40),
        (("tags", 0, "tag_message"), "WRONG"),
        (("tags", 0, "remote_ref_exists"), True),
        (("remote_approved_tag_count",), 1),
        (("observed_candidate_namespace_tag_count_at_review",), 5),
    ],
)
def test_builder_blocks_invalid_or_published_tag_snapshot(
    git_snapshot: dict, path: tuple, invalid: object
) -> None:
    mutated = deepcopy(git_snapshot)
    target = mutated
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewBlockedError) as caught:
        service.build_marketflow_repository_tagging_execution_results_review_v1(
            git_snapshot=mutated
        )
    assert caught.value.blocked_artifact["artifact_kind"] == service.MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_BLOCKED


def test_markdown_contains_required_sections(review: dict) -> None:
    markdown = service.build_marketflow_repository_tagging_execution_results_review_markdown_v1(review)
    for section in (
        "Title",
        "MarketFlow Repository Tagging Execution Results Review v1",
        "Source Tagging Execution",
        "Bound Evidence",
        "Repository Context",
        "Review Scope",
        "Reviewed Local Annotated Tags",
        "Tag Count Review",
        "Tag Message Review",
        "Remote Tag Publication Review",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(
    tmp_path, git_snapshot: dict
) -> None:
    result = service.write_marketflow_repository_tagging_execution_results_review_v1(
        tmp_path,
        git_snapshot=git_snapshot,
    )
    path = tmp_path / "marketflow_repository_tagging_execution_results_review_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    service.validate_marketflow_repository_tagging_execution_results_review_v1(payload)
    assert result["marketflow_repository_tagging_execution_results_review_digest"] == payload["marketflow_repository_tagging_execution_results_review_digest"]
    with pytest.raises(service.MarketFlowRepositoryTaggingExecutionResultsReviewError):
        service.write_marketflow_repository_tagging_execution_results_review_v1(
            tmp_path,
            git_snapshot=git_snapshot,
        )
