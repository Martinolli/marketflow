from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_service
    as service,
)


@pytest.fixture(scope="module")
def review() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1()


def test_operator_review_builds_offline(review: dict) -> None:
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("review_status", service.REVIEW_STATUS),
        ("review_scope", service.REVIEW_SCOPE),
        ("source_follow_on_results_review_commit", service.SOURCE_FOLLOW_ON_RESULTS_REVIEW_COMMIT),
        ("source_follow_on_results_review_digest", service.SOURCE_FOLLOW_ON_RESULTS_REVIEW_DIGEST),
        ("source_acquisition_candidate_review_digest", service.SOURCE_ACQUISITION_CANDIDATE_REVIEW_DIGEST),
        ("source_acquisition_scope_review_digest", service.SOURCE_ACQUISITION_SCOPE_REVIEW_DIGEST),
        ("source_missing_authority_mapping_review_digest", service.SOURCE_MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST),
        ("source_follow_on_results_review_manifest_digest", service.SOURCE_FOLLOW_ON_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_follow_on_execution_commit", "a5a78331058c37b348108f9599fec6a24763bf06"),
        ("source_follow_on_execution_after_results_review_digest", "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208"),
        ("source_authority_acquisition_candidate_digest", "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91"),
        ("source_authority_acquisition_scope_digest", "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8"),
        ("source_missing_authority_to_source_evidence_mapping_digest", "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334"),
        ("source_follow_on_execution_manifest_digest", "56a6d540ae16cb9670696255c775fb690b9273c13c120cd822facf4a8bb85347"),
        ("selected_follow_on_package", "PACKAGE_CREATE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS"),
        ("source_follow_on_approval_digest", "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6"),
        ("source_follow_on_candidate_operator_review_digest", "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"),
        ("source_follow_on_candidate_digest", "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"),
        ("source_results_review_digest", "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"),
        ("source_enrichment_plan_review_digest", "0cc52bd10f4b3fc61220f92f0024b728c98c43133c6b71906535037cbe824d46"),
        ("source_missing_authority_inventory_review_digest", "72dd695b4b112e4a4c7d285efd896a54bfd05ec0f8cd1c9bc3eb2087a40b49ec"),
        ("source_workstream_authority_mapping_review_digest", "f64e8575ef00ebacf54d1bf145140a94001c8e475e5a89c44e62a609421c7597"),
        ("source_workstream_mapping_review_digest", "f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334"),
        ("source_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
        ("source_approval_digest", "0a487e0e1e79b40edd80e785802dde3e9fd5cd0d6fe82995e2276ab43ab86972"),
        ("source_remediation_execution_after_plan_results_review_failure_diagnosis_digest", "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"),
        ("source_blocked_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("source_blocked_manifest_digest", "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"),
        ("primary_failure_class", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", "30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa"),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c"),
        ("source_remediation_or_method_results_review_after_diagnostic_capture_digest", "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"),
        ("source_remediation_or_method_execution_after_diagnostic_capture_digest", "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88"),
        ("source_receipt_recovery_or_recapture_results_review_digest", "427d2a76afcec7c8b9647a0f0c19b6037e5a451b0f70fad1a5025afc266946ba"),
        ("source_receipt_recovery_or_recapture_execution_digest", "25a70331c48eedeb62c6f8532dba0e1b782904ff4b753934c2fd12ccbec47e46"),
        ("source_planning_execution_digest", "846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b"),
        ("source_complete_29_row_binding_digest", "36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7"),
        ("source_materialized_payload_digest", "1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7"),
        ("source_recovery_detail_digest", "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"),
        ("source_module_grouping_digest", "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"),
        ("source_staged_inventory_digest", "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0"),
    ),
)
def test_committed_source_bindings(review: dict, field: str, expected: object) -> None:
    assert review[field] == expected


def test_retry_and_priority_context_is_bound(review: dict) -> None:
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    assert len(review["priority_1_target_modules"]) == 5
    assert review["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["not_retry_evidence"] is True


def test_diagnostic_and_planning_context_is_preserved(review: dict) -> None:
    diagnostic = review["diagnostic_capture_evidence_summary"]
    assert diagnostic["exit_code"] == 1
    assert diagnostic["stdout_byte_count"] == 1231380
    assert diagnostic["stderr_byte_count"] == 0
    assert diagnostic["stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert all(item["observable_evidence_count"] == 47 for item in review["reviewed_observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in review["reviewed_workstreams"])


def test_candidate_scope_and_mapping_are_reviewed_without_authority(review: dict) -> None:
    candidate = review["source_authority_acquisition_candidate_review"]
    assert candidate["candidate_status"] == "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED"
    assert candidate["approved"] is False and candidate["executed"] is False
    scope = review["acquisition_scope_sections_review"]
    assert scope["section_count"] == 4
    assert scope["all_sections_deny_evidence_acquisition"] is True
    assert scope["all_sections_deny_direct_changes"] is True
    mapping = review["missing_authority_to_source_evidence_mapping_review"]
    assert mapping["mapped_item_count"] == 30
    assert mapping["all_missing_not_acquired"] is True
    assert mapping["all_authority_acquired_now_false"] is True
    assert mapping["all_evidence_acquired_now_false"] is True
    assert mapping["all_direct_change_authorized_false"] is True


def test_reviewed_inventory_and_requirement_counts(review: dict) -> None:
    assert review["acceptable_source_artifact_inventory_review"]["artifact_type_count"] == 13
    assert review["acceptable_source_artifact_inventory_review"]["all_acquired_now_false"] is True
    assert review["operator_provided_evidence_requirements_review"]["requirement_count"] == 10
    assert review["evidence_custody_and_digest_requirements_review"]["requirement_count"] == 6
    assert review["candidate_results_review_requirements_review"]["requirement_count"] == 16


def test_all_twelve_packages_are_reviewed_and_unselected(review: dict) -> None:
    packages = review["reviewed_source_authority_acquisition_packages"]
    assert len(packages) == 12
    assert sum(item["source_status"] == "AVAILABLE_FOR_OPERATOR_REVIEW_NOT_SELECTED" for item in packages) == 6
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(not item["selected"] and not item["approved"] and not item["authorized"] and not item["executed"] for item in packages)
    assert review["recommended_source_authority_acquisition_package"] == service.RECOMMENDED_PACKAGE
    assert review["recommended_package"]["selected"] is False


def test_future_material_is_reviewed_not_executed(review: dict) -> None:
    assert len(review["reviewed_future_requirements"]) == 51
    assert len(review["reviewed_future_plan"]) == 13
    assert len(review["reviewed_planned_outputs"]) == 28
    assert len(review["reviewed_non_goals"]) == len(service.NON_GOALS)
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_plan"])
    assert all(item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_fact_is_true(review: dict, field: str) -> None:
    assert review[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_authority_and_action_boundary_is_false(review: dict, field: str) -> None:
    assert review[field] is False


def test_review_outputs_and_recommendation(review: dict) -> None:
    assert len(review["outputs_generated"]) == 33
    assert all(item["status"] == service.OUTPUT_STATUS for item in review["outputs_generated"])
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert review["ready_for_source_authority_acquisition_approval"] is False
    assert review["ready_for_retry_candidate"] is False


def test_checklist_passes(review: dict) -> None:
    assert review["summary"]["total_checks"] == len(review["checklist"])
    assert review["summary"]["passed_checks"] == len(review["checklist"])
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" for item in review["checklist"])


def test_review_digests_are_deterministic_and_valid(review: dict) -> None:
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1()
    for key in (
        service.OPERATOR_REVIEW_DIGEST_KEY,
        service.CANDIDATE_REVIEW_DIGEST_KEY,
        service.SCOPE_REVIEW_DIGEST_KEY,
        service.MAPPING_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert rebuilt[key] == review[key]
        assert len(review[key]) == 64


def test_validator_accepts_valid_review(review: dict) -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(deepcopy(review))
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    "field",
    (
        "artifact_kind", "review_status", "review_scope",
        "source_follow_on_results_review_digest", "source_acquisition_candidate_review_digest",
        "source_acquisition_scope_review_digest", "source_missing_authority_mapping_review_digest",
        "source_follow_on_results_review_manifest_digest", "source_follow_on_execution_after_results_review_digest",
        "source_authority_acquisition_candidate_digest", "source_authority_acquisition_scope_digest",
        "source_missing_authority_to_source_evidence_mapping_digest", "selected_follow_on_package",
        "source_follow_on_approval_digest", "source_follow_on_candidate_operator_review_digest",
        "source_follow_on_candidate_digest", "source_results_review_digest", "source_execution_digest",
        "source_approval_digest", "source_blocked_reason", "primary_failure_class",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_planning_execution_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_detail_digest", "source_module_grouping_digest", "source_staged_inventory_digest",
        service.OPERATOR_REVIEW_DIGEST_KEY, service.CANDIDATE_REVIEW_DIGEST_KEY,
        service.SCOPE_REVIEW_DIGEST_KEY, service.MAPPING_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ),
)
def test_validator_rejects_changed_scalar_binding(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_review_fact_false(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_prohibited_action_true(review: dict, field: str) -> None:
    changed = deepcopy(review)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(changed)


@pytest.mark.parametrize(
    ("container", "mutation"),
    (
        ("reviewed_source_authority_acquisition_packages", "pop"),
        ("reviewed_future_requirements", "pop"),
        ("reviewed_future_plan", "pop"),
        ("reviewed_planned_outputs", "pop"),
        ("reviewed_non_goals", "pop"),
        ("outputs_generated", "pop"),
        ("next_chain", "pop"),
        ("next_gates", "pop"),
        ("risk_controls", "pop"),
    ),
)
def test_validator_rejects_missing_reviewed_material(review: dict, container: str, mutation: str) -> None:
    changed = deepcopy(review)
    getattr(changed[container], mutation)()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(changed)


def test_validator_rejects_nested_package_selection(review: dict) -> None:
    changed = deepcopy(review)
    changed["reviewed_source_authority_acquisition_packages"][0]["selected"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(changed)


def test_validator_rejects_candidate_scope_and_mapping_mutations(review: dict) -> None:
    mutations = []
    changed = deepcopy(review)
    changed["source_authority_acquisition_candidate_review"]["candidate_status"] = "changed"
    mutations.append(changed)
    changed = deepcopy(review)
    changed["acquisition_scope_sections_review"]["sections"].pop()
    mutations.append(changed)
    changed = deepcopy(review)
    changed["missing_authority_to_source_evidence_mapping_review"]["items"][0]["authority_acquired_now"] = True
    mutations.append(changed)
    changed = deepcopy(review)
    changed["acceptable_source_artifact_inventory_review"]["artifact_types"][0]["acquired_now"] = True
    mutations.append(changed)
    for candidate in mutations:
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(candidate)


def test_builder_rejects_mutated_injected_source() -> None:
    source_review = service._committed_source_follow_on_results_review()
    source_review[service.source.REVIEW_DIGEST_KEY] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureSourceAuthorityAcquisitionCandidateOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(source_follow_on_results_review=source_review)


def test_builder_does_not_call_prohibited_public_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("prohibited source builder called")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1",
        forbidden,
    )
    review = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1()
    assert review["operator_review_only"] is True


def test_markdown_contains_every_required_section(review: dict) -> None:
    rendered = service.build_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_markdown_v1(review)
    assert rendered.startswith("# MarketFlow Repository Integration Branch Retry Failure")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in rendered


def test_writer_uses_isolated_output_directory(tmp_path: Path) -> None:
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_source_authority_acquisition_candidate_operator_review_after_follow_on_execution_results_review_v1(tmp_path)
    expected = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_OPERATOR_REVIEW_AFTER_FOLLOW_ON_EXECUTION_RESULTS_REVIEW_STATUS.md"
    assert expected.is_file()
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
