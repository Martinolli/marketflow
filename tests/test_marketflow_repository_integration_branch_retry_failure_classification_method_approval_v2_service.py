from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_service as service,
)


def _attestation(**overrides):
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-31T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_v2_digest": service.source.SOURCE_CANDIDATE_V2_DIGEST,
        "operator_confirms_source_reentry_digest": service.source.source.SOURCE_REENTRY_DIGEST,
        "operator_confirms_source_results_review_digest": service.source.source.SOURCE_RESULTS_REVIEW_DIGEST,
        "operator_confirms_source_cache_manifest_digest": service.source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST,
        "operator_confirms_retry_execution_commit": "ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_v2_package": service.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_BOOLEAN_FIELDS})
    values.update(overrides)
    return service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_attestation(
        **values
    )


@pytest.fixture
def approval():
    return service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["selected_classification_method_v2_package"] == service.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


@pytest.mark.parametrize(
    "override",
    [
        {"operator_reference": ""},
        {"operator_attestation_timestamp_utc": "2026-08-31"},
        {"operator_attestation_phrase": "wrong"},
        {"operator_confirms_source_operator_review_digest": "0" * 64},
        {"operator_confirms_source_candidate_v2_digest": "0" * 64},
        {"operator_confirms_source_reentry_digest": "0" * 64},
        {"operator_confirms_source_results_review_digest": "0" * 64},
        {"operator_confirms_source_cache_manifest_digest": "0" * 64},
        {"operator_confirms_retry_execution_commit": "0" * 40},
        {"operator_confirms_selected_v2_package": "wrong"},
        {"operator_confirms_retry_failure_counts": False},
        {"operator_confirms_cache_counts": False},
        {"operator_confirms_module_summary": False},
        {"operator_confirms_classification_source_limitations": False},
        {"operator_confirms_approval_scope_only": False},
        {"operator_confirms_no_v2_execution": False},
        {"operator_confirms_no_classification_execution": False},
        {"operator_confirms_no_cache_read": False},
        {"operator_confirms_no_retry": False},
        {"operator_confirms_no_full_pytest": False},
        {"operator_confirms_runtime_not_authorized": False},
        {"operator_confirms_broker_not_authorized": False},
    ],
)
def test_attestation_builder_rejects_missing_or_incorrect_confirmation(override):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error):
        _attestation(**override)


def test_approval_builds_offline(approval):
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["operator_attestation_required"] is True


