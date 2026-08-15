from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import (
    predictive_usefulness_reassessment_candidate_operator_review_service as review,
)


@pytest.fixture(scope="module")
def review_package() -> dict:
    return review.build_predictive_usefulness_reassessment_candidate_review_package_v1()


def _redigest(package: dict) -> dict:
    package["review_checklist"] = review._checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["predictive_usefulness_reassessment_candidate_review_package_digest"] = (
        review.predictive_usefulness_reassessment_candidate_review_package_digest_v1(
            package
        )
    )
    return package


def test_review_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    package = review.build_predictive_usefulness_reassessment_candidate_review_package_v1()
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_accepts_exact_supplied_candidate() -> None:
    candidate = review.candidate_service.build_predictive_usefulness_reassessment_candidate_v1()
    package = review.build_predictive_usefulness_reassessment_candidate_review_package_v1(
        candidate
    )
    assert package["reviewed_predictive_usefulness_reassessment_candidate_digest"] == (
        candidate["predictive_usefulness_reassessment_candidate_digest"]
    )


def test_artifact_kind_schema_and_status(review_package: dict) -> None:
    assert review_package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE
    )
    assert review_package["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_V1
    )
    assert review_package["review_status"] == (
        review.PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_READY
    )


def test_reviewed_candidate_identity_and_checklist_are_bound(review_package: dict) -> None:
    assert review_package["reviewed_predictive_usefulness_reassessment_candidate_kind"] == (
        review.candidate_service.ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE
    )
    assert review_package["reviewed_predictive_usefulness_reassessment_candidate_status"] == (
        review.candidate_service.PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW
    )
    assert review_package["reviewed_predictive_usefulness_reassessment_candidate_digest"] == (
        review.EXPECTED_CANDIDATE_DIGEST
    )
    assert review_package[
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_total"
    ] == 62
    assert review_package[
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_passed"
    ] == 62
    assert review_package[
        "reviewed_predictive_usefulness_reassessment_candidate_checklist_failed"
    ] == 0
    assert review_package[
        "reviewed_predictive_usefulness_reassessment_candidate_blocker_count"
    ] == 0


def test_source_digests_are_bound(review_package: dict) -> None:
    assert review_package["additional_predictive_evidence_results_review_package_digest"] == (
        review.EXPECTED_RESULTS_REVIEW_PACKAGE_DIGEST
    )
    assert review_package["additional_predictive_evidence_execution_digest"] == (
        review.EXPECTED_EXECUTION_DIGEST
    )
    assert review_package["additional_predictive_evidence_execution_approval_digest"] == (
        review.EXPECTED_EXECUTION_APPROVAL_DIGEST
    )
    assert review_package["research_registry_approval_digest"] == (
        review.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
    )
    assert review_package["records_digest"] == review.EXPECTED_RECORDS_DIGEST


