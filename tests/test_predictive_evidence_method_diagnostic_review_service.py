from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    predictive_evidence_method_diagnostic_review_service as review,
)


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_predictive_evidence_method_diagnostic_review_package_v1()


def test_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = review.build_predictive_evidence_method_diagnostic_review_package_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_review"] is False
    assert built["live_provider_transport_enabled_in_review"] is False


def test_artifact_status_and_diagnostic_state_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_READY
    )
    assert package["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_V1
    )
    assert package["method_diagnostic_review_created"] is True
    assert package["method_diagnostic_review_ready"] is True
    assert package["ready_for_operator_method_path_selection"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    list(review.REQUIRED_DIGEST_FIELDS.items()),
)
def test_required_digest_chain_is_bound(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_dataset_universe_and_record_counts_are_preserved(package: dict) -> None:
    assert package["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert package["source_profile"] == "RTH_FULL_SESSION_1D"
    assert package["timeframe"] == "1d"
    assert package["date_range_start"] == "2022-01-01"
    assert package["date_range_end"] == "2025-12-31"
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["records_digest"] == review.EXPECTED_RECORDS_DIGEST
    assert package["meta_record_count"] == 913
    assert package["meta_reduced_record_count_preserved"] is True
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in review.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_readiness_and_diagnostic_findings_are_conservative(package: dict) -> None:
    assert package["original_readiness_decision"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
    )
    assert package["refined_readiness_decision"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE"
    )
    assert package["overall_method_signal_status"] == "WEAK_OR_MIXED"
    assert package["baseline_outperformance_status"] == "INSUFFICIENT_OR_MIXED"
    assert package["oos_generalization_status"] == "LOW_TO_MIXED"
    assert package["acceptance_readiness_status"] == "NOT_READY_TWICE"
    assert package["method_diagnostic_conclusion"] == (
        "METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION"
    )


def test_evidence_comparison_is_exact(package: dict) -> None:
    assert package["evidence_comparison"] == {
        "original_oos_majority_accuracy": "0.539491",
        "original_oos_previous_direction_accuracy": "0.495984",
        "original_oos_ticker_cross_sectional_accuracy": "0.502677",
        "original_oos_brier_score": "0.24875351",
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "refined_signal_consistency": "WEAK_OR_MIXED",
        "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
        "refined_model_comparison": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
    }
    assert package["two_readiness_gates_not_ready"] is True
    assert package["refined_evidence_did_not_create_acceptance_readiness"] is True


def test_diagnostic_domains_are_complete_and_non_actionable(package: dict) -> None:
    domains = package["diagnostic_domains"]
    assert [item["domain_id"] for item in domains] == review.DIAGNOSTIC_DOMAIN_IDS
    assert len(domains) == 16
    for domain in domains:
        assert domain["domain_status"] == "DIAGNOSIS_RECORDED_RESEARCH_ONLY"
        assert domain["evidence_basis"]
        assert domain["diagnostic_observation"]
        assert domain["possible_failure_mechanism"]
        assert domain["recommended_investigation"]
        assert domain["execution_required"] is False
        assert domain["research_only"] is True
        assert domain["non_actionable"] is True


def test_failure_mechanisms_are_complete(package: dict) -> None:
    assert package["possible_failure_mechanisms"] == review.FAILURE_MECHANISMS
    assert len(package["possible_failure_mechanisms"]) == 13
    domain_mechanisms = {
        item["possible_failure_mechanism"] for item in package["diagnostic_domains"]
    }
    assert set(review.FAILURE_MECHANISMS).issubset(domain_mechanisms)


def test_method_path_options_are_non_authorizing(package: dict) -> None:
    options = package["method_path_options"]
    assert [item["option_id"] for item in options] == review.OPTION_IDS
    assert all(item["selected_or_approved"] is False for item in options)
    assert all(item["execution_authorized"] is False for item in options)
    option_map = {item["option_id"]: item for item in options}
    assert option_map["OPTION_B_METHOD_DIAGNOSTIC_REVIEW"]["status"] == (
        review.COMPLETED_BY_THIS_PACKAGE
    )
    assert option_map["OPTION_G_ACCEPTANCE_CANDIDATE"]["status"] == (
        review.NOT_ALLOWED_CURRENTLY
    )


def test_operator_method_path_selection_is_recommended_but_not_selected(
    package: dict,
) -> None:
    assert package["recommended_next_path"] == "OPERATOR_METHOD_PATH_SELECTION"
    assert package["recommended_immediate_action"] == (
        "OPERATOR_METHOD_PATH_SELECTION_BEFORE_ANY_NEW_EXECUTION"
    )
    assert package["recommendation_reason"] == (
        "TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE"
    )
    assert package["allowed_selections_later"] == review.ALLOWED_SELECTIONS_LATER
    assert package["operator_method_path_selected"] is False
    assert package["approved_execution_path"] is None


def test_risk_controls_and_planned_outputs_are_exact(package: dict) -> None:
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert len(package["risk_controls"]) == 13
    assert [item["output_name"] for item in package["planned_outputs"]] == (
        review.PLANNED_OUTPUT_NAMES
    )
    assert all(
        item["status"] == review.PLANNED_NOT_GENERATED
        for item in package["planned_outputs"]
    )
    assert all(
        item["label"] == review.RESEARCH_ONLY_NON_ACTIONABLE
        for item in package["planned_outputs"]
    )


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_regeneration_performed_in_review",
        "original_predictive_evidence_rerun_performed",
        "refined_predictive_evidence_rerun_performed",
        "label_generation_rerun_performed",
        "feature_generation_rerun_performed",
        "metrics_recomputation_performed",
        "model_training_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "label_objective_redesign_candidate_created",
        "feature_method_redesign_candidate_created",
        "data_scope_expansion_candidate_created",
        "new_modeling_approach_candidate_created",
    ],
)
def test_execution_acceptance_and_redesign_actions_remain_false(
    package: dict, field: str
) -> None:
    assert package[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", review.NOT_ACCEPTED),
        ("profitability", review.NOT_ACCEPTED),
        ("runtime_use", review.NOT_AUTHORIZED),
        ("strategy_use", review.NOT_AUTHORIZED),
        ("paper_trading", review.NOT_AUTHORIZED),
        ("broker_execution", review.NOT_AUTHORIZED),
    ],
)
def test_final_authorities_remain_closed(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_checklist_and_summary_pass(package: dict) -> None:
    checklist = package["review_checklist"]
    assert [item["check_id"] for item in checklist] == review.CHECK_IDS
    assert all(
        set(item)
        == {"check_id", "status", "expected", "actual", "severity", "message"}
        for item in checklist
    )
    assert all(item["status"] == review.PASS for item in checklist)
    assert package["review_summary"] == {
        "total_checks": 35,
        "passed_checks": 35,
        "failed_checks": 0,
        "blocker_count": 0,
        "method_diagnostic_review_ready": True,
        "recommended_next_path": review.RECOMMENDED_NEXT_PATH,
        "acceptance_candidate_allowed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_package_digest_is_deterministic(package: dict) -> None:
    repeated = review.build_predictive_evidence_method_diagnostic_review_package_v1()
    field = "predictive_evidence_method_diagnostic_review_package_digest"
    assert repeated[field] == package[field]
    assert repeated[field] == (
        review.predictive_evidence_method_diagnostic_review_package_digest_v1(
            repeated
        )
    )
    assert len(repeated[field]) == 64


def test_validator_accepts_valid_package(package: dict) -> None:
    validation = review.validate_predictive_evidence_method_diagnostic_review_package_v1(
        package
    )
    assert validation["status"] == (
        "PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_VALID"
    )
    assert validation["diagnostic_domain_count"] == 16
    assert validation["failure_mechanism_count"] == 13
    assert validation["blocker_count"] == 0
    assert validation["recommended_next_path"] == review.RECOMMENDED_NEXT_PATH


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("predictive_evidence_planning_tree_review_package_digest", None),
        ("latest_readiness_rerun_using_refined_evidence_digest", None),
        ("latest_reassessment_rerun_using_refined_evidence_digest", None),
        ("original_acceptance_readiness_review_digest", None),
        ("research_registry_approval_digest", None),
        ("records_digest", "0" * 64),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("runtime_migration_approved", True),
        ("trade_recommendations_generated", True),
        ("diagnostic_domains", []),
        ("possible_failure_mechanisms", []),
        ("recommended_next_path", None),
        ("risk_controls", []),
        ("predictive_evidence_method_diagnostic_review_package_digest", None),
    ],
)
def test_validator_rejects_changed_contract_fields(
    package: dict, field: str, replacement: object
) -> None:
    invalid = deepcopy(package)
    invalid[field] = replacement
    with pytest.raises(review.PredictiveEvidenceMethodDiagnosticReviewError):
        review.validate_predictive_evidence_method_diagnostic_review_package_v1(
            invalid
        )


