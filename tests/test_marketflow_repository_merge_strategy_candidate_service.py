from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_merge_strategy_candidate_service as service


@pytest.fixture
def snapshot():
    return service.approved_marketflow_repository_merge_strategy_git_snapshot_v1()


@pytest.fixture
def candidate(snapshot):
    return service.build_marketflow_repository_merge_strategy_candidate_v1(git_snapshot=snapshot)


def test_candidate_builds_offline_deterministically(candidate):
    assert service.build_marketflow_repository_merge_strategy_candidate_v1() == candidate


def test_candidate_uses_injected_snapshot(snapshot):
    snapshot["local_branch_count"] = 999
    result = service.build_marketflow_repository_merge_strategy_candidate_v1(git_snapshot=snapshot)
    assert result["source_repository_context"]["local_branch_count"] == 999


def test_candidate_rejects_changed_origin_main(snapshot):
    snapshot["origin_main_commit"] = "0" * 40
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.build_marketflow_repository_merge_strategy_candidate_v1(git_snapshot=snapshot)


def test_candidate_rejects_tracked_marketflow(snapshot):
    snapshot["tracked_marketflow_file_count"] = 1
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.build_marketflow_repository_merge_strategy_candidate_v1(git_snapshot=snapshot)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tag_push_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_remote_tag_manifest_review_digest", service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST),
        ("source_tag_push_execution_digest", service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST),
        ("source_tag_push_approval_digest", service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_tag_push_results_review_commit", service.EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT),
        ("repository_merge_strategy_candidate_created", True),
        ("repository_merge_strategy_candidate_ready_for_operator_review", True),
        ("ready_for_repository_merge_strategy_operator_review", True),
        ("repository_merge_strategy_selected", False),
        ("repository_merge_strategy_approved", False),
        ("repository_merge_strategy_authorized", False),
        ("repository_merge_strategy_executed", False),
        ("repository_integration_branch_created", False),
        ("git_merge_performed", False), ("git_rebase_performed", False),
        ("git_squash_merge_performed", False), ("git_cherry_pick_performed", False),
        ("git_main_push_performed", False), ("origin_main_modified_by_this_task", False),
        ("repository_cleanup_candidate_created", False),
        ("repository_cleanup_approved", False), ("repository_cleanup_executed", False),
        ("git_branch_delete_performed", False), ("git_remote_delete_performed", False),
        ("git_force_push_performed", False), ("git_remote_prune_performed", False),
        ("repository_tags_pushed_again", False), ("additional_tag_push_performed", False),
        ("additional_tags_created", False), ("tags_modified", False), ("tags_deleted", False),
        ("provider_requests_made_in_candidate", False),
        ("market_data_acquisition_performed_in_candidate", False),
        ("dataset_generation_performed_in_candidate", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_candidate_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_merge_strategy_philosophy(candidate):
    assert candidate["merge_strategy_philosophy"] == service.MERGE_STRATEGY_PHILOSOPHY
    assert candidate["merge_strategy_boundary"] == service.MERGE_STRATEGY_BOUNDARY
    assert candidate["merge_strategy_goal"] == service.MERGE_STRATEGY_GOAL


def test_recommended_package_is_not_selected(candidate):
    assert candidate["recommended_merge_strategy_package"] == service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    recommended = [row for row in candidate["proposed_merge_strategy_packages"] if row["package_id"] == candidate["recommended_merge_strategy_package"]]
    assert len(recommended) == 1
    assert recommended[0]["selected"] is False
    assert recommended[0]["approved"] is False
    assert recommended[0]["executed"] is False


def test_six_candidate_packages(candidate):
    packages = candidate["proposed_merge_strategy_packages"]
    assert packages == service.PROPOSED_MERGE_STRATEGY_PACKAGES
    assert len(packages) == 6
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_merge_prerequisites(candidate):
    assert candidate["merge_prerequisites"] == service.MERGE_PREREQUISITES
    assert all(candidate["merge_prerequisites"].values())


def test_integration_branch_plan_is_planned_not_created(candidate):
    plan = candidate["candidate_integration_branch_plan"]
    assert plan == service.CANDIDATE_INTEGRATION_BRANCH_PLAN
    assert plan["candidate_integration_branch_name"] == "integration/marketflow-terminal-evidence-stack-validation-v1"
    assert plan["candidate_integration_status"] == "PLANNED_NOT_CREATED"
    assert plan["integration_branch_created"] is False
    assert plan["integration_merge_performed"] is False
    assert plan["main_push_performed"] is False


def test_merge_non_goals(candidate):
    assert candidate["merge_non_goals"] == service.MERGE_NON_GOALS
    assert "do_not_merge_now" in candidate["merge_non_goals"]
    assert "do_not_create_integration_branch_now" in candidate["merge_non_goals"]


def test_chain_merge_impact_summary(candidate):
    rows = candidate["chain_merge_impact_summary"]
    assert [row["chain_id"] for row in rows] == service.CHAIN_IDS
    assert len(rows) == 10
    assert all(row["merge_required_now"] is False for row in rows)
    assert all(row["operator_review_required"] is True for row in rows)
    assert all(row["main_push_required_now"] is False for row in rows)


def test_next_chain_gates_and_risk_controls(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert candidate["recommended_next_task"] == "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1"


def test_checklist_passes(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate):
    assert candidate["marketflow_repository_merge_strategy_candidate_digest"] == service.marketflow_repository_merge_strategy_candidate_digest_v1(candidate)


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_merge_strategy_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"), (("candidate_status",), "WRONG"),
        (("candidate_scope",), "WRONG"), (("source_tag_push_results_review_digest",), "0" * 64),
        (("source_remote_tag_manifest_review_digest",), "0" * 64),
        (("source_tag_push_execution_digest",), "0" * 64),
        (("source_tag_push_approval_digest",), "0" * 64),
        (("origin_main_commit",), "0" * 40),
        (("repository_merge_strategy_candidate_created",), False),
        (("repository_merge_strategy_candidate_ready_for_operator_review",), False),
        (("recommended_merge_strategy_package",), "MISSING"),
        (("proposed_merge_strategy_packages",), []),
        (("candidate_integration_branch_plan",), {}),
        (("candidate_integration_branch_plan", "integration_branch_created"), True),
        (("repository_integration_branch_created",), True),
        (("repository_merge_strategy_selected",), True),
        (("repository_merge_strategy_approved",), True),
        (("repository_merge_strategy_authorized",), True),
        (("repository_merge_strategy_executed",), True),
        (("git_merge_performed",), True), (("git_rebase_performed",), True),
        (("git_squash_merge_performed",), True), (("git_cherry_pick_performed",), True),
        (("git_main_push_performed",), True), (("git_force_push_performed",), True),
        (("git_branch_delete_performed",), True), (("git_remote_delete_performed",), True),
        (("git_remote_prune_performed",), True), (("origin_main_modified_by_this_task",), True),
        (("repository_tags_pushed_again",), True), (("additional_tags_created",), True),
        (("tags_modified",), True), (("tags_deleted",), True),
        (("repository_cleanup_candidate_created",), True),
        (("provider_requests_made_in_candidate",), True),
        (("market_data_acquisition_performed_in_candidate",), True),
        (("dataset_generation_performed_in_candidate",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness_accepted",), True), (("profitability_accepted",), True),
        (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("chain_merge_impact_summary",), []), (("merge_prerequisites",), {}),
        (("merge_non_goals",), []), (("next_chain",), []), (("next_gates",), []),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutations(candidate, path, bad_value):
    changed = deepcopy(candidate)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.validate_marketflow_repository_merge_strategy_candidate_v1(changed)


def test_validator_rejects_missing_digest(candidate):
    changed = deepcopy(candidate)
    changed.pop("marketflow_repository_merge_strategy_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.validate_marketflow_repository_merge_strategy_candidate_v1(changed)


def test_source_review_mismatch_is_rejected(snapshot):
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.build_marketflow_repository_merge_strategy_candidate_v1(
            source_review={"marketflow_repository_tag_push_results_review_digest": "0" * 64},
            git_snapshot=snapshot,
        )


def test_writer_round_trip(tmp_path, snapshot):
    result = service.write_marketflow_repository_merge_strategy_candidate_v1(tmp_path, git_snapshot=snapshot)
    payload = json.loads((tmp_path / "marketflow_repository_merge_strategy_candidate_v1.json").read_text(encoding="utf-8"))
    assert result["marketflow_repository_merge_strategy_candidate_digest"] == payload["marketflow_repository_merge_strategy_candidate_digest"]
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_overwrite(tmp_path, snapshot):
    service.write_marketflow_repository_merge_strategy_candidate_v1(tmp_path, git_snapshot=snapshot)
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyCandidateError):
        service.write_marketflow_repository_merge_strategy_candidate_v1(tmp_path, git_snapshot=snapshot)


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_merge_strategy_candidate_markdown_v1(candidate)
    for section in (
        "Title", "MarketFlow Repository Merge Strategy Candidate v1",
        "Source Tag Push Results Review", "Bound Evidence", "Repository Context",
        "Candidate Scope", "Merge Strategy Philosophy", "Recommended Merge Strategy",
        "Proposed Merge Packages", "Merge Prerequisites", "Candidate Integration Branch Plan",
        "Merge Non-Goals", "Chain Merge Impact Summary", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert section in markdown
