from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_service
    as service,
)


def _build() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
        run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def _reject(execution: dict) -> None:
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError
    ):
        service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
            execution
        )


def test_execution_is_offline_and_does_not_call_public_upstream_builders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def prohibited(*args, **kwargs):
        raise AssertionError("public upstream builder called")

    for name in dir(service.source):
        if name.startswith(("build_", "write_", "validate_")):
            monkeypatch.setattr(service.source, name, prohibited)
    execution = _build()
    assert execution["created_offline"] is True
    assert execution["governance_only"] is True
    assert execution["template_preparation_execution_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("execution_status", service.EXECUTION_STATUS),
        ("execution_scope", service.EXECUTION_SCOPE),
        ("source_approval_commit", service.SOURCE_APPROVAL_COMMIT),
        ("source_approval_digest", service.SOURCE_APPROVAL_DIGEST),
        ("source_attestation_digest", service.SOURCE_ATTESTATION_DIGEST),
        ("selected_operator_source_authority_evidence_package_preparation_package", service.SELECTED_PACKAGE),
        ("operator_source_authority_evidence_item_count", 0),
        ("operator_source_authority_evidence_item_template_count", 30),
        ("operator_fillable_evidence_item_template_count", 30),
        ("actual_covered_missing_authority_item_count", 0),
        ("actual_uncovered_missing_authority_item_count", 30),
        ("template_mapped_missing_authority_item_count", 30),
        ("mapped_missing_authority_item_count", 30),
        ("missing_authority_items_status", "MISSING_NOT_ACQUIRED"),
        ("acquisition_scope_section_count", 4),
        ("acceptable_source_artifact_type_count", 13),
        ("operator_provided_evidence_requirement_count", 10),
        ("evidence_custody_and_digest_requirement_count", 6),
        ("candidate_results_review_requirement_count", 16),
        ("observable_failure_family_count", 4),
        ("total_observable_evidence_items", 188),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("package_option_count", 12),
        ("available_package_count", 7),
        ("blocked_package_count", 5),
        ("approved_future_requirement_count", 62),
        ("approved_future_plan_step_count", 15),
        ("planned_output_count", 28),
        ("generated_output_count", 28),
        ("non_goal_count", 71),
        ("risk_control_count", 104),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ),
)
def test_execution_identity_scope_counts_and_authority_values(
    field: str, expected: object
) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_required_execution_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_unsupported_claims_and_actions_remain_false(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    (
        ("source_operator_review_commit", "139b03c87e9ce48b38435c7dcc0761c2300a7a4b"),
        ("source_operator_review_digest", "36e75dec88c71cc2e73109254a5a37b3b8e6415b598b0b8b4f7a025c3911bc22"),
        ("source_package_options_review_digest", "39aa0548562fd85763fc937fe3c306734a60749500b3607a75f42ad9b3e62ae8"),
        ("source_template_requirements_review_digest", "ac2fff06d39bd4361a81b7a26fec8bc43f18c8da1169bc38cde3ede9476d5c18"),
        ("source_missing_authority_coverage_review_digest", "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"),
        ("source_operator_review_manifest_digest", "30d2cba7243845b01df595ce922c07dae7a4d876345022e7d51046bf8b76c8df"),
        ("source_preparation_candidate_commit", "8d2944edfb7a54056f4a59c3d5817e823da80ce8"),
        ("source_preparation_candidate_digest", "8866cec5ecfcebe7fd52a4b38e0e47ea1d7f77e281f35bfd0e1fb0680d59b391"),
        ("source_preparation_package_options_digest", "5eb1efe8ccb86f243c3db861b983c86fff9b9b868b146ae866da29975cfca400"),
        ("source_preparation_template_requirements_digest", "3dd55cbdcf191c46c2bd5d314a20019c59b107029e6fd178754d79eddc06b2d7"),
        ("source_preparation_missing_authority_coverage_digest", "a8b22f743a1711bb83e2738e0412d30320f9119007e0eaee560b27885d8b25af"),
        ("source_preparation_manifest_digest", "c95671cf372c8bdf7f15c019bd994ae58f547d025117e12456fd780b5f9fd3d3"),
        ("source_failure_diagnosis_commit", "e51b3f58215a3ecb25f863655c79490cbdd65342"),
        ("source_failure_diagnosis_digest", "4ecc51acb6b037757e6dfcb406af8afc45627bc0bc5487feea2af88b79fc232c"),
        ("source_blocked_acquisition_execution_commit", "ff1635456a5c880f9a99a3b8359f94428383123e"),
        ("source_blocked_acquisition_execution_reason", "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PROVIDED"),
        ("source_blocked_acquisition_execution_manifest_digest", "57417475ee6eea2639afa1817262846b812add68de609ec055100b2afc8d92f3"),
        ("source_acquisition_approval_commit", "f8189e7421720879bd2a6d30f05353c8b65adff4"),
        ("source_acquisition_approval_digest", "1aadaddb1a8f27cce5e0903a7fdfdd7de4de7d2add8ff2a3e61d17b94bb74b69"),
        ("source_acquisition_attestation_digest", "db079d7b71f141dafba8439eba51caa1bc663ddf1158d3ea34b1f102ce4fb879"),
        ("source_follow_on_results_review_digest", "8745187fb404606e3ec99f5449373bf5148c0e2431fa74723fa0e1a4f9816bbb"),
        ("source_follow_on_execution_digest", "ff189df2bb4cf05ca18a56c76edb1d591bcc1312bbc770df49bf9363180b5208"),
        ("source_authority_acquisition_candidate_digest", "ef16430ea98fb1179005cd8194f7d6ee935a82fcf7be1c898763d729fa62bf91"),
        ("source_authority_acquisition_scope_digest", "a54e132f1e2badb409eec68873e65b2aa3abf016c1d8f364c974af141c648aa8"),
        ("source_missing_authority_to_source_evidence_mapping_digest", "71c9df4d61be3e3f9d89faa18d3a4666440d547f6208f9b2c339c8098303d334"),
        ("source_follow_on_approval_digest", "a4454f2a4fed53252be47103968558c1d4b59046906150cd9e9503e1730984a6"),
        ("source_follow_on_operator_review_digest", "c4073ce0ceb53e5dc7c651c294d40c863a532f02c7f5dc2571a7890044d6bfcb"),
        ("source_follow_on_candidate_digest", "59a1d5bf7de058901428892544f5731f3df613308618f4df760a5637973b6468"),
        ("source_results_review_digest", "df613ae941cf366af79be8d6e74e648ca72b3453a63a6830e53b0c0b51a9c1bb"),
        ("source_enrichment_execution_digest", "99036084adcbea62679c64d3dc2ae2a51a351f0c0fbf8933603c7ee3bd24624c"),
        ("historical_blocked_remediation_reason", "NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED"),
        ("historical_blocked_remediation_manifest_digest", "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"),
        ("source_durable_receipt_path", "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json"),
    ),
)
def test_source_chain_is_bound_to_approved_values(field: str, expected: object) -> None:
    assert _build()[field] == expected


