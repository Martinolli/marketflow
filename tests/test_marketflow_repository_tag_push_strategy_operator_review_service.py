from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_tag_push_strategy_operator_review_service as service


@pytest.fixture()
def review() -> dict:
    return service.build_marketflow_repository_tag_push_strategy_operator_review_v1()


def test_review_builds_offline_without_candidate_rerun(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("source candidate must not be rerun")

    monkeypatch.setattr(
        service.source_service,
        "build_marketflow_repository_tag_push_strategy_candidate_v1",
        fail_if_called,
    )
    built = service.build_marketflow_repository_tag_push_strategy_operator_review_v1()
    assert built["created_offline"] is True
    assert built["planning_only"] is True
    assert built["governance_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_READY),
        ("review_scope", service.REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tag_push_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tagging_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_tag_manifest_review_digest", service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST),
        ("source_tagging_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_tagging_execution_tag_manifest_digest", service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST),
        ("source_tagging_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_candidate_commit", service.EXPECTED_SOURCE_CANDIDATE_COMMIT),
    ],
)
def test_review_binds_required_fields(review, field, expected):
    assert review[field] == expected


def test_source_candidate_and_review_readiness_are_true(review):
    assert review["repository_tag_push_strategy_candidate_created"] is True
    assert review["repository_tag_push_strategy_candidate_ready_for_operator_review"] is True
    assert review["repository_tag_push_strategy_operator_review_created"] is True
    assert review["repository_tag_push_strategy_operator_review_ready"] is True


@pytest.mark.parametrize(
    "field",
    [
        "tag_push_packages_reviewed",
        "tag_push_records_reviewed",
        "tag_push_prerequisites_reviewed",
        "tag_push_policy_reviewed",
    ],
)
def test_review_completion_flags_are_true(review, field):
    assert review[field] is True


def test_ready_for_approval_is_false(review):
    assert review["ready_for_repository_tag_push_strategy_approval"] is False
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"


def test_recommended_package_is_reviewed_not_selected(review):
    assert review["recommended_tag_push_package"] == (
        service.source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN
    )
    assert review["recommended_package_selected"] is False
    assert review["reviewed_push_packages"][0]["review_status"] == (
        "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    )


def test_four_push_packages_are_reviewed(review):
    assert review["reviewed_push_packages"] == service.REVIEWED_PUSH_PACKAGES
    assert len(review["reviewed_push_packages"]) == 4
    assert all(row["selected"] is False for row in review["reviewed_push_packages"])
    assert all(row["approved"] is False for row in review["reviewed_push_packages"])


def test_four_push_records_and_remote_refs_are_reviewed(review):
    records = review["reviewed_push_records"]
    assert records == service.REVIEWED_PUSH_RECORDS
    assert len(records) == 4
    assert [row["candidate_remote_ref"] for row in records] == (
        service.source_service.CANDIDATE_REMOTE_REFS
    )
    assert all(row["candidate_push_status"] == "REVIEWED_CANDIDATE_NOT_PUSHED" for row in records)


def test_local_tag_objects_and_targets_are_bound(review):
    records = review["reviewed_push_records"]
    assert [row["local_tag_object_sha"] for row in records] == (
        service.source_service.source_review_service.EXPECTED_TAG_OBJECT_SHAS
    )
    assert [row["target_commit"] for row in records] == [
        row["target_commit"]
        for row in service.source_service.source_review_service.EXPECTED_TAGS
    ]


def test_remote_refs_remain_absent_in_source_review(review):
    assert all(
        row["remote_ref_exists_in_source_review"] is False
        for row in review["reviewed_push_records"]
    )
    assert review["source_repository_context"]["source_remote_approved_tag_count"] == 0


def test_push_command_is_reviewed_but_not_executed(review):
    assert review["reviewed_push_command_template"] == (
        service.source_service.CANDIDATE_PUSH_COMMAND_TEMPLATE
    )
    assert review["command_review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED"
    assert review["remote_publication_status"] == "NOT_PUSHED"


def test_all_prerequisites_are_reviewed_not_executed(review):
    assert review["reviewed_tag_push_prerequisites"] == service.REVIEWED_TAG_PUSH_PREREQUISITES
    assert len(review["reviewed_tag_push_prerequisites"]) == 13
    assert all(row["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_TAG_PUSH" for row in review["reviewed_tag_push_prerequisites"])
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in review["reviewed_tag_push_prerequisites"])


def test_all_non_goals_are_reviewed_active(review):
    assert review["reviewed_tag_push_non_goals"] == service.REVIEWED_TAG_PUSH_NON_GOALS
    assert len(review["reviewed_tag_push_non_goals"]) == 15
    assert all(row["review_status"] == "REVIEWED_ACTIVE" for row in review["reviewed_tag_push_non_goals"])


@pytest.mark.parametrize(
    "field",
    [
        "ready_for_repository_tag_push_strategy_approval",
        "repository_tag_push_strategy_selected",
        "repository_tag_push_strategy_approved",
        "repository_tag_push_strategy_authorized",
        "repository_tag_push_strategy_executed",
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
def test_approval_execution_and_acceptance_flags_remain_false(review, field):
    assert review[field] is False


def test_marketflow_tracked_file_count_is_zero(review):
    assert review["tracked_marketflow_file_count"] == 0
    assert review["no_tracked_marketflow_files"] is True


def test_acceptance_and_authority_boundaries_remain_closed(review):
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_defined(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["recommended_next_task"] == (
        "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1_IF_SELECTED"
    )


def test_risk_controls_are_defined(review):
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert "review_does_not_select_tag_push_package" in review["risk_controls"]
    assert "operator_approval_required_before_tag_push" in review["risk_controls"]


def test_checklist_passes(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == 69
    assert review["summary"]["passed_checks"] == 69
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic():
    first = service.build_marketflow_repository_tag_push_strategy_operator_review_v1()
    second = service.build_marketflow_repository_tag_push_strategy_operator_review_v1()
    assert first["marketflow_repository_tag_push_strategy_operator_review_digest"] == second[
        "marketflow_repository_tag_push_strategy_operator_review_digest"
    ]
    assert first["marketflow_repository_tag_push_strategy_operator_review_digest"] == (
        service.marketflow_repository_tag_push_strategy_operator_review_digest_v1(first)
    )


def test_validator_accepts_valid_review(review):
    result = service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_VALID
    assert result["passed_checks"] == 69


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("source_tag_push_candidate_digest", "0" * 64),
        ("source_tagging_results_review_digest", "0" * 64),
        ("source_tag_manifest_review_digest", "0" * 64),
        ("source_tagging_execution_digest", "0" * 64),
        ("source_tagging_approval_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tag_push_strategy_operator_review_created", False),
        ("repository_tag_push_strategy_operator_review_ready", False),
        ("ready_for_repository_tag_push_strategy_approval", True),
        ("repository_tag_push_strategy_selected", True),
        ("repository_tag_push_strategy_approved", True),
        ("repository_tag_push_strategy_authorized", True),
        ("repository_tag_push_strategy_executed", True),
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
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_changed_boundaries(review, field, replacement):
    mutated = deepcopy(review)
    mutated[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyOperatorReviewError):
        service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(mutated)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("reviewed_push_packages", []),
        ("reviewed_push_records", []),
        ("reviewed_tag_push_prerequisites", []),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_missing_review_content(review, field, replacement):
    mutated = deepcopy(review)
    mutated[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyOperatorReviewError):
        service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(mutated)


def test_validator_rejects_missing_digest(review):
    mutated = deepcopy(review)
    mutated.pop("marketflow_repository_tag_push_strategy_operator_review_digest")
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyOperatorReviewError):
        service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(mutated)


def test_markdown_includes_required_sections(review):
    markdown = service.build_marketflow_repository_tag_push_strategy_operator_review_markdown_v1(review)
    for section in (
        "Title",
        "MarketFlow Repository Tag Push Strategy Operator Review v1",
        "Source Tag Push Candidate",
        "Bound Evidence",
        "Repository Context",
        "Review Scope",
        "Reviewed Tag Push Philosophy",
        "Reviewed Push Packages",
        "Reviewed Push Records",
        "Reviewed Remote Publication Plan",
        "Reviewed Tag Push Prerequisites",
        "Reviewed Tag Push Non-Goals",
        "Recommendation",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json(tmp_path):
    receipt = service.write_marketflow_repository_tag_push_strategy_operator_review_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_tag_push_strategy_operator_review_v1.json").read_text())
    service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(payload)
    assert receipt["marketflow_repository_tag_push_strategy_operator_review_digest"] == payload[
        "marketflow_repository_tag_push_strategy_operator_review_digest"
    ]


def test_writer_refuses_to_overwrite(tmp_path):
    service.write_marketflow_repository_tag_push_strategy_operator_review_v1(tmp_path)
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyOperatorReviewError):
        service.write_marketflow_repository_tag_push_strategy_operator_review_v1(tmp_path)
