from copy import deepcopy
import json
import pytest
from marketflow import services
from marketflow.services import marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_service as service

def _attestation(**overrides):
    values={
        "operator_reference":"TEST_OPERATOR","operator_attestation_timestamp_utc":"2026-09-01T00:00:00Z",
        "operator_attestation_phrase":service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest":service.SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_after_v2_candidate_digest":service.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
        "operator_confirms_source_results_review_v2_digest":service.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        "operator_confirms_source_review_manifest_digest":service.source.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST,
        "operator_confirms_source_execution_v2_digest":service.source.source.source.SOURCE_EXECUTION_V2_DIGEST,
        "operator_confirms_source_module_grouping_digest":service.source.source.source.SOURCE_MODULE_GROUPING_DIGEST,
        "operator_confirms_retry_execution_commit":"ab178b65c69f0274b0abbf9c20df102d35e78d34",
        "operator_confirms_selected_after_v2_package":service.SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE,
    }
    values.update({k:True for k in service.ATTESTATION_BOOLEAN_FIELDS}); values.update(overrides)
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_attestation_v1(**values)

@pytest.fixture(scope="module")
def approval(): return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(operator_attestation=_attestation())

def test_attestation_builder_creates_required_fields():
    a=_attestation(); assert a["operator_reference"]=="TEST_OPERATOR"; assert a["operator_decision"]==service.OPERATOR_DECISION; assert all(a[k] is True for k in service.ATTESTATION_BOOLEAN_FIELDS)

def test_approval_builds_offline(approval): assert approval["created_offline"] is True and approval["governance_only"] is True

