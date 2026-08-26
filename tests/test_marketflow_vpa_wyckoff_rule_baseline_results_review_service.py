from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_file
from marketflow.services import marketflow_vpa_wyckoff_rule_baseline_execution_service as execution
from marketflow.services import marketflow_vpa_wyckoff_rule_baseline_results_review_service as service


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def _common_report(report_kind: str) -> dict:
    return {
        "report_kind": report_kind,
        "output_label": execution.OUTPUT_LABEL,
        "evidence_scope": execution.EVIDENCE_SCOPE,
        "selected_vpa_wyckoff_package": execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "predictive_usefulness": service.NOT_ACCEPTED,
        "profitability": service.NOT_ACCEPTED,
        "runtime_use": service.NOT_AUTHORIZED,
        "backtest_execution_authorized": False,
        "model_training_authorized": False,
        "metric_computation_authorized": False,
        "trade_recommendations_generated": False,
    }


def _rule_row(index: int, matrix_digest: str) -> dict:
    return {
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "ticker": "META",
        "date": f"2022-01-{(index % 28) + 1:02d}",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "canonical_record_index": index // 15,
        "target_family": f"TARGET_{index % 5}",
        "target_horizon_sessions": (5, 10, 20)[index % 3],
        "target_profile": f"TARGET_PROFILE_{index}",
        "target_available": True,
        "target_unavailable_reason": None,
        "selected_vpa_wyckoff_package": execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "rule_family_count": len(execution.SELECTED_RULE_FAMILY_IDS),
        "state_family_count": len(execution.SELECTED_STATE_FAMILY_IDS),
        "rule_values": {
            family: {"available": True, "tag": "neutral"}
            for family in execution.SELECTED_RULE_FAMILY_IDS
        },
        "state_values": {
            family: {"available": True, "value": False}
            for family in execution.SELECTED_STATE_FAMILY_IDS
        },
        "rule_values_available": True,
        "state_values_available": True,
        "rule_unavailable_reason": None,
        "state_unavailable_reason": None,
        "source_matrix_rows_digest": matrix_digest,
        "source_matrix_approval_digest": "matrix-approval",
        "records_digest": service.EXPECTED_SOURCE_RECORDS_DIGEST,
        "research_only": True,
        "non_actionable": True,
    }


