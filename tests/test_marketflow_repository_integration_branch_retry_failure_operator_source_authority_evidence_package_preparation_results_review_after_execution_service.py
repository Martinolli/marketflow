from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1()


def _reject(review: dict) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(review)


def test_review_builds_offline_without_calling_source_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def prohibited(*args, **kwargs):
        raise AssertionError("source builder called")

    for name in dir(service.source):
        if name.startswith(("build_", "execute_", "write_", "validate_", "_assemble_", "_committed_")):
            monkeypatch.setattr(service.source, name, prohibited)
    review = _build()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True
    assert review["template_execution_rerun_performed"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("artifact_kind", service.ARTIFACT_KIND), ("schema_version", service.SCHEMA_VERSION),
        ("results_review_status", service.RESULTS_REVIEW_STATUS), ("results_review_scope", service.RESULTS_REVIEW_SCOPE),
        ("source_execution_commit", service.SOURCE_EXECUTION_COMMIT), ("source_execution_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_execution_status", service.source.EXECUTION_STATUS), ("source_execution_scope", service.source.EXECUTION_SCOPE),
        ("source_execution_digest", service.SOURCE_EXECUTION_DIGEST), ("source_package_template_digest", service.SOURCE_PACKAGE_TEMPLATE_DIGEST),
        ("source_evidence_item_template_digest", service.SOURCE_EVIDENCE_ITEM_TEMPLATE_DIGEST),
        ("source_preparation_checklist_digest", service.SOURCE_PREPARATION_CHECKLIST_DIGEST),
        ("source_template_coverage_digest", service.SOURCE_TEMPLATE_COVERAGE_DIGEST),
        ("source_execution_manifest_digest", service.SOURCE_EXECUTION_MANIFEST_DIGEST),
        ("selected_operator_source_authority_evidence_package_preparation_package", service.SELECTED_PACKAGE),
        ("operator_source_authority_evidence_item_count", 0), ("operator_source_authority_evidence_item_template_count", 30),
        ("operator_fillable_evidence_item_template_count", 30), ("reviewed_template_row_count", 30),
        ("actual_covered_missing_authority_item_count", 0), ("actual_uncovered_missing_authority_item_count", 30),
        ("template_mapped_missing_authority_item_count", 30), ("mapped_missing_authority_item_count", 30),
        ("missing_authority_items_status", "MISSING_NOT_ACQUIRED"), ("acquisition_scope_section_count", 4),
        ("acceptable_source_artifact_type_count", 13), ("operator_provided_evidence_requirement_count", 10),
        ("evidence_custody_and_digest_requirement_count", 6), ("candidate_results_review_requirement_count", 16),
        ("observable_failure_family_count", 4), ("total_observable_evidence_items", 188),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069), ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29), ("package_option_count", 12), ("available_package_count", 7),
        ("blocked_package_count", 5), ("approved_future_requirement_count", 62), ("approved_future_plan_step_count", 15),
        ("planned_output_count", 28), ("source_generated_output_count", 28), ("review_generated_output_count", 30),
        ("non_goal_count", 71), ("risk_control_count", 104), ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"), ("runtime_use", "NOT_AUTHORIZED"), ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ),
)
def test_review_identity_source_execution_counts_and_authority(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_review_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_prohibited_claims_and_actions_remain_false(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize("field", tuple(service.SOURCE_BINDINGS))
def test_all_committed_source_bindings_are_preserved(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


def test_retry_priority_validation_and_diagnostic_context_is_bound() -> None:
    review = _build()
    retry = review["retry_failure_context"]
    assert retry["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert retry["first_result_authoritative"] is True
    assert retry["pytest_passed"] is False and retry["pytest_failed"] is True
    assert retry["root_full_regression_is_retry_evidence"] is False
    assert len(review["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]) == 612
    validation = review["priority1_validation_summary"]
    assert validation["pre_change_passed_count"] == validation["post_change_passed_count"] == 675
    assert validation["not_retry_evidence"] is True
    diagnostic = review["diagnostic_capture_evidence_summary"]
    assert diagnostic["exit_code"] == 1 and diagnostic["diagnostic_only"] is True
    assert diagnostic["stdout_byte_count"] == diagnostic["combined_output_byte_count"] == 1231380
    assert diagnostic["stderr_byte_count"] == 0


def test_families_workstreams_scope_and_mapping_are_reviewed() -> None:
    review = _build()
    assert len(review["reviewed_observable_failure_families"]) == 4
    assert all(item["confidence"] == "HIGH" and item["observable_evidence_count"] == 47 for item in review["reviewed_observable_failure_families"])
    assert len(review["reviewed_workstreams"]) == 4
    assert {item["workstream_id"] for item in review["reviewed_workstreams"]} == set(service.source.ALLOWED_WORKSTREAM_IDS)
    mapping = review["missing_authority_mapping"]
    assert len(mapping) == 30
    assert {item["missing_authority_id"] for item in mapping} == {f"MA-{index:03d}" for index in range(1, 31)}
    assert all(item["current_status"] == "MISSING_NOT_ACQUIRED" for item in mapping)
    assert review["acceptable_source_artifact_type_inventory"] == list(service.source.ALLOWED_SOURCE_ARTIFACT_TYPES)


def test_package_header_template_review_preserves_required_placeholders() -> None:
    header = _build()["package_header_template_review"]
    assert header["package_kind"] == "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1"
    assert header["package_status"] == "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY"
    for field in ("package_source_owner_or_origin", "package_reference", "package_created_utc", "package_digest_or_reproducible_provenance", "evidence_items"):
        assert header[field].startswith("<REQUIRED_")
    for field in ("package_declares_no_secrets", "package_declares_no_api_keys", "package_declares_no_broker_credentials", "package_declares_no_personal_financial_credentials", "package_distinguishes_specification_from_observation", "package_distinguishes_expected_from_actual", "package_distinguishes_source_authority_from_diagnostic_output"):
        assert header[field] == "<REQUIRED_TRUE>"
    assert header["template_only"] is True and header["actual_evidence_package_created"] is False


def test_evidence_item_contract_and_all_thirty_rows_remain_template_only() -> None:
    review = _build()
    contract = review["evidence_item_template_review"]
    assert contract["results_review_required_before_use"] is True
    for field in ("direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now"):
        assert contract[field] is False
    rows = review["thirty_missing_authority_template_rows_review"]
    assert len(rows) == 30
    for row in rows:
        assert row["mapped_missing_authority_id"] in {item["missing_authority_id"] for item in review["missing_authority_mapping"]}
        assert row["section_id"] in service.source.ALLOWED_SECTION_IDS
        assert row["workstream_id"] in service.source.ALLOWED_WORKSTREAM_IDS
        assert set(row["allowed_acceptable_source_artifact_types"]) <= set(service.source.ALLOWED_SOURCE_ARTIFACT_TYPES)
        assert row["template_only"] is row["results_review_required_before_use"] is True
        assert row["current_status"] == "MISSING_NOT_ACQUIRED"
        assert all(row[field] is False for field in ("actual_evidence_supplied", "actual_evidence_validated", "actual_evidence_bound", "direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now"))


def test_checklist_guidance_actual_absence_and_zero_coverage_are_reviewed() -> None:
    review = _build()
    assert review["preparation_checklist_review"] == {"source_requirement_count": 62, "template_requirements_included": 62, "actual_evidence_satisfied": 0}
    assert review["source_owner_request_guidance_review"]["contact_performed"] is False
    assert review["custody_and_digest_guidance_review"]["requirement_count"] == 6
    assert review["no_secret_boundary_review"]["secrets_captured"] is False
    assert review["results_review_before_use"]["required"] is True
    assert not any(review["actual_evidence_absence"].values())
    assert review["template_coverage_review"] == {"template_rows": 30, "actual_covered": 0, "actual_uncovered": 30, "status": "MISSING_NOT_ACQUIRED"}
    assert review["template_source_authority_disposition"] == "TEMPLATE_NOT_ACTUAL_EVIDENCE_NOT_SOURCE_AUTHORITY_NOT_ACQUIRED_EVIDENCE"


def test_findings_domains_outputs_recommendation_gates_and_controls_are_complete() -> None:
    review = _build()
    assert len(review["review_findings"]) == 24
    assert len(review["review_domains"]) == 13
    assert len(review["outputs"]) == len(service.OUTPUT_IDS) == 30
    assert all(item["status"] == "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_RESULTS_REVIEW_ONLY" for item in review["outputs"])
    assert review["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["recommended_action"] == service.RECOMMENDED_ACTION
    assert len(review["next_chain"]) == 13 and len(review["next_gates"]) == 17
    assert len(review["risk_controls"]) == 100
    assert review["risk_control_count"] == 104


def test_review_digests_are_deterministic_and_validator_accepts() -> None:
    first, second = _build(), _build()
    keys = (service.RESULTS_REVIEW_DIGEST_KEY, service.TEMPLATE_REVIEW_DIGEST_KEY, service.EVIDENCE_ITEM_TEMPLATE_REVIEW_DIGEST_KEY, service.CHECKLIST_REVIEW_DIGEST_KEY, service.COVERAGE_REVIEW_DIGEST_KEY, service.MANIFEST_DIGEST_KEY)
    assert all(first[key] == second[key] and len(first[key]) == 64 for key in keys)
    result = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(first)
    assert result["failed_checks"] == result["blocker_count"] == 0
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    "field",
    ("artifact_kind", "results_review_status", "results_review_scope", "source_execution_digest", "source_package_template_digest",
     "source_evidence_item_template_digest", "source_preparation_checklist_digest", "source_template_coverage_digest",
     "source_execution_manifest_digest", "selected_operator_source_authority_evidence_package_preparation_package",
     "source_approval_digest", "source_attestation_digest", "source_operator_review_digest", "source_preparation_candidate_digest",
     "source_failure_diagnosis_digest", "source_blocked_acquisition_execution_reason", "priority_1_total_nodeids",
     "actual_covered_missing_authority_item_count", "recommended_next_task", "runtime_use", "broker_execution"),
)
def test_validator_rejects_changed_scalar(field: str) -> None:
    review = _build()
    review[field] = "WRONG"
    _reject(review)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_missing_required_review_fact(field: str) -> None:
    review = _build()
    review[field] = False
    _reject(review)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_prohibited_boundary(field: str) -> None:
    review = _build()
    review[field] = True
    _reject(review)


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("package_header_template_review",), None), (("evidence_item_template_review",), None),
        (("thirty_missing_authority_template_rows_review",), []),
        (("thirty_missing_authority_template_rows_review", 0, "mapped_missing_authority_id"), "UNKNOWN"),
        (("thirty_missing_authority_template_rows_review", 0, "section_id"), "UNKNOWN"),
        (("thirty_missing_authority_template_rows_review", 0, "workstream_id"), "UNKNOWN"),
        (("thirty_missing_authority_template_rows_review", 0, "allowed_acceptable_source_artifact_types"), ["UNKNOWN"]),
        (("thirty_missing_authority_template_rows_review", 0, "direct_change_authorized_now"), True),
        (("thirty_missing_authority_template_rows_review", 0, "remediation_authorized_now"), True),
        (("thirty_missing_authority_template_rows_review", 0, "retry_authorized_now"), True),
        (("thirty_missing_authority_template_rows_review", 0, "main_merge_authorized_now"), True),
        (("reviewed_observable_failure_families", 0, "confidence"), "LOW"),
        (("reviewed_workstreams", 0, "workstream_id"), "UNKNOWN"), (("review_findings",), []),
        (("review_domains",), []), (("outputs",), []), (("next_chain",), []), (("next_gates",), []), (("risk_controls",), []),
    ),
)
def test_validator_rejects_changed_template_context_or_review_content(path: tuple, value: object) -> None:
    review = _build()
    target = review
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    _reject(review)


@pytest.mark.parametrize(
    ("field", "value"),
    (("source_execution_digest", "0" * 64), ("source_package_template_digest", "0" * 64),
     ("source_evidence_item_template_digest", "0" * 64), ("source_preparation_checklist_digest", "0" * 64),
     ("source_template_coverage_digest", "0" * 64), ("source_execution_manifest_digest", "0" * 64),
     ("source_approval_digest", "0" * 64), ("source_blocked_acquisition_execution_reason", "WRONG")),
)
def test_injected_source_execution_rejects_changed_binding(field: str, value: object) -> None:
    execution = service._committed_source_execution()
    execution[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(source_execution=execution)


@pytest.mark.parametrize(
    ("path", "value"),
    ((("evidence_item_template_rows",), []), (("evidence_item_template_rows", 0, "mapped_missing_authority_id"), "UNKNOWN"),
     (("evidence_item_template_rows", 0, "section_id"), "UNKNOWN"), (("evidence_item_template_rows", 0, "workstream_id"), "UNKNOWN"),
     (("evidence_item_template_rows", 0, "allowed_acceptable_source_artifact_types"), ["UNKNOWN"]),
     (("evidence_item_template_rows", 0, "direct_change_authorized_now"), True),
     (("evidence_item_template_rows", 0, "actual_evidence_supplied"), True)),
)
def test_injected_source_execution_rejects_changed_template_rows(path: tuple, value: object) -> None:
    execution = service._committed_source_execution()
    target = execution
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(source_execution=execution)


def test_writer_and_markdown_create_only_requested_status(tmp_path: Path) -> None:
    review = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    markdown = files[0].read_text(encoding="utf-8")
    assert review[service.RESULTS_REVIEW_DIGEST_KEY] in markdown
    assert all(f"## {section}" in markdown for section in service.MARKDOWN_SECTIONS)
    assert service.RECOMMENDED_NEXT_TASK in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_directories(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1(tmp_path / protected)


def test_package_exports_are_available() -> None:
    import marketflow.services as exports

    assert exports.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_RESULTS_REVIEW_AFTER_EXECUTION_DIGEST_KEY == service.RESULTS_REVIEW_DIGEST_KEY
    assert exports.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1 is service.build_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_results_review_after_execution_v1