@pytest.mark.parametrize("field,expected",[
    ("artifact_kind",service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW_V1),
    ("approval_status",service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVED_AFTER_CLASSIFICATION_V2_REVIEW),
    ("approval_scope",service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN),
    ("selected_remediation_or_method_after_v2_package",service.SELECTED_REMEDIATION_OR_METHOD_AFTER_V2_PACKAGE),
    ("source_after_v2_operator_review_digest",service.SOURCE_OPERATOR_REVIEW_DIGEST),
    ("source_after_v2_candidate_digest",service.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST),
    ("source_results_review_v2_digest",service.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
    ("source_review_manifest_digest",service.source.source.SOURCE_RESULTS_REVIEW_V2_MANIFEST_DIGEST),
    ("source_execution_v2_digest",service.source.source.source.SOURCE_EXECUTION_V2_DIGEST),
    ("source_module_grouping_digest",service.source.source.source.SOURCE_MODULE_GROUPING_DIGEST),
    ("retry_execution_commit","ab178b65c69f0274b0abbf9c20df102d35e78d34"),
    ("module_level_grouping_reviewed",True),("module_summary_module_count",29),("largest_module_nodeid_counts",[136,131,122,112,111]),
    ("remediation_or_method_after_v2_selected",True),("remediation_or_method_after_v2_approved",True),("remediation_or_method_after_v2_authorized",True),("remediation_or_method_after_v2_approval_created",True),("ready_for_remediation_or_method_after_v2_execution",True),
    ("remediation_or_method_after_v2_executed",False),("diagnostic_method_after_v2_executed",False),("code_remediation_after_v2_executed",False),("evidence_remediation_after_v2_executed",False),
    ("new_retry_candidate_created",False),("new_retry_executed",False),("new_retry_results_review_created",False),("main_merge_approval_created",False),("retry_rerun_performed",False),("full_pytest_performed",False),("diagnostic_command_executed",False),("diagnostic_output_captured",False),("integration_execution_successful",False),("successful_integration_execution_digest_generated",False),("integration_branch_pushed",False),("main_push_performed",False),("origin_main_modified_by_this_task",False),("marketflow_outputs_committed",False),("pytest_cache_committed",False),("evidence_regenerated",False),("provider_requests_made_in_approval",False),("market_data_acquisition_performed_in_approval",False),("dataset_generation_performed_in_approval",False),("metric_recomputation_from_raw_rows_performed",False),("model_training_performed",False),("strategy_scoring_performed",False),("trade_recommendations_generated",False),("predictive_usefulness","not accepted"),("profitability","not accepted"),("runtime_use","NOT_AUTHORIZED"),("broker_execution","NOT_AUTHORIZED"),
])
def test_required_bindings_and_boundaries(approval,field,expected): assert approval[field]==expected

def test_counts_claims_and_attestation(approval):
    assert [approval[f"retry_pytest_{n}_count"] for n in ("passed","failed","error","skipped")]==[24877,1292,112,7]
    assert approval["unsupported_claims_boundary"]==service.source._unsupported_claims_boundary()
    assert approval["operator_attestation"]["operator_attestation_phrase"]==service.REQUIRED_OPERATOR_ATTESTATION_PHRASE

def test_approved_material(approval):
    assert len(approval["approved_future_requirements"])==13 and all(r["approval_status"]==service.APPROVED_ONLY for r in approval["approved_future_requirements"])
    assert len(approval["approved_future_plan"])==7 and all(r["execution_status"]=="NOT_EXECUTED" for r in approval["approved_future_plan"])
    assert len(approval["authorized_planned_outputs"])==11 and all(r["authorization_status"]=="AUTHORIZED_NOT_GENERATED" for r in approval["authorized_planned_outputs"])
    assert len(approval["supporting_packages"])==5 and all(not r["selected"] for r in approval["supporting_packages"])
    assert len(approval["blocked_packages"])==3 and all(not r["approved"] for r in approval["blocked_packages"])

def test_chain_risks_checklist_digest(approval):
    assert len(approval["next_chain"])==7 and len(approval["next_gates"])==7 and len(approval["risk_controls"])==49
    assert approval["summary"]["passed_checks"]==approval["summary"]["total_checks"]==62 and approval["summary"]["failed_checks"]==0
    rebuilt=service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(operator_attestation=_attestation()); assert rebuilt==approval

def test_validator_accepts(approval): assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(approval)["failed_checks"]==0

_DELETE=object()
@pytest.mark.parametrize("field,value",[
    ("artifact_kind","WRONG"),("approval_status","WRONG"),("approval_scope","WRONG"),("selected_remediation_or_method_after_v2_package","WRONG"),
    ("source_after_v2_operator_review_digest","0"*64),("source_after_v2_candidate_digest","0"*64),("source_results_review_v2_digest","0"*64),("source_module_grouping_digest","0"*64),
    ("retry_pytest_failed_count",_DELETE),("module_level_grouping_reviewed",_DELETE),("module_summary_module_count",28),("largest_module_nodeid_counts",[136]),("unsupported_claims_boundary",_DELETE),
    ("remediation_or_method_after_v2_approval_created",False),("remediation_or_method_after_v2_selected",False),("remediation_or_method_after_v2_approved",False),("remediation_or_method_after_v2_authorized",False),("ready_for_remediation_or_method_after_v2_execution",False),
    ("remediation_or_method_after_v2_executed",True),("diagnostic_method_after_v2_executed",True),("code_remediation_after_v2_executed",True),("evidence_remediation_after_v2_executed",True),("new_retry_candidate_created",True),("new_retry_executed",True),("new_retry_results_review_created",True),("main_merge_approval_created",True),("retry_rerun_performed",True),("full_pytest_performed",True),("diagnostic_command_executed",True),("integration_execution_successful",True),("successful_integration_execution_digest_generated",True),("integration_branch_pushed",True),("main_push_performed",True),("origin_main_modified_by_this_task",True),("marketflow_outputs_committed",True),("pytest_cache_committed",True),("evidence_regenerated",True),("provider_requests_made_in_approval",True),("market_data_acquisition_performed_in_approval",True),("dataset_generation_performed_in_approval",True),("metric_recomputation_from_raw_rows_performed",True),("model_training_performed",True),("strategy_scoring_performed",True),("trade_recommendations_generated",True),("predictive_usefulness","accepted"),("profitability","accepted"),("runtime_use","AUTHORIZED"),("broker_execution","AUTHORIZED"),("risk_controls",_DELETE),("marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest",_DELETE),
])
def test_validator_rejects_changed_missing_or_authorizing_values(approval,field,value):
    x=deepcopy(approval); x.pop(field,None) if value is _DELETE else x.__setitem__(field,value)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError): service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(x)

@pytest.mark.parametrize("field,value",[("operator_decision","WRONG"),("operator_attestation_phrase","WRONG")])
def test_validator_rejects_bad_attestation(approval,field,value):
    x=deepcopy(approval); x["operator_attestation"][field]=value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterClassificationV2ReviewError): service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(x)

def test_markdown_writer_and_exports(tmp_path,approval):
    md=service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_markdown_v1(approval)
    for h in ("Operator Attestation","Source Operator Review","Selected Package","Approved Future Requirements","Approved Future Plan","Planned Outputs","Supporting Packages","Blocked Packages","Risk Controls","Guardrails"): assert h in md
    result=service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(tmp_path,operator_attestation=_attestation()); assert json.loads(open(result["path"],encoding="utf-8").read())==approval
    assert services.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1 is service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1