def test_retry_priority_validation_diagnostic_and_planning_context_is_preserved() -> None:
    execution = _build()
    retry = execution["retry_failure_context"]
    assert (retry["counts"]["passed"], retry["counts"]["failed"], retry["counts"]["errors"], retry["counts"]["skipped"]) == (24877, 1292, 112, 7)
    assert retry["first_result_authoritative"] is True
    assert retry["pytest_passed"] is False and retry["pytest_failed"] is True
    assert retry["root_full_regression_is_retry_evidence"] is False
    assert len(execution["priority_1_target_modules"]) == 5
    assert sum(item["failed_or_errored_nodeid_count"] for item in execution["priority_1_target_modules"]) == 612
    validation = execution["priority1_validation_summary"]
    assert validation["pre_change_passed_count"] == validation["post_change_passed_count"] == 675
    assert validation["not_retry_evidence"] is True
    diagnostic = execution["diagnostic_capture_evidence_summary"]
    assert diagnostic["exit_code"] == 1
    assert diagnostic["stdout_byte_count"] == diagnostic["combined_output_byte_count"] == 1231380
    assert diagnostic["stderr_byte_count"] == 0
    assert diagnostic["redaction_checked"] is True
    assert len(execution["reviewed_observable_failure_families"]) == 4
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in execution["reviewed_observable_failure_families"])
    assert len(execution["reviewed_workstreams"]) == 4


