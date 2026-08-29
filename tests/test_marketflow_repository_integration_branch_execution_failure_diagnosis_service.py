from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_execution_failure_diagnosis_service as service,
)


@pytest.fixture
def diagnosis():
    return service.build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1()


def test_diagnosis_builds_offline_and_deterministically(diagnosis):
    assert service.build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1() == diagnosis
    assert diagnosis["created_offline"] is True
    assert diagnosis["governance_only"] is True
    assert diagnosis["failure_diagnosis_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1),
        ("diagnosis_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY),
        ("diagnosis_scope", service.REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW),
        ("source_merge_strategy_approval_artifact_kind", service.SOURCE_APPROVAL_ARTIFACT_KIND),
        ("source_merge_strategy_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("attempted_execution_artifact_kind", service.ATTEMPTED_EXECUTION_ARTIFACT_KIND),
        ("attempted_execution_blocked_status", service.ATTEMPTED_EXECUTION_BLOCKED_STATUS),
        ("attempted_execution_branch", service.ATTEMPTED_EXECUTION_BRANCH),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit", service.INTEGRATION_HEAD_COMMIT),
        ("integration_merge_method", service.INTEGRATION_MERGE_METHOD),
        ("integration_base_commit", service.INTEGRATION_BASE_COMMIT),
        ("integration_source_commit", service.INTEGRATION_SOURCE_COMMIT),
        ("origin_main_commit_before_execution", service.INTEGRATION_BASE_COMMIT),
        ("origin_main_commit_after_execution", service.INTEGRATION_BASE_COMMIT),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("first_integration_pytest_skipped_count", 7),
        ("later_isolated_rerun_passed", True),
        ("later_isolated_rerun_passed_count", 26842),
        ("later_isolated_rerun_skipped_count", 7),
        ("later_isolated_rerun_overrides_first_failure", False),
        ("later_isolated_rerun_label_validated", False),
        ("representative_failure_domain", service.REPRESENTATIVE_FAILURE_DOMAIN),
        ("representative_actual_digest_prefix", "783e0013"),
        ("representative_required_digest_prefix", "57c0a06e"),
        ("integration_execution_successful", False),
        ("successful_execution_digest_generated", False),
        ("successful_validation_digest_generated", False),
        ("integration_results_review_ready", False),
        ("integration_results_review_created", False),
        ("repository_integration_branch_created", True),
        ("integration_branch_created", True),
        ("integration_merge_performed", True),
        ("integration_pytest_performed", True),
        ("integration_pytest_passed", False),
        ("integration_validation_completed", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_merge_performed", False),
        ("main_push_performed", False),
        ("git_main_push_performed", False),
        ("git_rebase_performed", False),
        ("git_squash_merge_performed", False),
        ("git_cherry_pick_performed", False),
        ("git_branch_delete_performed", False),
        ("git_remote_delete_performed", False),
        ("git_force_push_performed", False),
        ("git_remote_prune_performed", False),
        ("repository_cleanup_candidate_created", False),
        ("repository_cleanup_executed", False),
        ("repository_tags_pushed_again", False),
        ("additional_tag_push_performed", False),
        ("additional_tags_created", False),
        ("tags_modified", False),
        ("tags_deleted", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("provider_requests_made_in_diagnosis", False),
        ("market_data_acquisition_performed_in_diagnosis", False),
        ("dataset_generation_performed_in_diagnosis", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
        ("recommended_next_task_status", service.RECOMMENDED_NEXT_TASK_STATUS),
        ("recommended_action", service.RECOMMENDED_ACTION),
        ("integration_results_review_blocked", True),
        ("integration_retry_allowed_now", False),
        ("integration_retry_requires_remediation_approval", True),
    ],
)
def test_required_diagnosis_fields(diagnosis, field, expected):
    assert diagnosis[field] == expected


def test_diagnosis_domains_and_confirmed_root_cause_are_present(diagnosis):
    assert diagnosis["diagnosis_domains"] == service.DIAGNOSIS_DOMAINS
    assert len(diagnosis["diagnosis_domains"]) >= 10
    assert {row["domain"] for row in diagnosis["diagnosis_domains"]} >= {
        "FAILURE_GATE_STATUS", "DIGEST_MISMATCH_DOMAIN", "STATE_ORDER_DEPENDENCE",
        "PYTEST_ISOLATION", "EVIDENCE_ROOT_DEPENDENCY", "RERUN_CWD_TRACE",
    }
    findings = {row["finding_id"]: row for row in diagnosis["confirmed_root_cause_findings"]}
    assert findings["ACTUAL_DIGEST_TRACE"]["status"] == "CONFIRMED"
    assert "acquisition_provider_evidence_run_manifest.json" in findings["ACTUAL_DIGEST_TRACE"]["finding"]
    assert findings["LATER_RERUN_CWD"]["status"] == "CONFIRMED"


def test_root_cause_questions_are_preserved(diagnosis):
    assert diagnosis["root_cause_questions"] == service.ROOT_CAUSE_QUESTIONS
    assert len(diagnosis["root_cause_questions"]) == 10


def test_recommendation_chain_gates_and_risk_controls(diagnosis):
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert diagnosis["next_chain"] == service.NEXT_CHAIN
    assert diagnosis["next_gates"] == service.NEXT_GATES
    assert diagnosis["risk_controls"] == service.RISK_CONTROLS
    assert "diagnosis_does_not_retry_integration" in diagnosis["risk_controls"]
    assert "preserve_meta_limitation" in diagnosis["risk_controls"]


def test_checklist_and_summary_pass(diagnosis):
    assert [row["check_id"] for row in diagnosis["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in diagnosis["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in diagnosis["checklist"])
    assert diagnosis["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 60
    assert diagnosis["summary"]["passed_checks"] == 60
    assert diagnosis["summary"]["failed_checks"] == 0
    assert diagnosis["summary"]["blocker_count"] == 0
    assert diagnosis["summary"]["integration_execution_successful"] is False
    assert diagnosis["summary"]["integration_results_review_ready"] is False


def test_diagnosis_digest_is_deterministic(diagnosis):
    assert diagnosis["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"] == service.marketflow_repository_integration_branch_execution_failure_diagnosis_digest_v1(diagnosis)


def test_validator_accepts_valid_diagnosis(diagnosis):
    result = service.validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(diagnosis)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("diagnosis_status", "WRONG"),
        ("diagnosis_scope", "WRONG"),
        ("source_merge_strategy_approval_digest", "0" * 64),
        ("attempted_execution_commit", ""),
        ("integration_branch_name", ""),
        ("integration_branch_head_commit", ""),
        ("origin_main_commit_after_execution", "0" * 40),
        ("first_integration_pytest_authoritative", False),
        ("later_isolated_rerun_overrides_first_failure", True),
        ("integration_execution_successful", True),
        ("successful_execution_digest_generated", True),
        ("successful_validation_digest_generated", True),
        ("integration_results_review_ready", True),
        ("integration_results_review_created", True),
        ("integration_pytest_passed", True),
        ("integration_validation_completed", True),
        ("integration_branch_pushed", True),
        ("remote_integration_branch_created", True),
        ("main_merge_performed", True),
        ("main_push_performed", True),
        ("git_rebase_performed", True),
        ("git_squash_merge_performed", True),
        ("git_cherry_pick_performed", True),
        ("git_branch_delete_performed", True),
        ("git_remote_delete_performed", True),
        ("git_force_push_performed", True),
        ("git_remote_prune_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("tags_modified", True),
        ("repository_cleanup_candidate_created", True),
        ("provider_requests_made_in_diagnosis", True),
        ("market_data_acquisition_performed_in_diagnosis", True),
        ("dataset_generation_performed_in_diagnosis", True),
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
def test_validator_rejects_invalid_boundaries(diagnosis, field, bad_value):
    invalid = deepcopy(diagnosis)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(invalid)


@pytest.mark.parametrize("field", ["diagnosis_domains", "root_cause_questions", "risk_controls"])
def test_validator_rejects_missing_governance_sections(diagnosis, field):
    invalid = deepcopy(diagnosis)
    invalid.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(invalid)


def test_validator_rejects_missing_digest(diagnosis):
    diagnosis.pop("marketflow_repository_integration_branch_execution_failure_diagnosis_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(diagnosis)


def test_invalid_failure_snapshot_fails_closed():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(
            failure_snapshot={"integration_branch_head_commit": "0" * 40}
        )


def test_markdown_includes_required_sections(diagnosis):
    markdown = service.build_marketflow_repository_integration_branch_execution_failure_diagnosis_markdown_v1(diagnosis)
    for title in (
        "MarketFlow Repository Integration Branch Execution Failure Diagnosis v1",
        "Source Merge Strategy Approval", "Attempted Execution State",
        "Integration Branch State", "Authoritative Pytest Failure",
        "Later Diagnostic Rerun", "Representative Failure", "Diagnosis Domains",
        "Root-Cause Questions", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown
    assert "not integration acceptance evidence" in markdown


def test_writer_round_trips_without_overwrite(tmp_path, diagnosis):
    receipt = service.write_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(tmp_path)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_execution_failure_diagnosis_v1.json").read_text(encoding="utf-8"))
    assert payload == diagnosis
    assert receipt["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"] == diagnosis["marketflow_repository_integration_branch_execution_failure_diagnosis_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchExecutionFailureDiagnosisError):
        service.write_marketflow_repository_integration_branch_execution_failure_diagnosis_v1(tmp_path)
