from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_evidence_improvement_candidate_service as candidate_service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return candidate_service.build_predictive_evidence_improvement_candidate_v1()


def test_candidate_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = candidate_service.build_predictive_evidence_improvement_candidate_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made"] is False


def test_candidate_accepts_exact_supplied_readiness_review() -> None:
    source = candidate_service.readiness_service.build_predictive_usefulness_acceptance_readiness_review_v1()
    package = candidate_service.build_predictive_evidence_improvement_candidate_v1(
        readiness_review=source
    )
    assert package["predictive_usefulness_acceptance_readiness_review_digest"] == (
        source["predictive_usefulness_acceptance_readiness_review_digest"]
    )


def test_artifact_schema_and_status(candidate: dict) -> None:
    assert candidate["artifact_kind"] == (
        candidate_service.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE
    )
    assert candidate["schema_version"] == (
        candidate_service.SCHEMA_VERSION_PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_V1
    )
    assert candidate["candidate_status"] == (
        candidate_service.PREDICTIVE_EVIDENCE_IMPROVEMENT_READY_FOR_OPERATOR_REVIEW
    )


def test_all_source_digests_are_bound(candidate: dict) -> None:
    expected = {
        "predictive_usefulness_acceptance_readiness_review_digest": candidate_service.EXPECTED_READINESS_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_review_package_digest": candidate_service.EXPECTED_REASSESSMENT_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_candidate_review_package_digest": candidate_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_results_review_package_digest": candidate_service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_digest": candidate_service.EXPECTED_EXECUTION_DIGEST,
        "additional_predictive_evidence_execution_approval_digest": candidate_service.EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "research_registry_approval_digest": candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "canonical_dataset_freeze_digest": candidate_service.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST,
        "records_digest": candidate_service.EXPECTED_RECORDS_DIGEST,
    }
    assert {key: candidate[key] for key in expected} == expected


def test_target_universe_is_exact_and_ordered(candidate: dict) -> None:
    assert candidate["target_universe_count"] == 12
    assert candidate["target_universe"] == [
        "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
    ]


def test_readiness_failure_summary_is_preserved(candidate: dict) -> None:
    assert candidate["readiness_failure_summary"] == {
        "stability_consistency_required": "FAIL_OR_NOT_MET",
        "baseline_outperformance_consistency_required": "FAIL_OR_NOT_MET",
        "readiness_decision": "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY",
        "readiness_reason": "MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE",
    }


