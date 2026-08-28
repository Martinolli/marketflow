from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_tag_push_strategy_approval_service as service


def attestation_kwargs() -> dict:
    return {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-28T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_results_review_digest": service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_source_tag_manifest_review_digest": service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "operator_confirms_source_execution_digest": service.EXPECTED_SOURCE_EXECUTION_DIGEST,
        "operator_confirms_source_approval_digest": service.EXPECTED_SOURCE_APPROVAL_DIGEST,
        "operator_confirms_origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_confirms_selected_tag_push_package": service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "operator_confirms_approved_remote_refs": service.APPROVED_REMOTE_REFS,
        "operator_confirms_approved_tag_object_shas": service.APPROVED_TAG_OBJECT_SHAS,
        "operator_confirms_approved_target_commits": service.APPROVED_TARGET_COMMITS,
        "operator_confirms_approved_tag_push_count": 4,
        **{field: True for field in service.ATTESTATION_TRUE_FIELDS},
    }


@pytest.fixture()
def attestation() -> dict:
    return service.build_marketflow_repository_tag_push_strategy_approval_attestation_v1(
        **attestation_kwargs()
    )


@pytest.fixture()
def approval(attestation) -> dict:
    return service.build_marketflow_repository_tag_push_strategy_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_all_required_fields(attestation):
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert set(service.ATTESTATION_STRING_FIELDS).issubset(attestation)
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_approval_builds_offline_without_source_review_rerun(attestation, monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("source review must not be rerun")

    monkeypatch.setattr(
        service.source_service,
        "build_marketflow_repository_tag_push_strategy_operator_review_v1",
        fail_if_called,
    )
    built = service.build_marketflow_repository_tag_push_strategy_approval_v1(
        operator_attestation=attestation
    )
    assert built["created_offline"] is True
    assert built["planning_only"] is True
    assert built["governance_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED),
        ("approval_scope", service.REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("selected_tag_push_package", service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN),
        ("source_tag_push_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_tag_push_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tagging_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_tag_manifest_review_digest", service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST),
        ("source_tagging_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_tagging_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_operator_review_commit", service.EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT),
    ],
)
def test_approval_binds_required_fields(approval, field, expected):
    assert approval[field] == expected


def test_operator_decision_and_phrase_match(approval):
    assert approval["operator_attestation"]["operator_decision"] == service.OPERATOR_DECISION
    assert approval["operator_attestation"]["operator_attestation_phrase"] == (
        service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    )


def test_approval_selection_and_authorization_are_true(approval):
    assert approval["repository_tag_push_strategy_approval_created"] is True
    assert approval["repository_tag_push_strategy_selected"] is True
    assert approval["repository_tag_push_strategy_approved"] is True
    assert approval["repository_tag_push_strategy_authorized"] is True
    assert approval["ready_for_repository_tag_push_execution"] is True


def test_strategy_execution_remains_false(approval):
    assert approval["repository_tag_push_strategy_executed"] is False
    assert approval["approved_selected_package"]["executed"] is False


def test_four_tag_pushes_are_approved_for_future_execution(approval):
    assert approval["approved_tag_push_count"] == 4
    assert len(approval["approved_tag_push_records"]) == 4
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_TAG_PUSH_EXECUTION_ONLY" for row in approval["approved_tag_push_records"])
    assert all(row["selected_for_push"] is True for row in approval["approved_tag_push_records"])
    assert all(row["approved_for_push"] is True for row in approval["approved_tag_push_records"])
    assert all(row["pushed"] is False for row in approval["approved_tag_push_records"])


def test_approved_refs_objects_and_targets_match(approval):
    assert approval["approved_remote_refs"] == service.APPROVED_REMOTE_REFS
    assert approval["approved_tag_object_shas"] == service.APPROVED_TAG_OBJECT_SHAS
    assert approval["approved_target_commits"] == service.APPROVED_TARGET_COMMITS


def test_approved_future_command_is_present_but_not_executed(approval):
    assert approval["approved_future_push_command_template"] == service.APPROVED_PUSH_COMMAND_TEMPLATE
    assert approval["command_approval_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY"
    assert approval["command_executed"] is False
    assert approval["remote_publication_status"] == "APPROVED_NOT_PUSHED"


def test_supporting_packages_are_available_not_selected(approval):
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert len(approval["supporting_packages"]) == 3
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in approval["supporting_packages"])


@pytest.mark.parametrize(
    "field",
    [
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
        "provider_requests_made_in_approval",
        "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ],
)
def test_execution_mutation_and_acceptance_flags_remain_false(approval, field):
    assert approval[field] is False


def test_marketflow_tracked_file_count_is_zero(approval):
    assert approval["tracked_marketflow_file_count"] == 0
    assert approval["no_tracked_marketflow_files"] is True


def test_acceptance_and_runtime_boundaries_remain_closed(approval):
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"
    assert approval["runtime_use"] == "NOT_AUTHORIZED"
    assert approval["strategy_use"] == "NOT_AUTHORIZED"
    assert approval["paper_trading"] == "NOT_AUTHORIZED"
    assert approval["broker_execution"] == "NOT_AUTHORIZED"


def test_next_chain_and_risk_controls_are_defined(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert approval["recommended_next_task"] == "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1"


def test_checklist_passes(approval):
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == 62
    assert approval["summary"]["passed_checks"] == 62
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(attestation):
    first = service.build_marketflow_repository_tag_push_strategy_approval_v1(operator_attestation=attestation)
    second = service.build_marketflow_repository_tag_push_strategy_approval_v1(operator_attestation=attestation)
    assert first["marketflow_repository_tag_push_strategy_approval_digest"] == second[
        "marketflow_repository_tag_push_strategy_approval_digest"
    ]
    assert first["marketflow_repository_tag_push_strategy_approval_digest"] == (
        service.marketflow_repository_tag_push_strategy_approval_digest_v1(first)
    )


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_tag_push_strategy_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_VALID
    assert result["passed_checks"] == 62


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("selected_tag_push_package", "WRONG"),
        ("source_tag_push_operator_review_digest", "0" * 64),
        ("source_tag_push_candidate_digest", "0" * 64),
        ("source_tagging_results_review_digest", "0" * 64),
        ("source_tag_manifest_review_digest", "0" * 64),
        ("source_tagging_execution_digest", "0" * 64),
        ("source_tagging_approval_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tag_push_strategy_approval_created", False),
        ("repository_tag_push_strategy_selected", False),
        ("repository_tag_push_strategy_approved", False),
        ("repository_tag_push_strategy_authorized", False),
        ("ready_for_repository_tag_push_execution", False),
        ("repository_tag_push_strategy_executed", True),
        ("repository_tags_pushed", True),
        ("git_tag_push_performed", True),
        ("additional_tags_created", True),
        ("tags_modified", True),
        ("tags_deleted", True),
        ("approved_tag_push_count", 3),
        ("approved_remote_refs", []),
        ("approved_tag_object_shas", []),
        ("approved_target_commits", []),
        ("command_executed", True),
        ("git_merge_performed", True),
        ("git_rebase_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_main_push_performed", True),
        ("git_force_push_performed", True),
        ("git_remote_prune_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
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
def test_validator_rejects_changed_boundaries(approval, field, replacement):
    mutated = deepcopy(approval)
    mutated[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.validate_marketflow_repository_tag_push_strategy_approval_v1(mutated)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("selected_tag_push_package", "WRONG"),
        ("operator_confirms_approved_remote_refs", []),
        ("operator_confirms_approved_tag_object_shas", []),
        ("operator_confirms_approved_target_commits", []),
        ("operator_confirms_approved_tag_push_count", 3),
    ],
)
def test_validator_rejects_attestation_mismatch(approval, field, replacement):
    mutated = deepcopy(approval)
    mutated["operator_attestation"][field] = replacement
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.validate_marketflow_repository_tag_push_strategy_approval_v1(mutated)


@pytest.mark.parametrize("field", service.ATTESTATION_TRUE_FIELDS)
def test_attestation_builder_rejects_false_confirmation(field):
    kwargs = attestation_kwargs()
    kwargs[field] = False
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.build_marketflow_repository_tag_push_strategy_approval_attestation_v1(**kwargs)


def test_validator_rejects_missing_risk_controls(approval):
    mutated = deepcopy(approval)
    mutated["risk_controls"] = []
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.validate_marketflow_repository_tag_push_strategy_approval_v1(mutated)


def test_validator_rejects_missing_digest(approval):
    mutated = deepcopy(approval)
    mutated.pop("marketflow_repository_tag_push_strategy_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.validate_marketflow_repository_tag_push_strategy_approval_v1(mutated)


def test_markdown_includes_required_sections(approval):
    markdown = service.build_marketflow_repository_tag_push_strategy_approval_markdown_v1(approval)
    for section in (
        "Title",
        "MarketFlow Repository Tag Push Strategy Approval v1",
        "Operator Attestation",
        "Source Tag Push Operator Review",
        "Bound Evidence",
        "Repository Context",
        "Approval Scope",
        "Selected Tag Push Package",
        "Approved Tag Push Records",
        "Approved Future Push Command",
        "Supporting Packages",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json(tmp_path, attestation):
    receipt = service.write_marketflow_repository_tag_push_strategy_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    payload = json.loads((tmp_path / "marketflow_repository_tag_push_strategy_approval_v1.json").read_text())
    service.validate_marketflow_repository_tag_push_strategy_approval_v1(payload)
    assert receipt["marketflow_repository_tag_push_strategy_approval_digest"] == payload[
        "marketflow_repository_tag_push_strategy_approval_digest"
    ]


def test_writer_refuses_to_overwrite(tmp_path, attestation):
    service.write_marketflow_repository_tag_push_strategy_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    with pytest.raises(service.MarketFlowRepositoryTagPushStrategyApprovalError):
        service.write_marketflow_repository_tag_push_strategy_approval_v1(
            tmp_path, operator_attestation=attestation
        )