def _create_source_outputs(root: Path, matrix_path: Path) -> dict:
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_path.write_bytes(canonical_json_bytes({"fixture": "matrix-source"}))
    matrix_digest = sha256_file(matrix_path)

    rule_values_path = root / "vpa_wyckoff_rule_values.jsonl"
    rule_values_path.parent.mkdir(parents=True, exist_ok=True)
    rule_values_path.write_bytes(b"".join(
        canonical_json_bytes(_rule_row(index, matrix_digest)) for index in range(30)
    ))
    rule_values_digest = sha256_file(rule_values_path)

    rule_schema = {
        **_common_report("vpa_wyckoff_rule_schema"),
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
        "executed_rule_families": [
            {"rule_family_id": family, "execution_status": "EXECUTED_RESEARCH_ONLY"}
            for family in execution.SELECTED_RULE_FAMILY_IDS
        ],
        "supporting_rule_families": [
            {
                "rule_family_id": family,
                "approval_status": "AVAILABLE_NOT_SELECTED",
                "execution_performed": False,
            }
            for family in execution.SUPPORTING_RULE_FAMILY_IDS
        ],
    }
    state_schema = {
        **_common_report("vpa_wyckoff_state_schema"),
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
        "executed_wyckoff_state_families": [
            {"state_family_id": family, "execution_status": "EXECUTED_RESEARCH_ONLY"}
            for family in execution.SELECTED_STATE_FAMILY_IDS
        ],
        "supporting_wyckoff_state_families": [
            {
                "state_family_id": family,
                "approval_status": "AVAILABLE_NOT_SELECTED",
                "execution_performed": False,
            }
            for family in execution.SUPPORTING_STATE_FAMILY_IDS
        ],
    }
    coverage = {
        **_common_report("vpa_wyckoff_rule_coverage_report"),
        "coverage_is_descriptive_not_performance_metric": True,
        "rule_family_reference_count": 240,
        "state_family_reference_count": 180,
        "coverage": {
            family: {"fixture_tag": 30}
            for family in execution.SELECTED_RULE_FAMILY_IDS + execution.SELECTED_STATE_FAMILY_IDS
        },
    }
    per_ticker = {
        **_common_report("vpa_wyckoff_per_ticker_report"),
        "per_ticker_execution_entries": [{"ticker": "META"}],
    }
    meta = {
        **_common_report("vpa_wyckoff_meta_limitation_report"),
        "ticker": "META",
        "historical_record_count": 2,
        "source_matrix_row_count": 30,
        "rule_value_row_count": 30,
        "state_value_row_count": 30,
        "meta_reduced_record_count_flag": True,
        "repair_or_inference_performed": False,
    }
    no_peek = {
        **_common_report("vpa_wyckoff_no_peek_report"),
        "no_peek_controls": {
            "target_values_absent": True,
            "target_classes_absent": True,
            "forward_returns_absent": True,
            "future_data_absent": True,
            "prediction_fields_absent": True,
            "strategy_score_fields_absent": True,
            "trade_recommendation_fields_absent": True,
            "broker_order_fields_absent": True,
            "provider_payload_fields_absent": True,
            "api_key_fields_absent": True,
        },
        "rule_output_row_fields": sorted(execution.RULE_OUTPUT_ROW_FIELDS),
        "forbidden_rule_output_fields": sorted(execution.FORBIDDEN_RULE_OUTPUT_FIELDS),
    }
    operator = {
        **_common_report("vpa_wyckoff_operator_summary"),
        "generated_output_count": 10,
        "backtest_or_performance_evaluation_performed": False,
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
    }
    ordinary = {
        "vpa_wyckoff_rule_schema.json": rule_schema,
        "vpa_wyckoff_state_schema.json": state_schema,
        "vpa_wyckoff_rule_coverage_report.json": coverage,
        "vpa_wyckoff_per_ticker_report.json": per_ticker,
        "vpa_wyckoff_meta_limitation_report.json": meta,
        "vpa_wyckoff_no_peek_report.json": no_peek,
        "vpa_wyckoff_operator_summary.json": operator,
    }
    for name, payload in ordinary.items():
        _write_json(root / name, payload)

    digest_rows = []
    for name in execution.OUTPUT_FILENAMES:
        if name == "vpa_wyckoff_baseline_manifest.json":
            digest_rows.append({
                "filename": name,
                "digest_kind": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
                "sha256": None,
            })
        elif name == "vpa_wyckoff_digest_manifest.json":
            digest_rows.append({
                "filename": name,
                "digest_kind": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                "sha256": None,
            })
        else:
            digest_rows.append({
                "filename": name,
                "digest_kind": "FILE_SHA256",
                "sha256": sha256_file(root / name),
            })

    source_execution_digest = "fixture-source-execution-digest"
    source_output_binding_digest = "fixture-output-binding-digest"
    manifest = {
        "artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED,
        "execution_status": execution.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
        "execution_scope": execution.VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest": source_execution_digest,
        "vpa_wyckoff_rule_baseline_output_binding_digest": source_output_binding_digest,
        "vpa_wyckoff_rule_values_digest": rule_values_digest,
        "source_vpa_wyckoff_rule_baseline_approval_digest": service.EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest": service.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest": service.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_output_binding_digest": service.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_matrix_rows_digest": matrix_digest,
        "source_feature_values_digest": service.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": service.EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": service.EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_matrix_row_count": 30,
        "rule_value_row_count": 30,
        "state_value_row_count": 30,
        "selected_rule_family_count": 8,
        "selected_state_family_count": 6,
        "rule_family_reference_count": 240,
        "state_family_reference_count": 180,
        "generated_output_count": 10,
        "expected_output_count": 10,
        "observed_output_count": 10,
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
        "source_evidence": {"complete_upstream_chain": "fixture-bound"},
        "no_tracked_marketflow_files": True,
        "output_digest_manifest": digest_rows,
    }
    digest_manifest = {
        **_common_report("vpa_wyckoff_digest_manifest"),
        "manifest_self_reference_policy": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "output_digest_manifest": digest_rows,
        "vpa_wyckoff_rule_baseline_output_binding_digest": source_output_binding_digest,
        "vpa_wyckoff_rule_values_digest": rule_values_digest,
    }
    _write_json(root / "vpa_wyckoff_baseline_manifest.json", manifest)
    _write_json(root / "vpa_wyckoff_digest_manifest.json", digest_manifest)
    return {
        "matrix_digest": matrix_digest,
        "rule_values_digest": rule_values_digest,
        "source_execution_digest": source_execution_digest,
        "source_output_binding_digest": source_output_binding_digest,
    }


