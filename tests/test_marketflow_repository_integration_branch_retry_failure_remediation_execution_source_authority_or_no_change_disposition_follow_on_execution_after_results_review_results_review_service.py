from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_service
    as service,
)


def build_review():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1()


def assert_rejected(review, mutate):
    changed = deepcopy(review)
    mutate(changed)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(changed)


def test_results_review_builds_offline_with_exact_identity():
    review = build_review()
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


def test_source_follow_on_execution_identity_and_digests_are_bound():
    review = build_review()
    assert review["source_follow_on_execution_commit"] == service.SOURCE_FOLLOW_ON_EXECUTION_COMMIT
    assert review["source_follow_on_execution_artifact_kind"] == service.source.SUCCESS_ARTIFACT_KIND
    assert review["source_follow_on_execution_status"] == service.source.SUCCESS_STATUS
    assert review["source_follow_on_execution_scope"] == service.source.EXECUTION_SCOPE
    assert review["source_follow_on_execution_after_results_review_digest"] == service.SOURCE_FOLLOW_ON_EXECUTION_DIGEST
    assert review["source_authority_acquisition_candidate_digest"] == service.SOURCE_ACQUISITION_CANDIDATE_DIGEST
    assert review["source_authority_acquisition_scope_digest"] == service.SOURCE_ACQUISITION_SCOPE_DIGEST
    assert review["source_missing_authority_to_source_evidence_mapping_digest"] == service.SOURCE_MISSING_AUTHORITY_MAPPING_DIGEST
    assert review["source_follow_on_execution_manifest_digest"] == service.SOURCE_FOLLOW_ON_EXECUTION_MANIFEST_DIGEST
    assert review["selected_follow_on_package"] == service.SELECTED_FOLLOW_ON_PACKAGE


@pytest.mark.parametrize("field", sorted(service.source.SOURCE_BINDINGS))
def test_every_historical_source_binding_is_preserved(field):
    assert build_review()[field] == service.source.SOURCE_BINDINGS[field]


def test_source_chain_summaries_are_present():
    review = build_review()
    required = (
        "source_follow_on_execution_summary", "source_follow_on_approval_summary",
        "source_follow_on_operator_review_summary", "source_follow_on_candidate_summary",
        "source_results_review_summary", "source_execution_summary", "source_approval_summary",
        "source_historical_operator_review_summary", "source_historical_candidate_summary",
        "source_failure_diagnosis_summary", "source_blocked_execution_summary",
        "source_plan_results_review_summary", "source_plan_execution_summary",
        "source_method_results_review_summary", "source_method_execution_summary",
        "source_diagnostic_results_review_summary", "source_controlled_recapture_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
    )
    assert all(key in review and review[key] for key in required)
    assert review["source_durable_receipt_summary"]["parsed"] is False


