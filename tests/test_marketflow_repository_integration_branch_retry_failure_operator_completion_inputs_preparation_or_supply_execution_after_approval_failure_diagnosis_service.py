from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1()


def _source_execution() -> dict:
    source = service.source
    return {
        "artifact_kind": source.BLOCKED_ARTIFACT_KIND,
        "execution_status": source.BLOCKED_STATUS,
        "execution_scope": source.EXECUTION_SCOPE,
        "blocked_reason": service.PRIMARY_FAILURE_CLASS,
        source.BLOCKED_DIGEST_KEY: service.SOURCE_BLOCKED_DIGEST,
        source.SOURCE_BINDING_DIGEST_KEY: service.SOURCE_SOURCE_BINDING_DIGEST,
        source.INPUT_ABSENCE_DIGEST_KEY: service.SOURCE_INPUT_ABSENCE_DIGEST,
        source.COVERAGE_DIGEST_KEY: service.SOURCE_COVERAGE_DIGEST,
        source.BLOCKED_MANIFEST_DIGEST_KEY: service.SOURCE_BLOCKED_MANIFEST_DIGEST,
        "prepared_operator_completion_inputs_digest": None,
        "prepared_operator_completion_inputs_manifest_digest": None,
        "success_execution_digest": None,
        "operator_completion_inputs_supplied_to_execution": False,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    }


def _reject(mutator) -> None:
    diagnosis = _build()
    mutator(diagnosis)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(diagnosis)


def test_builds_offline_with_expected_identity_and_source() -> None:
    diagnosis = _build()
    assert diagnosis["artifact_kind"] == service.ARTIFACT_KIND
    assert diagnosis["schema_version"] == service.SCHEMA_VERSION
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert diagnosis["diagnosis_scope"] == service.DIAGNOSIS_SCOPE
    assert diagnosis["source_execution_commit"] == service.SOURCE_EXECUTION_COMMIT
    assert diagnosis["source_execution_artifact_kind"] == service.source.BLOCKED_ARTIFACT_KIND
    assert diagnosis["source_execution_status"] == service.source.BLOCKED_STATUS
    assert diagnosis["source_execution_scope"] == service.source.EXECUTION_SCOPE


