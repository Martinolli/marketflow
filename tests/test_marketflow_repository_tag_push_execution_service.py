from copy import deepcopy

import pytest

from marketflow.services import marketflow_repository_tag_push_execution_service as service


@pytest.fixture
def execution():
    return service.execute_marketflow_repository_tag_push_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_git_operations=False,
    )


def test_fixture_execution_is_deterministic(execution):
    rebuilt = service.execute_marketflow_repository_tag_push_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_git_operations=False,
    )
    assert rebuilt == execution


def test_fixture_mode_never_invokes_git(monkeypatch):
    monkeypatch.setattr(service, "_git", lambda *_args: pytest.fail("git invoked"))
    artifact = service.execute_marketflow_repository_tag_push_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z",
        execute_git_operations=False,
    )
    assert artifact["repository_tags_pushed"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1),
        ("execution_status", service.MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED_REMOTE_TAGS_PUBLISHED),
        ("execution_scope", service.REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("selected_tag_push_package", service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN),
        ("source_tag_push_strategy_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_tag_push_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_tag_push_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tagging_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_tag_manifest_review_digest", service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit_before_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("repository_tag_push_strategy_selected", True),
        ("repository_tag_push_strategy_approved", True),
        ("repository_tag_push_strategy_authorized", True),
        ("repository_tag_push_strategy_executed", True),
        ("repository_tags_pushed", True),
        ("git_tag_push_performed", True),
        ("remote_terminal_tags_published", True),
        ("approved_tag_push_count", 4),
        ("additional_tags_created", False),
        ("tags_modified", False),
        ("tags_deleted", False),
        ("git_merge_performed", False),
        ("git_rebase_performed", False),
        ("git_branch_delete_performed", False),
        ("git_remote_delete_performed", False),
        ("git_remote_prune_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_execution_fields(execution, field, expected):
    assert execution[field] == expected


def test_tag_push_counts(execution):
    counts = execution["tag_push_count_summary"]
    assert counts == {
        "local_tag_count_before_push": 32,
        "remote_candidate_namespace_tag_count_before_push": 0,
        "approved_tag_push_count": 4,
        "pushed_terminal_tag_count": 4,
        "existing_matching_remote_tag_count": 0,
        "remote_candidate_namespace_tag_count_after_push": 4,
        "remote_approved_tag_count_after_push": 4,
        "extra_remote_candidate_namespace_tag_count_after_push": 0,
        "tag_push_count_observation_note": "First publication pushed all four approved tags.",
    }


def test_tag_records_match_approved_identity(execution):
    records = execution["tag_push_execution_records"]
    assert [row["tag_name"] for row in records] == [row["tag_name"] for row in service.APPROVED_TAGS]
    assert [row["local_tag_object_sha"] for row in records] == [row["local_tag_object_sha"] for row in service.APPROVED_TAGS]
    assert [row["remote_tag_object_sha"] for row in records] == [row["local_tag_object_sha"] for row in service.APPROVED_TAGS]
    assert [row["target_commit"] for row in records] == [row["target_commit"] for row in service.APPROVED_TAGS]
    assert [row["remote_peeled_target_commit"] for row in records] == [row["target_commit"] for row in service.APPROVED_TAGS]
    assert all(row["tag_push_status"] == "PUSHED_TO_ORIGIN_EXPLICIT_REFSPEC" for row in records)
    assert all(row["local_tag_verified_before_push"] for row in records)
    assert all(row["remote_tag_verified_after_push"] for row in records)


def test_exact_explicit_push_command_and_closed_git_boundaries(execution):
    assert execution["push_command_used"] == service.PUSH_COMMAND
    assert execution["push_command_used_explicit_refspecs"] is True
    assert execution["push_all_tags_used"] is False
    assert execution["branch_push_used"] is False
    assert execution["main_push_used"] is False
    assert execution["force_push_used"] is False
    assert "--tags" not in execution["push_command_used"]


def test_next_chain_gates_and_risk_controls(execution):
    assert execution["next_chain"] == service.NEXT_CHAIN
    assert execution["next_gates"] == service.NEXT_GATES
    assert execution["risk_controls"] == service.RISK_CONTROLS
    assert execution["recommended_next_task"] == "MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1"


def test_checklist_passes(execution):
    assert [row["check_id"] for row in execution["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in execution["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in execution["checklist"])
    assert execution["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert execution["summary"]["failed_checks"] == 0
    assert execution["summary"]["blocker_count"] == 0


def test_digests_are_deterministic(execution):
    assert execution["marketflow_repository_tag_push_execution_digest"] == service.marketflow_repository_tag_push_execution_digest_v1(execution)
    assert execution["marketflow_repository_tag_push_execution_remote_tag_manifest_digest"] == service.marketflow_repository_tag_push_execution_remote_tag_manifest_digest_v1(execution)


def test_validator_accepts_valid_execution(execution):
    validation = service.validate_marketflow_repository_tag_push_execution_v1(execution)
    assert validation["status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_VALID
    assert validation["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"),
        (("execution_status",), "WRONG"),
        (("execution_scope",), "WRONG"),
        (("selected_tag_push_package",), "WRONG"),
        (("source_tag_push_strategy_approval_digest",), "0" * 64),
        (("source_tag_push_operator_review_digest",), "0" * 64),
        (("source_tag_push_candidate_digest",), "0" * 64),
        (("source_tagging_results_review_digest",), "0" * 64),
        (("origin_main_commit_before_execution",), "0" * 40),
        (("origin_main_commit_after_execution",), "0" * 40),
        (("repository_tag_push_strategy_authorized",), False),
        (("repository_tag_push_strategy_executed",), False),
        (("repository_tags_pushed",), False),
        (("git_tag_push_performed",), False),
        (("approved_tag_push_count",), 3),
        (("tag_push_count_summary", "pushed_terminal_tag_count"), 3),
        (("tag_push_count_summary", "remote_approved_tag_count_after_push"), 3),
        (("tag_push_count_summary", "extra_remote_candidate_namespace_tag_count_after_push"), 1),
        (("tag_push_execution_records", 0, "tag_name"), "wrong"),
        (("tag_push_execution_records", 0, "local_tag_object_sha"), "0" * 40),
        (("tag_push_execution_records", 0, "remote_tag_object_sha"), "0" * 40),
        (("tag_push_execution_records", 0, "target_commit"), "0" * 40),
        (("tag_push_execution_records", 0, "remote_peeled_target_commit"), "0" * 40),
        (("push_all_tags_used",), True),
        (("branch_push_used",), True),
        (("main_push_used",), True),
        (("force_push_used",), True),
        (("additional_tags_created",), True),
        (("tags_modified",), True),
        (("tags_deleted",), True),
        (("git_merge_performed",), True),
        (("git_rebase_performed",), True),
        (("git_branch_delete_performed",), True),
        (("git_remote_delete_performed",), True),
        (("git_remote_prune_performed",), True),
        (("origin_main_modified_by_this_task",), True),
        (("provider_requests_made_in_execution",), True),
        (("market_data_acquisition_performed_in_execution",), True),
        (("dataset_generation_performed_in_execution",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True),
        (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness_accepted",), True),
        (("profitability_accepted",), True),
        (("runtime_use",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_boundary_mutations(execution, path, bad_value):
    changed = deepcopy(execution)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryTagPushExecutionError):
        service.validate_marketflow_repository_tag_push_execution_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "marketflow_repository_tag_push_execution_digest",
        "marketflow_repository_tag_push_execution_remote_tag_manifest_digest",
    ],
)
def test_validator_rejects_missing_digests(execution, field):
    changed = deepcopy(execution)
    changed.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTagPushExecutionError):
        service.validate_marketflow_repository_tag_push_execution_v1(changed)


def test_existing_matching_remote_tags_are_idempotent():
    statuses = {row["remote_ref"]: "EXISTING_MATCHING_REMOTE_TAG" for row in service.APPROVED_TAGS}
    remote = {
        row["remote_ref"]: {"object_sha": row["local_tag_object_sha"], "peeled_target": row["target_commit"]}
        for row in service.APPROVED_TAGS
    }
    records = service._execution_records(statuses, remote)
    assert all(row["tag_push_status"] == "EXISTING_MATCHING_REMOTE_TAG" for row in records)


def test_remote_precheck_rejects_extra_namespace_ref():
    remote = {"refs/tags/marketflow/expectancy-lab/extra/v1": {"object_sha": "a" * 40, "peeled_target": "b" * 40}}
    with pytest.raises(service.MarketFlowRepositoryTagPushExecutionError):
        service._verify_remote_precheck(remote)


def test_remote_precheck_rejects_mismatching_approved_ref():
    row = service.APPROVED_TAGS[0]
    remote = {row["remote_ref"]: {"object_sha": "0" * 40, "peeled_target": row["target_commit"]}}
    with pytest.raises(service.MarketFlowRepositoryTagPushExecutionError):
        service._verify_remote_precheck(remote)


def test_live_path_uses_only_one_explicit_tag_push(monkeypatch, tmp_path):
    before = {}
    after = {
        row["remote_ref"]: {"object_sha": row["local_tag_object_sha"], "peeled_target": row["target_commit"]}
        for row in service.APPROVED_TAGS
    }
    remote_states = iter((before, after))
    calls = []
    monkeypatch.setattr(service, "_origin_main", lambda _root: service.EXPECTED_ORIGIN_MAIN_COMMIT)
    monkeypatch.setattr(service, "_local_tag_count", lambda _root: 32)
    monkeypatch.setattr(service, "_verify_local_tags", lambda _root: service.APPROVED_TAGS)
    monkeypatch.setattr(service, "_remote_tags", lambda _root: next(remote_states))
    monkeypatch.setattr(service, "_tracked_marketflow_count", lambda _root: 0)
    monkeypatch.setattr(service, "_git", lambda _root, *args: calls.append(args) or "")
    result = service.execute_marketflow_repository_tag_push_v1(
        repo_root=tmp_path,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )
    assert result["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTED
    assert calls == [("push", "origin", *service.APPROVED_REMOTE_REFS)]


def test_precheck_failure_returns_blocked_artifact_without_push(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(service, "_origin_main", lambda _root: "0" * 40)
    monkeypatch.setattr(service, "_git", lambda _root, *args: calls.append(args) or "")
    result = service.execute_marketflow_repository_tag_push_v1(
        repo_root=tmp_path,
        run_timestamp_utc="2026-08-23T00:00:00Z",
    )
    assert result["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED
    assert result["execution_status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_BLOCKED_PRECHECK_OR_REMOTE_REF_MISMATCH
    assert result["git_tag_push_performed"] is False
    assert calls == []


def test_markdown_includes_required_sections(execution):
    markdown = service.build_marketflow_repository_tag_push_execution_markdown_v1(execution)
    for section in (
        "Title", "MarketFlow Repository Tag Push Execution v1", "Source Tag Push Approval",
        "Bound Evidence", "Repository Context", "Execution Scope",
        "Remote Tag Push Command", "Published Remote Tags", "Tag Push Count Summary",
        "Origin/Main Protection", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown
