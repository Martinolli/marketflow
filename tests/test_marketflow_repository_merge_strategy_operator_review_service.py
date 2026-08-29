from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_merge_strategy_candidate_service as candidate_service
from marketflow.services import marketflow_repository_merge_strategy_operator_review_service as service


@pytest.fixture
def review():
    return service.build_marketflow_repository_merge_strategy_operator_review_v1()


def test_review_builds_offline_deterministically(review):
    assert service.build_marketflow_repository_merge_strategy_operator_review_v1() == review


def test_review_accepts_valid_source_candidate(review):
    candidate = candidate_service.build_marketflow_repository_merge_strategy_candidate_v1()
    assert service.build_marketflow_repository_merge_strategy_operator_review_v1(
        source_candidate=candidate
    ) == review


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_merge_strategy_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tag_push_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_remote_tag_manifest_review_digest", service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST),
        ("source_tag_push_execution_digest", service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST),
        ("source_tag_push_remote_manifest_digest", service.EXPECTED_SOURCE_REMOTE_MANIFEST_DIGEST),
        ("source_tag_push_approval_digest", service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_candidate_commit", service.EXPECTED_SOURCE_CANDIDATE_COMMIT),
        ("repository_merge_strategy_candidate_ready_for_operator_review", True),
        ("repository_merge_strategy_operator_review_created", True),
        ("repository_merge_strategy_operator_review_ready", True),
        ("merge_packages_reviewed", True), ("merge_prerequisites_reviewed", True),
        ("integration_branch_plan_reviewed", True), ("chain_merge_impact_reviewed", True),
        ("merge_policy_reviewed", True),
        ("ready_for_repository_merge_strategy_approval", False),
        ("repository_merge_strategy_selected", False),
        ("repository_merge_strategy_approved", False),
        ("repository_merge_strategy_authorized", False),
        ("repository_merge_strategy_executed", False),
        ("repository_integration_branch_created", False),
        ("git_merge_performed", False), ("git_rebase_performed", False),
        ("git_squash_merge_performed", False), ("git_cherry_pick_performed", False),
        ("git_main_push_performed", False), ("git_force_push_performed", False),
        ("git_branch_delete_performed", False), ("git_remote_delete_performed", False),
        ("git_remote_prune_performed", False), ("origin_main_modified_by_this_task", False),
        ("repository_tags_pushed_again", False), ("additional_tag_push_performed", False),
        ("additional_tags_created", False), ("tags_modified", False), ("tags_deleted", False),
        ("repository_cleanup_candidate_created", False),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"), ("predictive_usefulness_accepted", False),
        ("profitability", "not accepted"), ("profitability_accepted", False),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
        ("tracked_marketflow_file_count", 0), ("no_tracked_marketflow_files", True),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_repository_context_is_bound(review):
    assert review["source_repository_context"] == service.SOURCE_REPOSITORY_CONTEXT
    assert review["source_repository_context"]["local_branch_count"] == 302
    assert review["source_repository_context"]["remote_ref_count"] == 274
    assert review["source_repository_context"]["total_ref_count"] == 576
    assert review["source_repository_context"]["local_tag_count"] == 32


def test_reviewed_merge_strategy_philosophy(review):
    assert review["reviewed_merge_strategy_philosophy"] == service.REVIEWED_MERGE_STRATEGY_PHILOSOPHY
    assert review["reviewed_merge_strategy_boundary"] == service.REVIEWED_MERGE_STRATEGY_BOUNDARY
    assert review["reviewed_merge_strategy_goal"] == service.REVIEWED_MERGE_STRATEGY_GOAL
    assert review["merge_strategy_philosophy_review_status"] == "REVIEWED_PLANNING_ONLY"


def test_six_merge_packages_are_reviewed_not_selected(review):
    packages = review["reviewed_merge_strategy_packages"]
    assert packages == service.REVIEWED_MERGE_STRATEGY_PACKAGES
    assert len(packages) == 6
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)
    assert all(row["executed"] is False for row in packages)


def test_recommended_package_is_reviewed_not_selected(review):
    assert review["recommended_merge_strategy_package"] == candidate_service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
    assert review["recommended_package_selected"] is False
    row = next(row for row in review["reviewed_merge_strategy_packages"] if row["package_id"] == review["recommended_merge_strategy_package"])
    assert row["source_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert row["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"


def test_integration_branch_plan_reviewed_not_created(review):
    plan = review["reviewed_integration_branch_plan"]
    assert plan == service.REVIEWED_INTEGRATION_BRANCH_PLAN
    assert plan["candidate_integration_branch_name"] == "integration/marketflow-terminal-evidence-stack-validation-v1"
    assert plan["candidate_integration_status"] == "REVIEWED_PLANNED_NOT_CREATED"
    assert plan["integration_branch_created"] is False
    assert plan["integration_merge_performed"] is False
    assert plan["integration_pytest_performed"] is False
    assert plan["main_merge_performed"] is False
    assert plan["main_push_performed"] is False


def test_merge_prerequisites_reviewed_not_executed(review):
    rows = review["reviewed_merge_prerequisites"]
    assert rows == service.REVIEWED_MERGE_PREREQUISITES
    assert len(rows) == 12
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_MERGE_OR_INTEGRATION" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_merge_non_goals_reviewed_active(review):
    assert review["reviewed_merge_non_goals"] == service.REVIEWED_MERGE_NON_GOALS
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_merge_non_goals"])


def test_chain_merge_impact_review(review):
    rows = review["chain_merge_impact_review"]
    assert rows == service.CHAIN_MERGE_IMPACT_REVIEW
    assert len(rows) == 10
    assert all(row["merge_required_now"] is False for row in rows)
    assert all(row["main_push_required_now"] is False for row in rows)
    assert all(row["merge_readiness"] == "NOT_EVALUATED_BY_THIS_REVIEW" for row in rows)


def test_next_chain_gates_and_risk_controls(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert review["recommended_next_task"] == "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1_IF_SELECTED"
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"


def test_checklist_and_summary_pass(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(review):
    assert review["marketflow_repository_merge_strategy_operator_review_digest"] == service.marketflow_repository_merge_strategy_operator_review_digest_v1(review)


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_merge_strategy_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"), (("review_status",), "WRONG"),
        (("review_scope",), "WRONG"), (("source_merge_strategy_candidate_digest",), "0" * 64),
        (("source_tag_push_results_review_digest",), "0" * 64),
        (("source_remote_tag_manifest_review_digest",), "0" * 64),
        (("source_tag_push_execution_digest",), "0" * 64),
        (("source_tag_push_approval_digest",), "0" * 64), (("origin_main_commit",), "0" * 40),
        (("repository_merge_strategy_operator_review_created",), False),
        (("repository_merge_strategy_operator_review_ready",), False),
        (("merge_packages_reviewed",), False), (("reviewed_merge_strategy_packages",), []),
        (("integration_branch_plan_reviewed",), False), (("reviewed_integration_branch_plan",), {}),
        (("merge_prerequisites_reviewed",), False), (("reviewed_merge_prerequisites",), []),
        (("chain_merge_impact_reviewed",), False), (("chain_merge_impact_review",), []),
        (("ready_for_repository_merge_strategy_approval",), True),
        (("repository_merge_strategy_selected",), True),
        (("repository_merge_strategy_approved",), True),
        (("repository_merge_strategy_authorized",), True),
        (("repository_merge_strategy_executed",), True),
        (("repository_integration_branch_created",), True),
        (("git_merge_performed",), True), (("git_rebase_performed",), True),
        (("git_squash_merge_performed",), True), (("git_cherry_pick_performed",), True),
        (("git_main_push_performed",), True), (("git_force_push_performed",), True),
        (("git_branch_delete_performed",), True), (("git_remote_delete_performed",), True),
        (("git_remote_prune_performed",), True), (("origin_main_modified_by_this_task",), True),
        (("repository_tags_pushed_again",), True), (("additional_tags_created",), True),
        (("tags_modified",), True), (("tags_deleted",), True),
        (("repository_cleanup_candidate_created",), True),
        (("provider_requests_made_in_review",), True),
        (("market_data_acquisition_performed_in_review",), True),
        (("dataset_generation_performed_in_review",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness_accepted",), True), (("profitability_accepted",), True),
        (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("reviewed_merge_non_goals",), []), (("next_chain",), []), (("next_gates",), []),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutations(review, path, bad_value):
    changed = deepcopy(review)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyOperatorReviewError):
        service.validate_marketflow_repository_merge_strategy_operator_review_v1(changed)


def test_validator_rejects_missing_digest(review):
    changed = deepcopy(review)
    changed.pop("marketflow_repository_merge_strategy_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyOperatorReviewError):
        service.validate_marketflow_repository_merge_strategy_operator_review_v1(changed)


def test_source_candidate_digest_mismatch_is_rejected():
    candidate = candidate_service.build_marketflow_repository_merge_strategy_candidate_v1()
    candidate["marketflow_repository_merge_strategy_candidate_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyOperatorReviewError):
        service.build_marketflow_repository_merge_strategy_operator_review_v1(source_candidate=candidate)


def test_writer_round_trip(tmp_path):
    result = service.write_marketflow_repository_merge_strategy_operator_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_merge_strategy_operator_review_v1.json").read_text(encoding="utf-8"))
    assert result["marketflow_repository_merge_strategy_operator_review_digest"] == payload["marketflow_repository_merge_strategy_operator_review_digest"]
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_overwrite(tmp_path):
    service.write_marketflow_repository_merge_strategy_operator_review_v1(tmp_path)
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyOperatorReviewError):
        service.write_marketflow_repository_merge_strategy_operator_review_v1(tmp_path)


def test_markdown_has_required_sections(review):
    markdown = service.build_marketflow_repository_merge_strategy_operator_review_markdown_v1(review)
    for title in (
        "Title", "MarketFlow Repository Merge Strategy Operator Review v1",
        "Source Merge Strategy Candidate", "Bound Evidence", "Repository Context",
        "Review Scope", "Reviewed Merge Strategy Philosophy", "Reviewed Merge Packages",
        "Reviewed Integration Branch Plan", "Reviewed Merge Prerequisites",
        "Reviewed Merge Non-Goals", "Chain Merge Impact Review", "Recommendation",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {title}" in markdown