def test_retry_priority_one_and_diagnostic_context_are_bound():
    review = build_review()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert [item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert review["priority1_validation_summary"]["pre_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["post_change_passed_count"] == 675
    assert review["priority1_validation_summary"]["not_retry_evidence"] is True
    assert review["diagnostic_capture_evidence_summary"]["exit_code"] == 1
    assert review["diagnostic_capture_evidence_summary"]["stdout_byte_count"] == 1231380
    assert review["diagnostic_capture_evidence_summary"]["stderr_byte_count"] == 0


def test_four_observable_families_and_workstreams_are_reviewed():
    review = build_review()
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in review["reviewed_observable_failure_families"]) == 188
    assert all(item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert all(item["direct_change_authorized"] is False for item in review["reviewed_workstreams"])


def test_source_enrichment_inventory_and_mapping_facts_are_reviewed():
    review = build_review()
    assert review["source_authority_enrichment_review_summary"]["source_authority_acquired"] is False
    assert review["missing_authority_inventory_review_summary"] == {"reviewed": True, "section_count": 4, "item_count": 30, "item_status": "MISSING_NOT_ACQUIRED"}
    assert review["workstream_authority_mapping_review_summary"] == {"reviewed": True, "mapping_count": 4, "mapping_status": "PLANNED_NOT_EXECUTED"}


def test_acquisition_candidate_review_preserves_candidate_only_status():
    candidate = build_review()["source_authority_acquisition_candidate_review"]
    assert candidate["candidate_type"] == "SOURCE_AUTHORITY_ACQUISITION_CANDIDATE_FROM_ENRICHMENT_RESULTS"
    assert candidate["candidate_status"] == "CREATED_FOR_RESULTS_REVIEW_NOT_APPROVED_NOT_EXECUTED"
    assert "NOT_SOURCE_AUTHORITY_ACQUISITION" in candidate["candidate_scope"]
    assert candidate["reviewed"] is True
    assert candidate["created_reviewed"] is True
    assert candidate["ready_for_results_review_reviewed"] is True
    assert candidate["approved"] is False
    assert candidate["executed"] is False


def test_acquisition_scope_review_has_four_complete_non_authorizing_sections():
    scope = build_review()["acquisition_scope_definition_review"]
    assert scope["reviewed"] is True
    assert scope["section_count"] == 4
    assert {item["section_id"] for item in scope["sections"]} == set(service.source.ACQUISITION_SCOPE_REQUIREMENTS)
    assert all(len(item["requirements_to_obtain_or_bind"]) == 8 for item in scope["sections"])
    assert scope["all_sections_deny_evidence_acquisition"] is True
    assert scope["all_sections_deny_direct_changes"] is True


def test_missing_authority_mapping_review_has_thirty_closed_items():
    mapping = build_review()["missing_authority_to_source_evidence_mapping_review"]
    assert mapping["reviewed"] is True
    assert mapping["mapped_item_count"] == 30
    assert len(mapping["items"]) == 30
    assert mapping["all_missing_not_acquired"] is True
    assert mapping["all_authority_acquired_now_false"] is True
    assert mapping["all_evidence_acquired_now_false"] is True
    assert mapping["all_direct_change_authorized_false"] is True


def test_acceptable_source_artifact_review_has_thirteen_unacquired_types():
    inventory = build_review()["acceptable_source_artifact_inventory_review"]
    assert inventory["reviewed"] is True
    assert inventory["artifact_type_count"] == 13
    assert inventory["all_acquired_now_false"] is True
    assert inventory["all_require_results_review"] is True


@pytest.mark.parametrize(
    ("field", "count"),
    [
        ("operator_provided_evidence_requirements_review", 10),
        ("evidence_custody_and_digest_requirements_review", 6),
        ("candidate_results_review_requirements_review", 16),
    ],
)
def test_requirement_reviews_preserve_counts_and_future_only_boundary(field, count):
    requirement_review = build_review()[field]
    assert requirement_review["reviewed"] is True
    assert requirement_review["requirement_count"] == count
    assert len(requirement_review["requirements"]) == count
    assert requirement_review["satisfied_or_acquired_now"] is False


def test_review_has_fifteen_findings_and_twelve_domains():
    review = build_review()
    assert len(review["results_review_findings"]) == 15
    assert [item["finding_id"] for item in review["results_review_findings"]] == [f"finding_{i}" for i in range(1, 16)]
    assert len(review["results_review_domains"]) == 12
    assert {item["domain_id"] for item in review["results_review_domains"]} == {item[0] for item in service.RESULTS_REVIEW_DOMAINS}


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_facts_are_true(field):
    assert build_review()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_protected_actions_and_authorities_remain_false(field):
    assert build_review()[field] is False


def test_acceptance_runtime_and_trading_remain_closed():
    review = build_review()
    assert review["predictive_usefulness"] == "not accepted"
    assert review["profitability"] == "not accepted"
    assert review["runtime_use"] == "NOT_AUTHORIZED"
    assert review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == "NOT_AUTHORIZED"
    assert review["broker_execution"] == "NOT_AUTHORIZED"


def test_review_outputs_recommendation_chain_gates_and_controls_are_complete():
    review = build_review()
    assert review["outputs_generated"] == [{"output_id": item, "status": service.OUTPUT_STATUS} for item in service.OUTPUT_IDS]
    assert len(review["outputs_generated"]) == 33
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_OPERATOR_REVIEW_NOT_CREATED"
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert review["next_chain"] == list(service.NEXT_CHAIN)
    assert review["next_gates"] == list(service.NEXT_GATES)
    assert review["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_and_summary_pass():
    review = build_review()
    assert review["summary"]["total_checks"] == len(review["checklist"])
    assert review["summary"]["passed_checks"] == len(review["checklist"])
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in review["checklist"])


def test_all_five_review_digests_are_deterministic_and_content_bound():
    first, second = build_review(), build_review()
    for key in (
        service.REVIEW_DIGEST_KEY, service.ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY,
        service.ACQUISITION_SCOPE_REVIEW_DIGEST_KEY, service.MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    ):
        assert first[key] == second[key]
        assert len(first[key]) == 64
    assert first[service.ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY] == semantic_digest(first["source_authority_acquisition_candidate_review"])
    assert first[service.ACQUISITION_SCOPE_REVIEW_DIGEST_KEY] == semantic_digest(first["acquisition_scope_definition_review"])
    assert first[service.MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY] == semantic_digest(first["missing_authority_to_source_evidence_mapping_review"])
    assert first[service.MANIFEST_DIGEST_KEY] == semantic_digest(first["digest_manifest"])


def test_validator_accepts_valid_review():
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(build_review())
    assert result["artifact_kind"] == service.ARTIFACT_KIND
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_follow_on_execution_commit", "0" * 40),
        ("source_follow_on_execution_after_results_review_digest", "0" * 64),
        ("source_authority_acquisition_candidate_digest", "0" * 64),
        ("source_authority_acquisition_scope_digest", "0" * 64),
        ("source_missing_authority_to_source_evidence_mapping_digest", "0" * 64),
        ("source_follow_on_execution_manifest_digest", "0" * 64),
        ("selected_follow_on_package", "WRONG"), ("source_follow_on_approval_digest", "0" * 64),
        ("source_follow_on_candidate_operator_review_digest", "0" * 64),
        ("source_follow_on_candidate_digest", "0" * 64), ("source_results_review_digest", "0" * 64),
        ("source_enrichment_plan_review_digest", "0" * 64),
        ("source_missing_authority_inventory_review_digest", "0" * 64),
        ("source_workstream_authority_mapping_review_digest", "0" * 64),
        ("source_results_review_manifest_digest", "0" * 64), ("source_execution_commit", "0" * 40),
        ("source_execution_digest", "0" * 64), ("source_authority_enrichment_plan_digest", "0" * 64),
        ("source_missing_authority_inventory_digest", "0" * 64),
        ("source_workstream_authority_mapping_digest", "0" * 64), ("source_execution_manifest_digest", "0" * 64),
        ("source_approval_digest", "0" * 64), ("source_operator_review_digest", "0" * 64),
        ("source_candidate_digest", "0" * 64),
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
        ("source_staged_inventory_digest", "0" * 64),
        ("acquisition_scope_section_count", 3), ("mapped_missing_authority_item_count", 29),
        ("acceptable_source_artifact_type_count", 12), ("operator_provided_evidence_requirement_count", 9),
        ("evidence_custody_and_digest_requirement_count", 5), ("candidate_results_review_requirement_count", 15),
        ("missing_authority_inventory_item_count", 29), ("missing_authority_items_status", "ACQUIRED"),
        ("workstream_mapping_status", "EXECUTED"),
    ],
)
def test_validator_rejects_changed_bound_value(field, bad):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, bad))


