from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_service
    as service,
)


@pytest.fixture
def execution():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def _assert_rejected(execution):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(execution)


def _blocked(field, value):
    source = service._committed_source_approval()
    source[field] = value
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
        source_approval=source, run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def test_success_artifact_builds_offline(execution):
    assert execution["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert execution["execution_status"] == service.SUCCESS_STATUS
    assert execution["execution_scope"] == service.EXECUTION_SCOPE
    assert execution["created_offline"] is True
    assert execution["governance_only"] is True


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"), ("approval_status", "WRONG"), ("approval_scope", "WRONG"),
        (service.source.APPROVAL_DIGEST_KEY, "0" * 64),
        ("selected_source_authority_or_no_change_disposition_package", "WRONG"),
        ("source_authority_or_no_change_disposition_package_authorized", False),
        ("source_authority_enrichment_performed", True),
    ],
)
def test_invalid_source_approval_builds_fail_closed(field, value):
    blocked = _blocked(field, value)
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert blocked["execution_scope"] == service.EXECUTION_SCOPE
    assert blocked["source_authority_or_no_change_disposition_execution_performed"] is False
    assert blocked["source_authority_enrichment_plan_created"] is False
    assert blocked["outputs_generated"] == []
    assert blocked["blocked_reason"]
    assert len(blocked[service.BLOCKED_MANIFEST_DIGEST_KEY]) == 64
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK


def test_non_mapping_source_approval_blocks():
    blocked = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
        source_approval=[], run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert blocked["blocked_reason"] == "SOURCE_APPROVAL_NOT_AN_OBJECT"


def test_invalid_timestamp_rejected():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(run_timestamp_utc="not-a-date")


def test_selected_package_and_source_approval_bound(execution):
    assert execution["selected_source_authority_or_no_change_disposition_package"] == service.SELECTED_PACKAGE
    assert execution["source_approval_commit"] == service.SOURCE_APPROVAL_COMMIT
    assert execution["source_approval_digest"] == service.SOURCE_APPROVAL_DIGEST


@pytest.mark.parametrize("field,expected", service.SOURCE_BINDINGS.items())
def test_all_source_bindings_preserved(execution, field, expected):
    assert execution[field] == expected