def test_evidence_and_performance_interpretation_are_preserved(
    review_package: dict,
) -> None:
    assert review_package["reviewed_evidence_summary"] == {
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
    performance = review_package["reviewed_performance_interpretation"]
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


def test_evidence_supports_review_but_not_acceptance(review_package: dict) -> None:
    assert review_package["evidence_supports_future_reassessment_review"] is True
    assert review_package["evidence_supports_direct_acceptance"] is False
    assert review_package["operator_review_required_before_acceptance"] is True
    assert review_package["acceptance_recommendation"] == (
        "NOT_RECOMMENDED_AT_CANDIDATE_STAGE"
    )


def test_review_checklist_and_summary_are_complete(review_package: dict) -> None:
    assert [row["check_id"] for row in review_package["review_checklist"]] == (
        review.REQUIRED_CHECK_IDS
    )
    assert all(row["status"] == review.PASS for row in review_package["review_checklist"])
    assert review_package["review_summary"] == {
        "total_checks": len(review.REQUIRED_CHECK_IDS),
        "passed_checks": len(review.REQUIRED_CHECK_IDS),
        "failed_checks": 0,
        "blocker_count": 0,
        "ready_for_operator_assessment": True,
        "ready_for_predictive_usefulness_reassessment_review": False,
        "ready_for_predictive_usefulness_acceptance": False,
        "predictive_usefulness_accepted": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def test_review_digest_is_deterministic(review_package: dict) -> None:
    second = review.build_predictive_usefulness_reassessment_candidate_review_package_v1()
    assert second == review_package
    assert len(
        review_package[
            "predictive_usefulness_reassessment_candidate_review_package_digest"
        ]
    ) == 64


def test_validator_accepts_valid_review_package(review_package: dict) -> None:
    result = review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
        review_package
    )
    assert result["status"] == (
        "PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE_REVIEW_PACKAGE_VALID"
    )
    assert result["per_ticker_review_entry_count"] == 12
    assert result["blocker_count"] == 0
    assert result["ready_for_predictive_usefulness_reassessment_review"] is False
    assert result["ready_for_predictive_usefulness_acceptance"] is False


EXPECTED_FIELDS = [
    ("target_universe", review.TARGET_UNIVERSE),
    ("target_universe_count", 12),
    ("additional_predictive_evidence_executed", True),
    ("additional_predictive_evidence_results_created", True),
    ("additional_predictive_evidence_results_review_created", True),
    ("additional_predictive_evidence_results_review_ready", True),
    ("ready_for_predictive_usefulness_reassessment_candidate", True),
    ("predictive_usefulness_reassessment_candidate_created", True),
    ("predictive_usefulness_reassessment_candidate_review_created", True),
    ("predictive_usefulness_reassessment_ready_for_operator_review", True),
    ("predictive_usefulness_reassessment_review_created", False),
    ("provider_requests_made_in_review", False),
    ("live_provider_transport_enabled_in_review", False),
    ("market_data_acquisition_performed_in_review", False),
    ("dataset_generation_performed_in_review", False),
    ("canonical_dataset_regenerated_in_review", False),
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
    ("predictive_usefulness", review.NOT_ACCEPTED),
    ("predictive_usefulness_acceptance_ready", False),
    ("predictive_usefulness_acceptance_recommended", False),
    ("predictive_usefulness_acceptance_candidate_created", False),
    ("profitability", review.NOT_ACCEPTED),
    ("profitability_acceptance_ready", False),
    ("profitability_acceptance_recommended", False),
    ("runtime_migration_approved", False),
    ("runtime_migration_active", False),
    ("runtime_use", review.NOT_AUTHORIZED),
    ("strategy_use", review.NOT_AUTHORIZED),
    ("paper_trading", review.NOT_AUTHORIZED),
    ("broker_execution", review.NOT_AUTHORIZED),
    ("automatic_stitching", False),
    ("research_only", True),
    ("operator_review_required", True),
    ("planned_output_count", 7),
    ("planned_outputs_status", review.PLANNED_NOT_GENERATED),
    ("planned_outputs_label", review.RESEARCH_ONLY_NON_ACTIONABLE),
    ("predictive_usefulness_acceptance_artifact_created", False),
    ("profitability_acceptance_created", False),
    ("runtime_migration_approval_created", False),
]


@pytest.mark.parametrize(("field", "expected"), EXPECTED_FIELDS)
def test_review_package_expected_field(
    review_package: dict, field: str, expected: object
) -> None:
    assert review_package[field] == expected


@pytest.mark.parametrize(("ticker", "expected_count"), review.EXPECTED_RECORD_COUNTS.items())
def test_per_ticker_review_entry_preserves_record_count_and_boundaries(
    review_package: dict, ticker: str, expected_count: int
) -> None:
    entry = next(
        item
        for item in review_package["per_ticker_reassessment_candidate_review_entries"]
        if item["ticker"] == ticker
    )
    assert entry["historical_record_count"] == expected_count
    assert entry["meta_reduced_record_count_flag"] is (ticker == "META")
    assert entry["predictive_usefulness_reassessment_candidate_status"] == (
        "READY_FOR_OPERATOR_REVIEW"
    )
    assert entry["predictive_usefulness_reassessment_candidate_review_status"] == (
        review.READY_FOR_OPERATOR_ASSESSMENT
    )
    assert entry["predictive_usefulness"] == review.NOT_ACCEPTED
    assert entry["runtime_use"] == review.NOT_AUTHORIZED


@pytest.mark.parametrize("ticker", review.TARGET_UNIVERSE)
def test_per_ticker_candidate_and_review_digests_are_deterministic(
    review_package: dict, ticker: str
) -> None:
    entry = next(
        item
        for item in review_package["per_ticker_reassessment_candidate_review_entries"]
        if item["ticker"] == ticker
    )
    assert len(
        entry["per_ticker_predictive_usefulness_reassessment_candidate_digest"]
    ) == 64
    review_digest = entry[
        "per_ticker_predictive_usefulness_reassessment_candidate_review_digest"
    ]
    assert len(review_digest) == 64
    assert review_digest == (
        review.per_ticker_predictive_usefulness_reassessment_candidate_review_digest_v1(
            entry
        )
    )


@pytest.mark.parametrize("domain_id", review.candidate_service.REASSESSMENT_DOMAIN_IDS)
def test_reviewed_reassessment_domain_preserves_candidate_boundary(
    review_package: dict, domain_id: str
) -> None:
    domain = next(
        item
        for item in review_package["reviewed_reassessment_domains"]
        if item["domain_id"] == domain_id
    )
    assert domain["candidate_status"] == (
        review.candidate_service.CANDIDATE_READY_FOR_OPERATOR_REVIEW
    )
    assert domain["acceptance_status"] == review.candidate_service.NOT_ACCEPTANCE
    assert domain["output_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE


@pytest.mark.parametrize("output_id", review.candidate_service.PLANNED_OUTPUT_IDS)
def test_reviewed_planned_output_remains_not_generated(
    review_package: dict, output_id: str
) -> None:
    output = next(
        item
        for item in review_package["reviewed_planned_outputs"]
        if item["output_id"] == output_id
    )
    assert output["generation_status"] == review.PLANNED_NOT_GENERATED
    assert output["output_label"] == review.RESEARCH_ONLY_NON_ACTIONABLE


def test_future_chain_gates_and_risk_controls_are_preserved(review_package: dict) -> None:
    assert review_package["reviewed_future_reassessment_chain"] == (
        review.candidate_service.FUTURE_REASSESSMENT_CHAIN
    )
    assert review_package["reviewed_future_gates"] == review.candidate_service.FUTURE_GATES
    assert review_package["reviewed_risk_controls"] == review.candidate_service.RISK_CONTROLS


VALIDATOR_MUTATIONS = [
    ("artifact_kind", "WRONG"),
    ("schema_version", "WRONG"),
    ("review_status", "WRONG"),
    ("reviewed_predictive_usefulness_reassessment_candidate_digest", "0" * 64),
    ("reviewed_predictive_usefulness_reassessment_candidate_status", "WRONG"),
    ("target_universe", list(reversed(review.TARGET_UNIVERSE))),
    ("target_universe_count", 11),
    ("additional_predictive_evidence_results_review_package_digest", "0" * 64),
    ("additional_predictive_evidence_execution_digest", "0" * 64),
    ("additional_predictive_evidence_executed", False),
    ("additional_predictive_evidence_results_review_ready", False),
    ("predictive_usefulness_reassessment_candidate_created", False),
    ("predictive_usefulness_reassessment_candidate_review_created", False),
    ("evidence_supports_direct_acceptance", True),
    ("acceptance_recommendation", "RECOMMENDED"),
    ("provider_requests_made_in_review", True),
    ("live_provider_transport_enabled_in_review", True),
    ("market_data_acquisition_performed_in_review", True),
    ("dataset_generation_performed_in_review", True),
    ("canonical_dataset_regenerated_in_review", True),
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
    ("profitability_acceptance_recommended", True),
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
    review_package: dict, field: str, value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid[field] = value
    _redigest(invalid)
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
            invalid
        )


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
    review_package: dict, field: str, value: object
) -> None:
    invalid = deepcopy(review_package)
    invalid["reviewed_evidence_summary"][field] = value
    _redigest(invalid)
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_reassessment_domains",
        "reviewed_future_reassessment_chain",
        "reviewed_future_gates",
        "reviewed_risk_controls",
    ],
)
def test_validator_rejects_missing_reviewed_governance_collection(
    review_package: dict, field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid.pop(field)
    _redigest(invalid)
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
            invalid
        )


