from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_tag_push_strategy_candidate_service as service


@pytest.fixture()
def candidate() -> dict:
    return service.build_marketflow_repository_tag_push_strategy_candidate_v1()


def test_candidate_builds_offline_without_source_review_rerun(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("source review must not be rerun")

    monkeypatch.setattr(
        service.source_review_service,
        "build_marketflow_repository_tagging_execution_results_review_v1",
        fail_if_called,
    )
    built = service.build_marketflow_repository_tag_push_strategy_candidate_v1()
    assert built["created_offline"] is True
    assert built["planning_only"] is True
    assert built["governance_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1),
        ("candidate_status", service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_READY_FOR_OPERATOR_REVIEW),
        ("candidate_scope", service.REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tagging_results_review_digest", service.EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_DIGEST),
        ("source_tagging_results_review_tag_manifest_digest", service.EXPECTED_SOURCE_TAGGING_RESULTS_REVIEW_TAG_MANIFEST_DIGEST),
        ("source_tagging_execution_digest", service.EXPECTED_SOURCE_TAGGING_EXECUTION_DIGEST),
        ("source_tagging_execution_tag_manifest_digest", service.EXPECTED_SOURCE_TAGGING_EXECUTION_TAG_MANIFEST_DIGEST),
        ("source_tagging_approval_digest", service.EXPECTED_SOURCE_TAGGING_APPROVAL_DIGEST),
        ("source_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_results_review_commit", service.EXPECTED_SOURCE_RESULTS_REVIEW_COMMIT),
    ],
)
def test_candidate_binds_required_fields(candidate, field, expected):
    assert candidate[field] == expected


def test_source_tag_review_and_candidate_readiness_are_true(candidate):
    assert candidate["source_tag_review_ready"] is True
    assert candidate["repository_tag_push_strategy_candidate_created"] is True
    assert candidate["repository_tag_push_strategy_candidate_ready_for_operator_review"] is True
    assert candidate["ready_for_repository_tag_push_strategy_operator_review"] is True


def test_recommended_push_package_is_present(candidate):
    assert candidate["recommended_tag_push_package"] == (
        service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN
    )
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"


def test_four_candidate_push_packages_are_present(candidate):
    assert candidate["tag_push_packages"] == service.TAG_PUSH_PACKAGES
    assert len(candidate["tag_push_packages"]) == 4


def test_four_candidate_push_records_and_remote_refs_are_present(candidate):
    assert candidate["candidate_push_records"] == service.TAG_PUSH_RECORDS
    assert len(candidate["candidate_push_records"]) == 4
    assert [row["candidate_remote_ref"] for row in candidate["candidate_push_records"]] == (
        service.CANDIDATE_REMOTE_REFS
    )


def test_local_tag_objects_and_targets_are_bound(candidate):
    records = candidate["candidate_push_records"]
    assert [row["local_tag_object_sha"] for row in records] == (
        service.source_review_service.EXPECTED_TAG_OBJECT_SHAS
    )
    assert [row["target_commit"] for row in records] == [
        row["target_commit"] for row in service.source_review_service.EXPECTED_TAGS
    ]


def test_remote_refs_were_absent_in_source_review(candidate):
    assert all(
        row["remote_ref_exists_in_source_review"] is False
        for row in candidate["candidate_push_records"]
    )
    assert candidate["source_tag_counts"]["remote_approved_tag_count"] == 0


def test_push_command_is_present_but_not_executed(candidate):
    assert candidate["candidate_push_command_template"] == service.CANDIDATE_PUSH_COMMAND_TEMPLATE
    assert all(ref in candidate["candidate_push_command_template"] for ref in service.CANDIDATE_REMOTE_REFS)
    assert candidate["command_status"] == "PLANNED_NOT_EXECUTED"
    assert candidate["remote_publication_status"] == "NOT_PUSHED"


@pytest.mark.parametrize(
    "field",
    [
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
        "provider_requests_made_in_candidate",
        "market_data_acquisition_performed_in_candidate",
        "dataset_generation_performed_in_candidate",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ],
)
def test_execution_and_acceptance_flags_remain_false(candidate, field):
    assert candidate[field] is False


def test_marketflow_tracked_file_count_is_zero(candidate):
    assert candidate["tracked_marketflow_file_count"] == 0
    assert candidate["no_tracked_marketflow_files"] is True


def test_acceptance_and_authority_boundaries_remain_closed(candidate):
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"
    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"
    assert candidate["paper_trading"] == "NOT_AUTHORIZED"
    assert candidate["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_and_gates_are_defined(candidate):
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["recommended_next_task"] == (
        "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1"
    )


def test_risk_controls_are_defined(candidate):
    assert candidate["risk_controls"] == service.RISK_CONTROLS
    assert "explicit_refspec_required_for_future_push" in candidate["risk_controls"]
    assert "push_all_tags_forbidden" in candidate["risk_controls"]


def test_checklist_passes(candidate):
    assert [row["check_id"] for row in candidate["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == 63
    assert candidate["summary"]["passed_checks"] == 63
    assert candidate["summary"]["failed_checks"] == 0
    assert candidate["summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic():
    first = service.build_marketflow_repository_tag_push_strategy_candidate_v1()
    second = service.build_marketflow_repository_tag_push_strategy_candidate_v1()
    assert first["marketflow_repository_tag_push_strategy_candidate_digest"] == second[
        "marketflow_repository_tag_push_strategy_candidate_digest"
    ]
    assert first["marketflow_repository_tag_push_strategy_candidate_digest"] == (
        service.marketflow_repository_tag_push_strategy_candidate_digest_v1(first)
    )


def test_validator_accepts_valid_candidate(candidate):
    result = service.validate_marketflow_repository_tag_push_strategy_candidate_v1(candidate)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_VALID
    assert result["passed_checks"] == 63


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("source_tagging_results_review_digest", "0" * 64),
        ("source_tagging_results_review_tag_manifest_digest", "0" * 64),
        ("source_tagging_execution_digest", "0" * 64),
        ("source_tagging_approval_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tag_push_strategy_candidate_created", False),
        ("repository_tag_push_strategy_candidate_ready_for_operator_review", False),
        ("command_status", "EXECUTED"),
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
        ("provider_requests_made_in_candidate", True),
        ("market_data_acquisition_performed_in_candidate", True),
        ("dataset_generation_performed_in_candidate", True),
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
def test_validator_rejects_changed_boundaries(candidate, field, replacement):
    mutated = deepcopy(candidate)
    mutated[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.validate_marketflow_repository_tag_push_strategy_candidate_v1(mutated)


@pytest.mark.parametrize("field", ["recommended_tag_push_package", "candidate_push_command_template"])
def test_validator_rejects_missing_required_field(candidate, field):
    mutated = deepcopy(candidate)
    mutated.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.validate_marketflow_repository_tag_push_strategy_candidate_v1(mutated)


def test_validator_rejects_missing_push_records(candidate):
    mutated = deepcopy(candidate)
    mutated["candidate_push_records"] = []
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.validate_marketflow_repository_tag_push_strategy_candidate_v1(mutated)


def test_validator_rejects_missing_risk_controls(candidate):
    mutated = deepcopy(candidate)
    mutated["risk_controls"] = []
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.validate_marketflow_repository_tag_push_strategy_candidate_v1(mutated)


def test_validator_rejects_missing_digest(candidate):
    mutated = deepcopy(candidate)
    mutated.pop("marketflow_repository_tag_push_strategy_candidate_digest")
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.validate_marketflow_repository_tag_push_strategy_candidate_v1(mutated)


def test_markdown_includes_required_sections(candidate):
    markdown = service.build_marketflow_repository_tag_push_strategy_candidate_markdown_v1(candidate)
    for section in (
        "Title",
        "MarketFlow Repository Tag Push Strategy Candidate v1",
        "Source Tagging Results Review",
        "Bound Evidence",
        "Repository Context",
        "Candidate Scope",
        "Tag Push Philosophy",
        "Recommended Push Package",
        "Candidate Push Packages",
        "Candidate Push Records",
        "Remote Publication Plan",
        "Tag Push Prerequisites",
        "Tag Push Non-Goals",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json(tmp_path):
    receipt = service.write_marketflow_repository_tag_push_strategy_candidate_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_tag_push_strategy_candidate_v1.json").read_text())
    service.validate_marketflow_repository_tag_push_strategy_candidate_v1(payload)
    assert receipt["marketflow_repository_tag_push_strategy_candidate_digest"] == payload[
        "marketflow_repository_tag_push_strategy_candidate_digest"
    ]


def test_writer_refuses_to_overwrite(tmp_path):
    service.write_marketflow_repository_tag_push_strategy_candidate_v1(tmp_path)
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyCandidateError):
        service.write_marketflow_repository_tag_push_strategy_candidate_v1(tmp_path)
