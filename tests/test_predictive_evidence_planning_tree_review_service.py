from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import predictive_evidence_planning_tree_review_service as review


@pytest.fixture(scope="module")
def package() -> dict:
    return review.build_predictive_evidence_planning_tree_review_package_v1()


def test_package_builds_offline_without_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    built = review.build_predictive_evidence_planning_tree_review_package_v1()
    assert built["created_offline"] is True
    assert built["provider_requests_made_in_review"] is False
    assert built["live_provider_transport_enabled_in_review"] is False


def test_artifact_and_status_are_exact(package: dict) -> None:
    assert package["artifact_kind"] == (
        review.ARTIFACT_KIND_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE
    )
    assert package["review_status"] == (
        review.PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_READY
    )
    assert package["schema_version"] == (
        review.SCHEMA_VERSION_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_V1
    )
    assert package["planning_tree_review_created"] is True
    assert package["planning_tree_review_ready"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    list(review.REQUIRED_DIGEST_FIELDS.items()),
)
def test_required_digest_chain_is_bound(
    package: dict, field: str, expected: str
) -> None:
    assert package[field] == expected


def test_dataset_universe_and_record_counts_are_preserved(package: dict) -> None:
    assert package["registry_approved_dataset_metadata"] == (
        review.REGISTRY_APPROVED_DATASET_METADATA
    )
    assert package["target_universe"] == review.TARGET_UNIVERSE
    assert package["target_universe_count"] == 12
    assert package["total_canonical_record_count"] == 11946
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert all(
        package["per_ticker_record_counts"][ticker] == 1003
        for ticker in review.TARGET_UNIVERSE
        if ticker != "META"
    )


def test_planning_tree_has_all_twelve_required_sections(package: dict) -> None:
    assert [item["section_id"] for item in package["planning_tree_sections"]] == [
        "research_registry_and_canonical_dataset_state",
        "original_additional_predictive_evidence_execution",
        "original_predictive_usefulness_reassessment",
        "original_acceptance_readiness_decision",
        "predictive_evidence_improvement_candidate_chain",
        "feature_label_refinement_chain",
        "refined_additional_predictive_evidence_chain",
        "predictive_usefulness_reassessment_rerun_using_refined_evidence",
        "acceptance_readiness_rerun_using_refined_evidence",
        "final_decision_state",
        "current_blocked_downstream_authorities",
        "recommended_next_planning_options",
    ]


def test_original_evidence_cycle_is_summarized_without_acceptance(package: dict) -> None:
    cycle = package["original_evidence_cycle"]
    assert cycle["additional_predictive_evidence_execution_status"] == (
        "COMPLETED_RESEARCH_ONLY"
    )
    assert cycle["predictive_usefulness_reassessment_status"] == (
        "COMPLETED_RESEARCH_ONLY"
    )
    assert cycle["readiness_decision"] == review.ORIGINAL_READINESS_DECISION
    assert cycle["predictive_usefulness_accepted"] is False


def test_refined_evidence_cycle_is_summarized_without_acceptance(package: dict) -> None:
    cycle = package["refined_evidence_cycle"]
    assert cycle["feature_label_refinement_status"] == "COMPLETED_RESEARCH_ONLY"
    assert cycle["additional_predictive_evidence_status"] == (
        "COMPLETED_RESEARCH_ONLY"
    )
    assert cycle["predictive_usefulness_reassessment_status"] == (
        "COMPLETED_RESEARCH_ONLY"
    )
    assert cycle["readiness_decision"] == review.REFINED_READINESS_DECISION
    assert cycle["predictive_usefulness_accepted"] is False


def test_final_readiness_decisions_and_authority_state_are_exact(package: dict) -> None:
    assert package["original_readiness_decision"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
    )
    assert package["refined_readiness_decision"] == (
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE"
    )
    assert package["final_predictive_usefulness_state"] == review.NOT_ACCEPTED
    assert package["final_profitability_state"] == review.NOT_ACCEPTED
    assert package["final_runtime_state"] == review.NOT_AUTHORIZED
    assert package["final_decision_summary"] == {
        "original_readiness_decision": review.ORIGINAL_READINESS_DECISION,
        "refined_readiness_decision": review.REFINED_READINESS_DECISION,
        "final_predictive_usefulness_state": review.NOT_ACCEPTED,
        "final_profitability_state": review.NOT_ACCEPTED,
        "final_runtime_state": review.NOT_AUTHORIZED,
    }


def test_key_evidence_comparison_is_exact(package: dict) -> None:
    assert package["key_evidence_comparison"] == {
        "original_oos_majority_accuracy": "0.539491",
        "original_oos_previous_direction_accuracy": "0.495984",
        "original_oos_ticker_cross_sectional_accuracy": "0.502677",
        "original_oos_brier_score": "0.24875351",
        "refined_oos_accuracy_range": "0.119813 to 0.480924",
        "refined_signal_consistency": "WEAK_OR_MIXED",
        "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
        "refined_model_comparison": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
    }
    assert package["refined_evidence_did_not_create_acceptance_readiness"] is True
    assert package["additional_improvement_loop_not_automatically_recommended"] is True
    assert package["methodology_review_recommended_before_more_execution"] is True


def test_options_are_defined_and_acceptance_is_not_allowed(package: dict) -> None:
    options = package["recommended_next_options"]
    assert [item["option_id"] for item in options] == review.OPTION_IDS
    assert all(item["execution_authorized"] is False for item in options)
    acceptance = options[-1]
    assert acceptance["option_id"] == "OPTION_G_ACCEPTANCE_CANDIDATE"
    assert acceptance["status"] == review.NOT_ALLOWED_CURRENTLY
    assert package["recommended_next_option"] == (
        "OPTION_B_METHOD_DIAGNOSTIC_REVIEW"
    )
    assert package["recommended_next_option_reason"] == (
        "TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE"
    )


def test_risk_controls_are_exact(package: dict) -> None:
    assert package["risk_controls"] == review.RISK_CONTROLS
    assert len(package["risk_controls"]) == 11


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_regeneration_performed_in_review",
        "predictive_evidence_rerun_performed",
        "refined_evidence_rerun_performed",
        "label_generation_rerun_performed",
        "feature_generation_rerun_performed",
        "metrics_recomputation_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ],
)
def test_execution_acceptance_and_runtime_actions_remain_false(
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
        "total_checks": 22,
        "passed_checks": 22,
        "failed_checks": 0,
        "blocker_count": 0,
        "planning_tree_review_ready": True,
        "recommended_next_option": review.RECOMMENDED_NEXT_OPTION,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_package_digest_is_deterministic(package: dict) -> None:
    repeated = review.build_predictive_evidence_planning_tree_review_package_v1()
    field = "predictive_evidence_planning_tree_review_package_digest"
    assert repeated[field] == package[field]
    assert repeated[field] == (
        review.predictive_evidence_planning_tree_review_package_digest_v1(repeated)
    )
    assert len(repeated[field]) == 64


def test_validator_accepts_valid_package(package: dict) -> None:
    validation = review.validate_predictive_evidence_planning_tree_review_package_v1(
        package
    )
    assert validation["status"] == (
        "PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_VALID"
    )
    assert validation["planning_tree_section_count"] == 12
    assert validation["blocker_count"] == 0
    assert validation["recommended_next_option"] == review.RECOMMENDED_NEXT_OPTION


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        (
            "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest",
            None,
        ),
        (
            "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest",
            None,
        ),
        (
            "additional_predictive_evidence_results_review_for_refined_evidence_digest",
            None,
        ),
        ("original_predictive_usefulness_acceptance_readiness_review_digest", None),
        ("research_registry_approval_digest", None),
        ("records_digest", "0" * 64),
        ("final_predictive_usefulness_state", "accepted"),
        ("predictive_usefulness", "accepted"),
        ("final_profitability_state", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("runtime_migration_approved", True),
        ("trade_recommendations_generated", True),
        ("recommended_next_option", None),
        ("risk_controls", []),
        ("predictive_evidence_planning_tree_review_package_digest", None),
    ],
)
def test_validator_rejects_changed_contract_fields(
    package: dict, field: str, replacement: object
) -> None:
    invalid = deepcopy(package)
    invalid[field] = replacement
    with pytest.raises(review.PredictiveEvidencePlanningTreeReviewError):
        review.validate_predictive_evidence_planning_tree_review_package_v1(invalid)


def test_validator_rejects_acceptance_option_allowed(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["recommended_next_options"][-1]["status"] = (
        review.AVAILABLE_FOR_PLANNING_REVIEW
    )
    with pytest.raises(review.PredictiveEvidencePlanningTreeReviewError):
        review.validate_predictive_evidence_planning_tree_review_package_v1(invalid)


def test_validator_rejects_missing_planning_section(package: dict) -> None:
    invalid = deepcopy(package)
    invalid["planning_tree_sections"].pop()
    with pytest.raises(review.PredictiveEvidencePlanningTreeReviewError):
        review.validate_predictive_evidence_planning_tree_review_package_v1(invalid)


def test_markdown_contains_required_sections(package: dict) -> None:
    markdown = review.build_predictive_evidence_planning_tree_review_markdown_v1(
        package
    )
    for heading in (
        "Title",
        "Planning Tree Review",
        "Bound Evidence",
        "Dataset and Universe",
        "Original Evidence Cycle",
        "Refined Evidence Cycle",
        "Readiness Decisions",
        "Final Authority State",
        "Evidence Comparison",
        "Recommended Options",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_writer_emits_canonical_json_and_does_not_overwrite(tmp_path) -> None:
    result = review.write_predictive_evidence_planning_tree_review_package_v1(
        tmp_path
    )
    output_path = tmp_path / result["filename"]
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    review.validate_predictive_evidence_planning_tree_review_package_v1(payload)
    with pytest.raises(review.PredictiveEvidencePlanningTreeReviewError):
        review.write_predictive_evidence_planning_tree_review_package_v1(tmp_path)
