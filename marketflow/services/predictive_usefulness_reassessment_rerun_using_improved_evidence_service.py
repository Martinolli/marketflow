"""Offline predictive-usefulness reassessment using reviewed improved evidence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_V1 = (
    "predictive_usefulness_reassessment_rerun_using_improved_evidence_v1"
)
PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY = (
    "PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY"
)
SOURCE_RESULTS_REVIEW_ARTIFACT_KIND = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE"
)
SOURCE_RESULTS_REVIEW_STATUS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY"
)

NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
SELECTED_DIRECTION = "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"

EXPECTED_RESULTS_REVIEW_DIGEST = "75a69f5a20a4309dcfe4d9e82333d0348f8459e4ecfe2ac3a9f4373d4af3551f"
EXPECTED_EXECUTION_DIGEST = "b6e6429fefd2d8b0ed450845d104aab415e0142740d62bd49fc76678677aab17"
EXPECTED_OUTPUT_BINDING_DIGEST = "d6d272c9369430546c73f96d220c3e33183631de98a0a5cf9471c9179bf0710a"
EXPECTED_APPROVAL_DIGEST = "c2ce4254de6c4fa3934a6c1fddb04f8bad334054ba914119c915f6b6071c558f"
EXPECTED_CANDIDATE_REVIEW_DIGEST = "1db2b5a32e4cbd475330b3558706e8f7319bdf8d29a53c9e8c26bc32cc2b2442"
EXPECTED_CANDIDATE_DIGEST = "5705fd75afa0d614836f5b74d8a074054fd4f45b9395d5694f9f647a9322956f"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"

SOURCE_EVIDENCE = {
    "additional_predictive_evidence_results_review_using_improved_evidence_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_using_improved_evidence_digest": EXPECTED_EXECUTION_DIGEST,
    "additional_predictive_evidence_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
    "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": EXPECTED_APPROVAL_DIGEST,
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
    "improved_evidence_planning_results_review_using_redesigned_evidence_digest": "8f316cceeb2a9303d8d448fcf70cec249ab4d11876acad893b386f89b118a379",
    "improved_evidence_planning_execution_using_redesigned_evidence_digest": "1f2f04133a6b1d80dd30b5e8b4af08f1ae78aca8a164aa7a760a693192a894a4",
    "improved_evidence_planning_output_binding_digest": "23edda5191badabced31ff152a60f2428ffa08730ebaa0ba8b2facfd2d87269c",
    "improved_evidence_planning_approval_using_redesigned_evidence_digest": "6aad4b27a57310b59c33e3ecfc93754df7da815c3ea15d8e686f8fe73abef664",
    "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": "d69cf64437f1dbd69a929e00c94a6cc9c13e6148102cd2adc91d1ed4eff8ceb6",
    "improved_evidence_planning_candidate_using_redesigned_evidence_digest": "bfda433e36eb6d333dcc2169d8d18bb31ab0671403cc6d447dc1eda0b10fd72b",
    "label_objective_redesign_results_review_using_redesigned_evidence_digest": "6bbf7af2ae72e33dbc0a86da2b8ba8faa05edeea982baea89c6b511b3cd7d1f4",
    "label_objective_redesign_execution_using_redesigned_evidence_digest": "1ec655cff3efcb14bb7f72e6fe0debaf067850c686b539c6e9359d881186eb00",
    "label_objective_redesign_output_binding_digest": "a86063a3de2517af101ca23bc985939c7ede69c7848372b148d7d44fb6f42778",
    "label_objective_redesign_approval_using_redesigned_evidence_digest": "4ffb335cd01041c6db16974b2f9733b6235d96bfe941cd6c3739d99c45a894c7",
    "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest": "66ef0356d4bb73fe405db5e56cfa8ab10d499fc842d2906e3aeaf56c85df2494",
    "label_objective_redesign_candidate_using_redesigned_evidence_digest": "3ee05e4b4316d9dd874a3916fed7cf8ee8aa3f73ba7596d0f9473a9714145e45",
    "label_objective_target_definition_results_review_using_redesigned_evidence_digest": "682907f87575b8fde514c6db17b141420bfd55781b0b77c297ba358a378aff46",
    "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": "7b5c299191abfd6aa8ef33ebed804757a2d57a6fb966ed1d51c78d1b233abe30",
    "label_objective_target_definition_review_output_binding_digest": "7efd91b24e1af35f93e37dc9bbb5e90fe03f1080f6296abe57afdbd326d0fbee",
    "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": "01f667deeea9a478dca8e1f326b672ffbcedbf9c0a0b3da93d3fac1714c622db",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": "ebf9f1dddddc37167c457c64f28baab021b50249987e888e1ea0a31c78102d45",
    "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": "735d531f39c3eac771694b9044ed67f62c9aecbdc9ca0d5cd3e3368c45caf892",
    "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": "d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22",
    "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": "6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da",
    "predictive_usefulness_reassessment_using_redesigned_evidence_digest": "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985",
    "additional_predictive_evidence_results_review_using_redesigned_labels_digest": "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed",
    "additional_predictive_evidence_execution_using_redesigned_labels_digest": "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b",
    "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
    "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
    "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE}

DOMAIN_INTERPRETATIONS = {
    "DOMAIN_SOURCE_EVIDENCE_INTEGRITY": ("All supplied source digests remain bound.", False),
    "DOMAIN_DATASET_AND_UNIVERSE": ("The frozen 12-ticker dataset remains unchanged.", False),
    "DOMAIN_LABEL_SCHEMA_BINDING": ("Redesigned labels remain bound and were not regenerated.", False),
    "DOMAIN_FEATURE_MATRIX_BINDING": ("Feature and matrix evidence remain bound and were not regenerated.", False),
    "DOMAIN_WALK_FORWARD_EVIDENCE": ("Reviewed walk-forward evidence requires readiness review.", True),
    "DOMAIN_OOS_EVIDENCE": ("Reviewed OOS evidence requires readiness review.", True),
    "DOMAIN_BASELINE_OUTPERFORMANCE": ("The small cross-sectional edge is not acceptance evidence.", True),
    "DOMAIN_LOCAL_MODEL_EQUIVALENCE": ("The local model matches the majority baseline.", True),
    "DOMAIN_CROSS_SECTIONAL_EDGE": ("The small cross-sectional edge requires readiness review.", True),
    "DOMAIN_METRIC_FAMILY_REVIEW": ("Reviewed metric families were not recomputed.", True),
    "DOMAIN_CALIBRATION_AND_BRIER": ("The small Brier edge requires readiness review.", True),
    "DOMAIN_LEAKAGE_AND_NO_PEEK_CONTROLS": ("Eight controls passed with zero failures.", False),
    "DOMAIN_PER_TICKER_CONSISTENCY": ("All 12 ticker entries remain research-only.", True),
    "DOMAIN_META_LIMITATION": ("META remains limited to 913 records.", True),
    "DOMAIN_ACCEPTANCE_BOUNDARY": ("Predictive usefulness is not accepted.", False),
    "DOMAIN_PROFITABILITY_BOUNDARY": ("Profitability is not accepted.", False),
    "DOMAIN_RUNTIME_BOUNDARY": ("Runtime and trading authority remain closed.", False),
}

NEXT_CHAIN = [
    "Predictive Usefulness Acceptance Readiness Review Using Improved Evidence v1.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Predictive usefulness acceptance ceremony, only if separately approved.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_acceptance_readiness_review_using_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "predictive_usefulness_acceptance_ceremony_if_approved",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "reassessment_does_not_accept_predictive_usefulness",
    "reassessment_does_not_create_acceptance_readiness_review",
    "reassessment_does_not_create_acceptance_candidate",
    "reassessment_does_not_accept_profitability",
    "reassessment_does_not_authorize_runtime",
    "reassessment_does_not_authorize_strategy",
    "reassessment_does_not_authorize_paper_trading",
    "reassessment_does_not_authorize_broker_execution",
    "reassessment_does_not_generate_trade_recommendations",
    "reassessment_does_not_regenerate_labels",
    "reassessment_does_not_create_new_targets",
    "reassessment_does_not_authorize_target_definition_change",
    "reassessment_does_not_generate_features",
    "reassessment_does_not_create_canonical_feature_label_matrix",
    "reassessment_does_not_rerun_predictive_evidence",
    "reassessment_does_not_recompute_metrics",
    "reassessment_does_not_train_models",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]


class PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(ValueError):
    """Raised when the research-only reassessment package is invalid."""


def _domain_package() -> dict[str, dict[str, Any]]:
    return {
        domain: {
            "domain_status": "REVIEWED_RESEARCH_ONLY",
            "evidence_summary": summary,
            "acceptance_evidence": False,
            "requires_acceptance_readiness_review": requires_review,
            "research_only": True,
            "non_actionable": True,
        }
        for domain, (summary, requires_review) in DOMAIN_INTERPRETATIONS.items()
    }


def _per_ticker_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_predictive_usefulness_reassessment_digest", None)
    return payload


def per_ticker_predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker reassessment."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "additional_predictive_evidence_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_status": "REASSESSED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "label_regeneration_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
            "metric_recomputation_performed_in_reassessment": False,
            "model_training_performed_in_reassessment": False,
            "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
            "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
            "reassessment_note": (
                "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_IMPROVED_EVIDENCE"
                if is_meta else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry["per_ticker_predictive_usefulness_reassessment_digest"] = (
            per_ticker_predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_V1,
        "reassessment_status": PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_results_review_artifact_kind": SOURCE_RESULTS_REVIEW_ARTIFACT_KIND,
        "source_results_review_status": SOURCE_RESULTS_REVIEW_STATUS,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence": True,
        "predictive_usefulness_reassessment_using_improved_evidence_created": True,
        "predictive_usefulness_reassessment_using_improved_evidence_ready": True,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence": True,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created": False,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_ready": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_reassessment": False,
        "model_training_performed_in_reassessment": False,
        "provider_requests_made_in_reassessment": False,
        "live_provider_transport_enabled_in_reassessment": False,
        "market_data_acquisition_performed_in_reassessment": False,
        "dataset_generation_performed_in_reassessment": False,
        "canonical_dataset_regenerated_in_reassessment": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "additional_predictive_evidence_execution_rerun_performed": False,
        "improved_evidence_planning_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "source_results_review_ready": True,
        "source_evidence_classification": "COMPLETED_RESEARCH_ONLY",
        "source_execution_scope_review": "RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE",
        "matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_count": 1152,
        "walk_forward_status": "COMPUTED_RESEARCH_ONLY",
        "oos_status": "COMPUTED_RESEARCH_ONLY",
        "oos_row_count": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "majority_brier": "0.04867526",
        "local_model_brier": "0.04867526",
        "cross_sectional_brier": "0.04831065",
        "optional_tree_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "optional_ensemble_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "leakage_control_passed": True,
        "leakage_failed_control_count": 0,
        "leakage_control_count": 8,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "reassessment_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_review": "WEAK_TO_MODEST_MIXED",
        "baseline_outperformance_review": "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_review": "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE",
        "cross_sectional_review": "SMALL_EDGE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "oos_review": "MODEST_RESEARCH_EVIDENCE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "walk_forward_review": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "calibration_brier_review": "SMALL_CROSS_SECTIONAL_BRIER_EDGE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "optional_model_coverage_review": "INCOMPLETE_OPTIONAL_MODELS_UNAVAILABLE",
        "leakage_review": "PASS_ZERO_FAILED_CONTROLS",
        "meta_limitation_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "acceptance_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "next_required_gate": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE",
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "reassessment_domains": _domain_package(),
        "per_ticker_reassessment_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and all(
        isinstance(entry.get("per_ticker_predictive_usefulness_reassessment_digest"), str)
        and entry["per_ticker_predictive_usefulness_reassessment_digest"]
        == per_ticker_predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(entry)
        for entry in entries
    )


def _check_definitions(package: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    entries = package.get("per_ticker_reassessment_entries", [])
    unavailable = "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"
    return [
        ("source_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, package.get("source_results_review_digest")),
        ("source_execution_digest_bound", EXPECTED_EXECUTION_DIGEST, package.get("source_execution_digest")),
        ("source_output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, package.get("source_output_binding_digest")),
        ("source_approval_digest_bound", EXPECTED_APPROVAL_DIGEST, package.get("source_approval_digest")),
        ("source_candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest")),
        ("source_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest")),
        ("planning_results_review_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_results_review_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_results_review_using_redesigned_evidence_digest")),
        ("planning_execution_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_execution_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_execution_using_redesigned_evidence_digest")),
        ("planning_output_binding_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_output_binding_digest"], package.get("improved_evidence_planning_output_binding_digest")),
        ("planning_approval_digest_bound", SOURCE_EVIDENCE["improved_evidence_planning_approval_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_approval_using_redesigned_evidence_digest")),
        ("redesign_results_review_digest_bound", SOURCE_EVIDENCE["label_objective_redesign_results_review_using_redesigned_evidence_digest"], package.get("label_objective_redesign_results_review_using_redesigned_evidence_digest")),
        ("redesign_execution_digest_bound", SOURCE_EVIDENCE["label_objective_redesign_execution_using_redesigned_evidence_digest"], package.get("label_objective_redesign_execution_using_redesigned_evidence_digest")),
        ("target_definition_results_review_digest_bound", SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest")),
        ("target_definition_execution_digest_bound", SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest")),
        ("path_selection_digest_bound", SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], package.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest")),
        ("prior_readiness_review_digest_bound", SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], package.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest")),
        ("prior_reassessment_digest_bound", SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest")),
        ("prior_predictive_results_review_digest_bound", SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest")),
        ("prior_predictive_execution_digest_bound", SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, package.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, package.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, package.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, package.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("target_universe_12_preserved", TARGET_UNIVERSE, package.get("target_universe")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("meta_913_preserved", 913, package.get("meta_record_count")),
        ("source_results_review_ready_true", True, package.get("source_results_review_ready")),
        ("reassessment_created_true", True, package.get("predictive_usefulness_reassessment_using_improved_evidence_created")),
        ("reassessment_ready_true", True, package.get("predictive_usefulness_reassessment_using_improved_evidence_ready")),
        ("ready_for_acceptance_readiness_review_true", True, package.get("ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence")),
        ("acceptance_readiness_review_created_false", False, package.get("predictive_usefulness_acceptance_readiness_using_improved_evidence_created")),
        ("acceptance_readiness_review_ready_false", False, package.get("predictive_usefulness_acceptance_readiness_using_improved_evidence_ready")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, package.get("predictive_usefulness")),
        ("acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_candidate_created_false", False, package.get("predictive_usefulness_acceptance_candidate_created")),
        ("profitability_not_accepted", NOT_ACCEPTED, package.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("trade_recommendations_false", False, package.get("trade_recommendations_generated")),
        ("label_regeneration_authorized_false", False, package.get("label_regeneration_authorized")),
        ("label_regeneration_performed_false", False, package.get("label_regeneration_performed")),
        ("new_targets_created_false", False, package.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, package.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, package.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, package.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, package.get("feature_label_matrix_created")),
        ("metric_recomputation_in_reassessment_false", False, package.get("metric_recomputation_performed_in_reassessment")),
        ("model_training_in_reassessment_false", False, package.get("model_training_performed_in_reassessment")),
        ("matrix_rows_preserved", 143352, package.get("matrix_row_count")),
        ("evaluable_rows_preserved", 142200, package.get("evaluable_matrix_row_count")),
        ("unavailable_targets_preserved", 1152, package.get("unavailable_target_count")),
        ("oos_rows_preserved", 34848, package.get("oos_row_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", package.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", package.get("majority_accuracy"), package.get("local_model_accuracy")),
        ("brier_values_preserved", ["0.04867526", "0.04867526", "0.04831065"], [package.get("majority_brier"), package.get("local_model_brier"), package.get("cross_sectional_brier")]),
        ("optional_models_unavailable_preserved", [unavailable, unavailable], [package.get("optional_tree_model_status"), package.get("optional_ensemble_model_status")]),
        ("leakage_controls_passed", [True, 0, 8], [package.get("leakage_control_passed"), package.get("leakage_failed_control_count"), package.get("leakage_control_count")]),
        ("meta_limitation_preserved", True, package.get("meta_reduced_record_count_preserved")),
        ("reassessment_classification_conservative", "COMPLETED_RESEARCH_ONLY", package.get("reassessment_classification")),
        ("acceptance_recommendation_not_accept", "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE", package.get("acceptance_recommendation")),
        ("reassessment_domains_present", list(DOMAIN_INTERPRETATIONS), list(package.get("reassessment_domains", {}))),
        ("per_ticker_entries_12", 12, len(entries) if isinstance(entries, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, package.get("provider_requests_made_in_reassessment")),
        ("market_data_acquisition_false", False, package.get("market_data_acquisition_performed_in_reassessment")),
        ("dataset_regeneration_false", False, package.get("canonical_dataset_regenerated_in_reassessment")),
        ("redesigned_label_regeneration_false", False, package.get("redesigned_label_regeneration_performed")),
        ("feature_regeneration_false", False, package.get("feature_regeneration_performed")),
        ("predictive_evidence_rerun_false", False, package.get("additional_predictive_evidence_execution_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
        ("next_chain_defined", NEXT_CHAIN, package.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, package.get("risk_controls")),
        ("no_tracked_marketflow_files", True, package.get("no_tracked_marketflow_files")),
    ]


def _checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [_check(check_id, expected, actual) for check_id, expected, actual in _check_definitions(package)]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "predictive_usefulness_reassessment_using_improved_evidence_ready": not failed,
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence": not failed,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_reassessment": False,
        "model_training_performed_in_reassessment": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop("predictive_usefulness_reassessment_rerun_using_improved_evidence_digest", None)
    return payload


def predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(
    reassessment: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the reassessment package."""
    return semantic_digest(_digest_payload(reassessment))


