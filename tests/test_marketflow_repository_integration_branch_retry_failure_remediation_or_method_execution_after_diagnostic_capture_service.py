from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_service
    as target,
)


RUN_TIMESTAMP = "2026-08-23T00:00:00Z"


def valid_execution() -> dict:
    return target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        run_timestamp_utc=RUN_TIMESTAMP
    )


def assert_rejected(execution: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterDiagnosticCaptureError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
            execution
        )


def write_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    stdout: str,
    stderr: str = "",
) -> Path:
    receipt = json.loads(target.DEFAULT_DURABLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    receipt["bounded_stdout_excerpt"] = stdout
    receipt["bounded_stderr_excerpt"] = stderr
    receipt[target.RECEIPT_DIGEST_KEY] = target._receipt_digest(receipt)
    monkeypatch.setattr(target.approval_source.source, "SOURCE_RECEIPT_DIGEST", receipt[target.RECEIPT_DIGEST_KEY])
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    return path


def test_default_committed_receipt_executes_successfully() -> None:
    execution = valid_execution()
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_SUCCESS
    assert execution["execution_status"] == target.EXECUTION_STATUS_SUCCESS
    assert execution["execution_scope"] == target.EXECUTION_SCOPE
    assert execution["selected_remediation_or_method_package"] == target.SELECTED_PACKAGE
    assert execution["blocked_reason"] is None
    assert execution["summary"]["blocker_count"] == 0


def test_execution_does_not_call_prohibited_source_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("source builders and execution functions must not run")

    names = [
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1",
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1",
    ]
    for name in names:
        if hasattr(target.approval_source, name):
            monkeypatch.setattr(target.approval_source, name, forbidden)
    assert valid_execution()["method_analysis_executed"] is True


@pytest.mark.parametrize(
    ("line", "family_id"),
    [
        ("AssertionError: expected 1 actual 2", "assertion_or_value_mismatch"),
        ("KeyError: missing_name", "missing_or_unexpected_field"),
        ("digest mismatch detected", "digest_or_hash_mismatch"),
        ("artifact kind mismatch", "artifact_status_scope_or_kind_mismatch"),
        ("boundary flag mismatch", "boundary_boolean_flag_mismatch"),
        ("fixture setup failed", "fixture_or_test_isolation_issue"),
        ("ModuleNotFoundError: package", "import_or_collection_error"),
        ("worktree path not found", "path_cwd_or_worktree_assumption"),
        ("evidence root unavailable", "evidence_root_or_file_availability"),
        ("JSONDecodeError while reading", "serialization_or_determinism_issue"),
        ("operator attestation mismatch", "approval_attestation_or_confirmation_mismatch"),
        ("NameError: missing symbol", "runtime_exception_or_name_error"),
        ("opaque diagnostic text", "insufficient_visible_pattern_detail"),
    ],
)
def test_supported_family_classification(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, line: str, family_id: str
) -> None:
    path = write_receipt(tmp_path, monkeypatch, stdout=line)
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path, run_timestamp_utc=RUN_TIMESTAMP
    )
    ids = {item["family_id"] for item in execution["observable_failure_families"]}
    assert family_id in ids


def test_family_order_is_count_descending_then_id_ascending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = write_receipt(
        tmp_path,
        monkeypatch,
        stdout="KeyError: x\nAssertionError: x\nKeyError: y\nAssertionError: y\nKeyError: z",
    )
    families = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path, run_timestamp_utc=RUN_TIMESTAMP
    )["observable_failure_families"]
    order = [(item["observable_evidence_count"], item["family_id"]) for item in families]
    assert order == sorted(order, key=lambda item: (-item[0], item[1]))


def test_snippets_are_redacted_and_bounded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = write_receipt(
        tmp_path,
        monkeypatch,
        stdout="\n".join(f"AssertionError marker-{index} token=secret-{index} {'x' * 700}" for index in range(8)),
    )
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path,
        run_timestamp_utc=RUN_TIMESTAMP,
        max_snippets_per_family=99,
        max_snippet_chars=999,
    )
    family = next(item for item in execution["observable_failure_families"] if item["family_id"] == "assertion_or_value_mismatch")
    assert len(family["representative_redacted_snippets"]) == 5
    assert all(len(item) <= 500 for item in family["representative_redacted_snippets"])
    assert all("secret-" not in item for item in family["representative_redacted_snippets"])