def test_template_header_is_blank_non_secret_and_not_an_evidence_package() -> None:
    header = _build()["operator_fillable_evidence_package_template"]
    assert header == {
        "package_kind": "MARKETFLOW_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_FOR_RETRY_FAILURE_ACQUISITION_V1",
        "package_status": "OPERATOR_PROVIDED_FOR_SOURCE_AUTHORITY_ACQUISITION_EXECUTION_REVIEW_NOT_ACCEPTED_AS_FINAL_AUTHORITY",
        "package_source_owner_or_origin": "<REQUIRED_NON_EMPTY_SOURCE_OWNER_OR_ORIGIN>",
        "package_reference": "<REQUIRED_NON_EMPTY_SOURCE_REFERENCE>",
        "package_created_utc": "<REQUIRED_UTC_TIMESTAMP>",
        "package_digest_or_reproducible_provenance": "<REQUIRED_DIGEST_OR_REPRODUCIBLE_PROVENANCE>",
        "package_declares_no_secrets": "<REQUIRED_TRUE>",
        "package_declares_no_api_keys": "<REQUIRED_TRUE>",
        "package_declares_no_broker_credentials": "<REQUIRED_TRUE>",
        "package_declares_no_personal_financial_credentials": "<REQUIRED_TRUE>",
        "package_distinguishes_specification_from_observation": "<REQUIRED_TRUE>",
        "package_distinguishes_expected_from_actual": "<REQUIRED_TRUE>",
        "package_distinguishes_source_authority_from_diagnostic_output": "<REQUIRED_TRUE>",
        "evidence_items": "<REQUIRED_LIST_OF_ONE_OR_MORE_FILLED_EVIDENCE_ITEMS_FOR_FUTURE_ACQUISITION_REATTEMPT>",
        "template_only": True,
        "actual_evidence_package_created": False,
    }


def test_evidence_item_contract_and_all_thirty_template_rows_are_closed() -> None:
    execution = _build()
    contract = execution["operator_fillable_evidence_item_template_contract"]
    assert contract["results_review_required_before_use"] is True
    for field in ("direct_change_authorized_now", "remediation_authorized_now", "retry_authorized_now", "main_merge_authorized_now"):
        assert contract[field] is False
    rows = execution["operator_fillable_evidence_item_templates"]
    mappings = execution["missing_authority_to_source_evidence_mapping_review"]["items"]
    assert len(rows) == len(mappings) == 30
    assert {row["mapped_missing_authority_id"] for row in rows} == {item["missing_authority_id"] for item in mappings}
    for row in rows:
        assert row["section_id"] in service.ALLOWED_SECTION_IDS
        assert row["workstream_id"] in service.ALLOWED_WORKSTREAM_IDS
        assert row["allowed_acceptable_source_artifact_types"]
        assert set(row["allowed_acceptable_source_artifact_types"]) <= set(service.ALLOWED_SOURCE_ARTIFACT_TYPES)
        assert row["template_only"] is True
        assert row["actual_evidence_supplied"] is False
        assert row["actual_evidence_validated"] is False
        assert row["actual_evidence_bound"] is False
        assert row["current_status"] == "MISSING_NOT_ACQUIRED"


def test_inventory_checklist_outputs_gates_and_guidance_are_complete() -> None:
    execution = _build()
    assert execution["allowed_acquisition_scope_section_ids"] == list(service.ALLOWED_SECTION_IDS)
    assert execution["allowed_workstream_ids"] == list(service.ALLOWED_WORKSTREAM_IDS)
    assert execution["acceptable_source_artifact_type_inventory"] == list(service.ALLOWED_SOURCE_ARTIFACT_TYPES)
    assert len(execution["operator_fillable_preparation_checklist"]) == 62
    assert all(item["template_requirement_included"] is True and item["actual_evidence_satisfied"] is False for item in execution["operator_fillable_preparation_checklist"])
    assert len(execution["outputs"]) == len(service.OUTPUT_IDS) == 28
    assert all(item["status"] == "GENERATED_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_TEMPLATE_PREPARATION_EXECUTION_ONLY" for item in execution["outputs"])
    assert execution["source_owner_request_guidance"]["contact_performed"] is False
    assert execution["source_owner_request_guidance"]["actual_source_owner_information_supplied"] is False
    assert execution["no_secret_boundary"]["secrets_captured"] is False
    assert execution["results_review_before_use"]["required"] is True
    assert execution["results_review_before_use"]["actual_package_use_authorized"] is False
    assert len(execution["next_chain"]) == 10
    assert len(execution["next_gates"]) == 15
    assert len(execution["risk_controls"]) == 115
    assert execution["risk_control_count"] == 104


def test_digests_are_deterministic_and_validator_accepts_valid_execution() -> None:
    first, second = _build(), _build()
    digest_keys = (
        service.EXECUTION_DIGEST_KEY,
        service.TEMPLATE_DIGEST_KEY,
        service.EVIDENCE_ITEM_TEMPLATE_DIGEST_KEY,
        service.PREPARATION_CHECKLIST_DIGEST_KEY,
        service.COVERAGE_DIGEST_KEY,
        service.MANIFEST_DIGEST_KEY,
    )
    assert all(first[key] == second[key] and len(first[key]) == 64 for key in digest_keys)
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(first)
    assert validation["failed_checks"] == validation["blocker_count"] == 0
    assert validation["passed_checks"] == validation["total_checks"]


