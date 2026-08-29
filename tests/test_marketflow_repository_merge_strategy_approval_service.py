from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_merge_strategy_approval_service as service
from marketflow.services import marketflow_repository_merge_strategy_operator_review_service as review_service


def _attestation_kwargs():
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-29T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_tag_push_results_review_digest": service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_source_remote_manifest_review_digest": service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST,
        "operator_confirms_source_tag_push_execution_digest": service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST,
        "operator_confirms_source_tag_push_approval_digest": service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST,
        "operator_confirms_origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_confirms_selected_merge_strategy_package": service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION,
        "operator_confirms_integration_branch_name": service.INTEGRATION_BRANCH_NAME,
        "operator_confirms_integration_base": service.INTEGRATION_BASE,
        "operator_confirms_integration_source_branch": service.INTEGRATION_SOURCE_BRANCH,
        "operator_confirms_integration_source_commit": service.INTEGRATION_SOURCE_COMMIT,
    }
    values.update({field: True for field in service.ATTESTATION_TRUE_FIELDS})
    return values


@pytest.fixture
def attestation():
    return service.build_marketflow_repository_merge_strategy_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture
def approval(attestation):
    return service.build_marketflow_repository_merge_strategy_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation):
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["selected_merge_strategy_package"] == service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_approval_builds_offline_deterministically(attestation, approval):
    assert service.build_marketflow_repository_merge_strategy_approval_v1(
        operator_attestation=attestation
    ) == approval


def test_approval_accepts_valid_source_review(attestation, approval):
    source_review = review_service.build_marketflow_repository_merge_strategy_operator_review_v1()
    assert service.build_marketflow_repository_merge_strategy_approval_v1(
        source_review=source_review, operator_attestation=attestation
    ) == approval


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED),
        ("approval_scope", service.REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("selected_merge_strategy_package", service.PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION),
        ("source_merge_strategy_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_merge_strategy_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_tag_push_results_review_digest", service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_remote_manifest_review_digest", service.EXPECTED_SOURCE_REMOTE_MANIFEST_REVIEW_DIGEST),
        ("source_tag_push_execution_digest", service.EXPECTED_SOURCE_TAG_PUSH_EXECUTION_DIGEST),
        ("source_tag_push_approval_digest", service.EXPECTED_SOURCE_TAG_PUSH_APPROVAL_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_operator_review_commit", service.EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT),
        ("repository_merge_strategy_candidate_created", True),
        ("repository_merge_strategy_operator_review_created", True),
        ("repository_merge_strategy_operator_review_ready", True),
        ("repository_merge_strategy_selected", True),
        ("repository_merge_strategy_approved", True),
        ("repository_merge_strategy_authorized", True),
        ("repository_merge_strategy_approval_created", True),
        ("ready_for_repository_integration_branch_execution", True),
        ("repository_merge_strategy_executed", False),
        ("repository_integration_branch_created", False), ("integration_branch_created", False),
        ("integration_merge_performed", False), ("integration_pytest_performed", False),
        ("main_merge_performed", False), ("main_push_performed", False),
        ("git_merge_performed", False), ("git_rebase_performed", False),
        ("git_squash_merge_performed", False), ("git_cherry_pick_performed", False),
        ("git_main_push_performed", False), ("origin_main_modified_by_this_task", False),
        ("repository_cleanup_candidate_created", False), ("repository_cleanup_approved", False),
        ("repository_cleanup_executed", False), ("git_branch_delete_performed", False),
        ("git_remote_delete_performed", False), ("git_force_push_performed", False),
        ("git_remote_prune_performed", False), ("repository_tags_pushed_again", False),
        ("additional_tag_push_performed", False), ("additional_tags_created", False),
        ("tags_modified", False), ("tags_deleted", False),
        ("provider_requests_made_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False), ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"), ("predictive_usefulness_accepted", False),
        ("profitability", "not accepted"), ("profitability_accepted", False),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
        ("tracked_marketflow_file_count", 0), ("no_tracked_marketflow_files", True),
    ],
)
def test_required_approval_fields(approval, field, expected):
    assert approval[field] == expected


def test_operator_attestation_is_bound(approval, attestation):
    assert approval["operator_attestation"] == attestation
    assert approval["operator_attestation"]["operator_decision"] == service.OPERATOR_DECISION


def test_repository_context_is_preserved(approval):
    assert approval["source_repository_context"] == {
        "local_branch_count": 302, "remote_ref_count": 274, "total_ref_count": 576,
        "local_tag_count": 32, "verified_terminal_tags": 4,
    }


def test_selected_package_is_approved_for_future_execution_only(approval):
    package = approval["approved_selected_package"]
    assert package == service.APPROVED_SELECTED_PACKAGE
    assert package["selected"] is True
    assert package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False
    assert package["integration_branch_created"] is False


def test_supporting_packages_are_available_not_selected(approval):
    packages = approval["supporting_packages"]
    assert packages == service.SUPPORTING_PACKAGES
    assert len(packages) == 5
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in packages)
    assert all(row["selected"] is False for row in packages)