def test_family_records_and_summary_are_bounded_method_analysis() -> None:
    execution = valid_execution()
    required = {
        "family_id", "family_label", "classification_source", "classification_basis",
        "observable_evidence_count", "representative_redacted_snippets",
        "priority_1_modules_visible", "confidence", "limitations",
        "root_cause_claimed", "direct_remediation_recommended", "retry_success_claimed",
    }
    assert all(required <= set(item) for item in execution["observable_failure_families"])
    assert all(item["root_cause_claimed"] is False for item in execution["observable_failure_families"])
    summary = execution["failure_family_classification_summary"]
    assert summary["total_families_detected"] == len(execution["observable_failure_families"])
    assert summary["direct_remediation_ready"] is False
    assert summary["retry_ready"] is False
    assert summary["main_merge_ready"] is False


@pytest.mark.parametrize("field", target.SUCCESS_TRUE_FIELDS)
def test_success_fields_are_true(field: str) -> None:
    assert valid_execution()[field] is True


@pytest.mark.parametrize("field", target.COMMON_FALSE_FIELDS)
def test_closed_boundary_fields_are_false(field: str) -> None:
    assert valid_execution()[field] is False


def test_authority_strings_remain_closed() -> None:
    execution = valid_execution()
    assert execution["predictive_usefulness"] == execution["profitability"] == "not accepted"
    assert execution["runtime_use"] == execution["strategy_use"] == "NOT_AUTHORIZED"
    assert execution["paper_trading"] == execution["broker_execution"] == "NOT_AUTHORIZED"


def test_outputs_recommendation_chain_gates_and_controls() -> None:
    execution = valid_execution()
    assert execution["outputs"] == target.SUCCESS_OUTPUTS
    assert all(item["status"] == "GENERATED_METHOD_ANALYSIS_ONLY" for item in execution["outputs"])
    assert execution["recommended_next_task"] == target.SUCCESS_NEXT_TASK
    assert execution["next_chain"] == target.SUCCESS_NEXT_CHAIN
    assert execution["next_gates"] == target.NEXT_GATES
    assert execution["risk_controls"] == target.RISK_CONTROLS


def test_success_digests_are_deterministic() -> None:
    first, second = valid_execution(), valid_execution()
    for field in (
        target.EXECUTION_DIGEST_KEY,
        target.CLASSIFICATION_DIGEST_KEY,
        target.BOUNDED_ANALYSIS_DIGEST_KEY,
        target.MANIFEST_DIGEST_KEY,
    ):
        assert first[field] == second[field]


def test_missing_receipt_blocks(tmp_path: Path) -> None:
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=tmp_path / "missing.json", run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert execution["execution_status"] == target.EXECUTION_STATUS_BLOCKED
    assert execution["blocked_reason"] == "DURABLE_RECEIPT_FILE_UNAVAILABLE"


