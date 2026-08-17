from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import redesigned_label_generation_candidate_service as candidate_service
from marketflow.services import redesigned_label_generation_candidate_operator_review_service as review_service


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review_service.build_redesigned_label_generation_candidate_review_package_v1()


def test_review_package_builds_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review_service.build_redesigned_label_generation_candidate_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made"] is False
    assert package["market_data_acquisition_performed"] is False


def test_artifact_kind_is_correct(review_package: dict) -> None:
    assert review_package["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE"


def test_review_status_is_correct(review_package: dict) -> None:
    assert review_package["review_status"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY"


def test_reviewed_candidate_evidence_is_exact(review_package: dict) -> None:
    assert review_package["reviewed_redesigned_label_generation_candidate_kind"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE"
    assert review_package["reviewed_redesigned_label_generation_candidate_status"] == "REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW"
    assert review_package["reviewed_redesigned_label_generation_candidate_digest"] == review_service.EXPECTED_CANDIDATE_DIGEST
    assert review_package["reviewed_redesigned_label_generation_candidate_checklist_total"] == 46
    assert review_package["reviewed_redesigned_label_generation_candidate_checklist_passed"] == 46
    assert review_package["reviewed_redesigned_label_generation_candidate_checklist_failed"] == 0
    assert review_package["reviewed_redesigned_label_generation_candidate_blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("redesigned_label_generation_candidate_digest", review_service.EXPECTED_CANDIDATE_DIGEST),
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
def test_key_digests_are_bound(review_package: dict, field: str, expected: str) -> None:
    assert review_package[field] == expected


def test_universe_count_and_order_are_preserved(review_package: dict) -> None:
    assert review_package["target_universe_count"] == 12
    assert review_package["target_universe"] == candidate_service.TARGET_UNIVERSE
    assert review_package["total_canonical_record_count"] == 11946


def test_meta_913_is_preserved(review_package: dict) -> None:
    assert review_package["meta_record_count"] == 913
    assert review_package["per_ticker_record_counts"]["META"] == 913
    assert review_package["meta_reduced_record_count_preserved"] is True


def test_source_readiness_and_review_creation_are_true(review_package: dict) -> None:
    assert review_package["label_objective_redesign_results_review_ready"] is True
    assert review_package["ready_for_redesigned_label_generation_candidate"] is True
    assert review_package["redesigned_label_generation_candidate_created"] is True
    assert review_package["redesigned_label_generation_candidate_review_created"] is True


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
def test_generation_and_downstream_actions_remain_false(review_package: dict, field: str) -> None:
    assert review_package[field] is False


def test_predictive_usefulness_is_not_accepted(review_package: dict) -> None:
    assert review_package["predictive_usefulness"] == "not accepted"
    assert review_package["predictive_usefulness_acceptance_candidate_created"] is False


def test_profitability_is_not_accepted(review_package: dict) -> None:
    assert review_package["profitability"] == "not accepted"
    assert review_package["profitability_acceptance_ready"] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_authority_remain_closed(review_package: dict, field: str) -> None:
    assert review_package[field] == "NOT_AUTHORIZED"


def test_source_design_inputs_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_redesigned_label_generation_inputs"]
    assert [row["source_input_id"] for row in rows] == candidate_service.SOURCE_DESIGN_INPUT_IDS
    assert all(row["source_input_status"] == "SOURCE_REVIEWED_NOT_REGENERATED" for row in rows)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in rows)


def test_planned_label_families_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_planned_redesigned_label_families"]
    assert [row["planned_label_family_id"] for row in rows] == candidate_service.PLANNED_LABEL_FAMILY_IDS
    assert all(row["planned_label_status"] == "PLANNED_NOT_GENERATED" for row in rows)
    assert all(row["label_generation_authorized"] is False for row in rows)


def test_planned_threshold_strategies_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_planned_threshold_strategies"]
    assert [row["threshold_strategy_id"] for row in rows] == candidate_service.PLANNED_THRESHOLD_STRATEGY_IDS
    assert all(row["strategy_status"] == "PLANNED_NOT_COMPUTED" for row in rows)
    assert all(row["threshold_computation_performed"] is False for row in rows)


def test_planned_horizon_strategies_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_planned_horizon_strategies"]
    assert [row["horizon_strategy_id"] for row in rows] == candidate_service.PLANNED_HORIZON_STRATEGY_IDS
    assert all(row["horizon_selection_performed"] is False for row in rows)


def test_planned_availability_rules_are_reviewed(review_package: dict) -> None:
    rows = review_package["reviewed_planned_label_availability_rules"]
    assert [row["availability_rule_id"] for row in rows] == candidate_service.PLANNED_AVAILABILITY_RULE_IDS
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_per_ticker_review_entries_are_complete(review_package: dict) -> None:
    entries = review_package["per_ticker_review_entries"]
    assert len(entries) == 12
    assert [entry["ticker"] for entry in entries] == candidate_service.TARGET_UNIVERSE
    assert all(entry["redesigned_label_generation_candidate_review_status"] == "READY_FOR_OPERATOR_ASSESSMENT" for entry in entries)
    assert all(entry["redesigned_label_generation_authorized"] is False for entry in entries)


def test_per_ticker_candidate_digests_are_present(review_package: dict) -> None:
    assert all(len(entry["per_ticker_redesigned_label_generation_candidate_digest"]) == 64 for entry in review_package["per_ticker_review_entries"])


def test_per_ticker_review_digests_are_present_and_valid(review_package: dict) -> None:
    for entry in review_package["per_ticker_review_entries"]:
        digest = entry["per_ticker_redesigned_label_generation_candidate_review_digest"]
        assert len(digest) == 64
        assert digest == review_service.per_ticker_redesigned_label_generation_candidate_review_digest_v1(entry)


def test_meta_review_entry_preserves_limitation(review_package: dict) -> None:
    entries = {entry["ticker"]: entry for entry in review_package["per_ticker_review_entries"]}
    assert entries["META"]["historical_record_count"] == 913
    assert entries["META"]["meta_reduced_record_count_flag"] is True
    assert entries["META"]["label_availability_note"] == "PRESERVE_REDUCED_RECORD_COUNT_NO_BACKFILL_OR_SYNTHETIC_LABELS"


def test_future_chain_is_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_future_chain"] == candidate_service.FUTURE_CHAIN


def test_future_gates_are_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_future_gates"] == candidate_service.FUTURE_GATES


def test_risk_controls_are_reviewed(review_package: dict) -> None:
    assert review_package["reviewed_risk_controls"] == candidate_service.RISK_CONTROLS


def test_planned_outputs_remain_not_generated(review_package: dict) -> None:
    outputs = review_package["reviewed_planned_outputs"]
    assert [row["planned_output_id"] for row in outputs] == candidate_service.PLANNED_OUTPUT_IDS
    assert all(row["planned_output_status"] == "PLANNED_NOT_GENERATED" for row in outputs)
    assert all(row["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE" for row in outputs)


def test_checklist_passes(review_package: dict) -> None:
    assert [row["check_id"] for row in review_package["review_checklist"]] == review_service.CHECK_IDS
    assert all(row["status"] == "PASS" for row in review_package["review_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review_package["review_checklist"])
    assert review_package["review_summary"]["total_checks"] == 53
    assert review_package["review_summary"]["passed_checks"] == 53
    assert review_package["review_summary"]["blocker_count"] == 0


def test_review_digest_is_deterministic(review_package: dict) -> None:
    rebuilt = review_service.build_redesigned_label_generation_candidate_review_package_v1()
    assert rebuilt["redesigned_label_generation_candidate_review_package_digest"] == review_package["redesigned_label_generation_candidate_review_package_digest"]


def test_per_ticker_review_digests_are_deterministic(review_package: dict) -> None:
    rebuilt = review_service.build_redesigned_label_generation_candidate_review_package_v1()
    assert [row["per_ticker_redesigned_label_generation_candidate_review_digest"] for row in rebuilt["per_ticker_review_entries"]] == [row["per_ticker_redesigned_label_generation_candidate_review_digest"] for row in review_package["per_ticker_review_entries"]]


def test_validator_accepts_valid_review_package(review_package: dict) -> None:
    result = review_service.validate_redesigned_label_generation_candidate_review_package_v1(review_package)
    assert result["status"] == review_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_VALID
    assert result["ready_for_operator_assessment"] is True
    assert result["ready_for_redesigned_label_generation_approval"] is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("reviewed_redesigned_label_generation_candidate_digest", "0" * 64),
        ("reviewed_redesigned_label_generation_candidate_status", "WRONG"),
        ("reviewed_redesigned_label_generation_candidate_blocker_count", 1),
        ("redesigned_label_generation_candidate_digest", None),
        ("label_objective_redesign_results_review_package_digest", None),
        ("records_digest", None),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("meta_record_count", 914),
        ("label_objective_redesign_results_review_ready", False),
        ("ready_for_redesigned_label_generation_candidate", False),
        ("redesigned_label_generation_candidate_created", False),
        ("redesigned_label_generation_candidate_review_created", False),
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
def test_validator_rejects_guardrail_mutations(review_package: dict, field: str, bad_value) -> None:
    changed = deepcopy(review_package)
    changed[field] = bad_value
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.validate_redesigned_label_generation_candidate_review_package_v1(changed)


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_planned_redesigned_label_families",
        "reviewed_planned_threshold_strategies",
        "reviewed_planned_horizon_strategies",
        "reviewed_planned_label_availability_rules",
        "reviewed_future_chain",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_review_structures(review_package: dict, field: str) -> None:
    changed = deepcopy(review_package)
    changed.pop(field)
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.validate_redesigned_label_generation_candidate_review_package_v1(changed)


def test_builder_rejects_source_candidate_with_blocker() -> None:
    source = candidate_service.build_redesigned_label_generation_candidate_v1()
    source["review_summary"]["blocker_count"] = 1
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.build_redesigned_label_generation_candidate_review_package_v1(source)


def test_validator_rejects_missing_review_digest(review_package: dict) -> None:
    changed = deepcopy(review_package)
    changed.pop("redesigned_label_generation_candidate_review_package_digest")
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.validate_redesigned_label_generation_candidate_review_package_v1(changed)


def test_validator_rejects_missing_per_ticker_candidate_digest(review_package: dict) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_review_entries"][0].pop(
        "per_ticker_redesigned_label_generation_candidate_digest"
    )
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.validate_redesigned_label_generation_candidate_review_package_v1(changed)


def test_validator_rejects_missing_per_ticker_review_digest(review_package: dict) -> None:
    changed = deepcopy(review_package)
    changed["per_ticker_review_entries"][0].pop(
        "per_ticker_redesigned_label_generation_candidate_review_digest"
    )
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.validate_redesigned_label_generation_candidate_review_package_v1(changed)


def test_markdown_includes_required_sections(review_package: dict) -> None:
    markdown = review_service.build_redesigned_label_generation_candidate_review_markdown_v1(review_package)
    for heading in (
        "## Title",
        "## Redesigned Label Generation Candidate Review Package",
        "## Reviewed Candidate",
        "## Bound Evidence",
        "## Dataset and Universe",
        "## Source Design Artifacts",
        "## Reviewed Redesigned Label Generation Inputs",
        "## Reviewed Planned Label Families",
        "## Reviewed Planned Threshold Strategies",
        "## Reviewed Planned Horizon Strategies",
        "## Reviewed Planned Availability Rules",
        "## Per-Ticker Review Entries",
        "## Future Chain",
        "## Future Gates",
        "## Risk Controls",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_canonical_json_once(review_package: dict, tmp_path) -> None:
    receipt = review_service.write_redesigned_label_generation_candidate_review_package_v1(tmp_path)
    written = json.loads((tmp_path / receipt["filename"]).read_text(encoding="utf-8"))
    assert written == review_package
    with pytest.raises(review_service.RedesignedLabelGenerationCandidateReviewError):
        review_service.write_redesigned_label_generation_candidate_review_package_v1(tmp_path)


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE == review_service.ARTIFACT_KIND_REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE
    assert services.REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY == review_service.REDESIGNED_LABEL_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY
    assert services.build_redesigned_label_generation_candidate_review_package_v1 is review_service.build_redesigned_label_generation_candidate_review_package_v1
    assert services.validate_redesigned_label_generation_candidate_review_package_v1 is review_service.validate_redesigned_label_generation_candidate_review_package_v1
    assert services.write_redesigned_label_generation_candidate_review_package_v1 is review_service.write_redesigned_label_generation_candidate_review_package_v1
    assert services.build_redesigned_label_generation_candidate_review_markdown_v1 is review_service.build_redesigned_label_generation_candidate_review_markdown_v1