def test_validator_rejects_missing_secondary_failure_class():
    assert_rejected(build_review(), lambda review: review["secondary_failure_classes"].pop())


def test_validator_rejects_retry_priority_and_diagnostic_mutations():
    assert_rejected(build_review(), lambda review: review["retry_failure_context"]["counts"].__setitem__("failed", 1))
    assert_rejected(build_review(), lambda review: review["priority_1_target_modules"].pop())
    assert_rejected(build_review(), lambda review: review["priority1_validation_summary"].__setitem__("post_change_passed", False))
    assert_rejected(build_review(), lambda review: review["diagnostic_capture_evidence_summary"].__setitem__("stdout_sha256", "0" * 64))


def test_validator_rejects_observable_family_or_workstream_mutations():
    assert_rejected(build_review(), lambda review: review["reviewed_observable_failure_families"].pop())
    assert_rejected(build_review(), lambda review: review["reviewed_workstreams"].pop())


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_required_review_fact(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, False))


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_protected_action_or_authority_claim(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, True))


def test_validator_rejects_candidate_status_scope_or_readiness_change():
    assert_rejected(build_review(), lambda review: review["source_authority_acquisition_candidate_review"].__setitem__("candidate_status", "APPROVED"))
    assert_rejected(build_review(), lambda review: review["source_authority_acquisition_candidate_review"].__setitem__("candidate_scope", "WRONG"))
    assert_rejected(build_review(), lambda review: review["source_authority_acquisition_candidate_review"].__setitem__("ready_for_results_review_reviewed", False))