def test_invalid_json_blocks(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("not json", encoding="utf-8")
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert "BOUNDARY_FAILURE" in execution["blocked_reason"]


def test_receipt_digest_mismatch_blocks(tmp_path: Path) -> None:
    receipt = json.loads(target.DEFAULT_DURABLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    receipt["bounded_stdout_excerpt"] += "changed"
    path = tmp_path / "changed.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert "receipt digest mismatch" in execution["blocked_reason"]


def test_absent_bounded_excerpts_block(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = write_receipt(tmp_path, monkeypatch, stdout="", stderr="")
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=path, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert "bounded excerpts unavailable" in execution["blocked_reason"]


def test_invalid_source_approval_blocks() -> None:
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        source_approval={}, run_timestamp_utc=RUN_TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert execution["recommended_next_task"] == target.BLOCKED_NEXT_TASK
    assert execution[target.BLOCKED_MANIFEST_DIGEST_KEY]


def test_blocked_digest_is_deterministic(tmp_path: Path) -> None:
    kwargs = {"durable_receipt_path": tmp_path / "missing.json", "run_timestamp_utc": RUN_TIMESTAMP}
    first = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(**kwargs)
    second = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(**kwargs)
    assert first[target.BLOCKED_MANIFEST_DIGEST_KEY] == second[target.BLOCKED_MANIFEST_DIGEST_KEY]
    assert first["next_chain"] == target.BLOCKED_NEXT_CHAIN


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "execution_status", "execution_scope",
        "selected_remediation_or_method_package",
        "source_remediation_or_method_approval_after_diagnostic_capture_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_payload_review_digest",
        "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_payload_digest",
        "source_receipt_recovery_or_recapture_receipt_digest",
        "source_durable_receipt_path", "source_targeted_diagnostic_output_capture_execution_blocked_reason",
        "source_primary_failure_class", "source_planning_execution_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_detail_digest", "source_module_grouping_digest",
        "source_exit_code", "source_stdout_sha256", "source_stdout_byte_count",
        "priority_1_total_nodeids", "top_10_count_sum", "module_summary_module_count",
        "failed_or_errored_nodeids_count", "risk_controls", "outputs",
    ],
)
def test_validator_rejects_changed_required_field(field: str) -> None:
    execution = valid_execution()
    execution[field] = "changed"
    assert_rejected(execution)


@pytest.mark.parametrize(
    "field",
    [
        "remediation_execution_performed", "code_remediation_executed",
        "controlled_recapture_rerun_performed", "diagnostic_command_rerun_performed",
        "targeted_pytest_performed_in_execution", "full_pytest_performed",
        "retry_rerun_performed", "cache_read_in_execution", "cache_modified_in_execution",
        "pytest_cache_committed", "marketflow_outputs_committed", "terminal_logs_parsed",
        "operator_logs_parsed", "env_inspection_performed", "prior_lost_values_reconstructed",
        "full_stdout_reconstructed", "full_stderr_reconstructed", "failure_modules_classified",
        "error_modules_classified", "failure_error_separation_claimed", "first_failure_identified",
        "first_error_identified", "traceback_root_cause_claimed", "root_cause_claimed",
        "direct_code_remediation_recommended", "retry_success_claimed", "main_merge_readiness_claimed",
        "new_retry_candidate_created", "new_retry_executed", "main_merge_approval_created",
        "integration_execution_successful", "main_push_performed", "integration_branch_pushed",
        "evidence_regenerated", "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution", "dataset_generation_performed_in_execution",
        "metric_recomputation_from_raw_rows_performed", "model_training_performed",
        "strategy_scoring_performed", "trade_recommendations_generated",
    ],
)
def test_validator_rejects_opened_boundary(field: str) -> None:
    execution = valid_execution()
    execution[field] = True
    assert_rejected(execution)


@pytest.mark.parametrize(
    "field",
    [
        "source_durable_receipt_file_read", "remediation_or_method_execution_performed",
        "diagnostic_receipt_parsed_in_execution", "diagnostic_output_analyzed_in_execution",
        "failure_family_classification_performed", "observable_failure_families_generated",
        "ready_for_method_results_review_after_diagnostic_capture",
    ],
)
def test_validator_rejects_missing_success_fact(field: str) -> None:
    execution = valid_execution()
    execution[field] = False
    assert_rejected(execution)


def test_validator_accepts_success_and_blocked(tmp_path: Path) -> None:
    success = valid_execution()
    blocked = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        durable_receipt_path=tmp_path / "missing.json", run_timestamp_utc=RUN_TIMESTAMP
    )
    assert target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(success)["failed_checks"] == 0
    assert target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(blocked)["failed_checks"] == 0


def test_writer_writes_only_status_markdown(tmp_path: Path) -> None:
    execution = target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1(
        tmp_path, run_timestamp_utc=RUN_TIMESTAMP
    )
    files = list(tmp_path.iterdir())
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_SUCCESS
    assert [path.name for path in files] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_STATUS.md"
    ]


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_markdown_v1(valid_execution())
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Diagnostic Capture v1",
        "## Source Approval", "## Source Operator Review and Candidate",
        "## Source Diagnostic Results Review", "## Source Controlled Recapture Execution",
        "## Source Durable Receipt", "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence", "## Retry Failure Context",
        "## Execution Scope", "## Selected Remediation or Method Package",
        "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Method Input Source", "## Durable Receipt Integrity", "## Bounded Excerpt Integrity",
        "## Failure-Family Classification Method", "## Observable Failure Families",
        "## Family Confidence and Limitations", "## Unsupported Claims Boundary",
        "## Success or Blocked Disposition", "## Recommendation", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ]
    assert all(item in markdown for item in required)