@pytest.mark.parametrize(
    "field,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2),
        ("approval_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2),
        ("approval_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("selected_classification_method_v2_package", service.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE),
        ("source_classification_method_candidate_v2_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_classification_method_candidate_v2_digest", service.source.SOURCE_CANDIDATE_V2_DIGEST),
        ("source_classification_method_reentry_digest", service.source.source.SOURCE_REENTRY_DIGEST),
        ("source_classification_source_results_review_digest", service.source.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_cache_manifest_review_digest", service.source.source.SOURCE_CACHE_MANIFEST_REVIEW_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
    ],
)
def test_identity_and_source_bindings(approval, field, expected):
    assert approval[field] == expected


def test_retry_failure_counts_bound(approval):
    assert [approval[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert approval["retry_pytest_first_result_authoritative"] is True
    assert approval["root_full_regression_is_retry_evidence"] is False


def test_cache_counts_and_module_summary_bound(approval):
    assert [approval["lastfailed_cache_entry_count"], approval["nodeids_cache_entry_count"]] == [1404, 26288]
    assert approval["module_summary_module_count"] == 29
    assert approval["largest_module_nodeid_counts"] == [136, 131, 122, 112, 111]


def test_classification_source_limitations_bound(approval):
    assert approval["classification_source_valid_for_v2_candidate"] is True
    assert approval["classification_source_type"] == "DETACHED_PYTEST_CACHE_LASTFAILED"
    assert approval["classification_source_accepted_for_module_level_only"] is True
    for field in (
        "classification_source_not_accepted_for_failure_error_separation",
        "classification_source_not_accepted_for_first_order_failure_analysis",
        "classification_source_not_accepted_for_traceback_root_cause",
        "classification_source_not_retry_success_evidence",
    ):
        assert approval[field] is True


def test_operator_decision_and_phrase_match(approval):
    assert approval["operator_attestation"]["operator_decision"] == service.OPERATOR_DECISION
    assert approval["operator_attestation"]["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE


@pytest.mark.parametrize(
    "field,expected",
    [
        ("classification_method_v2_approval_created", True),
        ("classification_method_v2_selected", True),
        ("classification_method_v2_approved", True),
        ("classification_method_v2_authorized", True),
        ("ready_for_classification_method_v2_execution", True),
        ("classification_method_v2_executed", False),
        ("classification_execution_created", False),
        ("classification_execution_performed", False),
        ("failure_modules_classified", False),
        ("error_modules_classified", False),
        ("first_failure_identified", False),
        ("first_error_identified", False),
        ("failure_error_separation_claimed", False),
        ("traceback_root_cause_claimed", False),
        ("new_retry_candidate_created", False),
        ("new_retry_executed", False),
        ("new_retry_results_review_created", False),
        ("main_merge_approval_created", False),
        ("retry_rerun_performed", False),
        ("full_pytest_performed", False),
        ("diagnostic_command_executed", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("pytest_cache_committed", False),
        ("evidence_regenerated", False),
        ("provider_requests_made_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_approval_authority_and_closed_boundaries(approval, field, expected):
    assert approval[field] == expected


def test_selected_package_is_future_execution_only(approval):
    assert approval["selected_v2_package"] == {
        "package_id": service.SELECTED_CLASSIFICATION_METHOD_V2_PACKAGE,
        "approval_status": service.APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY,
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
    }


def test_requirements_approved(approval):
    rows = approval["approved_future_v2_requirements"]
    assert len(rows) == 16
    assert all(row["requirement_value"] is True for row in rows)
    assert all(row["approval_status"] == service.APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY for row in rows)


def test_future_plan_approved_not_executed(approval):
    rows = approval["approved_future_v2_execution_plan"]
    assert len(rows) == 10
    assert approval["future_v2_plan_approval_status"] == service.APPROVED_FOR_FUTURE_CLASSIFICATION_METHOD_V2_EXECUTION_ONLY
    assert approval["future_v2_plan_execution_status"] == "NOT_EXECUTED"
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_planned_outputs_authorized_not_generated(approval):
    assert len(approval["planned_outputs"]) == 9
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for row in approval["planned_outputs"])


def test_supporting_and_blocked_packages(approval):
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert all(row["approval_status"].startswith("AVAILABLE_NOT_SELECTED") for row in approval["supporting_packages"])
    assert all(row["approval_status"] == "BLOCKED_NOT_APPROVED" for row in approval["blocked_packages"])


def test_next_chain_gates_and_risk_controls_defined(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert len(approval["next_chain"]) == 7
    assert len(approval["next_gates"]) == 7
    assert len(approval["risk_controls"]) == 49


def test_checklist_passes(approval):
    assert len(approval["checklist"]) == 65
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert all(row["status"] == "PASS" for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == 65
    assert approval["summary"]["passed_checks"] == 65
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_deterministic():
    first = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(operator_attestation=_attestation())
    second = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(operator_attestation=_attestation())
    field = "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest"
    assert first[field] == second[field]


def test_validator_accepts_valid_approval(approval):
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(approval)
    assert validation["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2
    assert validation["passed_checks"] == 65


def _set_field(field, value):
    return lambda record: record.__setitem__(field, value)


def _set_attestation(field, value):
    return lambda record: record["operator_attestation"].__setitem__(field, value)


def _delete_field(field):
    return lambda record: record.pop(field, None)


VALIDATOR_MUTATIONS = [
    ("wrong_artifact", _set_field("artifact_kind", "wrong")),
    ("wrong_status", _set_field("approval_status", "wrong")),
    ("wrong_scope", _set_field("approval_scope", "wrong")),
    ("wrong_package", _set_field("selected_classification_method_v2_package", "wrong")),
    ("source_review_digest", _set_field("source_classification_method_candidate_v2_operator_review_digest", "0" * 64)),
    ("source_candidate_digest", _set_field("source_classification_method_candidate_v2_digest", "0" * 64)),
    ("source_reentry_digest", _set_field("source_classification_method_reentry_digest", "0" * 64)),
    ("source_results_digest", _set_field("source_classification_source_results_review_digest", "0" * 64)),
    ("source_cache_digest", _set_field("source_cache_manifest_review_digest", "0" * 64)),
    ("operator_decision", _set_attestation("operator_decision", "wrong")),
    ("attestation_phrase", _set_attestation("operator_attestation_phrase", "wrong")),
    ("retry_counts", _delete_field("retry_pytest_failed_count")),
    ("cache_counts", _delete_field("lastfailed_cache_entry_count")),
    ("module_summary", _delete_field("module_summary_module_count")),
    ("limitations", _set_field("classification_source_not_accepted_for_failure_error_separation", False)),
    ("selected_false", _set_field("classification_method_v2_selected", False)),
    ("approved_false", _set_field("classification_method_v2_approved", False)),
    ("authorized_false", _set_field("classification_method_v2_authorized", False)),
    ("ready_false", _set_field("ready_for_classification_method_v2_execution", False)),
    ("method_executed", _set_field("classification_method_v2_executed", True)),
    ("classification_execution", _set_field("classification_execution_performed", True)),
    ("failure_modules", _set_field("failure_modules_classified", True)),
    ("error_modules", _set_field("error_modules_classified", True)),
    ("first_failure", _set_field("first_failure_identified", True)),
    ("first_error", _set_field("first_error_identified", True)),
    ("failure_error_separation", _set_field("failure_error_separation_claimed", True)),
    ("traceback", _set_field("traceback_root_cause_claimed", True)),
    ("new_retry_candidate", _set_field("new_retry_candidate_created", True)),
    ("new_retry_executed", _set_field("new_retry_executed", True)),
    ("retry_review", _set_field("new_retry_results_review_created", True)),
    ("main_approval", _set_field("main_merge_approval_created", True)),
    ("retry_rerun", _set_field("retry_rerun_performed", True)),
    ("full_pytest", _set_field("full_pytest_performed", True)),
    ("diagnostic", _set_field("diagnostic_command_executed", True)),
    ("integration_success", _set_field("integration_execution_successful", True)),
    ("success_digest", _set_field("successful_integration_execution_digest_generated", True)),
    ("integration_push", _set_field("integration_branch_pushed", True)),
    ("main_push", _set_field("main_push_performed", True)),
    ("origin_main", _set_field("origin_main_modified_by_this_task", True)),
    ("marketflow_commit", _set_field("marketflow_outputs_committed", True)),
    ("pytest_cache_commit", _set_field("pytest_cache_committed", True)),
    ("provider", _set_field("provider_requests_made_in_approval", True)),
    ("predictive", _set_field("predictive_usefulness", "accepted")),
    ("runtime", _set_field("runtime_use", "AUTHORIZED")),
    ("risk_controls", _set_field("risk_controls", [])),
    ("missing_digest", _delete_field("marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_digest")),
]


@pytest.mark.parametrize("name,mutate", VALIDATOR_MUTATIONS, ids=[row[0] for row in VALIDATOR_MUTATIONS])
def test_validator_rejects_invalid_approval(approval, name, mutate):
    invalid = deepcopy(approval)
    mutate(invalid)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error):
        service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(invalid)


def test_markdown_includes_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_markdown_v1(approval)
    for title in (
        "MarketFlow Repository Integration Branch Retry Failure Classification Method Approval v2",
        "Operator Attestation", "Source Operator Review", "Source Candidate v2",
        "Source Classification-Source Review", "Retry Failure Context", "Approval Scope",
        "Selected v2 Package", "Approved Future v2 Requirements",
        "Approved Future v2 Execution Plan", "Planned Outputs", "Supporting Packages",
        "Blocked Packages", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ):
        assert title in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path):
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
        tmp_path, operator_attestation=_attestation()
    )
    path = tmp_path / "marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["path"] == str(path)
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVED_V2
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureClassificationMethodApprovalV2Error):
        service.write_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2(
            tmp_path, operator_attestation=_attestation()
        )


def test_services_exports_approval_v2_surface():
    assert services.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_attestation is service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_attestation
    assert services.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2 is service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2
    assert services.validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2 is service.validate_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2
    assert services.write_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2 is service.write_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2
    assert services.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_markdown_v1 is service.build_marketflow_repository_integration_branch_retry_failure_classification_method_approval_v2_markdown_v1