def test_source_failure_and_historical_approval_preserved(execution):
    assert execution["source_blocked_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert execution["primary_failure_class"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert len(execution["secondary_failure_classes"]) == 4
    assert execution["historical_selected_remediation_execution_package"] == "PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY"


def test_retry_context_and_priority_modules_preserved(execution):
    assert execution["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert execution["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert execution["retry_failure_context"]["first_result_authoritative"] is True
    assert execution["priority_1_total_nodeids"] == 612
    assert execution["top_10_count_sum"] == 1069
    assert execution["module_summary_module_count"] == 29
    assert execution["failed_or_errored_nodeids_count"] == 1404
    assert [row["failed_or_errored_nodeid_count"] for row in execution["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_priority_1_validation_is_bound_as_non_retry_evidence(execution):
    summary = execution["priority1_validation_summary"]
    assert summary["pre_change_passed_count"] == 675
    assert summary["post_change_passed_count"] == 675
    assert summary["post_change_duration_seconds"] == "41.88"
    assert summary["not_retry_evidence"] is True
    assert summary["post_change_stdout_sha256"] == "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374"


def test_diagnostic_metadata_bound_without_analysis(execution):
    evidence = execution["diagnostic_capture_evidence_summary"]
    assert evidence["exit_code"] == 1
    assert evidence["duration_seconds"] == "21.584361"
    assert evidence["stdout_byte_count"] == 1231380
    assert evidence["stderr_byte_count"] == 0
    assert evidence["stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert evidence["diagnostic_only"] is True
    assert execution["diagnostic_output_analyzed_in_execution"] is False


def test_four_families_and_workstreams_preserved(execution):
    assert [row["family_id"] for row in execution["reviewed_observable_failure_families"]] == [row[1] for row in service.WORKSTREAM_SOURCES]
    assert all(row["observable_evidence_count"] == 47 and row["confidence"] == "HIGH" for row in execution["reviewed_observable_failure_families"])
    assert [row["workstream_id"] for row in execution["reviewed_workstreams"]] == [row[0] for row in service.WORKSTREAM_SOURCES]
    assert execution["observable_failure_family_count"] == 4
    assert execution["total_observable_evidence_items"] == 188
    assert execution["source_workstream_count"] == 4


@pytest.mark.parametrize("workstream", service.WORKSTREAM_REQUIREMENTS)
def test_missing_authority_inventory_has_required_workstream_content(execution, workstream):
    item = next(row for row in execution["missing_authority_inventory"] if row["workstream_id"] == workstream)
    assert item["missing_authority_items"] == list(service.WORKSTREAM_REQUIREMENTS[workstream])
    assert item["authority_status"] == "MISSING_NOT_ACQUIRED"
    assert item["direct_change_authorized"] is False


def test_workstream_authority_mapping_created_without_authority_acquisition(execution):
    assert len(execution["workstream_to_missing_authority_mapping"]) == 4
    assert all(row["mapping_status"] == "PLANNED_NOT_EXECUTED" for row in execution["workstream_to_missing_authority_mapping"])
    assert all(row["source_authority_acquired"] is False for row in execution["workstream_to_missing_authority_mapping"])


def test_required_planning_outputs_created(execution):
    assert execution["source_authority_enrichment_plan"]["planning_only"] is True
    assert execution["source_authority_enrichment_plan"]["source_authority_acquisition_performed"] is False
    assert len(execution["source_evidence_requirements"]) == 4
    assert execution["canonical_serialization_authority_requirements"] == list(service.WORKSTREAM_REQUIREMENTS["digest_hash_boundary_workstream"])
    assert execution["schema_field_contract_authority_requirements"] == list(service.WORKSTREAM_REQUIREMENTS["schema_field_contract_workstream"])
    assert execution["fixture_isolation_authority_requirements"] == list(service.WORKSTREAM_REQUIREMENTS["fixture_isolation_determinism_workstream"])
    assert execution["no_change_disposition_input_requirements"] == list(service.NO_CHANGE_REQUIREMENTS)
    assert execution["alternate_diagnostic_input_requirements"] == list(service.ALTERNATE_DIAGNOSTIC_REQUIREMENTS)
    assert execution["retry_basis_requirements"] == list(service.RETRY_BASIS_REQUIREMENTS)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_success_fact_true(execution, field):
    assert execution[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_boundary_false(execution, field):
    assert execution[field] is False


def test_runtime_and_acceptance_boundaries_closed(execution):
    assert execution["predictive_usefulness"] == service.NOT_ACCEPTED
    assert execution["profitability"] == service.NOT_ACCEPTED
    assert execution["runtime_use"] == service.NOT_AUTHORIZED
    assert execution["strategy_use"] == service.NOT_AUTHORIZED
    assert execution["paper_trading"] == service.NOT_AUTHORIZED
    assert execution["broker_execution"] == service.NOT_AUTHORIZED


def test_outputs_recommendation_chain_gates_and_risks(execution):
    assert [row["output_id"] for row in execution["outputs_generated"]] == list(service.OUTPUT_IDS)
    assert all(row["status"] == service.GENERATED_PLANNING_ONLY for row in execution["outputs_generated"])
    assert execution["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert execution["recommended_next_task_status"] == "FUTURE_RESULTS_REVIEW_NOT_CREATED"
    assert execution["next_chain"] == list(service.SUCCESS_NEXT_CHAIN)
    assert execution["next_gates"] == list(service.SUCCESS_NEXT_GATES)
    assert execution["risk_controls"] == list(service.RISK_CONTROLS)


def test_success_digests_are_deterministic(execution):
    again = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(run_timestamp_utc="2026-08-23T00:00:00Z")
    for field in (service.EXECUTION_DIGEST_KEY, service.ENRICHMENT_PLAN_DIGEST_KEY,
                  service.MISSING_AUTHORITY_INVENTORY_DIGEST_KEY, service.WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY,
                  service.MANIFEST_DIGEST_KEY):
        assert execution[field] == again[field]
        assert len(execution[field]) == 64
    assert execution[service.BLOCKED_MANIFEST_DIGEST_KEY] is None


def test_blocked_manifest_is_deterministic():
    first = _blocked("artifact_kind", "WRONG")
    second = _blocked("artifact_kind", "WRONG")
    assert first[service.BLOCKED_MANIFEST_DIGEST_KEY] == second[service.BLOCKED_MANIFEST_DIGEST_KEY]
    assert first[service.EXECUTION_DIGEST_KEY] == second[service.EXECUTION_DIGEST_KEY]


def test_success_and_blocked_checklists_pass(execution):
    blocked = _blocked("approval_status", "WRONG")
    assert execution["summary"]["total_checks"] == execution["summary"]["passed_checks"]
    assert blocked["summary"]["total_checks"] == blocked["summary"]["passed_checks"]
    assert execution["summary"]["blocker_count"] == 0
    assert blocked["summary"]["blocker_count"] == 0


@pytest.mark.parametrize("field", service.SOURCE_BINDINGS)
def test_validator_rejects_changed_source_binding(execution, field):
    changed = deepcopy(execution)
    changed[field] = "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_success_fact(execution, field):
    changed = deepcopy(execution)
    changed[field] = False
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_opened_boundary(execution, field):
    changed = deepcopy(execution)
    changed[field] = True
    _assert_rejected(changed)


@pytest.mark.parametrize(
    "field",
    ["artifact_kind", "execution_status", "execution_scope", "selected_source_authority_or_no_change_disposition_package",
     "retry_failure_context", "priority_1_target_modules", "priority_1_total_nodeids", "top_10_count_sum",
     "module_summary_module_count", "failed_or_errored_nodeids_count", "priority1_validation_summary",
     "diagnostic_capture_evidence_summary", "reviewed_observable_failure_families", "reviewed_workstreams",
     "source_authority_enrichment_plan", "missing_authority_inventory", "workstream_to_missing_authority_mapping",
     "source_evidence_requirements", "canonical_serialization_authority_requirements",
     "schema_field_contract_authority_requirements", "fixture_isolation_authority_requirements",
     "no_change_disposition_input_requirements", "alternate_diagnostic_input_requirements", "retry_basis_requirements",
     "outputs_generated", "recommended_next_task", "recommended_next_task_status", "next_chain", "next_gates",
     "risk_controls", service.ENRICHMENT_PLAN_DIGEST_KEY, service.MISSING_AUTHORITY_INVENTORY_DIGEST_KEY,
     service.WORKSTREAM_AUTHORITY_MAPPING_DIGEST_KEY, service.MANIFEST_DIGEST_KEY, service.EXECUTION_DIGEST_KEY],
)
def test_validator_rejects_changed_success_content(execution, field):
    changed = deepcopy(execution)
    changed[field] = "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_acceptance(execution, field):
    changed = deepcopy(execution)
    changed[field] = "accepted"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_validator_rejects_runtime_or_trading_authority(execution, field):
    changed = deepcopy(execution)
    changed[field] = "AUTHORIZED"
    _assert_rejected(changed)


def test_validator_accepts_success_and_blocked(execution):
    success_result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(deepcopy(execution))
    blocked_result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(_blocked("approval_scope", "WRONG"))
    assert success_result["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert blocked_result["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND


def test_validator_rejects_blocked_without_reason_or_manifest():
    for field in ("blocked_reason", service.BLOCKED_MANIFEST_DIGEST_KEY):
        blocked = _blocked("approval_scope", "WRONG")
        blocked[field] = None
        _assert_rejected(blocked)


def test_markdown_contains_required_sections(execution):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_markdown_v1(execution)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert service.SUCCESS_NEXT_TASK in markdown


def test_writer_round_trips_status_document(tmp_path: Path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_v1(
        tmp_path, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_EXECUTION_AFTER_BLOCKED_EXECUTION_STATUS.md"
    assert output.read_text(encoding="utf-8") == service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_execution_after_blocked_execution_markdown_v1(artifact)
