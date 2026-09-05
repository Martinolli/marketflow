from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_service
    as service,
)


def build_success():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1()


def build_blocked():
    approval = service._committed_source_follow_on_approval()
    approval["selected_follow_on_package"] = "UNAPPROVED_PACKAGE"
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
        source_follow_on_approval=approval
    )


def assert_rejected(artifact, mutate):
    changed = deepcopy(artifact)
    mutate(changed)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(changed)


def test_success_artifact_builds_offline():
    artifact = build_success()
    assert artifact["created_offline"] is True
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND


def test_blocked_artifact_builds_for_invalid_approval_package():
    artifact = build_blocked()
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert "SELECTED_FOLLOW_ON_PACKAGE_MISMATCH" in artifact["blocked_reason"]


@pytest.mark.parametrize(
    ("artifact_factory", "kind", "status"),
    [
        (build_success, service.SUCCESS_ARTIFACT_KIND, service.SUCCESS_STATUS),
        (build_blocked, service.BLOCKED_ARTIFACT_KIND, service.BLOCKED_STATUS),
    ],
)
def test_identity_status_and_scope(artifact_factory, kind, status):
    artifact = artifact_factory()
    assert artifact["artifact_kind"] == kind
    assert artifact["execution_status"] == status
    assert artifact["execution_scope"] == service.EXECUTION_SCOPE
    assert artifact["selected_follow_on_package"] == service.SELECTED_FOLLOW_ON_PACKAGE


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_all_committed_source_bindings_are_preserved(field):
    assert build_success()[field] == service.SOURCE_BINDINGS[field]


def test_follow_on_approval_identity_is_bound():
    artifact = build_success()
    assert artifact["source_follow_on_approval_commit"] == service.SOURCE_FOLLOW_ON_APPROVAL_COMMIT
    assert artifact["source_follow_on_approval_digest"] == service.SOURCE_FOLLOW_ON_APPROVAL_DIGEST


def test_follow_on_review_and_candidate_are_bound():
    artifact = build_success()
    assert artifact["source_follow_on_candidate_operator_review_commit"] == service.SOURCE_FOLLOW_ON_OPERATOR_REVIEW_COMMIT
    assert artifact["source_follow_on_candidate_operator_review_digest"] == service.SOURCE_FOLLOW_ON_OPERATOR_REVIEW_DIGEST
    assert artifact["source_follow_on_candidate_commit"] == service.SOURCE_FOLLOW_ON_CANDIDATE_COMMIT
    assert artifact["source_follow_on_candidate_digest"] == service.SOURCE_FOLLOW_ON_CANDIDATE_DIGEST


def test_current_results_review_and_execution_are_bound():
    artifact = build_success()
    assert artifact["source_results_review_commit"] == service.SOURCE_RESULTS_REVIEW_COMMIT
    assert artifact["source_results_review_digest"] == service.SOURCE_RESULTS_REVIEW_DIGEST
    assert artifact["source_execution_commit"] == service.SOURCE_EXECUTION_COMMIT
    assert artifact["source_execution_digest"] == service.SOURCE_EXECUTION_DIGEST


def test_historical_chain_and_failure_classification_are_bound():
    artifact = build_success()
    assert artifact["source_approval_commit"] == "c88d4c238224a5c532d07374ab191e8b8b859af5"
    assert artifact["source_operator_review_digest"] == "8c3715141f8a52643dd7262406dce003a4868db279d66b74164c7b0c9d7baf51"
    assert artifact["source_candidate_digest"] == "bae832a665e9a1d389a2955536401c87b2032ad773c5de799f9ee90958cb324c"
    assert artifact["source_blocked_reason"] == "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"
    assert artifact["primary_failure_class"] == artifact["source_blocked_reason"]
    assert len(artifact["secondary_failure_classes"]) == 4


