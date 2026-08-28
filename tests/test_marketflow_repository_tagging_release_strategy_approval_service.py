from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_tagging_release_strategy_approval_service as service,
)


def _attestation(**overrides: object) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-28T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_inventory_plan_digest": service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "operator_confirms_source_final_archive_digest": service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "operator_confirms_origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_confirms_selected_tagging_package": service.SELECTED_TAGGING_PACKAGE,
        "operator_confirms_approved_terminal_tag_names": service.APPROVED_TERMINAL_TAG_NAMES,
        "operator_confirms_approved_terminal_tag_count": 4,
        **{field: True for field in service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS},
    }
    values.update(overrides)
    return service.build_marketflow_repository_tagging_release_strategy_approval_attestation_v1(
        **values
    )


@pytest.fixture
def attestation() -> dict:
    return _attestation()


@pytest.fixture
def approval(attestation: dict) -> dict:
    return service.build_marketflow_repository_tagging_release_strategy_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_exact_required_fields(attestation: dict) -> None:
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE
    assert attestation["operator_confirms_approved_terminal_tag_names"] == service.APPROVED_TERMINAL_TAG_NAMES
    assert all(attestation[field] is True for field in service.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_approval_builds_offline_without_rerunning_source_review(
    monkeypatch: pytest.MonkeyPatch, attestation: dict
) -> None:
    monkeypatch.setattr(
        service.source_review_service,
        "build_marketflow_repository_tagging_release_strategy_operator_review_v1",
        lambda *args, **kwargs: pytest.fail("source review must not be rerun"),
    )
    result = service.build_marketflow_repository_tagging_release_strategy_approval_v1(
        operator_attestation=attestation
    )
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED),
        ("approval_scope", service.REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("selected_tagging_package", service.SELECTED_TAGGING_PACKAGE),
        ("source_tagging_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_tagging_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_inventory_plan_digest", service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
    ],
)
def test_identity_and_bound_sources(approval: dict, field: str, expected: object) -> None:
    assert approval[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_selected",
        "repository_tagging_release_strategy_approved",
        "repository_tagging_release_strategy_authorized",
        "repository_tagging_release_strategy_approval_created",
        "ready_for_repository_tagging_execution",
    ],
)
def test_approval_authority_flags_are_true(approval: dict, field: str) -> None:
    assert approval[field] is True


def test_operator_decision_and_phrase_match(approval: dict) -> None:
    attestation = approval["operator_attestation"]
    assert attestation["operator_decision"] == service.OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE


def test_four_exact_terminal_tags_are_approved_not_created(approval: dict) -> None:
    rows = approval["approved_terminal_tags"]
    assert approval["approved_terminal_tag_count"] == len(rows) == 4
    assert [row["tag_name"] for row in rows] == service.APPROVED_TERMINAL_TAG_NAMES
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY" for row in rows)
    assert all(row["tag_status"] == "APPROVED_NOT_CREATED" for row in rows)
    assert all(row["tag_created"] is False and row["tag_pushed"] is False for row in rows)
    assert all(row["separate_execution_required"] is True for row in rows)


@pytest.mark.parametrize(
    ("tag_name", "target_commit"),
    [
        ("marketflow/expectancy-lab/final-archive-not-ready/v1", "0be55dc8a65a586368c192d6bc13302b9830a0b4"),
        ("marketflow/expectancy-lab/archive-record-not-ready/v1", "e2fcfb792ad14db8a2de69556c291529fda47a8e"),
        ("marketflow/expectancy-lab/operator-selection-option-a/v1", "15c4fae495f88b54e30380f3d8b4aa54989fad39"),
        ("marketflow/expectancy-lab/readiness-not-ready/v1", "611a7c73d5e3567a6eb5f3664ba3b004edb1c1a0"),
    ],
)
def test_terminal_tag_target_commits_are_exact(
    approval: dict, tag_name: str, target_commit: str
) -> None:
    row = next(item for item in approval["approved_terminal_tags"] if item["tag_name"] == tag_name)
    assert row["tag_target_commit"] == target_commit


def test_supporting_packages_are_available_not_selected(approval: dict) -> None:
    rows = approval["supporting_tagging_packages"]
    assert len(rows) == 3
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in rows)
    assert all(row["selected"] is False and row["approved"] is False for row in rows)


def test_governance_and_protection_tags_are_unapproved(approval: dict) -> None:
    assert len(approval["unapproved_governance_tags"]) == 7
    assert len(approval["unapproved_source_protection_tags"]) == 3
    for row in approval["unapproved_governance_tags"] + approval["unapproved_source_protection_tags"]:
        assert row["approval_status"] == "NOT_APPROVED_AVAILABLE_FOR_FUTURE_SELECTION"
        assert row["tag_created"] is False
        assert row["tag_pushed"] is False


def test_future_tag_message_template_is_approved(approval: dict) -> None:
    assert approval["future_tag_message_template"] == service.source_review_service.source_candidate_service.FUTURE_TAG_MESSAGE_TEMPLATE
    assert approval["future_tag_message_template_status"] == "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY"