def test_validator_rejects_acceptance_option_allowed(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["method_path_options"][-1]["status"] = (
        review.AVAILABLE_FOR_OPERATOR_SELECTION
    )
    with pytest.raises(review.PredictiveEvidenceMethodDiagnosticReviewError):
        review.validate_predictive_evidence_method_diagnostic_review_package_v1(
            invalid
        )


def test_validator_rejects_selected_or_approved_method_path(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["method_path_options"][0]["selected_or_approved"] = True
    with pytest.raises(review.PredictiveEvidenceMethodDiagnosticReviewError):
        review.validate_predictive_evidence_method_diagnostic_review_package_v1(
            invalid
        )


def test_markdown_contains_required_sections(package: dict) -> None:
    markdown = review.build_predictive_evidence_method_diagnostic_review_markdown_v1(
        package
    )
    for heading in (
        "Title",
        "Method Diagnostic Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Evidence Comparison",
        "Diagnostic Domains",
        "Possible Failure Mechanisms",
        "Method Path Options",
        "Recommended Next Path",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_emits_canonical_json_and_does_not_overwrite(tmp_path) -> None:
    result = review.write_predictive_evidence_method_diagnostic_review_package_v1(
        tmp_path
    )
    output_path = tmp_path / result["filename"]
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    review.validate_predictive_evidence_method_diagnostic_review_package_v1(payload)
    with pytest.raises(review.PredictiveEvidenceMethodDiagnosticReviewError):
        review.write_predictive_evidence_method_diagnostic_review_package_v1(
            tmp_path
        )