def test_integration_branch_plan_is_approved_not_executed(approval):
    plan = approval["approved_integration_branch_plan"]
    assert plan == service.APPROVED_INTEGRATION_BRANCH_PLAN
    assert plan["integration_branch_name"] == service.INTEGRATION_BRANCH_NAME
    assert plan["integration_base"] == "origin/main"
    assert plan["integration_source_commit"] == service.INTEGRATION_SOURCE_COMMIT
    assert plan["integration_plan_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY"
    assert plan["integration_branch_created"] is False
    assert plan["integration_merge_performed"] is False
    assert plan["integration_pytest_performed"] is False
    assert plan["main_merge_performed"] is False
    assert plan["main_push_performed"] is False


def test_future_execution_boundary(approval):
    boundary = approval["future_execution_boundary"]
    assert boundary == service.FUTURE_EXECUTION_BOUNDARY
    assert boundary["future_execution_may_create_integration_branch"] is True
    assert boundary["future_execution_may_attempt_integration_merge_on_integration_branch"] is True
    assert boundary["future_execution_must_not_push_main"] is True
    assert boundary["future_execution_must_not_authorize_runtime"] is True


def test_next_chain_gates_and_risk_controls(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert approval["recommended_next_task"] == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1"


def test_checklist_and_summary_pass(approval):
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert approval["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(approval):
    assert approval["marketflow_repository_merge_strategy_approval_digest"] == service.marketflow_repository_merge_strategy_approval_digest_v1(approval)


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_merge_strategy_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVAL_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_candidate_digest", "0" * 64),
        ("operator_confirms_source_tag_push_results_review_digest", "0" * 64),
        ("operator_confirms_source_remote_manifest_review_digest", "0" * 64),
        ("operator_confirms_source_tag_push_execution_digest", "0" * 64),
        ("operator_confirms_source_tag_push_approval_digest", "0" * 64),
        ("operator_confirms_origin_main_commit", "0" * 40),
        ("operator_confirms_selected_merge_strategy_package", "WRONG"),
        ("operator_confirms_integration_branch_name", "WRONG"),
        ("operator_confirms_integration_base", "WRONG"),
        ("operator_confirms_integration_source_branch", "WRONG"),
        ("operator_confirms_integration_source_commit", "0" * 40),
        *[(field, False) for field in service.ATTESTATION_TRUE_FIELDS],
    ],
)
def test_attestation_builder_rejects_mismatch(field, bad_value):
    kwargs = _attestation_kwargs()
    kwargs[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyApprovalError):
        service.build_marketflow_repository_merge_strategy_approval_attestation_v1(**kwargs)


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"), (("approval_status",), "WRONG"),
        (("approval_scope",), "WRONG"), (("selected_merge_strategy_package",), "WRONG"),
        (("source_merge_strategy_operator_review_digest",), "0" * 64),
        (("source_merge_strategy_candidate_digest",), "0" * 64),
        (("source_tag_push_results_review_digest",), "0" * 64),
        (("source_tag_push_execution_digest",), "0" * 64),
        (("source_tag_push_approval_digest",), "0" * 64), (("origin_main_commit",), "0" * 40),
        (("operator_attestation", "operator_decision"), "WRONG"),
        (("operator_attestation", "operator_attestation_phrase"), "WRONG"),
        (("repository_merge_strategy_approval_created",), False),
        (("repository_merge_strategy_selected",), False),
        (("repository_merge_strategy_approved",), False),
        (("repository_merge_strategy_authorized",), False),
        (("ready_for_repository_integration_branch_execution",), False),
        (("repository_merge_strategy_executed",), True),
        (("approved_integration_branch_plan",), {}),
        (("integration_branch_created",), True), (("integration_merge_performed",), True),
        (("integration_pytest_performed",), True), (("main_merge_performed",), True),
        (("main_push_performed",), True), (("git_merge_performed",), True),
        (("git_rebase_performed",), True), (("git_squash_merge_performed",), True),
        (("git_cherry_pick_performed",), True), (("git_main_push_performed",), True),
        (("git_force_push_performed",), True), (("git_branch_delete_performed",), True),
        (("git_remote_delete_performed",), True), (("git_remote_prune_performed",), True),
        (("origin_main_modified_by_this_task",), True), (("repository_tags_pushed_again",), True),
        (("additional_tags_created",), True), (("tags_modified",), True), (("tags_deleted",), True),
        (("repository_cleanup_candidate_created",), True),
        (("provider_requests_made_in_approval",), True),
        (("market_data_acquisition_performed_in_approval",), True),
        (("dataset_generation_performed_in_approval",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness_accepted",), True), (("profitability_accepted",), True),
        (("runtime_use",), "AUTHORIZED"), (("broker_execution",), "AUTHORIZED"),
        (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutations(approval, path, bad_value):
    changed = deepcopy(approval)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyApprovalError):
        service.validate_marketflow_repository_merge_strategy_approval_v1(changed)


def test_validator_rejects_missing_digest(approval):
    changed = deepcopy(approval)
    changed.pop("marketflow_repository_merge_strategy_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyApprovalError):
        service.validate_marketflow_repository_merge_strategy_approval_v1(changed)


def test_source_review_digest_mismatch_is_rejected(attestation):
    source_review = review_service.build_marketflow_repository_merge_strategy_operator_review_v1()
    source_review["marketflow_repository_merge_strategy_operator_review_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyApprovalError):
        service.build_marketflow_repository_merge_strategy_approval_v1(
            source_review=source_review, operator_attestation=attestation
        )


def test_writer_round_trip(tmp_path, attestation):
    result = service.write_marketflow_repository_merge_strategy_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    payload = json.loads((tmp_path / "marketflow_repository_merge_strategy_approval_v1.json").read_text(encoding="utf-8"))
    assert result["marketflow_repository_merge_strategy_approval_digest"] == payload["marketflow_repository_merge_strategy_approval_digest"]
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_overwrite(tmp_path, attestation):
    service.write_marketflow_repository_merge_strategy_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    with pytest.raises(service.MarketFlowRepositoryMergeStrategyApprovalError):
        service.write_marketflow_repository_merge_strategy_approval_v1(
            tmp_path, operator_attestation=attestation
        )


def test_markdown_has_required_sections(approval):
    markdown = service.build_marketflow_repository_merge_strategy_approval_markdown_v1(approval)
    for title in (
        "Title", "MarketFlow Repository Merge Strategy Approval v1", "Operator Attestation",
        "Source Merge Strategy Operator Review", "Bound Evidence", "Repository Context",
        "Approval Scope", "Selected Merge Strategy Package", "Approved Integration Branch Plan",
        "Supporting Packages", "Future Execution Boundary", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {title}" in markdown