def test_evidence_basis_is_preserved(candidate: dict) -> None:
    assert candidate["evidence_basis"] == {
        "walk_forward_accuracy_range": "0.498698 to 0.562842",
        "oos_majority_accuracy": "0.539491",
        "oos_previous_direction_accuracy": "0.495984",
        "oos_ticker_cross_sectional_accuracy": "0.502677",
        "oos_brier_score": "0.24875351",
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


def test_improvement_objective_scope_mode_and_authority(candidate: dict) -> None:
    assert candidate["predictive_evidence_improvement_objective"] == (
        candidate_service.IMPROVEMENT_OBJECTIVE
    )
    assert candidate["predictive_evidence_improvement_scope"] == (
        candidate_service.IMPROVEMENT_SCOPE
    )
    assert candidate["predictive_evidence_improvement_mode"] == (
        candidate_service.PLANNED_NOT_EXECUTED
    )
    assert candidate["predictive_evidence_improvement_authority_status"] == (
        candidate_service.NOT_AUTHORIZED
    )


def test_improvement_themes_are_planned_only(candidate: dict) -> None:
    themes = candidate["improvement_themes"]
    assert [row["theme_id"] for row in themes] == candidate_service.IMPROVEMENT_THEME_IDS
    assert all(row["status"] == candidate_service.PLANNED_NOT_EXECUTED for row in themes)
    assert all(row["label"] == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in themes)
    assert all(row["evidence_classification"] == "NOT_ACCEPTANCE_EVIDENCE" for row in themes)


def test_refinement_options_require_separate_review_and_approval(candidate: dict) -> None:
    options = candidate["refinement_options"]
    assert [row["option_id"] for row in options] == candidate_service.REFINEMENT_OPTION_IDS
    assert all(row["status"] == candidate_service.PLANNED_NOT_EXECUTED for row in options)
    assert all(row["requires_separate_operator_review"] is True for row in options)
    assert all(row["requires_separate_execution_approval"] is True for row in options)


def test_per_ticker_entries_preserve_counts_and_digests(candidate: dict) -> None:
    entries = candidate["per_ticker_improvement_candidate_entries"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == candidate_service.TARGET_UNIVERSE
    assert len({row["per_ticker_predictive_evidence_improvement_candidate_digest"] for row in entries}) == 12
    for row in entries:
        is_meta = row["ticker"] == "META"
        assert row["historical_record_count"] == (913 if is_meta else 1003)
        assert row["meta_reduced_record_count_flag"] is is_meta
        assert row["improvement_note"] == (
            "PRESERVE_REDUCED_RECORD_COUNT_AND_INCLUDE_LIMITATION_FLAG"
            if is_meta
            else None
        )
        assert row["readiness_status"] == "NOT_READY"
        assert row["improvement_candidate_status"] == "PLANNED_READY_FOR_OPERATOR_REVIEW"
        assert row["source_predictive_usefulness_acceptance_readiness_review_digest"] == candidate_service.EXPECTED_READINESS_REVIEW_DIGEST
        assert row["per_ticker_predictive_evidence_improvement_candidate_digest"] == candidate_service.per_ticker_predictive_evidence_improvement_candidate_digest_v1(row)
        assert row["predictive_usefulness"] == candidate_service.NOT_ACCEPTED
        assert row["runtime_use"] == candidate_service.NOT_AUTHORIZED


def test_future_chain_gates_and_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["future_improvement_chain"] == candidate_service.FUTURE_IMPROVEMENT_CHAIN
    assert candidate["future_gates"] == candidate_service.FUTURE_GATES
    assert candidate["risk_controls"] == candidate_service.RISK_CONTROLS


def test_planned_outputs_are_not_generated(candidate: dict) -> None:
    outputs = candidate["planned_outputs"]
    assert [row["output_name"] for row in outputs] == candidate_service.PLANNED_OUTPUT_NAMES
    assert all(row["status"] == candidate_service.PLANNED_NOT_GENERATED for row in outputs)
    assert all(row["label"] == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for row in outputs)


@pytest.mark.parametrize(
    "field,expected",
    [
        ("provider_requests_made", False),
        ("live_provider_transport_enabled", False),
        ("market_data_acquisition_performed", False),
        ("dataset_generation_performed", False),
        ("canonical_dataset_regenerated", False),
        ("predictive_execution_rerun_performed", False),
        ("label_generation_rerun_performed", False),
        ("feature_matrix_rerun_performed", False),
        ("walk_forward_validation_rerun_performed", False),
        ("out_of_sample_evaluation_rerun_performed", False),
        ("metrics_recomputation_performed", False),
        ("predictive_evidence_improvement_approved", False),
        ("predictive_evidence_improvement_executed", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("label_generation_authorized", False),
        ("label_generation_performed", False),
        ("feature_matrix_generation_authorized", False),
        ("feature_matrix_generation_performed", False),
        ("walk_forward_validation_authorized", False),
        ("walk_forward_validation_performed", False),
        ("out_of_sample_evaluation_authorized", False),
        ("out_of_sample_evaluation_performed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", candidate_service.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_recommended", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", candidate_service.NOT_ACCEPTED),
        ("profitability_acceptance_ready", False),
        ("profitability_acceptance_recommended", False),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", candidate_service.NOT_AUTHORIZED),
        ("strategy_use", candidate_service.NOT_AUTHORIZED),
        ("paper_trading", candidate_service.NOT_AUTHORIZED),
        ("broker_execution", candidate_service.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_closed_execution_and_authority_boundaries(
    candidate: dict, field: str, expected: object
) -> None:
    assert candidate[field] == expected


def test_checklist_is_complete_and_all_checks_pass(candidate: dict) -> None:
    checklist = candidate["candidate_checklist"]
    assert [row["check_id"] for row in checklist] == candidate_service.REQUIRED_CHECK_IDS
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in checklist)
    assert all(row["status"] == candidate_service.PASS for row in checklist)


def test_summary_counts_and_boundaries(candidate: dict) -> None:
    assert candidate["candidate_summary"] == {
        "total_checks": len(candidate_service.REQUIRED_CHECK_IDS),
        "passed_checks": len(candidate_service.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_feature_label_refinement_candidate": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_candidate_and_per_ticker_digests_are_deterministic(candidate: dict) -> None:
    second = candidate_service.build_predictive_evidence_improvement_candidate_v1()
    assert second == candidate
    assert len(candidate["predictive_evidence_improvement_candidate_digest"]) == 64
    assert [row["per_ticker_predictive_evidence_improvement_candidate_digest"] for row in second["per_ticker_improvement_candidate_entries"]] == [row["per_ticker_predictive_evidence_improvement_candidate_digest"] for row in candidate["per_ticker_improvement_candidate_entries"]]


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = candidate_service.validate_predictive_evidence_improvement_candidate_v1(
        candidate
    )
    assert result["status"] == "PREDICTIVE_EVIDENCE_IMPROVEMENT_CANDIDATE_VALID"
    assert result["per_ticker_improvement_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_operator_review"] is True
    assert result["predictive_evidence_improvement_authorized"] is False


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("artifact_kind", "WRONG"),
        ("candidate_status", "WRONG"),
        ("predictive_usefulness_acceptance_readiness_review_digest", "0" * 64),
        ("readiness_decision", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READY"),
        ("readiness_reason", "WRONG"),
        ("predictive_evidence_improvement_candidate_created", False),
        ("predictive_evidence_improvement_authority_status", "AUTHORIZED"),
        ("target_universe_count", 11),
        ("target_universe", list(reversed(candidate_service.TARGET_UNIVERSE))),
        ("predictive_evidence_improvement_approved", True),
        ("predictive_evidence_improvement_executed", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("label_generation_authorized", True),
        ("label_generation_performed", True),
        ("feature_matrix_generation_authorized", True),
        ("feature_matrix_generation_performed", True),
        ("walk_forward_validation_authorized", True),
        ("walk_forward_validation_performed", True),
        ("out_of_sample_evaluation_authorized", True),
        ("out_of_sample_evaluation_performed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("predictive_execution_rerun_performed", True),
        ("label_generation_rerun_performed", True),
        ("feature_matrix_rerun_performed", True),
        ("walk_forward_validation_rerun_performed", True),
        ("out_of_sample_evaluation_rerun_performed", True),
        ("metrics_recomputation_performed", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_changed_top_level_contract(
    candidate: dict, field: str, bad_value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = bad_value
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.validate_predictive_evidence_improvement_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "improvement_themes",
        "refinement_options",
        "future_improvement_chain",
        "future_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_missing_planning_structure(candidate: dict, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid.pop(field)
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.validate_predictive_evidence_improvement_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    ["stability_consistency_required", "baseline_outperformance_consistency_required"],
)
def test_validator_rejects_failed_criterion_marked_pass(candidate: dict, field: str) -> None:
    invalid = deepcopy(candidate)
    invalid["readiness_failure_summary"][field] = candidate_service.PASS
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.validate_predictive_evidence_improvement_candidate_v1(invalid)


def test_validator_rejects_missing_or_changed_candidate_digest(candidate: dict) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(candidate)
        if replacement is None:
            invalid.pop("predictive_evidence_improvement_candidate_digest")
        else:
            invalid["predictive_evidence_improvement_candidate_digest"] = replacement
        with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
            candidate_service.validate_predictive_evidence_improvement_candidate_v1(invalid)


def test_validator_rejects_missing_or_changed_per_ticker_digest(candidate: dict) -> None:
    for replacement in (None, "0" * 64):
        invalid = deepcopy(candidate)
        entry = invalid["per_ticker_improvement_candidate_entries"][0]
        if replacement is None:
            entry.pop("per_ticker_predictive_evidence_improvement_candidate_digest")
        else:
            entry["per_ticker_predictive_evidence_improvement_candidate_digest"] = replacement
        with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
            candidate_service.validate_predictive_evidence_improvement_candidate_v1(invalid)


def test_validator_rejects_missing_check_or_fabricated_summary(candidate: dict) -> None:
    missing_check = deepcopy(candidate)
    missing_check["candidate_checklist"].pop()
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.validate_predictive_evidence_improvement_candidate_v1(missing_check)
    fabricated = deepcopy(candidate)
    fabricated["candidate_summary"]["passed_checks"] = 0
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.validate_predictive_evidence_improvement_candidate_v1(fabricated)


def test_markdown_contains_required_sections(candidate: dict) -> None:
    markdown = candidate_service.build_predictive_evidence_improvement_candidate_markdown_v1(
        candidate
    )
    for heading in (
        "Title",
        "Predictive Evidence Improvement Candidate",
        "Source Acceptance Readiness Review",
        "Readiness Failure Summary",
        "Evidence Basis",
        "Improvement Themes",
        "Refinement Options",
        "Per-Ticker Improvement Candidate Entries",
        "Future Improvement Chain",
        "Future Gates",
        "Risk Controls",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_uses_canonical_json_and_does_not_overwrite(tmp_path: Path) -> None:
    result = candidate_service.write_predictive_evidence_improvement_candidate_v1(
        tmp_path
    )
    path = Path(result["path"])
    package = json.loads(path.read_text(encoding="utf-8"))
    payload = canonical_json_bytes(package)
    assert path.read_bytes() == payload
    assert result["payload_sha256"] == sha256_bytes(payload)
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.write_predictive_evidence_improvement_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["nested/candidate.json", "candidate.txt", "../candidate.json"])
def test_writer_rejects_unsafe_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(candidate_service.PredictiveEvidenceImprovementCandidateError):
        candidate_service.write_predictive_evidence_improvement_candidate_v1(
            tmp_path, filename=filename
        )