@pytest.mark.parametrize(
    "digest_field",
    [
        "per_ticker_predictive_usefulness_reassessment_candidate_digest",
        "per_ticker_predictive_usefulness_reassessment_candidate_review_digest",
    ],
)
def test_validator_rejects_missing_per_ticker_digest(
    review_package: dict, digest_field: str
) -> None:
    invalid = deepcopy(review_package)
    invalid["per_ticker_reassessment_candidate_review_entries"][0].pop(digest_field)
    _redigest(invalid)
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
            invalid
        )


def test_validator_rejects_missing_review_package_digest(review_package: dict) -> None:
    invalid = deepcopy(review_package)
    invalid.pop("predictive_usefulness_reassessment_candidate_review_package_digest")
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.validate_predictive_usefulness_reassessment_candidate_review_package_v1(
            invalid
        )


def test_builder_rejects_changed_candidate() -> None:
    candidate = review.candidate_service.build_predictive_usefulness_reassessment_candidate_v1()
    candidate["target_universe"] = list(reversed(candidate["target_universe"]))
    with pytest.raises(review.candidate_service.PredictiveUsefulnessReassessmentCandidateError):
        review.build_predictive_usefulness_reassessment_candidate_review_package_v1(
            candidate
        )


MARKDOWN_SECTIONS = [
    "Title",
    "Predictive Usefulness Reassessment Candidate Review Package",
    "Reviewed Candidate",
    "Source Additional Predictive Evidence Results Review",
    "Registry-Approved Dataset Metadata",
    "Target Universe",
    "Evidence Summary Review",
    "Performance Interpretation Review",
    "Per-Ticker Reassessment Candidate Review Entries",
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
def test_markdown_contains_required_section(review_package: dict, section: str) -> None:
    markdown = (
        review.build_predictive_usefulness_reassessment_candidate_review_markdown_v1(
            review_package
        )
    )
    assert f"## {section}" in markdown


def test_writer_writes_canonical_json_once(review_package: dict, tmp_path: Path) -> None:
    result = review.write_predictive_usefulness_reassessment_candidate_review_package_v1(
        tmp_path
    )
    path = Path(result["path"])
    assert path.read_bytes() == canonical_json_bytes(review_package)
    assert result["payload_sha256"] == sha256_bytes(path.read_bytes())
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.write_predictive_usefulness_reassessment_candidate_review_package_v1(
            tmp_path
        )


@pytest.mark.parametrize("filename", ["review.txt", "../review.json", "x/review.json"])
def test_writer_rejects_invalid_filename(tmp_path: Path, filename: str) -> None:
    with pytest.raises(review.PredictiveUsefulnessReassessmentCandidateReviewError):
        review.write_predictive_usefulness_reassessment_candidate_review_package_v1(
            tmp_path, filename=filename
        )
