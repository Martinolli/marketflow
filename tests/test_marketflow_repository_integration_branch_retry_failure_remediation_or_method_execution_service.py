from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_service as service,
)


SAMPLE_PYTEST_OUTPUT = """
============================= test session starts =============================
FAILED tests/test_evidence.py::test_manifest_available - FileNotFoundError: .marketflow manifest missing
FAILED tests/test_digest.py::test_historical_digest - AssertionError: digest mismatch
FAILED tests/test_evidence.py::test_rows_available - AssertionError: evidence root absent
ERROR tests/test_fixture.py::test_isolated_workspace - fixture setup failed
================ 24877 passed, 1292 failed, 112 errors, 7 skipped ===============
"""
TIMESTAMP = "2026-08-23T00:00:00Z"


@pytest.fixture
def success():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
        retry_output_text=SAMPLE_PYTEST_OUTPUT,
        run_timestamp_utc=TIMESTAMP,
    )


@pytest.fixture
def blocked():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
        run_timestamp_utc=TIMESTAMP
    )


def test_success_classification_builds_from_provided_sample_output(success):
    assert success["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED
    assert success["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_FAILURE_DOMAINS_CLASSIFIED
    assert success["execution_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert success["classification_source_type"] == "PROVIDED_RETRY_OUTPUT_TEXT"
    assert success["classification_source_available"] is True
    assert success["failure_domain_classification_generated"] is True
    assert success["planned_outputs_generated"] is True


def test_blocked_artifact_builds_when_committed_records_have_only_aggregate_data(blocked):
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED
    assert blocked["execution_status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE
    assert blocked["execution_scope"] == service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN
    assert blocked["classification_source_type"] == "AGGREGATE_COMMITTED_STATUS_ONLY"
    assert blocked["classification_source_available"] is False
    assert blocked["classification_blocked_reason"] == service.CLASSIFICATION_BLOCKED_REASON
    assert blocked["failure_domain_classification_generated"] is False
    assert blocked["planned_outputs_generated"] is False


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_source_evidence_and_retry_boundaries_are_exact(request, fixture_name):
    execution = request.getfixturevalue(fixture_name)
    assert execution["selected_retry_failure_method_package"] == service.SELECTED_RETRY_FAILURE_METHOD_PACKAGE
    assert execution["source_method_approval_digest"] == service.SOURCE_METHOD_APPROVAL_DIGEST
    assert execution["source_method_operator_review_digest"] == "cf541e8681724e1018cf0c343daf718a3a50249e3bdf8640c54d88791427f0be"
    assert execution["source_method_candidate_digest"] == "414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6"
    assert execution["source_retry_failure_diagnosis_digest"] == "f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1"
    assert execution["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert [execution[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert execution["retry_pytest_first_result_authoritative"] is True
    assert execution["root_full_regression_is_retry_evidence"] is False


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_method_executes_with_all_downstream_authority_closed(request, fixture_name):
    execution = request.getfixturevalue(fixture_name)
    assert execution["method_executed"] is True
    assert execution["diagnostic_method_executed"] is True
    for field in (
        "retry_rerun_performed",
        "full_pytest_performed",
        "retry_results_review_created",
        "integration_results_review_created",
        "integration_execution_successful",
        "new_remediation_candidate_created",
        "new_retry_candidate_created",
        "new_retry_approved",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "evidence_regenerated",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        assert execution[field] is False
    assert execution["predictive_usefulness"] == service.NOT_ACCEPTED
    assert execution["profitability"] == service.NOT_ACCEPTED
    assert all(execution[field] == service.NOT_AUTHORIZED for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"))


def test_success_classification_contains_bounded_module_and_domain_details(success):
    summary = success["classification_summary"]
    assert summary["authoritative_total_failed_tests_count"] == 1292
    assert summary["authoritative_total_error_count"] == 112
    assert summary["classified_failure_record_count"] == 3
    assert summary["classified_error_record_count"] == 1
    assert summary["failed_modules"] == ["tests/test_digest.py", "tests/test_evidence.py"]
    assert summary["error_modules"] == ["tests/test_fixture.py"]
    assert summary["first_failing_test_by_pytest_order"] == "tests/test_evidence.py::test_manifest_available"
    assert summary["first_error_by_pytest_order"] == "tests/test_fixture.py::test_isolated_workspace"
    assert summary["top_failure_modules_by_count"][0] == {"module": "tests/test_evidence.py", "count": 2}
    assert "missing_ignored_evidence_root" in summary["root_cause_family_candidates"]
    assert "digest_constant_or_historical_artifact_drift" in summary["root_cause_family_candidates"]
    assert "test_fixture_isolation" in summary["root_cause_family_candidates"]
    assert all(
        set(domain) == {
            "domain_id",
            "module_or_test",
            "classification_family",
            "confidence",
            "evidence_excerpt_type",
            "actionability",
        }
        for domain in summary["failure_domains"]
    )


def test_success_planned_outputs_and_next_path(success):
    assert len(success["planned_outputs"]) == 11
    assert all(row["status"] == "GENERATED_SUMMARY_ONLY" for row in success["planned_outputs"])
    assert success["next_chain"] == service.SUCCESS_NEXT_CHAIN
    assert success["next_gates"] == service.SUCCESS_NEXT_GATES
    assert success["recommended_next_task"] == service.SUCCESS_RECOMMENDED_NEXT_TASK


def test_blocked_records_available_missing_data_and_next_path(blocked):
    assert blocked["available_retry_data"]["aggregate_counts"] == {
        "passed": 24877,
        "failed": 1292,
        "errors": 112,
        "skipped": 7,
    }
    assert blocked["available_retry_data"]["duration_seconds"] == "1547.848456"
    assert blocked["missing_retry_data"] == service.MISSING_RETRY_DATA
    assert blocked["classification_summary"] is None
    assert all(row["status"] == "NOT_GENERATED_OUTPUT_UNAVAILABLE" for row in blocked["planned_outputs"])
    assert blocked["next_chain"] == service.BLOCKED_NEXT_CHAIN
    assert blocked["next_gates"] == service.BLOCKED_NEXT_GATES
    assert blocked["recommended_next_task"] == service.BLOCKED_RECOMMENDED_NEXT_TASK


def test_aggregate_text_does_not_fabricate_classification():
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
        retry_output_text="24877 passed, 1292 failed, 112 errors, 7 skipped",
        run_timestamp_utc=TIMESTAMP,
    )
    assert execution["classification_source_available"] is False
    assert execution["classification_summary"] is None
    assert execution["classification_blocked_reason"] == service.CLASSIFICATION_BLOCKED_REASON


def test_provided_retry_output_path_is_parsed(tmp_path):
    path = tmp_path / "retry.log"
    path.write_text(SAMPLE_PYTEST_OUTPUT, encoding="utf-8")
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
        retry_output_path=path,
        run_timestamp_utc=TIMESTAMP,
    )
    assert execution["classification_source_available"] is True
    assert execution["classification_source_type"] == "PROVIDED_RETRY_OUTPUT_PATH"


def test_execution_rejects_conflicting_inputs_and_env_path(tmp_path):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
            retry_output_text=SAMPLE_PYTEST_OUTPUT,
            retry_output_path=tmp_path / "retry.log",
            run_timestamp_utc=TIMESTAMP,
        )
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
            retry_output_path=tmp_path / ".env" / "retry.log",
            run_timestamp_utc=TIMESTAMP,
        )


def test_risk_controls_prechecks_and_execution_steps_are_complete(success, blocked):
    assert success["risk_controls"] == blocked["risk_controls"] == service.RISK_CONTROLS
    assert len(service.RISK_CONTROLS) == 41
    assert [row["step_id"] for row in success["precheck_results"]] == service.PRECHECK_IDS
    assert [row["step_id"] for row in blocked["execution_steps"]] == service.EXECUTION_STEP_IDS
    assert all(row["status"] == service.PASS for row in success["precheck_results"] + blocked["execution_steps"])


def test_checklists_pass_for_both_dispositions(success, blocked):
    assert len(success["checklist"]) == 46
    assert len(blocked["checklist"]) == 44
    assert all(row["status"] == service.PASS for row in success["checklist"] + blocked["checklist"])
    assert success["summary"]["passed_checks"] == 46
    assert blocked["summary"]["passed_checks"] == 44
    assert success["summary"]["failed_checks"] == blocked["summary"]["failed_checks"] == 0


def test_all_digests_are_deterministic(success, blocked):
    assert success["marketflow_repository_integration_branch_retry_failure_domain_manifest_digest"] == service.marketflow_repository_integration_branch_retry_failure_domain_manifest_digest_v1(success)
    assert blocked["marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest"] == service.marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest_v1(blocked)
    assert success["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest"] == service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest_v1(success)
    assert blocked["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest"] == service.marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest_v1(blocked)
    rebuilt = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
        retry_output_text=SAMPLE_PYTEST_OUTPUT,
        run_timestamp_utc=TIMESTAMP,
    )
    assert rebuilt == success


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_validator_accepts_both_dispositions(request, fixture_name):
    execution = request.getfixturevalue(fixture_name)
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(execution)
    assert result["execution_status"] == execution["execution_status"]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "fixture_name,field,value",
    [
        ("success", "artifact_kind", "wrong"),
        ("blocked", "execution_status", "wrong"),
        ("success", "execution_scope", "wrong"),
        ("success", "selected_retry_failure_method_package", "wrong"),
        ("blocked", "source_method_approval_digest", "0" * 64),
        ("success", "retry_pytest_failed_count", None),
        ("blocked", "root_full_regression_is_retry_evidence", True),
        ("success", "method_executed", False),
        ("blocked", "diagnostic_method_executed", False),
        ("success", "retry_rerun_performed", True),
        ("blocked", "full_pytest_performed", True),
        ("success", "retry_results_review_created", True),
        ("blocked", "integration_results_review_created", True),
        ("success", "integration_execution_successful", True),
        ("blocked", "successful_integration_execution_digest_generated", True),
        ("success", "new_retry_candidate_created", True),
        ("blocked", "main_merge_approval_created", True),
        ("success", "integration_branch_pushed", True),
        ("blocked", "main_push_performed", True),
        ("success", "origin_main_modified_by_this_task", True),
        ("blocked", "marketflow_outputs_committed", True),
        ("success", "evidence_regenerated", True),
        ("blocked", "provider_requests_made_in_execution", True),
        ("success", "market_data_acquisition_performed_in_execution", True),
        ("blocked", "dataset_generation_performed_in_execution", True),
        ("success", "metric_recomputation_from_raw_rows_performed", True),
        ("blocked", "model_training_performed", True),
        ("success", "strategy_scoring_performed", True),
        ("blocked", "trade_recommendations_generated", True),
        ("success", "predictive_usefulness", "accepted"),
        ("blocked", "profitability", "accepted"),
        ("success", "runtime_use", "AUTHORIZED"),
        ("blocked", "broker_execution", "AUTHORIZED"),
        ("success", "risk_controls", []),
    ],
)
def test_validator_rejects_contract_mutation(request, fixture_name, field, value):
    invalid = deepcopy(request.getfixturevalue(fixture_name))
    invalid[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(invalid)


def test_validator_rejects_success_without_classification_or_manifest(success):
    for field, value in (
        ("classification_summary", None),
        ("marketflow_repository_integration_branch_retry_failure_domain_manifest_digest", None),
    ):
        invalid = deepcopy(success)
        invalid[field] = value
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(invalid)


def test_validator_rejects_blocked_classification_or_missing_manifest(blocked):
    invalid = deepcopy(blocked)
    invalid["failure_domain_classification_generated"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(invalid)
    invalid = deepcopy(blocked)
    invalid["marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest"] = None
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(invalid)


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_validator_rejects_missing_execution_digest(request, fixture_name):
    invalid = deepcopy(request.getfixturevalue(fixture_name))
    invalid.pop("marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(invalid)


@pytest.mark.parametrize("fixture_name", ["success", "blocked"])
def test_markdown_includes_required_sections(request, fixture_name):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_markdown_v1(
        request.getfixturevalue(fixture_name)
    )
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution v1",
        "## Source Method Approval",
        "## Retry Failure Context",
        "## Execution Scope",
        "## Input Source Search",
        "## Failure Classification or Blocked Disposition",
        "## Available and Missing Data",
        "## Authority Boundaries",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown
