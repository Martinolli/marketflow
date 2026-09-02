from __future__ import annotations

from copy import deepcopy
import hashlib
import json

import pytest

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_service
    as service,
)


def _module_counts() -> list[tuple[str, int]]:
    top = list(zip(service.EXPECTED_TOP_FIVE_PATHS, service.EXPECTED_LARGEST_COUNTS))
    tier_two = [(f"tests/test_tier_two_{index:02d}.py", count) for index, count in enumerate([100, 95, 90, 87, 85], 1)]
    tier_three_counts = [18] * 12 + [17] * 7
    tier_three = [(f"tests/test_tier_three_{index:02d}.py", count) for index, count in enumerate(tier_three_counts, 1)]
    return [*top, *tier_two, *tier_three]


def _snapshot() -> dict:
    failed = [
        f"{module_path}::test_{item:04d}"
        for module_path, count in _module_counts()
        for item in range(count)
    ]
    nodeids = failed + [
        f"tests/test_inventory_only.py::test_{item:05d}"
        for item in range(service.EXPECTED_NODEIDS_COUNT - len(failed))
    ]
    return {"lastfailed": failed, "nodeids": nodeids}


@pytest.fixture(scope="module")
def success() -> dict:
    return service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
        complete_detail_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


@pytest.fixture(scope="module")
def blocked() -> dict:
    snapshot = _snapshot()
    snapshot["lastfailed_sha256"] = "0" * 64
    return service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
        complete_detail_snapshot=snapshot, run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def test_success_execution_builds_from_deterministic_complete_detail_snapshot(success: dict) -> None:
    assert success["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert success["execution_status"] == service.SUCCESS_STATUS
    assert success["execution_scope"] == service.EXECUTION_SCOPE
    assert success["materialization_package_executed"] is True
    assert success["complete_29_row_detail_materialized"] is True
    assert success["complete_29_row_detail_exposed"] is True
    assert success["complete_29_row_detail_bound"] is True
    assert success["complete_29_row_detail_committed_source_created"] is True


def test_success_execution_builds_from_temporary_reviewed_cache_files(tmp_path, monkeypatch) -> None:
    snapshot = _snapshot()
    last_raw = json.dumps({nodeid: True for nodeid in snapshot["lastfailed"]}, sort_keys=True).encode()
    node_raw = json.dumps(snapshot["nodeids"], sort_keys=True).encode()
    (tmp_path / "lastfailed").write_bytes(last_raw)
    (tmp_path / "nodeids").write_bytes(node_raw)
    monkeypatch.setattr(service, "EXPECTED_LASTFAILED_SHA256", hashlib.sha256(last_raw).hexdigest())
    monkeypatch.setattr(service, "EXPECTED_NODEIDS_SHA256", hashlib.sha256(node_raw).hexdigest())
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
        cache_root=tmp_path, run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert execution["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert execution["reviewed_cache_verification"]["deterministic_test_snapshot_injected"] is False
    assert execution["cache_modified"] is False


@pytest.mark.parametrize("missing", ["lastfailed", "nodeids"])
def test_blocked_execution_when_cache_file_missing(tmp_path, missing: str) -> None:
    if missing != "lastfailed":
        (tmp_path / "lastfailed").write_text("{}", encoding="utf-8")
    if missing != "nodeids":
        (tmp_path / "nodeids").write_text("[]", encoding="utf-8")
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(cache_root=tmp_path)
    assert execution["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert execution["blocked_reason"]


@pytest.mark.parametrize("hash_field", ["lastfailed_sha256", "nodeids_sha256"])
def test_blocked_execution_when_cache_hash_mismatches(hash_field: str) -> None:
    snapshot = _snapshot()
    snapshot[hash_field] = "0" * 64
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(complete_detail_snapshot=snapshot)
    assert execution["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert "SHA256_MISMATCH" in execution["blocked_reason"]


@pytest.mark.parametrize("mutation", ["lastfailed_count", "nodeids_count", "subset", "module_count", "total", "top_counts", "top_paths", "top_ten", "tier_sums"])
def test_blocked_execution_for_invalid_cache_or_materialized_integrity(mutation: str) -> None:
    snapshot = _snapshot()
    if mutation in {"lastfailed_count", "total"}:
        snapshot["lastfailed"].pop()
    elif mutation == "nodeids_count":
        snapshot["nodeids"].pop()
    elif mutation == "subset":
        snapshot["nodeids"].remove(snapshot["lastfailed"][0])
    elif mutation == "module_count":
        snapshot["lastfailed"][0] = "tests/test_extra_module.py::test_extra"
        snapshot["nodeids"].append(snapshot["lastfailed"][0])
        snapshot["nodeids"].pop()
    elif mutation == "top_counts":
        snapshot["lastfailed"][0] = "tests/test_tier_three_01.py::test_shifted"
        snapshot["nodeids"][0] = snapshot["lastfailed"][0]
    elif mutation == "top_paths":
        original = service.EXPECTED_TOP_FIVE_PATHS[0]
        snapshot["lastfailed"] = [nodeid.replace(original, "tests/test_alternate_top.py") for nodeid in snapshot["lastfailed"]]
        snapshot["nodeids"] = [nodeid.replace(original, "tests/test_alternate_top.py") for nodeid in snapshot["nodeids"]]
    else:
        source_path = "tests/test_tier_two_05.py"
        target_path = "tests/test_tier_three_01.py"
        source_index = next(i for i, nodeid in enumerate(snapshot["lastfailed"]) if nodeid.startswith(source_path))
        replacement = snapshot["lastfailed"][source_index].replace(source_path, target_path)
        snapshot["lastfailed"][source_index] = replacement
        snapshot["nodeids"][source_index] = replacement
    execution = service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(complete_detail_snapshot=snapshot)
    assert execution["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert execution["complete_29_row_detail_materialized"] is False


def test_success_source_digests_retry_facts_and_summary_are_bound(success: dict) -> None:
    assert success["source_complete_29_row_materialization_approval_digest"] == service.SOURCE_APPROVAL_DIGEST
    assert success["source_complete_29_row_materialization_operator_review_digest"] == "72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90"
    assert success["source_complete_29_row_materialization_candidate_digest"] == "4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061"
    assert success["source_detail_exposure_or_binding_execution_failure_diagnosis_digest"] == "8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41"
    assert success["primary_failure_class"] == "COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE"
    assert success["source_detail_exposure_or_binding_execution_blocked_digest"] == "9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca"
    assert success["source_detail_exposure_or_binding_execution_blocked_manifest_digest"] == "c732eac857725728bb856f2d145eb86101ce1f839ddca740b66db4d48ae3aa4c"
    assert success["source_detail_exposure_or_binding_execution_blocked_reason"] == "COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE"
    assert success["source_module_grouping_source_recovery_results_review_digest"] == "1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266"
    assert success["source_module_grouping_source_recovery_detail_digest"] == "a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5"
    assert success["source_module_grouping_digest"] == "34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff"
    assert success["retry_execution_commit"] == "ab178b65c69f0274b0abbf9c20df102d35e78d34"
    assert success["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert success["recovered_module_grouping_source_summary"]["module_summary_module_count"] == 29
    assert len(success["top_module_summary"]) == 5
    assert success["source_approval_authorizes_execution"] is True


def test_success_cache_verification_and_complete_rows(success: dict) -> None:
    verification = success["reviewed_cache_verification"]
    assert verification["lastfailed_hash_verified"] is True
    assert verification["nodeids_hash_verified"] is True
    assert verification["entry_counts_verified"] is True
    assert verification["lastfailed_subset_of_nodeids"] is True
    rows = success["complete_29_row_module_grouping_detail_source"]
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert [row["module_path"] for row in rows[:5]] == service.EXPECTED_TOP_FIVE_PATHS
    assert [row["failed_or_errored_nodeid_count"] for row in rows[:5]] == service.EXPECTED_LARGEST_COUNTS
    assert all(row["sample_nodeids_bounded_count"] <= 5 for row in rows)
    assert all(len(row["sample_nodeids_bounded"]) == row["sample_nodeids_bounded_count"] for row in rows)
    assert all(row["source"] == service.ROW_SOURCE and row["basis"] == service.ROW_BASIS for row in rows)


def test_complete_29_row_source_is_committed_and_digest_bound() -> None:
    rows = service.committed_complete_29_row_module_grouping_detail_source_v1()
    assert len(service.COMMITTED_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE) == 29
    assert len(rows) == 29
    assert sum(row["failed_or_errored_nodeid_count"] for row in rows) == 1404
    assert semantic_digest(rows) == "1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7"


def test_top_concentration_priority_tiers_and_outputs_are_preserved(success: dict) -> None:
    assert success["top_5_count_sum"] == 612
    assert success["top_5_percentage_of_failed_or_errored_nodeids"] == "43.58974359"
    assert success["top_10_count_sum"] == 1069
    assert success["top_10_percentage_of_failed_or_errored_nodeids"] == "76.13960114"
    assert success["priority_tier_1_count_sum"] == 612
    assert success["priority_tier_2_count_sum"] == 457
    assert success["priority_tier_3_count_sum"] == 335
    assert [item["output_id"] for item in success["outputs_generated"]] == service.OUTPUT_IDS
    assert all(item["status"] == "GENERATED_RESEARCH_ONLY" for item in success["outputs_generated"])
    assert success["ready_for_complete_29_row_materialization_results_review"] is True


def test_success_and_blocked_digests_are_deterministic(success: dict, blocked: dict) -> None:
    execution_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest"
    payload_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest"
    manifest_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest"
    blocked_key = "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_blocked_manifest_digest"
    rebuilt = service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
        complete_detail_snapshot=_snapshot(), run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    assert rebuilt == success
    assert success[execution_key] == service.marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_digest_v1(success)
    assert success[payload_key] == rebuilt[payload_key]
    assert success[manifest_key] == rebuilt[manifest_key]
    second_blocked = deepcopy(_snapshot())
    second_blocked["lastfailed_sha256"] = "0" * 64
    assert service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(complete_detail_snapshot=second_blocked)[blocked_key] == blocked[blocked_key]


def test_all_unsupported_claims_and_downstream_authorities_remain_closed(success: dict) -> None:
    assert all(success[field] is False for field in service.FALSE_BOUNDARIES)
    assert all(success[field] is False for field in service.UNSUPPORTED_CLAIMS_FIELDS)
    assert success["module_paths_recovered_by_execution"] is False
    assert success["per_module_counts_recovered_by_execution"] is False
    assert success["bounded_nodeid_samples_recovered_by_execution"] is False
    assert success["module_grouping_recovered_in_execution"] is False
    assert success["cache_modified"] is False
    assert success["predictive_usefulness"] == service.NOT_ACCEPTED
    assert success["profitability"] == service.NOT_ACCEPTED
    assert success["runtime_use"] == service.NOT_AUTHORIZED
    assert success["broker_execution"] == service.NOT_AUTHORIZED


def test_checklists_and_validators_accept_success_and_blocked(success: dict, blocked: dict) -> None:
    success_validation = service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(success)
    blocked_validation = service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(blocked)
    assert success_validation["passed_checks"] == success_validation["total_checks"] == 107
    assert blocked_validation["passed_checks"] == blocked_validation["total_checks"] == 107
    assert success_validation["failed_checks"] == blocked_validation["failed_checks"] == 0
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert blocked["blocked_reason"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "OTHER"), ("execution_status", "OTHER"), ("execution_scope", "OTHER"),
        ("selected_complete_29_row_materialization_package", "OTHER"),
        ("source_complete_29_row_materialization_approval_digest", "0" * 64),
        ("source_complete_29_row_materialization_operator_review_digest", "0" * 64),
        ("source_complete_29_row_materialization_candidate_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_failure_diagnosis_digest", "0" * 64),
        ("primary_failure_class", "OTHER"),
        ("source_detail_exposure_or_binding_execution_blocked_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", "0" * 64),
        ("source_detail_exposure_or_binding_execution_blocked_reason", ""),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_failure_context", {}),
        ("recovered_module_grouping_source_summary", {}), ("top_module_summary", []),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068), ("risk_controls", []),
    ],
)
def test_validator_rejects_changed_required_field(success: dict, field: str, value: object) -> None:
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES + service.UNSUPPORTED_CLAIMS_FIELDS)
def test_validator_rejects_open_boundary(success: dict, field: str) -> None:
    changed = deepcopy(success)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError):
        service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(changed)


def test_validator_rejects_missing_rows_total_top_paths_tiers_and_oversized_samples(success: dict) -> None:
    mutations = []
    changed = deepcopy(success); changed["complete_29_row_module_grouping_detail_source"] = []; mutations.append(changed)
    changed = deepcopy(success); changed["complete_29_row_module_grouping_detail_source"][0]["failed_or_errored_nodeid_count"] -= 1; mutations.append(changed)
    changed = deepcopy(success); changed["complete_29_row_module_grouping_detail_source"][0]["module_path"] = "tests/test_other.py"; mutations.append(changed)
    changed = deepcopy(success); changed["complete_29_row_module_grouping_detail_source"][9]["failed_or_errored_nodeid_count"] -= 1; mutations.append(changed)
    changed = deepcopy(success); changed["complete_29_row_module_grouping_detail_source"][0]["sample_nodeids_bounded"].append("extra"); mutations.append(changed)
    for mutation in mutations:
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError):
            service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(mutation)


def test_validator_rejects_missing_success_and_blocked_digests(success: dict, blocked: dict) -> None:
    for artifact, key in (
        (success, "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialized_payload_digest"),
        (success, "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_digest_manifest_digest"),
        (blocked, "marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_blocked_manifest_digest"),
    ):
        changed = deepcopy(artifact)
        changed.pop(key)
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError):
            service.validate_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(changed)


def test_invalid_source_approval_and_timestamp_fail_closed() -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureComplete29RowMaterializationExecutionError):
        service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
            complete_detail_snapshot=_snapshot(), run_timestamp_utc="2026-08-23"
        )
    with pytest.raises(ValueError):
        service.execute_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_v1(
            source_approval={}, complete_detail_snapshot=_snapshot()
        )


def test_markdown_includes_required_sections(success: dict) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_complete_29_row_module_grouping_detail_source_materialization_execution_markdown_v1(success)
    for heading in (
        "Source Approval", "Source Operator Review and Candidate", "Source Detail Exposure or Binding Failure Diagnosis",
        "Source Recovery Results Review", "Retry Failure Context", "Execution Scope", "Reviewed Cache Verification",
        "Complete 29-row Materialized Source", "Top Module Concentration Preservation", "Priority Tier Enablement",
        "Unsupported Claims Boundary", "Success or Blocked Disposition", "Authority Boundaries",
        "Next Chain", "Next Gates", "Risk Controls", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