def test_retry_counts_and_priority_one_context_are_bound():
    artifact = build_success()
    assert artifact["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert [item["failed_or_errored_nodeid_count"] for item in artifact["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert artifact["priority_1_total_nodeids"] == 612
    assert artifact["top_10_count_sum"] == 1069
    assert artifact["module_summary_module_count"] == 29
    assert artifact["failed_or_errored_nodeids_count"] == 1404


def test_priority_one_validation_and_diagnostic_metadata_are_bound():
    artifact = build_success()
    validation = artifact["priority1_validation_summary"]
    diagnostic = artifact["diagnostic_capture_evidence_summary"]
    assert validation["pre_change_passed_count"] == 675
    assert validation["post_change_passed_count"] == 675
    assert validation["not_retry_evidence"] is True
    assert diagnostic["exit_code"] == 1
    assert diagnostic["stdout_byte_count"] == 1231380
    assert diagnostic["stderr_byte_count"] == 0
    assert diagnostic["stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"


def test_observable_families_and_reviewed_workstreams_are_bound():
    artifact = build_success()
    assert [item["family_id"] for item in artifact["reviewed_observable_failure_families"]] == [
        "assertion_or_value_mismatch", "digest_or_hash_mismatch",
        "fixture_or_test_isolation_issue", "missing_or_unexpected_field",
    ]
    assert all(item["confidence"] == "HIGH" for item in artifact["reviewed_observable_failure_families"])
    assert len(artifact["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in artifact["reviewed_workstreams"])


def test_missing_inventory_and_mapping_review_facts_are_bound():
    artifact = build_success()
    assert artifact["missing_authority_inventory_section_count"] == 4
    assert artifact["missing_authority_inventory_item_count"] == 30
    assert artifact["missing_authority_items_status"] == "MISSING_NOT_ACQUIRED"
    assert artifact["workstream_mapping_count"] == 4
    assert artifact["workstream_mapping_status"] == "PLANNED_NOT_EXECUTED"
    assert artifact["source_outputs_generated_count"] == 27
    assert artifact["review_outputs_generated_count"] == 28


def test_candidate_identity_and_boundaries_are_exact():
    candidate = build_success()["source_authority_acquisition_candidate"]
    assert candidate["candidate_type"] == "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS"
    assert candidate["candidate_status"] == "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED"
    assert "NOT_SOURCE_AUTHORITY_ACQUISITION" in candidate["candidate_scope"]
    assert candidate["authority_acquired_now"] is False
    assert candidate["evidence_acquired_now"] is False
    assert candidate["direct_change_authorized"] is False


def test_four_acquisition_scope_sections_are_complete_and_non_authorizing():
    scopes = build_success()["source_authority_acquisition_scope_definition"]
    assert [item["section_id"] for item in scopes] == list(service.ACQUISITION_SCOPE_REQUIREMENTS)
    assert all(len(item["requirements_to_obtain_or_bind"]) == 8 for item in scopes)
    assert all(item["current_execution_does_not_acquire_evidence"] is True for item in scopes)
    for item in scopes:
        assert item[service.SCOPE_CHANGE_FLAGS[item["section_id"]]] is False


def test_thirty_missing_authority_items_are_mapped_for_future_acquisition_only():
    mapping = build_success()["missing_authority_to_source_evidence_mapping"]
    assert len(mapping) == 30
    assert len({item["missing_authority_id"] for item in mapping}) == 30
    assert {item["section_id"] for item in mapping} == set(service.ACQUISITION_SCOPE_REQUIREMENTS)
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in mapping)
    assert all(item["candidate_requirement_status"] == "DEFINED_FOR_FUTURE_ACQUISITION_CANDIDATE_ONLY" for item in mapping)
    assert all(item["authority_acquired_now"] is False for item in mapping)
    assert all(item["evidence_acquired_now"] is False for item in mapping)
    assert all(item["direct_change_authorized"] is False for item in mapping)


def test_acceptable_source_artifact_inventory_is_future_review_only():
    inventory = build_success()["acceptable_source_artifact_inventory"]
    assert len(inventory) == 13
    assert {item["artifact_type"] for item in inventory} == set(service.ACCEPTABLE_SOURCE_ARTIFACT_TYPES)
    assert all(item["allowed_for_future_review"] is True for item in inventory)
    assert all(item["acquired_now"] is False for item in inventory)
    assert all(item["requires_results_review_before_use"] is True for item in inventory)
    assert all(item["requires_digest_or_provenance_binding"] is True for item in inventory)
    assert all(item["may_authorize_direct_change_without_later_approval"] is False for item in inventory)


def test_operator_evidence_and_custody_requirements_are_created_not_satisfied():
    artifact = build_success()
    assert artifact["operator_provided_evidence_requirements"] == list(service.OPERATOR_EVIDENCE_REQUIREMENTS)
    assert artifact["evidence_custody_and_digest_requirements"] == list(service.EVIDENCE_CUSTODY_REQUIREMENTS)
    assert "must not include API keys" in artifact["operator_provided_evidence_requirements"]


def test_candidate_results_review_requirements_preserve_all_gates():
    requirements = build_success()["candidate_results_review_requirements"]
    assert requirements == list(service.CANDIDATE_RESULTS_REVIEW_REQUIREMENTS)
    assert "no source authority was acquired" in requirements
    assert "no retry candidate was created" in requirements


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_success_facts_are_true(field):
    assert build_success()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_protected_execution_actions_remain_false(field):
    assert build_success()[field] is False


def test_acceptance_runtime_and_trading_remain_closed():
    artifact = build_success()
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_use"] == "NOT_AUTHORIZED"
    assert artifact["strategy_use"] == "NOT_AUTHORIZED"
    assert artifact["paper_trading"] == "NOT_AUTHORIZED"
    assert artifact["broker_execution"] == "NOT_AUTHORIZED"


def test_outputs_recommendation_chain_gates_and_controls_are_complete():
    artifact = build_success()
    assert artifact["outputs_generated"] == [{"output_id": item, "status": service.OUTPUT_STATUS} for item in service.OUTPUT_IDS]
    assert artifact["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert artifact["next_chain"] == list(service.SUCCESS_NEXT_CHAIN)
    assert artifact["next_gates"] == list(service.SUCCESS_NEXT_GATES)
    assert artifact["risk_controls"] == list(service.RISK_CONTROLS)


@pytest.mark.parametrize("factory", [build_success, build_blocked])
def test_checklist_and_summary_pass(factory):
    artifact = factory()
    assert artifact["summary"]["total_checks"] == len(artifact["checklist"])
    assert artifact["summary"]["passed_checks"] == len(artifact["checklist"])
    assert artifact["summary"]["failed_checks"] == 0
    assert artifact["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in artifact["checklist"])


def test_success_digests_are_deterministic_and_content_bound():
    first = build_success()
    second = build_success()
    for key in (
        service.EXECUTION_DIGEST_KEY, service.ACQUISITION_CANDIDATE_DIGEST_KEY,
        service.ACQUISITION_SCOPE_DIGEST_KEY, service.MISSING_AUTHORITY_MAPPING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64
    assert first[service.ACQUISITION_CANDIDATE_DIGEST_KEY] == semantic_digest(first["source_authority_acquisition_candidate"])
    assert first[service.ACQUISITION_SCOPE_DIGEST_KEY] == semantic_digest(first["source_authority_acquisition_scope_definition"])
    assert first[service.MISSING_AUTHORITY_MAPPING_DIGEST_KEY] == semantic_digest(first["missing_authority_to_source_evidence_mapping"])
    assert first[service.MANIFEST_DIGEST_KEY] == semantic_digest(first["digest_manifest"])


def test_blocked_manifest_is_deterministic_and_success_digests_are_absent():
    first = build_blocked()
    second = build_blocked()
    assert first[service.BLOCKED_MANIFEST_DIGEST_KEY] == second[service.BLOCKED_MANIFEST_DIGEST_KEY]
    assert len(first[service.BLOCKED_MANIFEST_DIGEST_KEY]) == 64
    for key in (
        service.EXECUTION_DIGEST_KEY, service.ACQUISITION_CANDIDATE_DIGEST_KEY,
        service.ACQUISITION_SCOPE_DIGEST_KEY, service.MISSING_AUTHORITY_MAPPING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] is None


@pytest.mark.parametrize("factory", [build_success, build_blocked])
def test_validator_accepts_success_and_blocked(factory):
    artifact = factory()
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(artifact)
    assert result["artifact_kind"] == artifact["artifact_kind"]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"), ("execution_scope", "WRONG"),
        ("selected_follow_on_package", "WRONG"), ("source_follow_on_approval_digest", "0" * 64),
        ("source_follow_on_candidate_operator_review_digest", "0" * 64),
        ("source_follow_on_candidate_digest", "0" * 64), ("source_results_review_digest", "0" * 64),
        ("source_execution_digest", "0" * 64), ("source_authority_enrichment_plan_digest", "0" * 64),
        ("source_missing_authority_inventory_digest", "0" * 64),
        ("source_workstream_authority_mapping_digest", "0" * 64),
        ("source_execution_manifest_digest", "0" * 64), ("source_approval_digest", "0" * 64),
        ("source_operator_review_digest", "0" * 64), ("source_candidate_digest", "0" * 64),
        ("source_remediation_execution_after_plan_results_review_failure_diagnosis_digest", "0" * 64),
        ("source_blocked_execution_commit", "0" * 40), ("source_blocked_reason", "WRONG"),
        ("source_blocked_manifest_digest", "0" * 64), ("primary_failure_class", "WRONG"),
        ("source_remediation_execution_approval_after_plan_results_review_digest", "0" * 64),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", "0" * 64),
        ("source_targeted_remediation_plan_review_digest", "0" * 64),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "0" * 64),
        ("source_targeted_remediation_plan_digest", "0" * 64), ("source_workstream_mapping_digest", "0" * 64),
        ("source_remediation_or_method_results_review_after_diagnostic_capture_digest", "0" * 64),
        ("source_remediation_or_method_execution_after_diagnostic_capture_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_results_review_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_execution_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_receipt_digest", "0" * 64),
        ("source_durable_receipt_path", ""), ("source_planning_execution_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64), ("source_materialized_payload_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64), ("source_module_grouping_digest", "0" * 64),
        ("source_staged_inventory_digest", "0" * 64), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("missing_authority_inventory_item_count", 29),
        ("missing_authority_items_status", "ACQUIRED"), ("workstream_mapping_status", "EXECUTED"),
    ],
)
def test_validator_rejects_changed_bound_values(field, bad):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, bad))


def test_validator_rejects_missing_secondary_failure_class():
    assert_rejected(build_success(), lambda artifact: artifact["secondary_failure_classes"].pop())


def test_validator_rejects_changed_retry_count():
    assert_rejected(build_success(), lambda artifact: artifact["retry_failure_context"]["counts"].__setitem__("failed", 1291))


def test_validator_rejects_missing_priority_one_module():
    assert_rejected(build_success(), lambda artifact: artifact["priority_1_target_modules"].pop())


def test_validator_rejects_diagnostic_hash_or_byte_change():
    assert_rejected(build_success(), lambda artifact: artifact["diagnostic_capture_evidence_summary"].__setitem__("stdout_sha256", "0" * 64))
    assert_rejected(build_success(), lambda artifact: artifact["diagnostic_capture_evidence_summary"].__setitem__("stdout_byte_count", 1))


def test_validator_rejects_priority_one_validation_change():
    assert_rejected(build_success(), lambda artifact: artifact["priority1_validation_summary"].__setitem__("post_change_passed", False))


def test_validator_rejects_observable_family_or_workstream_change():
    assert_rejected(build_success(), lambda artifact: artifact["reviewed_observable_failure_families"].pop())
    assert_rejected(build_success(), lambda artifact: artifact["reviewed_workstreams"].pop())


@pytest.mark.parametrize(
    "field",
    [
        "source_authority_acquisition_candidate", "source_authority_acquisition_scope_definition",
        "missing_authority_to_source_evidence_mapping", "acceptable_source_artifact_inventory",
        "operator_provided_evidence_requirements", "candidate_results_review_requirements", "outputs_generated",
    ],
)
def test_validator_rejects_missing_success_output(field):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, None))


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_any_protected_action_claim(field):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, True))


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_acceptance_claim(field):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, "accepted"))


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_validator_rejects_runtime_or_trading_authority(field):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, "AUTHORIZED"))


