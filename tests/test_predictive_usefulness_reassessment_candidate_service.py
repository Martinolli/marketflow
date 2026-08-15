from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import predictive_usefulness_reassessment_candidate_service as service


@pytest.fixture(scope="module")
def candidate() -> dict:
    return service.build_predictive_usefulness_reassessment_candidate_v1()


def _redigest(candidate: dict) -> dict:
    candidate["candidate_checklist"] = service._checklist(candidate)
    candidate["candidate_summary"] = service._summary(candidate["candidate_checklist"])
    candidate["predictive_usefulness_reassessment_candidate_digest"] = (
        service.predictive_usefulness_reassessment_candidate_digest_v1(candidate)
    )
    return candidate


def test_candidate_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    candidate = service.build_predictive_usefulness_reassessment_candidate_v1()
    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_artifact_kind_schema_and_status(candidate: dict) -> None:
    assert candidate["artifact_kind"] == (
        service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE
    )
    assert candidate["schema_version"] == (
        service.SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_V1
    )
    assert candidate["candidate_status"] == (
        service.PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW
    )


def test_source_digests_are_bound(candidate: dict) -> None:
    assert candidate["additional_predictive_evidence_results_review_package_digest"] == (
        service.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert candidate["additional_predictive_evidence_execution_digest"] == (
        service.EXPECTED_EXECUTION_DIGEST
    )
    assert candidate["additional_predictive_evidence_execution_approval_digest"] == (
        service.EXPECTED_EXECUTION_APPROVAL_DIGEST
    )
    assert candidate["research_registry_approval_digest"] == (
        service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
    )
    assert candidate["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_evidence_summary_is_reviewed_fact_only(candidate: dict) -> None:
    assert candidate["reviewed_evidence_summary"] == {
        "label_coverage_entries": 84,
        "label_available_values": 82854,
        "label_unavailable_values": 768,
        "feature_rows": 11946,
        "feature_fields": 22,
        "walk_forward_fold_count": 4,
        "oos_evaluation_rows": 2988,
        "leakage_status": "PASS",
        "failed_leakage_controls": 0,
    }


def test_performance_interpretation_is_conservative(candidate: dict) -> None:
    performance = candidate["performance_interpretation"]
    assert performance["walk_forward_accuracy_range"] == "0.498698 to 0.562842"
    assert performance["walk_forward_accuracy_stability_status"] == (
        "MIXED_REQUIRES_OPERATOR_REVIEW"
    )
    assert performance["oos_majority_accuracy"] == "0.539491"
    assert performance["oos_previous_direction_accuracy"] == "0.495984"
    assert performance["oos_ticker_cross_sectional_accuracy"] == "0.502677"
    assert performance["oos_brier_score"] == "0.24875351"
    assert performance["performance_signal_status"] == (
        "REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE"
    )
    assert performance["baseline_outperformance_status"] == (
        "MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE"
    )


def test_evidence_supports_review_but_not_acceptance(candidate: dict) -> None:
    assert candidate["evidence_summary_status"] == "READY_FOR_OPERATOR_REVIEW"
    assert candidate["evidence_supports_future_reassessment_review"] is True
    assert candidate["evidence_supports_direct_acceptance"] is False
    assert candidate["operator_review_required_before_acceptance"] is True
    assert candidate["acceptance_recommendation"] == (
        "NOT_RECOMMENDED_AT_CANDIDATE_STAGE"
    )


def test_checklist_and_summary_are_complete(candidate: dict) -> None:
    assert [row["check_id"] for row in candidate["candidate_checklist"]] == (
        service.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == service.PASS for row in candidate["candidate_checklist"])
    assert candidate["candidate_summary"] == {
        "total_checks": len(service.REQUIRED_CHECK_IDS),
        "passed_checks": len(service.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_review": True,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_candidate_digest_is_deterministic(candidate: dict) -> None:
    second = service.build_predictive_usefulness_reassessment_candidate_v1()
    assert second == candidate
    assert len(candidate["predictive_usefulness_reassessment_candidate_digest"]) == 64


def test_validator_accepts_valid_candidate(candidate: dict) -> None:
    result = service.validate_predictive_usefulness_reassessment_candidate_v1(candidate)
    assert result["status"] == "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_VALID"
    assert result["per_ticker_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_predictive_usefulness_reassessment_review"] is False
    assert result["ready_for_predictive_usefulness_acceptance"] is False


EXPECTED_FIELDS = [
    ("target_universe", service.TARGET_UNIVERSE),
    ("target_universe_count", 12),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True),
    ("additional_predictive_evidence_results_review_created", True),
    ("additional_predictive_evidence_results_review_ready", True),
    ("ready_for_predictive_usefulness_reassessment_candidate", True),
    ("predictive_usefulness_reassessment_candidate_created", True),
    ("predictive_usefulness_reassessment_ready_for_operator_review", True),
    ("predictive_usefulness_reassessment_review_created", False),
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
    ("raw_provider_payloads_committed", False),
    ("api_keys_stored_or_printed", False),
    ("new_strategy_scoring_performed", False),
    ("trade_recommendations_generated", False),
    ("predictive_usefulness", service.NOT_ACCEPTED),
    ("predictive_usefulness_acceptance_ready", False),
    ("predictive_usefulness_acceptance_recommended", False),
    ("predictive_usefulness_acceptance_candidate_created", False),
    ("profitability", service.NOT_ACCEPTED),
    ("profitability_acceptance_ready", False),
    ("profitability_acceptance_recommended", False),
    ("runtime_migration_approved", False),
    ("runtime_migration_active", False),
    ("runtime_use", service.NOT_AUTHORIZED),
    ("strategy_use", service.NOT_AUTHORIZED),
    ("paper_trading", service.NOT_AUTHORIZED),
    ("broker_execution", service.NOT_AUTHORIZED),
    ("automatic_stitching", False),
    ("research_only", True),
    ("operator_review_required", True),
    ("predictive_usefulness_acceptance_artifact_created", False),
    ("profitability_acceptance_created", False),
    ("runtime_migration_approval_created", False),
]


@pytest.mark.parametrize(("field", "expected"), EXPECTED_FIELDS)
def test_candidate_expected_field(candidate: dict, field: str, expected: object) -> None:
    assert candidate[field] == expected


@pytest.mark.parametrize(("ticker", "expected_count"), service.EXPECTED_RECORD_COUNTS.items())
def test_per_ticker_entry_preserves_record_count(
    candidate: dict, ticker: str, expected_count: int
) -> None:
    by_ticker = {
        entry["ticker"]: entry
        for entry in candidate["per_ticker_reassessment_candidate_entries"]
    }
    entry = by_ticker[ticker]
    assert entry["historical_record_count"] == expected_count
    assert entry["meta_reduced_record_count_flag"] is (ticker == "META")
    assert entry["predictive_evidence_results_status"] == "REVIEWED_RESEARCH_ONLY"
    assert entry["predictive_usefulness"] == service.NOT_ACCEPTED
    assert entry["runtime_use"] == service.NOT_AUTHORIZED


@pytest.mark.parametrize("ticker", service.TARGET_UNIVERSE)
def test_per_ticker_digest_is_present_and_deterministic(candidate: dict, ticker: str) -> None:
    entry = next(
        item
        for item in candidate["per_ticker_reassessment_candidate_entries"]
        if item["ticker"] == ticker
    )
    digest = entry["per_ticker_predictive_usefulness_reassessment_candidate_digest"]
    assert len(digest) == 64
    assert digest == (
        service.per_ticker_predictive_usefulness_reassessment_candidate_digest_v1(entry)
    )


@pytest.mark.parametrize("domain_id", service.REASSESSMENT_DOMAIN_IDS)
def test_reassessment_domain_is_candidate_only(candidate: dict, domain_id: str) -> None:
    domain = next(
        item for item in candidate["reassessment_domains"] if item["domain_id"] == domain_id
    )
    assert domain["candidate_status"] == service.CANDIDATE_READY_FOR_OPERATOR_REVIEW
    assert domain["acceptance_status"] == service.NOT_ACCEPTANCE
    assert domain["output_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE


@pytest.mark.parametrize("output_id", service.PLANNED_OUTPUT_IDS)
def test_planned_output_is_not_generated_and_research_only(
    candidate: dict, output_id: str
) -> None:
    output = next(
        item for item in candidate["planned_outputs"] if item["output_id"] == output_id
    )
    assert output["generation_status"] == service.PLANNED_NOT_GENERATED
    assert output["output_label"] == service.RESEARCH_ONLY_NON_ACTIONABLE


def test_future_chain_gates_and_risk_controls_are_exact(candidate: dict) -> None:
    assert candidate["future_reassessment_chain"] == service.FUTURE_REASSESSMENT_CHAIN
    assert candidate["future_gates"] == service.FUTURE_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("schema_version", "WRONG"),
    ("candidate_status", "WRONG"),
    ("target_universe", list(reversed(service.TARGET_UNIVERSE))),
    ("target_universe_count", 11),
    ("additional_predictive_evidence_results_review_package_digest", "0" * 64),
    ("additional_predictive_evidence_execution_digest", "0" * 64),
    ("additional_predictive_evidence_executed", False),
    ("additional_predictive_evidence_results_review_ready", False),
    ("predictive_usefulness_reassessment_candidate_created", False),
    ("evidence_supports_direct_acceptance", True),
    ("acceptance_recommendation", "RECOMMENDED"),
    ("provider_requests_made", True),
    ("live_provider_transport_enabled", True),
    ("market_data_acquisition_performed", True),
    ("dataset_generation_performed", True),
    ("canonical_dataset_regenerated", True),
    ("predictive_execution_rerun_performed", True),
    ("label_generation_rerun_performed", True),
    ("feature_matrix_rerun_performed", True),
    ("walk_forward_validation_rerun_performed", True),
    ("out_of_sample_evaluation_rerun_performed", True),
    ("metrics_recomputation_performed", True),
    ("new_strategy_scoring_performed", True),
    ("trade_recommendations_generated", True),
    ("predictive_usefulness", "accepted"),
    ("predictive_usefulness_acceptance_ready", True),
    ("predictive_usefulness_acceptance_recommended", True),
    ("predictive_usefulness_acceptance_candidate_created", True),
    ("profitability", "accepted"),
    ("profitability_acceptance_ready", True),
    ("runtime_migration_approved", True),
    ("runtime_migration_active", True),
    ("runtime_use", "AUTHORIZED"),
    ("strategy_use", "AUTHORIZED"),
    ("paper_trading", "AUTHORIZED"),
    ("broker_execution", "AUTHORIZED"),
    ("automatic_stitching", True),
]


@pytest.mark.parametrize(("field", "value"), VALIDATOR_MUTATIONS)
def test_validator_rejects_invalid_top_level_field(
    candidate: dict, field: str, value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid[field] = value
    _redigest(invalid)
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.validate_predictive_usefulness_reassessment_candidate_v1(invalid)


NESTED_EVIDENCE_MUTATIONS = [
    ("label_coverage_entries", 83),
    ("label_available_values", 82853),
    ("label_unavailable_values", 767),
    ("feature_rows", 11945),
    ("feature_fields", 21),
    ("walk_forward_fold_count", 3),
    ("oos_evaluation_rows", 2987),
    ("leakage_status", "FAIL"),
    ("failed_leakage_controls", 1),
]


@pytest.mark.parametrize(("field", "value"), NESTED_EVIDENCE_MUTATIONS)
def test_validator_rejects_invalid_reviewed_evidence(
    candidate: dict, field: str, value: object
) -> None:
    invalid = deepcopy(candidate)
    invalid["reviewed_evidence_summary"][field] = value
    _redigest(invalid)
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.validate_predictive_usefulness_reassessment_candidate_v1(invalid)


@pytest.mark.parametrize(
    "field",
    [
        "reassessment_domains",
        "future_reassessment_chain",
        "future_gates",
        "risk_controls",
        "planned_outputs",
    ],
)
def test_validator_rejects_missing_governance_collection(
    candidate: dict, field: str
) -> None:
    invalid = deepcopy(candidate)
    invalid.pop(field)
    _redigest(invalid)
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.validate_predictive_usefulness_reassessment_candidate_v1(invalid)


def test_validator_rejects_changed_per_ticker_entry(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid["per_ticker_reassessment_candidate_entries"][4]["historical_record_count"] = 1003
    _redigest(invalid)
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.validate_predictive_usefulness_reassessment_candidate_v1(invalid)


def test_validator_rejects_missing_candidate_digest(candidate: dict) -> None:
    invalid = deepcopy(candidate)
    invalid.pop("predictive_usefulness_reassessment_candidate_digest")
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.validate_predictive_usefulness_reassessment_candidate_v1(invalid)


MARKDOWN_SECTIONS = [
    "Title",
    "Predictive Usefulness Reassessment Candidate",
    "Source Additional Predictive Evidence Results Review",
    "Registry-Approved Dataset Metadata",
    "Target Universe",
    "Evidence Summary",
    "Performance Interpretation",
    "Per-Ticker Reassessment Candidate Entries",
    "Reassessment Domains",
    "Future Reassessment Chain",
    "Future Gates",
    "Risk Controls",
    "Predictive Usefulness Boundary",
    "Profitability Boundary",
    "Runtime Boundary",
    "Checklist Summary",
    "Guardrails",
]


@pytest.mark.parametrize("section", MARKDOWN_SECTIONS)
def test_markdown_contains_required_section(candidate: dict, section: str) -> None:
    markdown = service.build_predictive_usefulness_reassessment_candidate_markdown_v1(
        candidate
    )
    assert f"## {section}" in markdown


def test_writer_writes_canonical_json_once(candidate: dict, tmp_path: Path) -> None:
    result = service.write_predictive_usefulness_reassessment_candidate_v1(tmp_path)
    path = Path(result["path"])
    assert path.read_bytes() == canonical_json_bytes(candidate)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.write_predictive_usefulness_reassessment_candidate_v1(tmp_path)


@pytest.mark.parametrize("filename", ["candidate.txt", "../candidate.json", "x/candidate.json"])
def test_writer_rejects_invalid_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(service.PredictiveUsefulnessReassessmentCandidateError):
        service.write_predictive_usefulness_reassessment_candidate_v1(
            tmp_path, filename=filename
        )