def test_validator_rejects_scope_mapping_inventory_or_requirement_mutation():
    assert_rejected(build_review(), lambda review: review["acquisition_scope_definition_review"]["sections"].pop())
    assert_rejected(build_review(), lambda review: review["missing_authority_to_source_evidence_mapping_review"]["items"].pop())
    assert_rejected(build_review(), lambda review: review["missing_authority_to_source_evidence_mapping_review"]["items"][0].__setitem__("authority_acquired_now", True))
    assert_rejected(build_review(), lambda review: review["missing_authority_to_source_evidence_mapping_review"]["items"][0].__setitem__("evidence_acquired_now", True))
    assert_rejected(build_review(), lambda review: review["missing_authority_to_source_evidence_mapping_review"]["items"][0].__setitem__("direct_change_authorized", True))
    assert_rejected(build_review(), lambda review: review["acceptable_source_artifact_inventory_review"]["artifact_types"][0].__setitem__("acquired_now", True))
    assert_rejected(build_review(), lambda review: review["operator_provided_evidence_requirements_review"]["requirements"].pop())
    assert_rejected(build_review(), lambda review: review["evidence_custody_and_digest_requirements_review"]["requirements"].pop())
    assert_rejected(build_review(), lambda review: review["candidate_results_review_requirements_review"]["requirements"].pop())


@pytest.mark.parametrize("field", ["predictive_usefulness", "profitability"])
def test_validator_rejects_acceptance(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, "accepted"))


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_validator_rejects_runtime_or_trading_authority(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, "AUTHORIZED"))


@pytest.mark.parametrize("field", ["results_review_domains", "results_review_findings", "outputs_generated", "recommendation", "next_chain", "next_gates", "risk_controls"])
def test_validator_rejects_missing_review_content_or_controls(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, []))


@pytest.mark.parametrize("field", [service.REVIEW_DIGEST_KEY, service.ACQUISITION_CANDIDATE_REVIEW_DIGEST_KEY, service.ACQUISITION_SCOPE_REVIEW_DIGEST_KEY, service.MISSING_AUTHORITY_MAPPING_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY])
def test_validator_rejects_missing_review_digest(field):
    assert_rejected(build_review(), lambda review: review.__setitem__(field, None))


def test_injected_source_follow_on_execution_is_validated_without_rerun():
    source_execution = service._committed_source_follow_on_execution()
    review = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(source_follow_on_execution=source_execution)
    assert review["source_follow_on_execution_reviewed"] is True
    source_execution["source_authority_acquisition_performed"] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureFollowOnExecutionResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(source_follow_on_execution=source_execution)


def test_writer_round_trips_to_requested_directory(tmp_path):
    review = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_FOLLOW_ON_EXECUTION_AFTER_RESULTS_REVIEW_RESULTS_REVIEW_STATUS.md"
    assert path.is_file()
    assert service.ARTIFACT_KIND in path.read_text(encoding="utf-8")
    assert review["review_status"] == service.REVIEW_STATUS


def test_markdown_contains_every_required_section():
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_results_review_markdown_v1(build_review())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Follow-On Execution After Results Review Results Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_service_source_contains_no_rerun_network_or_environment_mechanisms():
    source_text = Path(service.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "subprocess", "requests.", "httpx.", "urlopen(", "os.environ", "dotenv", "pytest.main",
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_follow_on_execution_after_results_review_v1(",
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(",
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1(",
    ):
        assert forbidden not in source_text