@pytest.mark.parametrize("field", ["risk_controls", "next_chain", "next_gates"])
def test_validator_rejects_missing_controls_or_next_path(field):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(field, []))


@pytest.mark.parametrize(
    "key",
    [
        service.EXECUTION_DIGEST_KEY, service.ACQUISITION_CANDIDATE_DIGEST_KEY,
        service.ACQUISITION_SCOPE_DIGEST_KEY, service.MISSING_AUTHORITY_MAPPING_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_missing_success_digest(key):
    assert_rejected(build_success(), lambda artifact: artifact.__setitem__(key, None))


def test_validator_rejects_missing_blocked_reason_or_manifest():
    assert_rejected(build_blocked(), lambda artifact: artifact.__setitem__("blocked_reason", ""))
    assert_rejected(build_blocked(), lambda artifact: artifact.__setitem__(service.BLOCKED_MANIFEST_DIGEST_KEY, None))


def test_writer_round_trips_success_to_requested_directory(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
        tmp_path, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.SUCCESS_ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert artifact["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND


def test_writer_round_trips_blocked_to_requested_directory(tmp_path):
    approval = service._committed_source_follow_on_approval()
    approval["future_execution_may_acquire_source_authority"] = True
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(
        tmp_path, source_follow_on_approval=approval
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["outputs_generated"] == []


def test_invalid_timestamp_fails_closed():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(run_timestamp_utc="not-utc")


def test_markdown_includes_every_required_section():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_markdown_v1(build_success())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Execution After Results Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_service_source_contains_no_execution_or_network_mechanisms():
    source = Path(service.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "subprocess", "requests.", "httpx.", "urlopen(", "os.environ", "dotenv", "pytest.main",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_approval_after_results_review_v1(",
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(",
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(",
    ):
        assert forbidden not in source