@pytest.mark.parametrize(
    "field",
    [
        "repository_tagging_release_strategy_executed",
        "git_tag_created",
        "git_tag_push_performed",
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
def test_execution_and_external_action_flags_remain_false(
    approval: dict, field: str
) -> None:
    assert approval[field] is False


def test_authority_strings_remain_closed(approval: dict) -> None:
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED
    assert approval["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert approval[field] == service.NOT_AUTHORIZED


def test_next_chain_gates_and_risk_controls_are_defined(approval: dict) -> None:
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert len(approval["next_chain"]) == 5
    assert len(approval["next_gates"]) == 6
    assert len(approval["risk_controls"]) == 31


def test_checklist_and_summary_pass(approval: dict) -> None:
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert len(approval["checklist"]) == 58
    assert all(row["status"] == service.PASS for row in approval["checklist"])
    assert approval["summary"]["passed_checks"] == 58
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(attestation: dict, approval: dict) -> None:
    rebuilt = service.build_marketflow_repository_tagging_release_strategy_approval_v1(
        operator_attestation=attestation
    )
    digest = approval["marketflow_repository_tagging_release_strategy_approval_digest"]
    assert rebuilt["marketflow_repository_tagging_release_strategy_approval_digest"] == digest
    assert service.marketflow_repository_tagging_release_strategy_approval_digest_v1(approval) == digest


def test_validator_accepts_valid_approval(approval: dict) -> None:
    result = service.validate_marketflow_repository_tagging_release_strategy_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_VALID
    assert result["passed_checks"] == 58
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("selected_tagging_package", "WRONG"),
        ("source_tagging_operator_review_digest", "0" * 64),
        ("source_tagging_candidate_digest", "0" * 64),
        ("source_inventory_plan_digest", "0" * 64),
        ("source_final_archive_digest", "0" * 64),
        ("origin_main_commit", "0" * 40),
        ("repository_tagging_release_strategy_approval_created", False),
        ("repository_tagging_release_strategy_selected", False),
        ("repository_tagging_release_strategy_approved", False),
        ("repository_tagging_release_strategy_authorized", False),
        ("ready_for_repository_tagging_execution", False),
        ("repository_tagging_release_strategy_executed", True),
        ("git_tag_created", True),
        ("git_tag_push_performed", True),
        ("approved_terminal_tag_count", 3),
        ("approved_terminal_tags", []),
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
        ("predictive_usefulness_accepted", True),
        ("profitability_accepted", True),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_top_level_contract_mutations(
    approval: dict, field: str, invalid: object
) -> None:
    mutated = deepcopy(approval)
    mutated[field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
        service.validate_marketflow_repository_tagging_release_strategy_approval_v1(mutated)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("selected_tagging_package", "WRONG"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_candidate_digest", "0" * 64),
        ("operator_confirms_source_inventory_plan_digest", "0" * 64),
        ("operator_confirms_source_final_archive_digest", "0" * 64),
        ("operator_confirms_origin_main_commit", "0" * 40),
        ("operator_confirms_approved_terminal_tag_count", 3),
        ("operator_confirms_approved_terminal_tag_names", []),
        ("operator_confirms_tags_not_created", False),
        ("operator_confirms_tags_not_pushed", False),
        ("operator_confirms_no_main_push", False),
        ("operator_confirms_no_provider_requests", False),
        ("operator_confirms_runtime_not_authorized", False),
    ],
)
def test_builder_rejects_attestation_mutations(field: str, invalid: object) -> None:
    attestation = _attestation()
    attestation[field] = invalid
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
        service.build_marketflow_repository_tagging_release_strategy_approval_v1(
            operator_attestation=attestation
        )


def test_validator_rejects_governance_or_protection_approval(approval: dict) -> None:
    for field in ("unapproved_governance_tags", "unapproved_source_protection_tags"):
        mutated = deepcopy(approval)
        mutated[field][0]["approval_status"] = "APPROVED"
        with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
            service.validate_marketflow_repository_tagging_release_strategy_approval_v1(mutated)


def test_validator_rejects_created_or_pushed_terminal_tag(approval: dict) -> None:
    for field in ("tag_created", "tag_pushed"):
        mutated = deepcopy(approval)
        mutated["approved_terminal_tags"][0][field] = True
        with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
            service.validate_marketflow_repository_tagging_release_strategy_approval_v1(mutated)


def test_validator_rejects_missing_digest(approval: dict) -> None:
    mutated = deepcopy(approval)
    mutated.pop("marketflow_repository_tagging_release_strategy_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
        service.validate_marketflow_repository_tagging_release_strategy_approval_v1(mutated)


def test_explicit_invalid_source_review_is_rejected(attestation: dict) -> None:
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
        service.build_marketflow_repository_tagging_release_strategy_approval_v1(
            source_review={"artifact_kind": "WRONG"},
            operator_attestation=attestation,
        )


def test_markdown_contains_all_required_sections(approval: dict) -> None:
    markdown = service.build_marketflow_repository_tagging_release_strategy_approval_markdown_v1(approval)
    for section in (
        "Title",
        "MarketFlow Repository Tagging / Release Strategy Approval v1",
        "Operator Attestation",
        "Source Operator Review",
        "Bound Evidence",
        "Repository Context",
        "Approval Scope",
        "Selected Tagging Package",
        "Approved Terminal Tags",
        "Supporting Packages",
        "Unapproved Tags",
        "Future Tag Message Template",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown


def test_writer_round_trips_canonical_json_and_refuses_overwrite(
    tmp_path, attestation: dict
) -> None:
    result = service.write_marketflow_repository_tagging_release_strategy_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    path = tmp_path / "marketflow_repository_tagging_release_strategy_approval_v1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    service.validate_marketflow_repository_tagging_release_strategy_approval_v1(payload)
    assert result["marketflow_repository_tagging_release_strategy_approval_digest"] == payload["marketflow_repository_tagging_release_strategy_approval_digest"]
    with pytest.raises(service.MarketFlowRepositoryTaggingReleaseStrategyApprovalError):
        service.write_marketflow_repository_tagging_release_strategy_approval_v1(
            tmp_path, operator_attestation=attestation
        )