def test_source_execution_and_blocked_digests_are_bound() -> None:
    diagnosis = _build()
    assert diagnosis["source_blocked_reason"] == service.PRIMARY_FAILURE_CLASS
    assert diagnosis["source_blocked_digest"] == service.SOURCE_BLOCKED_DIGEST
    assert diagnosis["source_source_binding_digest"] == service.SOURCE_SOURCE_BINDING_DIGEST
    assert diagnosis["source_input_absence_digest"] == service.SOURCE_INPUT_ABSENCE_DIGEST
    assert diagnosis["source_coverage_digest"] == service.SOURCE_COVERAGE_DIGEST
    assert diagnosis["source_blocked_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST
    assert diagnosis["source_success_digests_absent"] is True
    assert diagnosis["prepared_operator_completion_inputs_digest"] is None
    assert diagnosis["prepared_operator_completion_inputs_manifest_digest"] is None
    assert diagnosis["success_execution_digest"] is None


def test_failure_classification_domains_and_findings() -> None:
    diagnosis = _build()
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert tuple(diagnosis["secondary_failure_classes"]) == service.SECONDARY_FAILURE_CLASSES
    assert diagnosis["diagnosis_domains"] == [
        {"domain_id": domain, "status": status, "finding": finding}
        for domain, status, finding in service.DIAGNOSIS_DOMAINS
    ]
    assert diagnosis["diagnosis_findings"] == list(service.DIAGNOSIS_FINDINGS)
    assert len(diagnosis["diagnosis_domains"]) == 12
    assert len(diagnosis["diagnosis_findings"]) == 18


def test_upstream_identity_and_digest_chains_are_bound() -> None:
    diagnosis = _build()
    expected = {
        "source_approval_commit": "6623e6a6acb0a8da85fee15a29a52606a7fc6af1",
        "source_approval_digest": "351bf94d241be01c17fe96bf5f4db5ba983830aa997462a5f6c2bbaefdf4df72",
        "source_attestation_digest": "81e1d3e89e21394cc6b8f9164cb1911c545fb58d764f3205fbc566fd7a1bb3af",
        "source_operator_review_commit": "2efc22338250f9de88e76fbf6381796c82f817df",
        "source_candidate_commit": "b060a0ae9263e05d561ec0c7c5897558d8c2a9c1",
        "source_failure_diagnosis_commit": "07276fc4b171179eb7210ce679ba2a9bdbd17e8c",
        "source_completion_execution_commit": "945776b2164969e067d8dcc4809128282d3b1287",
        "source_completion_approval_commit": "40bee1289543bb07e64e383eb2e1c61d83615bd5",
        "source_completion_candidate_operator_review_commit": "d71bfb14a656592ab637d94d9dd30d73912104b0",
        "source_completion_candidate_commit": "7af6b1b5ad223f92da0997e2b7abcb73543470df",
        "source_template_preparation_results_review_commit": "268c84d7ef4ed550bb38f07670247540590885f6",
        "source_template_preparation_execution_commit": "a39332feb29a23612ee51cb45e8d5663b144c638",
    }
    for key, value in expected.items():
        assert diagnosis[key] == value
    assert diagnosis["selected_operator_completion_inputs_preparation_or_supply_package"] == service.SELECTED_PACKAGE
    assert diagnosis["source_blocked_acquisition_execution_reason"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"
    assert diagnosis["historical_blocked_remediation_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"


def test_retry_priority_diagnostic_and_reviewed_context_is_preserved() -> None:
    diagnosis = _build()
    assert (diagnosis["retry_pytest_passed_count"], diagnosis["retry_pytest_failed_count"], diagnosis["retry_pytest_error_count"], diagnosis["retry_pytest_skipped_count"]) == (24877, 1292, 112, 7)
    assert [row["failed_or_errored_nodeid_count"] for row in diagnosis["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert diagnosis["priority_1_total_nodeids"] == 612
    assert diagnosis["top_10_count_sum"] == 1069
    assert diagnosis["failed_or_errored_nodeids_count"] == 1404
    assert diagnosis["priority1_pre_change_validation_passed_count"] == 675
    assert diagnosis["priority1_post_change_validation_passed_count"] == 675
    assert diagnosis["priority1_validation_is_retry_evidence"] is False
    assert diagnosis["source_exit_code"] == 1
    assert diagnosis["source_stdout_byte_count"] == 1231380
    assert diagnosis["source_stderr_byte_count"] == 0
    assert diagnosis["source_diagnostic_metadata_only"] is True
    assert len(diagnosis["reviewed_observable_failure_families"]) == 4
    assert {row["confidence"] for row in diagnosis["reviewed_observable_failure_families"]} == {"HIGH"}
    assert len(diagnosis["reviewed_workstreams"]) == 4


def test_template_coverage_evidence_absence_and_count_labels() -> None:
    diagnosis = _build()
    assert len(diagnosis["missing_authority_mapping"]) == 30
    assert {row["current_status"] for row in diagnosis["missing_authority_mapping"]} == {"MISSING_NOT_ACQUIRED"}
    assert diagnosis["actual_coverage"] == {
        "reviewed_template_row_count": 30,
        "actual_covered_missing_authority_item_count": 0,
        "actual_uncovered_missing_authority_item_count": 30,
        "missing_authority_items_status": "MISSING_NOT_ACQUIRED",
    }
    assert not any(diagnosis["actual_evidence_absence"].values())
    assert [diagnosis[key] for key in ("future_completion_requirement_count", "source_enumerated_future_completion_requirement_count", "approved_future_completion_requirement_named_count")] == [67, 69, 69]
    assert [diagnosis[key] for key in ("source_non_goal_count", "source_enumerated_non_goal_count")] == [71, 76]
    assert [diagnosis[key] for key in ("source_risk_control_count", "source_enumerated_risk_control_count")] == [104, 106]


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_true_fields(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_required_false_fields(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize("field,value", service.COUNTS.items())
def test_required_counts(field: str, value) -> None:
    assert _build()[field] == value


@pytest.mark.parametrize("control", service.RISK_CONTROLS)
def test_required_risk_controls(control: str) -> None:
    assert control in _build()["risk_controls"]


@pytest.mark.parametrize("output_id", service.OUTPUT_IDS)
def test_required_outputs(output_id: str) -> None:
    assert {row["output_id"] for row in _build()["outputs"]} >= {output_id}


def test_recommendation_chain_gates_and_authority_boundary() -> None:
    diagnosis = _build()
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert diagnosis["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert diagnosis["next_chain"] == list(service.NEXT_CHAIN)
    assert diagnosis["next_gates"] == list(service.NEXT_GATES)
    assert diagnosis["predictive_usefulness"] == "not accepted"
    assert diagnosis["profitability"] == "not accepted"
    assert {diagnosis[key] for key in ("runtime_use", "strategy_use", "paper_trading", "broker_execution")} == {"NOT_AUTHORIZED"}


def test_checklist_and_all_digests_are_deterministic() -> None:
    first, second = _build(), _build()
    assert len(first["checklist"]) == first["summary"]["total_checks"]
    assert first["summary"]["passed_checks"] == len(first["checklist"])
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    for key in (
        service.DIAGNOSIS_DIGEST_KEY,
        service.FAILURE_CLASSIFICATION_DIGEST_KEY,
        service.INPUT_ABSENCE_DIAGNOSIS_DIGEST_KEY,
        service.SOURCE_BINDING_REVIEW_DIGEST_KEY,
        service.COVERAGE_DIAGNOSIS_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64


def test_validator_accepts_valid_diagnosis() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(_build())
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize("field", ("artifact_kind", "diagnosis_status", "diagnosis_scope", "source_execution_commit", "source_execution_status", "source_blocked_reason", "source_blocked_digest", "source_source_binding_digest", "source_input_absence_digest", "source_coverage_digest", "source_blocked_manifest_digest", "primary_failure_class", "source_approval_digest", "source_attestation_digest", "source_operator_review_digest", "source_candidate_digest", "source_failure_diagnosis_digest", "source_completion_execution_blocked_digest", "source_completion_approval_digest", "source_completion_candidate_operator_review_digest", "source_completion_candidate_digest", "source_template_preparation_results_review_digest", "source_template_preparation_execution_digest", "source_blocked_acquisition_execution_manifest_digest", "source_follow_on_execution_digest", "historical_blocked_remediation_manifest_digest", "source_targeted_remediation_plan_digest", "source_recovery_results_review_digest", "source_durable_receipt_path", "retry_pytest_failed_count", "priority_1_total_nodeids", "source_stdout_sha256", "missing_authority_items_status"))
def test_validator_rejects_scalar_drift(field: str) -> None:
    _reject(lambda diagnosis: diagnosis.__setitem__(field, "DRIFT"))


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_field_false(field: str) -> None:
    _reject(lambda diagnosis: diagnosis.__setitem__(field, False))


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_required_false_field_true(field: str) -> None:
    _reject(lambda diagnosis: diagnosis.__setitem__(field, True))


@pytest.mark.parametrize("field", ("prepared_operator_completion_inputs_digest", "prepared_operator_completion_inputs_manifest_digest", "success_execution_digest"))
def test_validator_rejects_success_digest_presence(field: str) -> None:
    _reject(lambda diagnosis: diagnosis.__setitem__(field, "a" * 64))


@pytest.mark.parametrize("collection", ("secondary_failure_classes", "diagnosis_domains", "diagnosis_findings", "outputs", "next_chain", "next_gates", "risk_controls", "missing_authority_mapping", "reviewed_observable_failure_families", "reviewed_workstreams"))
def test_validator_rejects_missing_collection_item(collection: str) -> None:
    _reject(lambda diagnosis: diagnosis[collection].pop())


def test_source_execution_validation_accepts_committed_projection() -> None:
    assert _build() == service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(source_execution=_source_execution())


@pytest.mark.parametrize("field", tuple(_source_execution()))
def test_source_execution_validation_rejects_drift(field: str) -> None:
    value = _source_execution()
    value[field] = "DRIFT"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(source_execution=value)


def test_source_builders_are_not_called(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*_args, **_kwargs):
        raise AssertionError("source builder called")

    monkeypatch.setattr(service.source, "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_v1", fail)
    assert _build()["source_execution_bound"] is True


@pytest.mark.parametrize("section", service.MARKDOWN_SECTIONS)
def test_markdown_contains_required_sections(section: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_markdown_v1(_build())
    assert f"## {section}" in markdown


def test_writer_writes_only_status_and_protects_runtime_dirs(tmp_path: Path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION_AFTER_APPROVAL_FAILURE_DIAGNOSIS_STATUS.md"
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    for protected in (tmp_path / ".marketflow", tmp_path / ".pytest_cache", tmp_path / ".env"):
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyExecutionFailureDiagnosisError):
            service.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_execution_after_approval_failure_diagnosis_v1(protected)