@pytest.fixture(scope="module")
def review_environment(tmp_path_factory: pytest.TempPathFactory):
    base = tmp_path_factory.mktemp("vpa_wyckoff_results_review")
    root = base / "source_outputs"
    matrix_path = base / "source_matrix" / "matrix_rows.jsonl"
    source = _create_source_outputs(root, matrix_path)
    replacements = {
        "DEFAULT_OUTPUT_ROOT": root,
        "DEFAULT_SOURCE_MATRIX_PATH": matrix_path,
        "TARGET_UNIVERSE": ["META"],
        "EXPECTED_RECORD_COUNTS": {"META": 2},
        "EXPECTED_SOURCE_MATRIX_ROW_COUNT": 30,
        "EXPECTED_RULE_VALUE_ROW_COUNT": 30,
        "EXPECTED_STATE_VALUE_ROW_COUNT": 30,
        "EXPECTED_RULE_FAMILY_REFERENCE_COUNT": 240,
        "EXPECTED_STATE_FAMILY_REFERENCE_COUNT": 180,
        "EXPECTED_SOURCE_MATRIX_ROWS_DIGEST": source["matrix_digest"],
        "EXPECTED_SOURCE_RULE_VALUES_DIGEST": source["rule_values_digest"],
        "EXPECTED_SOURCE_EXECUTION_DIGEST": source["source_execution_digest"],
        "EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST": source["source_output_binding_digest"],
    }
    originals = {name: getattr(service, name) for name in replacements}
    for name, value in replacements.items():
        setattr(service, name, value)
    review = service.build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1()
    yield {"review": review, "root": root, "matrix_path": matrix_path, "base": base}
    for name, value in originals.items():
        setattr(service, name, value)