@pytest.mark.parametrize(
    "field",
    (
        "artifact_kind", "execution_status", "execution_scope", "source_approval_digest",
        "source_attestation_digest", "selected_operator_source_authority_evidence_package_preparation_package",
        "source_operator_review_digest", "source_preparation_candidate_digest",
        "source_failure_diagnosis_digest", "source_blocked_acquisition_execution_reason",
        "retry_pytest_failed_count", "priority_1_total_nodeids", "source_exit_code",
        "observable_failure_family_count", "mapped_missing_authority_item_count",
        "risk_control_count", "recommended_next_task", "runtime_use", "broker_execution",
    ),
)
def test_validator_rejects_changed_scalar(field: str) -> None:
    execution = _build()
    execution[field] = "WRONG"
    _reject(execution)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_open_required_true_boundary(field: str) -> None:
    execution = _build()
    execution[field] = False
    _reject(execution)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_open_prohibited_boundary(field: str) -> None:
    execution = _build()
    execution[field] = True
    _reject(execution)


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("operator_fillable_evidence_package_template",), None),
        (("operator_fillable_evidence_item_templates",), []),
        (("operator_fillable_evidence_item_templates", 0, "mapped_missing_authority_id"), "UNKNOWN"),
        (("operator_fillable_evidence_item_templates", 0, "section_id"), "UNKNOWN"),
        (("operator_fillable_evidence_item_templates", 0, "workstream_id"), "UNKNOWN"),
        (("operator_fillable_evidence_item_templates", 0, "allowed_acceptable_source_artifact_types"), ["UNKNOWN"]),
        (("operator_fillable_evidence_item_templates", 0, "direct_change_authorized_now"), True),
        (("operator_fillable_evidence_item_templates", 0, "remediation_authorized_now"), True),
        (("operator_fillable_evidence_item_templates", 0, "retry_authorized_now"), True),
        (("operator_fillable_evidence_item_templates", 0, "main_merge_authorized_now"), True),
        (("outputs",), []),
        (("next_chain",), []),
        (("next_gates",), []),
        (("risk_controls",), []),
        (("reviewed_observable_failure_families", 0, "confidence"), "LOW"),
        (("reviewed_workstreams", 0, "workstream_id"), "UNKNOWN"),
    ),
)
def test_validator_rejects_changed_template_context_or_controls(path: tuple, value: object) -> None:
    execution = _build()
    target = execution
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    _reject(execution)


def test_source_approval_injection_must_match_committed_approval() -> None:
    approval = service._committed_source_approval()
    approval["source_approval_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
            source_approval=approval,
            run_timestamp_utc="2026-08-23T00:00:00Z",
        )


@pytest.mark.parametrize("timestamp", ("2026-08-23", "", None))
def test_explicit_invalid_timestamp_is_rejected(timestamp: object) -> None:
    if timestamp is None:
        execution = _build()
        execution["run_timestamp_utc"] = None
        _reject(execution)
        return
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
            run_timestamp_utc=timestamp
        )


def test_writer_and_markdown_create_only_the_requested_status_artifact(tmp_path: Path) -> None:
    execution = service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
        tmp_path, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    markdown = files[0].read_text(encoding="utf-8")
    assert execution[service.EXECUTION_DIGEST_KEY] in markdown
    assert all(f"## {section}" in markdown for section in service.MARKDOWN_SECTIONS)
    assert service.RECOMMENDED_NEXT_TASK in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown


@pytest.mark.parametrize("protected", (".marketflow", ".pytest_cache", ".env"))
def test_writer_rejects_protected_output_directories(tmp_path: Path, protected: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorSourceAuthorityEvidencePackagePreparationExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1(
            tmp_path / protected,
            run_timestamp_utc="2026-08-23T00:00:00Z",
        )


def test_package_level_exports_are_available() -> None:
    import marketflow.services as exports

    assert exports.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_PREPARATION_EXECUTION_AFTER_APPROVAL_DIGEST_KEY == service.EXECUTION_DIGEST_KEY
    assert exports.execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1 is service.execute_marketflow_repository_integration_branch_retry_failure_operator_source_authority_evidence_package_preparation_execution_after_approval_v1