def build_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1() -> dict:
    """Build the offline reassessment from committed, reviewed facts only."""
    package = _base_package()
    checklist = _checklist(package)
    package["reassessment_checklist"] = checklist
    package["reassessment_summary"] = _summary(checklist)
    package["predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"] = (
        predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(package)
    )
    validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(f"{field} must be false")


def validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(
    reassessment: dict,
) -> dict:
    """Validate source bindings, research classifications, and closed authority gates."""
    if not isinstance(reassessment, dict):
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment must be an object")

    expected_fields = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_V1,
        "reassessment_status": PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_PACKAGE_READY,
        "source_results_review_artifact_kind": SOURCE_RESULTS_REVIEW_ARTIFACT_KIND,
        "source_results_review_status": SOURCE_RESULTS_REVIEW_STATUS,
        "source_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_count": 1152,
        "oos_row_count": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "majority_brier": "0.04867526",
        "local_model_brier": "0.04867526",
        "cross_sectional_brier": "0.04831065",
        "reassessment_classification": "COMPLETED_RESEARCH_ONLY",
        "predictive_signal_review": "WEAK_TO_MODEST_MIXED",
        "baseline_outperformance_review": "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_review": "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE",
        "cross_sectional_review": "SMALL_EDGE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "oos_review": "MODEST_RESEARCH_EVIDENCE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "walk_forward_review": "REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "calibration_brier_review": "SMALL_CROSS_SECTIONAL_BRIER_EDGE_REQUIRES_ACCEPTANCE_READINESS_REVIEW",
        "optional_model_coverage_review": "INCOMPLETE_OPTIONAL_MODELS_UNAVAILABLE",
        "leakage_review": "PASS_ZERO_FAILED_CONTROLS",
        "meta_limitation_review": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "acceptance_recommendation": "DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE",
        "next_required_gate": "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_IMPROVED_EVIDENCE",
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    expected_fields.update(SOURCE_EVIDENCE)
    for field, value in expected_fields.items():
        _expect(reassessment.get(field), value, field)

    true_fields = (
        "created_offline",
        "research_only",
        "operator_review_required",
        "additional_predictive_evidence_executed",
        "additional_predictive_evidence_results_created",
        "additional_predictive_evidence_results_review_created",
        "additional_predictive_evidence_results_review_ready",
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence",
        "predictive_usefulness_reassessment_using_improved_evidence_created",
        "predictive_usefulness_reassessment_using_improved_evidence_ready",
        "ready_for_predictive_usefulness_acceptance_readiness_review_using_improved_evidence",
        "source_results_review_ready",
        "leakage_control_passed",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(reassessment.get(field), field)

    false_fields = (
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created",
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_ready",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "profitability_acceptance_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "runtime_migration_approval_created",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "metric_recomputation_performed_in_reassessment",
        "model_training_performed_in_reassessment",
        "provider_requests_made_in_reassessment",
        "live_provider_transport_enabled_in_reassessment",
        "market_data_acquisition_performed_in_reassessment",
        "dataset_generation_performed_in_reassessment",
        "canonical_dataset_regenerated_in_reassessment",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "additional_predictive_evidence_execution_rerun_performed",
        "improved_evidence_planning_execution_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in false_fields:
        _expect_false(reassessment.get(field), field)

    domains = reassessment.get("reassessment_domains")
    if not isinstance(domains, dict) or list(domains) != list(DOMAIN_INTERPRETATIONS):
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment domains mismatch")
    for domain, (_, requires_review) in DOMAIN_INTERPRETATIONS.items():
        value = domains.get(domain)
        if not isinstance(value, dict) or not value.get("evidence_summary"):
            raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(f"{domain} evidence missing")
        _expect(value.get("domain_status"), "REVIEWED_RESEARCH_ONLY", f"{domain} domain_status")
        _expect_false(value.get("acceptance_evidence"), f"{domain} acceptance_evidence")
        _expect(value.get("requires_acceptance_readiness_review"), requires_review, f"{domain} readiness")
        _expect_true(value.get("research_only"), f"{domain} research_only")
        _expect_true(value.get("non_actionable"), f"{domain} non_actionable")

    entries = reassessment.get("per_ticker_reassessment_entries")
    if not isinstance(entries, list) or len(entries) != 12:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("per-ticker entries mismatch")
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker order")
    for entry in entries:
        ticker = entry.get("ticker")
        _expect(entry.get("historical_record_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} record count")
        _expect(entry.get("meta_reduced_record_count_flag"), ticker == "META", f"{ticker} META flag")
        _expect(entry.get("selected_redesign_direction"), SELECTED_DIRECTION, f"{ticker} direction")
        _expect(entry.get("source_results_review_digest"), EXPECTED_RESULTS_REVIEW_DIGEST, f"{ticker} source review")
        _expect(entry.get("source_execution_digest"), EXPECTED_EXECUTION_DIGEST, f"{ticker} source execution")
        _expect(entry.get("predictive_usefulness"), NOT_ACCEPTED, f"{ticker} usefulness")
        _expect(entry.get("profitability"), NOT_ACCEPTED, f"{ticker} profitability")
        for field in (
            "predictive_usefulness_acceptance_ready",
            "predictive_usefulness_acceptance_candidate_created",
            "label_regeneration_authorized",
            "new_targets_created",
            "feature_generation_authorized",
            "feature_label_matrix_created",
            "metric_recomputation_performed_in_reassessment",
            "model_training_performed_in_reassessment",
        ):
            _expect_false(entry.get(field), f"{ticker} {field}")
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, f"{ticker} {field}")
        if ticker == "META":
            _expect(
                entry.get("reassessment_note"),
                "PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT_USING_IMPROVED_EVIDENCE",
                "META reassessment_note",
            )
        digest = entry.get("per_ticker_predictive_usefulness_reassessment_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError(f"{ticker} per-ticker digest missing")
        _expect(
            digest,
            per_ticker_predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(entry),
            f"{ticker} per-ticker digest",
        )

    checklist = reassessment.get("reassessment_checklist")
    expected_check_ids = [definition[0] for definition in _check_definitions(reassessment)]
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != expected_check_ids:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment checklist failed")
    _expect(reassessment.get("reassessment_summary"), _summary(checklist), "reassessment summary")

    digest = reassessment.get("predictive_usefulness_reassessment_rerun_using_improved_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment digest missing")
    _expect(
        digest,
        predictive_usefulness_reassessment_rerun_using_improved_evidence_digest_v1(reassessment),
        "reassessment digest",
    )
    return {
        "status": "PREDICTIVE_USEFULNESS_REASSESSMENT_RERUN_USING_IMPROVED_EVIDENCE_VALID",
        "artifact_kind": reassessment["artifact_kind"],
        "reassessment_status": reassessment["reassessment_status"],
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": digest,
        **{
            key: reassessment["reassessment_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_predictive_usefulness_reassessment_rerun_using_improved_evidence_markdown_v1(
    reassessment: dict,
) -> str:
    """Render a sanitized Markdown view of the validated reassessment."""
    validation = validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(reassessment)
    sections = [
        ("Title", ["Predictive Usefulness Reassessment Rerun Using Improved Evidence"]),
        (
            "Predictive Usefulness Reassessment Rerun Using Improved Evidence",
            [
                f"Artifact/status: `{reassessment['artifact_kind']}` / `{reassessment['reassessment_status']}`.",
                f"Digest: `{validation['predictive_usefulness_reassessment_rerun_using_improved_evidence_digest']}`.",
            ],
        ),
        (
            "Source Results Review",
            [
                f"Artifact/status: `{reassessment['source_results_review_artifact_kind']}` / `{reassessment['source_results_review_status']}`.",
                f"Digest: `{reassessment['source_results_review_digest']}`.",
            ],
        ),
        (
            "Bound Evidence",
            [
                f"Execution: `{reassessment['source_execution_digest']}`.",
                f"Output binding: `{reassessment['source_output_binding_digest']}`.",
                f"Matrix/features/labels: `{reassessment['feature_label_matrix_digest']}` / `{reassessment['feature_values_digest']}` / `{reassessment['redesigned_label_values_digest']}`.",
            ],
        ),
        (
            "Dataset and Universe",
            [
                f"Dataset/records: `{reassessment['dataset_name']}` / `{reassessment['total_canonical_record_count']}`.",
                "Universe: " + ", ".join(f"`{ticker}`" for ticker in reassessment["target_universe"]) + ".",
                "META remains `913`; each non-META ticker remains `1003`.",
            ],
        ),
        (
            "Evidence Summary",
            [
                f"Matrix/evaluable/unavailable: `{reassessment['matrix_row_count']} / {reassessment['evaluable_matrix_row_count']} / {reassessment['unavailable_target_count']}`.",
                f"OOS rows: `{reassessment['oos_row_count']}`.",
                f"Majority/local/cross-sectional accuracy: `{reassessment['majority_accuracy']} / {reassessment['local_model_accuracy']} / {reassessment['cross_sectional_accuracy']}`.",
            ],
        ),
        ("Reassessment Classification", [f"`{reassessment['reassessment_classification']}`."]),
        ("Predictive Signal Review", [f"`{reassessment['predictive_signal_review']}`."]),
        ("Baseline Outperformance Review", [f"`{reassessment['baseline_outperformance_review']}`."]),
        ("Local Model Review", [f"`{reassessment['local_model_review']}`."]),
        ("Cross-Sectional Edge Review", [f"`{reassessment['cross_sectional_review']}`."]),
        ("OOS Review", [f"`{reassessment['oos_review']}`."]),
        ("Walk-Forward Review", [f"`{reassessment['walk_forward_review']}`."]),
        (
            "Calibration / Brier Review",
            [
                f"`{reassessment['calibration_brier_review']}`.",
                f"Majority/local/cross-sectional Brier: `{reassessment['majority_brier']} / {reassessment['local_model_brier']} / {reassessment['cross_sectional_brier']}`.",
            ],
        ),
        (
            "Leakage Review",
            [f"`{reassessment['leakage_review']}`; `{reassessment['leakage_control_count']}` controls, `{reassessment['leakage_failed_control_count']}` failures."],
        ),
        ("META Limitation Review", [f"`{reassessment['meta_limitation_review']}`; META remains at `913` records."]),
        (
            "Acceptance Boundary",
            ["Predictive usefulness remains not accepted. No readiness-review or acceptance-candidate artifact was created."],
        ),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        (
            "Per-Ticker Reassessment",
            [
                f"`{row['ticker']}`: records `{row['historical_record_count']}`, digest `{row['per_ticker_predictive_usefulness_reassessment_digest']}`."
                for row in reassessment["per_ticker_reassessment_entries"]
            ],
        ),
        ("Next Chain", reassessment["next_chain"]),
        ("Next Gates", reassessment["next_gates"]),
        ("Risk Controls", reassessment["risk_controls"]),
        (
            "Checklist Summary",
            [
                f"Total/passed/failed/blockers: `{reassessment['reassessment_summary']['total_checks']} / {reassessment['reassessment_summary']['passed_checks']} / {reassessment['reassessment_summary']['failed_checks']} / {reassessment['reassessment_summary']['blocker_count']}`."
            ],
        ),
        (
            "Guardrails",
            ["No provider, acquisition, regeneration, predictive rerun, metric recomputation, model training, acceptance, runtime, broker, or trading action occurred."],
        ),
    ]
    lines = ["# Predictive Usefulness Reassessment Rerun Using Improved Evidence", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(
    output_dir: str | Path,
) -> dict:
    """Write canonical reassessment JSON without overwriting an existing package."""
    package = build_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1()
    validation = validate_predictive_usefulness_reassessment_rerun_using_improved_evidence_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "predictive_usefulness_reassessment_rerun_using_improved_evidence_v1.json"
    if path.exists():
        raise PredictiveUsefulnessReassessmentRerunImprovedEvidenceError("reassessment output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "reassessment_status": package["reassessment_status"],
        "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest": validation[
            "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