def test_results_review_builds_offline_without_mutating_sources(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["created_offline"] is True
    assert review["source_outputs_unchanged_during_review"] is True
    assert review["source_matrix_verification"]["source_matrix_output_unchanged_during_review"] is True
    assert review["provider_requests_made_in_review"] is False


def test_results_review_blocks_when_output_root_is_missing(tmp_path: Path) -> None:
    blocked = service.build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
        output_root=tmp_path / "missing"
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED
    assert blocked["review_status"] == service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert blocked["ready_for_expectancy_backtest_lab_candidate"] is False
    assert service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(blocked)["status"] == service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_VALID


def test_results_review_blocks_when_an_output_is_invalid(review_environment: dict, tmp_path: Path) -> None:
    copied = tmp_path / "invalid_outputs"
    copied.mkdir()
    for path in review_environment["root"].iterdir():
        (copied / path.name).write_bytes(path.read_bytes())
    payload = json.loads((copied / "vpa_wyckoff_rule_schema.json").read_text())
    payload["rule_threshold_policy"] = "CHANGED"
    _write_json(copied / "vpa_wyckoff_rule_schema.json", payload)
    blocked = service.build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
        output_root=copied
    )
    assert blocked["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED
    assert blocked["vpa_wyckoff_rule_baseline_results_review_ready"] is False


def test_rule_values_inspection_is_streaming() -> None:
    source = inspect.getsource(service._inspect_rule_values)
    assert ".open(" in source
    assert ".read_text(" not in source
    assert "STREAMING_JSONL_ONE_ROW_AT_A_TIME" in source


CORE_FIELDS = [
    ("artifact_kind", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE"),
    ("schema_version", "marketflow_vpa_wyckoff_rule_baseline_results_review_v1"),
    ("review_status", "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY"),
    ("review_scope", "VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"),
    ("selected_vpa_wyckoff_package", execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE),
    ("selected_matrix_package", execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX),
    ("selected_matrix_layout", execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE),
    ("selected_feature_package", execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET),
    ("selected_label_target_package", execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET),
    ("selected_objective_path", execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT),
    ("target_universe", ["META"]),
    ("target_universe_count", 1),
    ("meta_record_count", 2),
    ("expected_output_count", 10),
    ("observed_output_count", 10),
    ("output_digest_mismatch_count", 0),
]


@pytest.mark.parametrize(("field", "expected"), CORE_FIELDS)
def test_core_review_contract(review_environment: dict, field: str, expected: object) -> None:
    assert review_environment["review"][field] == expected


COUNT_FIELDS = [
    ("source_matrix_row_count", 30),
    ("rule_value_row_count", 30),
    ("state_value_row_count", 30),
    ("selected_rule_family_count", 8),
    ("selected_state_family_count", 6),
    ("rule_family_reference_count", 240),
    ("state_family_reference_count", 180),
    ("local_output_digest_count", 10),
    ("recorded_file_digest_match_count", 8),
]


@pytest.mark.parametrize(("field", "expected"), COUNT_FIELDS)
def test_review_counts(review_environment: dict, field: str, expected: int) -> None:
    assert review_environment["review"][field] == expected


@pytest.mark.parametrize("field", [
    "source_vpa_wyckoff_rule_baseline_execution_digest",
    "source_vpa_wyckoff_rule_baseline_output_binding_digest",
    "source_vpa_wyckoff_rule_values_digest",
    "source_vpa_wyckoff_rule_baseline_approval_digest",
    "source_candidate_review_digest",
    "source_candidate_digest",
    "source_matrix_results_review_digest",
    "source_matrix_execution_digest",
    "source_matrix_output_binding_digest",
    "source_matrix_rows_digest",
    "source_feature_values_digest",
    "source_target_values_digest",
    "source_records_digest",
])
def test_source_evidence_digest_is_bound(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field]


@pytest.mark.parametrize("field", [
    "rule_values_jsonl_schema_verified",
    "package_binding_verified",
    "research_only_non_actionable_verified",
    "selected_family_schema_verified",
    "non_meta_ticker_counts_verified",
    "meta_counts_verified",
    "rule_values_output_unchanged_during_review",
])
def test_streaming_rule_values_verifications_pass(review_environment: dict, field: str) -> None:
    assert review_environment["review"]["rule_values_inspection"][field] is True


@pytest.mark.parametrize("field", [
    "target_values_present",
    "target_classes_present",
    "forward_returns_present",
    "future_data_present",
    "prediction_fields_present",
    "strategy_score_fields_present",
    "trade_recommendation_fields_present",
    "broker_order_fields_present",
    "provider_payload_fields_present",
    "api_key_fields_present",
])
def test_leakage_and_sensitive_fields_are_absent(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is False


@pytest.mark.parametrize("field", [
    "common_output_boundary_verified",
    "rule_schema_verified",
    "state_schema_verified",
    "coverage_report_verified",
    "per_ticker_report_verified",
    "meta_limitation_report_verified",
    "no_peek_report_verified",
    "operator_summary_verified",
    "digest_manifest_verified",
    "executed_rule_families_verified",
    "executed_state_families_verified",
    "supporting_families_not_executed",
])
def test_all_source_reports_are_verified(review_environment: dict, field: str) -> None:
    assert review_environment["review"]["report_reviews"][field] is True


@pytest.mark.parametrize("field", [
    "vpa_wyckoff_rule_baseline_results_review_created",
    "vpa_wyckoff_rule_baseline_results_review_ready",
    "ready_for_expectancy_backtest_lab_candidate",
    "rule_values_jsonl_schema_verified",
    "rule_values_count_verified",
    "state_values_count_verified",
    "per_ticker_rule_counts_verified",
    "per_ticker_state_counts_verified",
    "meta_limitation_verified",
])
def test_review_readiness_and_verification_flags_are_true(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is True


@pytest.mark.parametrize("field", [
    "expectancy_backtest_lab_candidate_created",
    "backtest_execution_authorized",
    "backtest_execution_performed",
    "model_training_authorized",
    "model_training_performed",
    "metric_computation_authorized",
    "metric_computation_performed",
    "strategy_scoring_performed",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made_in_review",
    "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review",
    "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review",
    "vpa_wyckoff_rule_baseline_execution_rerun_performed",
    "feature_label_matrix_execution_rerun_performed",
    "feature_label_matrix_results_review_rerun_performed",
    "vpa_wyckoff_candidate_creation_rerun_performed",
    "vpa_wyckoff_candidate_review_rerun_performed",
    "vpa_wyckoff_approval_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
])
def test_closed_action_flags_remain_false(review_environment: dict, field: str) -> None:
    assert review_environment["review"][field] is False


def test_acceptance_runtime_and_trading_remain_closed(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["predictive_usefulness"] == service.NOT_ACCEPTED
    assert review["profitability"] == service.NOT_ACCEPTED
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert review[field] == service.NOT_AUTHORIZED


def test_per_ticker_review_entry_and_digest(review_environment: dict) -> None:
    rows = review_environment["review"]["per_ticker_vpa_wyckoff_rule_baseline_results_review_entries"]
    assert len(rows) == 1
    row = rows[0]
    assert (row["ticker"], row["historical_record_count"], row["rule_value_row_count"]) == ("META", 2, 30)
    assert row["review_note"] == "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW"
    payload = deepcopy(row)
    digest = payload.pop("per_ticker_vpa_wyckoff_rule_baseline_results_review_digest")
    assert digest == semantic_digest(payload)


def test_digest_manifest_policies_and_all_local_hashes_are_bound(review_environment: dict) -> None:
    review = review_environment["review"]
    assert review["digest_manifest_self_reference_policy"] == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
    assert list(review["local_output_digests"]) == execution.OUTPUT_FILENAMES
    assert all(row["verification_status"] == service.PASS for row in review["output_digest_bindings"])


def test_checklist_passes_completely(review_environment: dict) -> None:
    review = review_environment["review"]
    assert [row["check_id"] for row in review["review_checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in review["review_checklist"])
    assert review["review_summary"] == {
        **review["review_summary"],
        "total_checks": len(service.REQUIRED_CHECK_IDS),
        "passed_checks": len(service.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
    }


def test_review_and_per_ticker_digests_are_deterministic(review_environment: dict) -> None:
    first = review_environment["review"]
    second = service.build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1()
    assert first["marketflow_vpa_wyckoff_rule_baseline_results_review_digest"] == second["marketflow_vpa_wyckoff_rule_baseline_results_review_digest"]
    assert first["per_ticker_vpa_wyckoff_rule_baseline_results_review_entries"] == second["per_ticker_vpa_wyckoff_rule_baseline_results_review_entries"]


def test_validator_accepts_valid_review(review_environment: dict) -> None:
    validation = service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
        review_environment["review"]
    )
    assert validation["status"] == service.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_VALID
    assert validation["blocker_count"] == 0


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("review_status", "WRONG"),
    ("review_scope", "WRONG"),
    ("source_vpa_wyckoff_rule_baseline_execution_digest", "changed"),
    ("source_vpa_wyckoff_rule_baseline_output_binding_digest", "changed"),
    ("source_vpa_wyckoff_rule_values_digest", "changed"),
    ("source_vpa_wyckoff_rule_baseline_approval_digest", "changed"),
    ("selected_vpa_wyckoff_package", "WRONG"),
    ("selected_matrix_package", "WRONG"),
    ("selected_feature_package", "WRONG"),
    ("selected_label_target_package", "WRONG"),
    ("selected_objective_path", "WRONG"),
    ("target_universe", ["WRONG"]),
    ("target_universe_count", 2),
    ("records_digest", "changed"),
    ("meta_record_count", 3),
    ("expected_output_count", 9),
    ("observed_output_count", 9),
    ("output_digest_mismatch_count", 1),
    ("rule_value_row_count", 29),
    ("state_value_row_count", 29),
    ("selected_rule_family_count", 7),
    ("selected_state_family_count", 5),
    ("rule_family_reference_count", 239),
    ("state_family_reference_count", 179),
    ("vpa_wyckoff_rule_baseline_results_review_created", False),
    ("vpa_wyckoff_rule_baseline_results_review_ready", False),
    ("ready_for_expectancy_backtest_lab_candidate", False),
    ("expectancy_backtest_lab_candidate_created", True),
    ("backtest_execution_performed", True),
    ("model_training_performed", True),
    ("metric_computation_performed", True),
    ("strategy_scoring_performed", True),
    ("predictive_usefulness", "accepted"),
    ("profitability", "accepted"),
    ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"),
    ("trade_recommendations_generated", True),
    ("provider_requests_made_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
    ("vpa_wyckoff_rule_baseline_execution_rerun_performed", True),
    ("feature_label_matrix_execution_rerun_performed", True),
    ("feature_label_matrix_results_review_rerun_performed", True),
    ("vpa_wyckoff_candidate_creation_rerun_performed", True),
    ("vpa_wyckoff_candidate_review_rerun_performed", True),
    ("vpa_wyckoff_approval_rerun_performed", True),
    ("target_values_present", True),
    ("target_classes_present", True),
    ("forward_returns_present", True),
    ("future_data_present", True),
    ("prediction_fields_present", True),
    ("strategy_score_fields_present", True),
    ("trade_recommendation_fields_present", True),
    ("broker_order_fields_present", True),
    ("provider_payload_fields_present", True),
    ("api_key_fields_present", True),
    ("rule_values_jsonl_schema_verified", False),
    ("rule_values_count_verified", False),
    ("state_values_count_verified", False),
]


@pytest.mark.parametrize(("field", "value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_contract_mutations(
    review_environment: dict, field: str, value: object
) -> None:
    changed = deepcopy(review_environment["review"])
    changed[field] = value
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineResultsReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(changed)


def test_validator_rejects_missing_risk_controls(review_environment: dict) -> None:
    changed = deepcopy(review_environment["review"])
    changed.pop("risk_controls")
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineResultsReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(changed)


def test_validator_rejects_missing_output_review(review_environment: dict) -> None:
    changed = deepcopy(review_environment["review"])
    changed["report_reviews"]["coverage_report_verified"] = False
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineResultsReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(review_environment: dict) -> None:
    changed = deepcopy(review_environment["review"])
    changed["per_ticker_vpa_wyckoff_rule_baseline_results_review_entries"][0].pop(
        "per_ticker_vpa_wyckoff_rule_baseline_results_review_digest"
    )
    with pytest.raises(service.MarketFlowVpaWyckoffRuleBaselineResultsReviewError):
        service.validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(changed)


MARKDOWN_HEADINGS = [
    "VPA/Wyckoff Rule Baseline Results Review v1",
    "Source VPA/Wyckoff Execution",
    "Bound Evidence",
    "Dataset and Universe",
    "Output Verification",
    "Selected VPA/Wyckoff Package",
    "Rule Threshold Policy",
    "Executed Rule Families Review",
    "Executed Wyckoff State Families Review",
    "Rule Values Review",
    "State Values Review",
    "No-Peek and Leakage Review",
    "Coverage Report Review",
    "Per-Ticker Report Review",
    "META Limitation Review",
    "Output Digest Manifest",
    "Next Chain",
    "Next Gates",
    "Risk Controls",
    "Predictive Usefulness Boundary",
    "Profitability Boundary",
    "Runtime Boundary",
    "Checklist Summary",
    "Guardrails",
]


@pytest.mark.parametrize("heading", MARKDOWN_HEADINGS)
def test_markdown_contains_required_sections(review_environment: dict, heading: str) -> None:
    markdown = service.build_marketflow_vpa_wyckoff_rule_baseline_results_review_markdown_v1(
        review_environment["review"]
    )
    assert heading in markdown


def test_writer_round_trips_review_in_isolated_directory(
    review_environment: dict, tmp_path: Path
) -> None:
    written = service.write_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
        tmp_path / "review", output_root=review_environment["root"]
    )
    assert Path(written["json_path"]).is_file()
    assert Path(written["markdown_path"]).is_file()
    assert json.loads(Path(written["json_path"]).read_text()) == written["review"]


@pytest.mark.parametrize("name", [
    "ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE",
    "SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_V1",
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY",
    "VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING",
    "build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1",
    "validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1",
    "write_marketflow_vpa_wyckoff_rule_baseline_results_review_v1",
    "build_marketflow_vpa_wyckoff_rule_baseline_results_review_markdown_v1",
])
def test_public_exports(name: str) -> None:
    assert name in services.__all__
    assert getattr(services, name) is getattr(service, name)
