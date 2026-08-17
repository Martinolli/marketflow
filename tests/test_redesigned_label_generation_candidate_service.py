from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import redesigned_label_generation_candidate_service as candidate_service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_redesigned_label_generation_candidate_v1()


def test_candidate_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = candidate_service.build_redesigned_label_generation_candidate_v1()
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made"] is False
    assert artifact["market_data_acquisition_performed"] is False


def test_artifact_kind_is_correct(candidate: dict) -> None:
    assert candidate["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE"


def test_candidate_status_is_correct(candidate: dict) -> None:
    assert candidate["candidate_status"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("label_objective_redesign_results_review_package_digest", candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("label_objective_redesign_execution_digest", candidate_service.EXPECTED_EXECUTION_DIGEST),
        ("label_objective_redesign_execution_approval_digest", candidate_service.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("label_objective_redesign_execution_candidate_review_package_digest", candidate_service.EXPECTED_EXECUTION_CANDIDATE_REVIEW_DIGEST),
        ("label_objective_redesign_execution_candidate_digest", candidate_service.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("label_objective_redesign_approval_digest", candidate_service.EXPECTED_REDESIGN_APPROVAL_DIGEST),
        ("operator_method_path_selection_digest", candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST),
        ("research_registry_approval_digest", candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", candidate_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_key_digests_are_bound(candidate: dict, field: str, expected: str) -> None:
    assert candidate[field] == expected


def test_universe_count_and_order_are_preserved(candidate: dict) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == candidate_service.TARGET_UNIVERSE
    assert candidate["total_canonical_record_count"] == 11946


def test_meta_913_is_preserved(candidate: dict) -> None:
    assert candidate["meta_record_count"] == 913
    assert candidate["per_ticker_record_counts"]["META"] == 913
    assert candidate["meta_reduced_record_count_preserved"] is True


def test_results_review_and_candidate_readiness_are_true(candidate: dict) -> None:
    assert candidate["label_objective_redesign_results_review_ready"] is True
    assert candidate["ready_for_redesigned_label_generation_candidate"] is True
    assert candidate["redesigned_label_generation_candidate_created"] is True
    assert candidate["redesigned_label_generation_candidate_ready_for_operator_review"] is True


def test_candidate_review_created_is_false(candidate: dict) -> None:
    assert candidate["redesigned_label_generation_candidate_review_created"] is False


@pytest.mark.parametrize(
    "field",
    [
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_generation_and_downstream_action_fields_remain_false(candidate: dict, field: str) -> None:
    assert candidate[field] is False


def test_predictive_usefulness_is_not_accepted(candidate: dict) -> None:
    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(candidate: dict) -> None:
    assert candidate["profitability"] == "not accepted"
    assert candidate["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_authority_remain_closed(candidate: dict, field: str) -> None:
    assert candidate[field] == "NOT_AUTHORIZED"


def test_source_design_inputs_are_defined(candidate: dict) -> None:
    inputs = candidate["source_design_inputs"]
    assert [item["source_input_id"] for item in inputs] == candidate_service.SOURCE_DESIGN_INPUT_IDS
    assert all(item["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for item in inputs)
    assert all(item["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for item in inputs)


def test_planned_label_families_count_is_ten(candidate: dict) -> None:
    rows = candidate["planned_redesigned_label_families"]
    assert [row["planned_label_family_id"] for row in rows] == candidate_service.PLANNED_LABEL_FAMILY_IDS
    assert all(row["planned_label_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["label_generation_authorized"] is False for row in rows)
    assert all(row["label_generation_performed"] is False for row in rows)
    assert all(row["actual_label_values_created"] is False for row in rows)


def test_planned_threshold_strategies_count_is_seven(candidate: dict) -> None:
    rows = candidate["planned_threshold_strategies"]
    assert [row["threshold_strategy_id"] for row in rows] == candidate_service.PLANNED_THRESHOLD_STRATEGY_IDS
    assert all(row["strategy_status"] == "PLANNED_NOT_COMPUTED" for row in rows)
    assert all(row["threshold_computation_performed"] is False for row in rows)


def test_planned_horizon_strategies_count_is_five(candidate: dict) -> None:
    rows = candidate["planned_horizon_strategies"]
    assert [row["horizon_strategy_id"] for row in rows] == candidate_service.PLANNED_HORIZON_STRATEGY_IDS
    assert all(row["strategy_status"] == "PLANNED_NOT_COMPUTED" for row in rows)
    assert all(row["horizon_selection_performed"] is False for row in rows)


def test_planned_availability_rules_are_defined(candidate: dict) -> None:
    rows = candidate["planned_label_availability_rules"]
    assert [row["availability_rule_id"] for row in rows] == candidate_service.PLANNED_AVAILABILITY_RULE_IDS
    assert all(row["rule_status"] == "PLANNED_FOR_OPERATOR_REVIEW" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_per_ticker_entries_count_and_order_are_preserved(candidate: dict) -> None:
    entries = candidate["per_ticker_candidate_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == candidate_service.TARGET_UNIVERSE
    assert all(entry["redesigned_label_generation_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW" for entry in entries)
    assert all(entry["redesigned_label_generation_authorized"] is False for entry in entries)
    assert all(entry["actual_redesigned_labels_generated"] is False for entry in entries)


def test_meta_entry_preserves_reduced_count_note(candidate: dict) -> None:
    entries = {entry["ticker"]: entry for entry in candidate["per_ticker_candidate_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["label_availability_note"] == "PRESERVE_REDUCED_RECORD_COUNT_NO_BACKFILL_OR_SYNTHETIC_LABELS"
    assert all(entries[ticker]["historical_record_count"] == 1003 for ticker in candidate_service.TARGET_UNIVERSE if ticker != "META")


def test_per_ticker_digests_are_present_and_valid(candidate: dict) -> None:
    for entry in candidate["per_ticker_candidate_entries"]:
        digest = entry["per_ticker_redesigned_label_generation_candidate_digest"]
        assert len(digest) == 64
        assert digest == candidate_service.per_ticker_redesigned_label_generation_candidate_digest_v1(entry)


def test_future_chain_is_defined(candidate: dict) -> None:
    assert candidate["future_chain"] == candidate_service.FUTURE_CHAIN


def test_future_gates_are_defined(candidate: dict) -> None:
    assert candidate["future_gates"] == candidate_service.FUTURE_GATES


def test_risk_controls_are_defined(candidate: dict) -> None:
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_planned_outputs_are_not_generated_and_research_only(candidate: dict) -> None:
    outputs = candidate["planned_outputs"]
    assert [item["planned_output_id"] for item in outputs] == candidate_service.PLANNED_OUTPUT_IDS
    assert all(item["planned_output_status"] == "PLANNED_NOT_GENERATED" for item in outputs)
    assert all(item["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for item in outputs)
    assert all(item["research_only"] is True and item["non_actionable"] is True for item in outputs)


def test_checklist_passes(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["review_checklist"]] == candidate_service.CHECK_IDS
    assert all(row["status"] == "PASS" for row in candidate["review_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in candidate["review_checklist"])
    assert candidate["review_summary"]["total_checks"] == 46
    assert candidate["review_summary"]["passed_checks"] == 46
    assert candidate["review_summary"]["failed_checks"] == 0
    assert candidate["review_summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    rebuilt = candidate_service.build_redesigned_label_generation_candidate_v1()
    assert rebuilt["redesigned_label_generation_candidate_digest"] == candidate["redesigned_label_generation_candidate_digest"]


def test_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    rebuilt = candidate_service.build_redesigned_label_generation_candidate_v1()
    assert [entry["per_ticker_redesigned_label_generation_candidate_digest"] for entry in rebuilt["per_ticker_candidate_entries"]] == [entry["per_ticker_redesigned_label_generation_candidate_digest"] for entry in candidate["per_ticker_candidate_entries"]]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = candidate_service.validate_redesigned_label_generation_candidate_v1(candidate)
    assert result["status"] == candidate_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_VALID
    assert result["ready_for_operator_review"] is True
    assert result["ready_for_redesigned_label_generation_approval"] is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("label_objective_redesign_results_review_package_digest", None),
        ("records_digest", None),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("meta_record_count", 914),
        ("label_objective_redesign_results_review_ready", False),
        ("ready_for_redesigned_label_generation_candidate", False),
        ("redesigned_label_generation_candidate_created", False),
        ("redesigned_label_generation_candidate_review_created", True),
        ("redesigned_label_generation_approved", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
        ("actual_redesigned_labels_generated", True),
        ("feature_generation_performed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_guardrail_mutations(candidate: dict, field: str, bad_value) -> None:
    changed = deepcopy(candidate)
    changed[field] = bad_value
    with pytest.raises(candidate_service.RedesignedLabelGenerationCandidateError):
        candidate_service.validate_redesigned_label_generation_candidate_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "planned_redesigned_label_families",
        "planned_threshold_strategies",
        "planned_horizon_strategies",
        "planned_label_availability_rules",
        "future_chain",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_planning_structures(candidate: dict, field: str) -> None:
    changed = deepcopy(candidate)
    changed.pop(field)
    with pytest.raises(candidate_service.RedesignedLabelGenerationCandidateError):
        candidate_service.validate_redesigned_label_generation_candidate_v1(changed)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed.pop("redesigned_label_generation_candidate_digest")
    with pytest.raises(candidate_service.RedesignedLabelGenerationCandidateError):
        candidate_service.validate_redesigned_label_generation_candidate_v1(changed)


def test_validator_rejects_missing_per_ticker_digest(candidate: dict) -> None:
    changed = deepcopy(candidate)
    changed["per_ticker_candidate_entries"][0].pop(
        "per_ticker_redesigned_label_generation_candidate_digest"
    )
    with pytest.raises(candidate_service.RedesignedLabelGenerationCandidateError):
        candidate_service.validate_redesigned_label_generation_candidate_v1(changed)


def test_markdown_includes_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_redesigned_label_generation_candidate_markdown_v1(candidate)
    for heading in (
        "## Title",
        "## Redesigned Label Generation Candidate",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Source Design Artifacts",
        "## Planned Redesigned Label Families",
        "## Planned Threshold Strategies",
        "## Planned Horizon Strategies",
        "## Planned Availability Rules",
        "## Per-Ticker Candidate Entries",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_canonical_json_once(candidate: dict, tmp_path) -> None:
    receipt = candidate_service.write_redesigned_label_generation_candidate_v1(tmp_path)
    written = json.loads((tmp_path / receipt["filename"]).read_text(encoding="utf-8"))
    assert written == candidate
    with pytest.raises(candidate_service.RedesignedLabelGenerationCandidateError):
        candidate_service.write_redesigned_label_generation_candidate_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE == candidate_service.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE
    assert services.REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW == candidate_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert services.build_redesigned_label_generation_candidate_v1 is candidate_service.build_redesigned_label_generation_candidate_v1
    assert services.validate_redesigned_label_generation_candidate_v1 is candidate_service.validate_redesigned_label_generation_candidate_v1
    assert services.write_redesigned_label_generation_candidate_v1 is candidate_service.write_redesigned_label_generation_candidate_v1
    assert services.build_redesigned_label_generation_candidate_markdown_v1 is candidate_service.build_redesigned_label_generation_candidate_markdown_v1
