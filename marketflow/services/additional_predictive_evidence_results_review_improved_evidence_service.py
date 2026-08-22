"""Offline review of saved additional predictive evidence using improved evidence."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_improved_evidence_service as execution,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_IMPROVED_EVIDENCE_V1 = (
    "additional_predictive_evidence_results_review_using_improved_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_IMPROVED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_IMPROVED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS"
)

DEFAULT_SOURCE_OUTPUT_ROOT = Path(
    ".marketflow/additional_predictive_evidence_using_improved_evidence/expanded_universe_v1"
)
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

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
SELECTED_DIRECTION = "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"
TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE}

EXPECTED_OUTPUT_FILENAMES = [
    "additional_predictive_evidence_execution_manifest.json",
    "source_binding_manifest.json",
    "improved_label_schema_binding_report.json",
    "improved_feature_label_matrix_report.json",
    "walk_forward_results.json",
    "oos_results.json",
    "baseline_model_comparison.json",
    "metric_family_results.json",
    "calibration_stability_report.json",
    "leakage_quality_control_report.json",
    "per_ticker_meta_review.json",
    "operator_results_review_summary.json",
    "additional_predictive_evidence_digest_manifest.json",
]

LIMITATIONS = [
    "review_is_research_only",
    "review_does_not_regenerate_labels",
    "review_does_not_create_new_targets",
    "review_does_not_authorize_target_definition_change",
    "review_does_not_generate_new_source_features",
    "review_does_not_create_canonical_feature_label_matrix",
    "review_does_not_recompute_metrics",
    "review_does_not_train_models",
    "review_does_not_create_reassessment",
    "review_does_not_create_acceptance_readiness_review",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_approve_profitability",
    "review_does_not_authorize_runtime",
    "small_cross_sectional_edge_remains_not_acceptance_evidence",
    "local_model_matches_majority_baseline",
    "meta_reduced_record_count_preserved",
]
NEXT_CHAIN = [
    "Predictive usefulness reassessment rerun using improved evidence.",
    "Predictive usefulness acceptance-readiness rerun using improved evidence, if reassessment supports it.",
    "Predictive usefulness acceptance candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_reassessment_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_readiness_rerun_using_improved_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_regenerate_labels",
    "review_does_not_create_new_targets",
    "review_does_not_authorize_target_definition_change",
    "review_does_not_generate_new_source_features",
    "review_does_not_create_canonical_feature_label_matrix",
    "review_does_not_execute_predictive_evidence",
    "review_does_not_rerun_predictive_evidence",
    "review_does_not_retrain_models",
    "review_does_not_recompute_metrics",
    "review_does_not_create_reassessment",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_create_acceptance_candidate",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_prior_predictive_evidence_outputs",
    "do_not_mutate_improved_evidence_planning_outputs",
    "do_not_mutate_current_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

FALSE_AUTHORITY_FIELDS = [
    "predictive_usefulness_reassessment_using_improved_evidence_created",
    "predictive_usefulness_acceptance_readiness_using_improved_evidence_created",
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
    "metric_recomputation_performed_in_review", "model_training_performed_in_review",
    "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended", "profitability_acceptance_ready",
    "profitability_acceptance_recommended", "runtime_migration_approved", "runtime_migration_active",
    "automatic_stitching", "new_strategy_scoring_performed", "trade_recommendations_generated",
    "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
    "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
    "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
    "feature_regeneration_performed", "additional_predictive_evidence_execution_rerun_performed",
    "improved_evidence_planning_execution_rerun_performed", "raw_provider_payloads_committed",
    "api_keys_stored_or_printed", "predictive_usefulness_acceptance_artifact_created",
    "profitability_acceptance_created", "runtime_migration_approval_created",
]

SOURCE_EVIDENCE = {
    "additional_predictive_evidence_execution_using_improved_evidence_digest": EXPECTED_EXECUTION_DIGEST,
    "additional_predictive_evidence_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
    **deepcopy(execution.SOURCE_EVIDENCE),
}


class AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(ValueError):
    """Raised when saved outputs or the review contract are invalid."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            f"{path.name} is not valid readable JSON"
        ) from exc
    if not isinstance(value, dict):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            f"{path.name} must contain a JSON object"
        )
    return value


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered_key = str(key).lower()
            if lowered_key in {"api_key", "access_token", "provider_response_body"}:
                return True
            if _contains_sensitive_value(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in ("bearer ", "apikey=", "api_key=", "access_token="))
    return False


def _reject_source_authority(value: Any, path: str = "source") -> None:
    if isinstance(value, Mapping):
        forbidden_true = {
            "raw_provider_payloads_committed", "api_keys_stored_or_printed",
            "new_strategy_scoring_performed", "trade_recommendations_generated",
            "runtime_migration_approved", "runtime_migration_active",
            "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
            "target_definition_change_authorized", "target_definition_change_performed",
            "feature_generation_authorized", "feature_generation_performed",
            "feature_label_matrix_created", "predictive_usefulness_acceptance_ready",
            "predictive_usefulness_acceptance_candidate_created",
            "profitability_acceptance_ready", "profitability_acceptance_recommended",
            "provider_requests_made_in_execution", "live_provider_transport_enabled_in_execution",
            "market_data_acquisition_performed_in_execution",
            "dataset_generation_performed_in_execution",
            "canonical_dataset_regenerated_in_execution",
            "redesigned_label_regeneration_performed", "feature_regeneration_performed",
        }
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in forbidden_true and item is True:
                raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                    f"{child} exceeds review authority"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item != NOT_AUTHORIZED:
                raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                    f"{child} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item != NOT_ACCEPTED:
                raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                    f"{child} must remain not accepted"
                )
            _reject_source_authority(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_source_authority(item, f"{path}[{index}]")


def _expect_report_boundaries(payload: Mapping[str, Any], filename: str) -> None:
    expected = {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "research_only": True,
        "non_actionable": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }
    for field, expected_value in expected.items():
        if payload.get(field) != expected_value:
            raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                f"{filename} {field} mismatch"
            )
    if _contains_sensitive_value(payload):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            f"{filename} contains sensitive material"
        )
    _reject_source_authority(payload, filename)


def _per_ticker_review_digest(entry: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_additional_predictive_evidence_results_review_digest", None)
    return semantic_digest(payload)


def _build_per_ticker_entries(source_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_ticker = {row.get("ticker"): row for row in source_entries}
    if list(source_by_ticker) != TARGET_UNIVERSE:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "per-ticker source universe mismatch"
        )
    results = []
    for ticker in TARGET_UNIVERSE:
        source = source_by_ticker[ticker]
        if source.get("historical_record_count") != EXPECTED_RECORD_COUNTS[ticker]:
            raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                f"{ticker} source record count mismatch"
            )
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "additional_predictive_evidence_execution_status": "EXECUTED_RESEARCH_ONLY",
            "additional_predictive_evidence_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "metric_recomputation_performed_in_review": False,
            "model_training_performed_in_review": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
            "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        }
        if ticker == "META":
            entry["review_note"] = (
                "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_IMPROVED_EVIDENCE"
            )
        entry["per_ticker_additional_predictive_evidence_results_review_digest"] = (
            _per_ticker_review_digest(entry)
        )
        results.append(entry)
    return results


def _verify_outputs(output_root: Path) -> dict[str, Any]:
    if not output_root.is_dir():
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError("output root missing")
    names = sorted(path.name for path in output_root.iterdir() if path.is_file())
    if names != sorted(EXPECTED_OUTPUT_FILENAMES):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "expected exactly 13 execution output files"
        )
    initial_hashes = {
        filename: _sha256_file(output_root / filename) for filename in EXPECTED_OUTPUT_FILENAMES
    }
    payloads = {
        filename: _load_json(output_root / filename) for filename in EXPECTED_OUTPUT_FILENAMES
    }
    manifest = payloads["additional_predictive_evidence_execution_manifest.json"]
    try:
        execution.validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
            manifest
        )
    except execution.AdditionalPredictiveEvidenceExecutionImprovedEvidenceError as exc:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "source execution manifest validation failed"
        ) from exc

    required_manifest = {
        "artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        "execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        "additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "output_digest_manifest_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "generated_output_count": 13,
        "feature_label_matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152,
        "model_family_count": 9,
        "metric_family_count": 10,
        "leakage_control_count": 8,
        "leakage_failed_control_count": 0,
    }
    for field, expected_value in required_manifest.items():
        if manifest.get(field) != expected_value:
            raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                f"source execution {field} mismatch"
            )
    for field, expected_value in execution.SOURCE_EVIDENCE.items():
        if manifest.get(field) != expected_value:
            raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                f"source evidence {field} mismatch"
            )
    _reject_source_authority(manifest, "execution_manifest")
    if _contains_sensitive_value(manifest):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "execution manifest contains sensitive material"
        )

    report_names = [name for name in EXPECTED_OUTPUT_FILENAMES if name != "additional_predictive_evidence_execution_manifest.json"]
    for filename in report_names:
        _expect_report_boundaries(payloads[filename], filename)

    digest_payload = payloads["additional_predictive_evidence_digest_manifest.json"]
    entries = digest_payload.get("output_digest_entries")
    if not isinstance(entries, list) or len(entries) != 13:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "digest manifest entries mismatch"
        )
    recorded = {row.get("filename"): row for row in entries if isinstance(row, dict)}
    if set(recorded) != set(EXPECTED_OUTPUT_FILENAMES):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "digest manifest filenames mismatch"
        )
    output_digest_manifest = []
    mismatch_count = 0
    for filename in EXPECTED_OUTPUT_FILENAMES:
        source_entry = recorded[filename]
        local_sha256 = initial_hashes[filename]
        if filename == "additional_predictive_evidence_digest_manifest.json":
            matched = (
                source_entry.get("digest_kind") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
                and source_entry.get("sha256") is None
                and digest_payload.get("self_reference_policy")
                == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
            )
        else:
            matched = (
                source_entry.get("digest_kind") == "FILE_SHA256"
                and source_entry.get("sha256") == local_sha256
            )
        mismatch_count += int(not matched)
        output_digest_manifest.append(
            {
                "filename": filename,
                "local_sha256": local_sha256,
                "recorded_sha256": source_entry.get("sha256"),
                "digest_kind": source_entry.get("digest_kind"),
                "digest_match": matched,
            }
        )
    if mismatch_count:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            f"output digest mismatch count {mismatch_count}"
        )
    if (
        digest_payload.get("additional_predictive_evidence_execution_digest")
        != EXPECTED_EXECUTION_DIGEST
        or digest_payload.get("output_digest_manifest_digest")
        != EXPECTED_OUTPUT_BINDING_DIGEST
    ):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "digest manifest binding mismatch"
        )

    source_binding = payloads["source_binding_manifest.json"]
    label_schema = payloads["improved_label_schema_binding_report.json"]
    matrix = payloads["improved_feature_label_matrix_report.json"]
    walk = payloads["walk_forward_results.json"]
    oos = payloads["oos_results.json"]
    baseline = payloads["baseline_model_comparison.json"]
    metrics = payloads["metric_family_results.json"]
    calibration = payloads["calibration_stability_report.json"]
    leakage = payloads["leakage_quality_control_report.json"]
    per_ticker = payloads["per_ticker_meta_review.json"]
    operator = payloads["operator_results_review_summary.json"]
    model_rows = baseline.get("model_family_results")
    if not isinstance(model_rows, list) or len(model_rows) != 9:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "model family results mismatch"
        )
    model_by_id = {row.get("model_family_id"): row for row in model_rows if isinstance(row, dict)}
    expected_model_facts = {
        "MODEL_FAMILY_MAJORITY_BASELINE": "0.58626033",
        "MODEL_FAMILY_LOCAL_REGULARIZED_BASELINE": "0.58626033",
        "MODEL_FAMILY_CROSS_SECTIONAL_BASELINE": "0.58935950",
    }
    for model_id, accuracy in expected_model_facts.items():
        if model_by_id.get(model_id, {}).get("oos_metrics", {}).get("accuracy") != accuracy:
            raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
                f"{model_id} accuracy mismatch"
            )
    optional_statuses = {
        model_id: model_by_id.get(model_id, {}).get("evaluation_status")
        for model_id in (
            "MODEL_FAMILY_OPTIONAL_TREE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
            "MODEL_FAMILY_OPTIONAL_ENSEMBLE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
        )
    }
    if set(optional_statuses.values()) != {"NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE"}:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "optional model status mismatch"
        )
    deltas = metrics.get("baseline_outperformance_delta", {})
    controls = leakage.get("controls")
    source_per_ticker = per_ticker.get("per_ticker_execution_entries")
    if not isinstance(controls, list) or len(controls) != 8 or any(
        row.get("status") != PASS for row in controls if isinstance(row, dict)
    ):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "leakage controls mismatch"
        )
    if not isinstance(source_per_ticker, list):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "per-ticker source entries missing"
        )
    review_entries = _build_per_ticker_entries(source_per_ticker)
    verified_sections = {
        "execution_manifest": True,
        "source_binding_manifest": source_binding.get("binding_status")
        == "ALL_APPROVED_FROZEN_INPUTS_BOUND_READ_ONLY",
        "improved_label_schema_binding_report": label_schema.get("binding_status")
        == "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION",
        "improved_feature_label_matrix_report": (
            matrix.get("matrix_status") == "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX"
            and matrix.get("source_matrix_row_count") == 143352
            and matrix.get("evaluable_matrix_row_count") == 142200
            and matrix.get("unavailable_target_matrix_row_count") == 1152
        ),
        "walk_forward_results": walk.get("walk_forward_status") == "COMPUTED_RESEARCH_ONLY"
        and walk.get("fold_count") == 4 and len(walk.get("folds", [])) == 4,
        "oos_results": oos.get("oos_status") == "COMPUTED_RESEARCH_ONLY"
        and oos.get("oos_evaluated_rows") == 34848,
        "baseline_model_comparison": baseline.get("baseline_model_comparison_status")
        == "COMPUTED_RESEARCH_ONLY",
        "metric_family_results": metrics.get("metric_family_status") == "COMPUTED_RESEARCH_ONLY"
        and metrics.get("metric_family_count") == 10,
        "calibration_stability_report": calibration.get("calibration_stability_status")
        == "COMPUTED_RESEARCH_ONLY",
        "leakage_quality_control_report": leakage.get("leakage_quality_control_status")
        == "PASS_RESEARCH_ONLY" and leakage.get("failed_control_count") == 0,
        "per_ticker_meta_review": per_ticker.get("per_ticker_meta_review_status")
        == "COMPLETED_RESEARCH_ONLY" and len(review_entries) == 12,
        "operator_results_review_summary": operator.get("generated_output_count") == 13
        and operator.get("results_review_required") is True,
    }
    if not all(verified_sections.values()):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "source report verification failed"
        )
    if (
        deltas.get("BASELINE_TICKER_CROSS_SECTIONAL") != "0.00309917"
        or deltas.get("MODEL_FAMILY_REGULARIZED_LINEAR") != "0.00000000"
    ):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "baseline delta mismatch"
        )
    final_hashes = {
        filename: _sha256_file(output_root / filename) for filename in EXPECTED_OUTPUT_FILENAMES
    }
    if final_hashes != initial_hashes:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "source outputs changed during review"
        )
    return {
        "observed_output_count": len(names),
        "output_digest_mismatch_count": mismatch_count,
        "local_output_hashes": initial_hashes,
        "output_digest_manifest": output_digest_manifest,
        "digest_manifest_self_reference_policy": digest_payload.get("self_reference_policy"),
        "verified_sections": verified_sections,
        "per_ticker_results_review_entries": review_entries,
        "optional_model_statuses": optional_statuses,
        "walk_forward_stability": deepcopy(calibration.get("walk_forward_stability", {})),
        "oos_method_metrics": deepcopy(oos.get("oos_method_metrics", {})),
        "metric_families": deepcopy(metrics.get("metric_families", [])),
        "source_outputs_unchanged": True,
    }


def _base_package(output_root: Path) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_IMPROVED_EVIDENCE_V1,
        "output_root": str(output_root).replace("\\", "/"),
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        **deepcopy(SOURCE_EVIDENCE),
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence": True,
        **{field: False for field in FALSE_AUTHORITY_FIELDS},
        "selected_redesign_direction": SELECTED_DIRECTION,
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
        "generated_output_count": 13,
        "planned_source_input_count": 15,
        "execution_activity_count": 12,
        "model_family_count": 9,
        "metric_family_count": 10,
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
        "optional_tree_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "optional_ensemble_model_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        "leakage_control_passed": True,
        "leakage_failed_control_count": 0,
        "leakage_control_count": 8,
        "results_review_classification": "COMPLETED_RESEARCH_ONLY",
        "additional_predictive_evidence_execution_classification": "COMPLETED_RESEARCH_ONLY",
        "execution_scope_review": "RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE",
        "selected_redesign_direction_review": "USED_AS_RESEARCH_CONTEXT_ONLY",
        "label_schema_binding_review": "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION",
        "improved_feature_label_matrix_review": "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX",
        "walk_forward_review": "REVIEWED_RESEARCH_ONLY",
        "oos_review": "REVIEWED_RESEARCH_ONLY",
        "baseline_model_comparison_review": "REVIEWED_RESEARCH_ONLY",
        "metric_family_review": "REVIEWED_RESEARCH_ONLY",
        "calibration_stability_review": "REVIEWED_RESEARCH_ONLY",
        "leakage_quality_control_review": "PASS_RESEARCH_ONLY",
        "per_ticker_meta_review": "COMPLETED_RESEARCH_ONLY",
        "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_REASSESSMENT",
        "profitability_interpretation": "NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "reassessment_readiness": "READY_FOR_FUTURE_REASSESSMENT_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "limitations": list(LIMITATIONS),
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


def _review_checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    sections = package.get("verified_sections", {})
    entries = package.get("per_ticker_results_review_entries", [])
    output_manifest = package.get("output_digest_manifest", [])
    specs: list[tuple[str, Any, Any]] = [
        ("execution_digest_bound", EXPECTED_EXECUTION_DIGEST, package.get("source_execution_digest")),
        ("output_binding_digest_bound", EXPECTED_OUTPUT_BINDING_DIGEST, package.get("source_output_binding_digest")),
        ("approval_digest_bound", EXPECTED_APPROVAL_DIGEST, package.get("source_approval_digest")),
        ("candidate_review_digest_bound", EXPECTED_CANDIDATE_REVIEW_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest")),
        ("candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, package.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest")),
        ("planning_results_review_digest_bound", execution.SOURCE_EVIDENCE["improved_evidence_planning_results_review_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_results_review_using_redesigned_evidence_digest")),
        ("planning_execution_digest_bound", execution.EXPECTED_PLANNING_EXECUTION_DIGEST, package.get("improved_evidence_planning_execution_using_redesigned_evidence_digest")),
        ("planning_output_binding_digest_bound", execution.EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST, package.get("improved_evidence_planning_output_binding_digest")),
        ("planning_approval_digest_bound", execution.SOURCE_EVIDENCE["improved_evidence_planning_approval_using_redesigned_evidence_digest"], package.get("improved_evidence_planning_approval_using_redesigned_evidence_digest")),
        ("redesign_results_review_digest_bound", execution.SOURCE_EVIDENCE["label_objective_redesign_results_review_using_redesigned_evidence_digest"], package.get("label_objective_redesign_results_review_using_redesigned_evidence_digest")),
        ("redesign_execution_digest_bound", execution.SOURCE_EVIDENCE["label_objective_redesign_execution_using_redesigned_evidence_digest"], package.get("label_objective_redesign_execution_using_redesigned_evidence_digest")),
        ("target_definition_results_review_digest_bound", execution.SOURCE_EVIDENCE["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_results_review_using_redesigned_evidence_digest")),
        ("target_definition_execution_digest_bound", execution.SOURCE_EVIDENCE["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], package.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest")),
        ("path_selection_digest_bound", execution.SOURCE_EVIDENCE["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], package.get("method_evidence_improvement_path_selection_using_redesigned_evidence_digest")),
        ("readiness_review_digest_bound", execution.SOURCE_EVIDENCE["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], package.get("predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest")),
        ("reassessment_digest_bound", execution.SOURCE_EVIDENCE["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], package.get("predictive_usefulness_reassessment_using_redesigned_evidence_digest")),
        ("prior_predictive_results_review_digest_bound", execution.SOURCE_EVIDENCE["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest")),
        ("prior_predictive_execution_digest_bound", execution.SOURCE_EVIDENCE["additional_predictive_evidence_execution_using_redesigned_labels_digest"], package.get("additional_predictive_evidence_execution_using_redesigned_labels_digest")),
        ("matrix_digest_bound", EXPECTED_MATRIX_DIGEST, package.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", EXPECTED_FEATURE_VALUES_DIGEST, package.get("feature_values_digest")),
        ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, package.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, package.get("research_registry_approval_digest")),
        ("records_digest_bound", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("target_universe_12_preserved", 12, package.get("target_universe_count")),
        ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, package.get("records_digest")),
        ("meta_913_preserved", 913, package.get("meta_record_count")),
        ("source_execution_status_research_only", execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY, package.get("source_execution_status")),
        ("selected_redesign_direction_preserved", SELECTED_DIRECTION, package.get("selected_redesign_direction")),
        ("generated_output_count_13", 13, package.get("generated_output_count")),
        ("output_digests_bound", 13, len(output_manifest)),
        ("output_digest_mismatch_count_zero", 0, package.get("output_digest_mismatch_count")),
        ("outputs_research_only_non_actionable", True, package.get("outputs_research_only_non_actionable")),
        ("execution_manifest_verified", True, sections.get("execution_manifest")),
        ("source_binding_manifest_verified", True, sections.get("source_binding_manifest")),
        ("label_schema_binding_report_verified", True, sections.get("improved_label_schema_binding_report")),
        ("feature_label_matrix_report_verified", True, sections.get("improved_feature_label_matrix_report")),
        ("walk_forward_results_verified", True, sections.get("walk_forward_results")),
        ("oos_results_verified", True, sections.get("oos_results")),
        ("baseline_model_comparison_verified", True, sections.get("baseline_model_comparison")),
        ("metric_family_results_verified", True, sections.get("metric_family_results")),
        ("calibration_stability_report_verified", True, sections.get("calibration_stability_report")),
        ("leakage_quality_control_report_verified", True, sections.get("leakage_quality_control_report")),
        ("per_ticker_meta_review_verified", True, sections.get("per_ticker_meta_review")),
        ("operator_summary_verified", True, sections.get("operator_results_review_summary")),
        ("results_review_created_true", True, package.get("additional_predictive_evidence_results_review_created")),
        ("results_review_ready_true", True, package.get("additional_predictive_evidence_results_review_ready")),
        ("ready_for_reassessment_true", True, package.get("ready_for_predictive_usefulness_reassessment_using_improved_evidence")),
        ("reassessment_created_false", False, package.get("predictive_usefulness_reassessment_using_improved_evidence_created")),
        ("acceptance_readiness_created_false", False, package.get("predictive_usefulness_acceptance_readiness_using_improved_evidence_created")),
    ]
    for field in (
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "feature_generation_authorized", "feature_generation_performed", "feature_label_matrix_created",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
    ):
        specs.append((f"{field}_false", False, package.get(field)))
    specs.extend([
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, package.get("predictive_usefulness")),
        ("acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        ("acceptance_candidate_created_false", False, package.get("predictive_usefulness_acceptance_candidate_created")),
        ("profitability_not_accepted", NOT_ACCEPTED, package.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("trade_recommendations_false", False, package.get("trade_recommendations_generated")),
        ("matrix_rows_preserved", 143352, package.get("matrix_row_count")),
        ("evaluable_rows_preserved", 142200, package.get("evaluable_matrix_row_count")),
        ("unavailable_targets_preserved", 1152, package.get("unavailable_target_count")),
        ("small_cross_sectional_edge_preserved", "0.00309917", package.get("cross_sectional_delta_vs_majority")),
        ("local_model_equivalence_preserved", package.get("majority_accuracy"), package.get("local_model_accuracy")),
        ("leakage_controls_passed", True, package.get("leakage_control_passed")),
        ("meta_limitation_preserved", True, package.get("meta_reduced_record_count_preserved")),
        ("per_ticker_entries_12", 12, len(entries)),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(entries)),
        ("provider_requests_made_false", False, package.get("provider_requests_made_in_review")),
        ("market_data_acquisition_false", False, package.get("market_data_acquisition_performed_in_review")),
        ("dataset_regeneration_false", False, package.get("dataset_generation_performed_in_review")),
        ("redesigned_label_regeneration_false", False, package.get("redesigned_label_regeneration_performed")),
        ("feature_regeneration_false", False, package.get("feature_regeneration_performed")),
        ("predictive_evidence_rerun_false", False, package.get("additional_predictive_evidence_execution_rerun_performed")),
        ("additional_predictive_evidence_execution_rerun_false", False, package.get("additional_predictive_evidence_execution_rerun_performed")),
        ("metric_recomputation_in_review_false", False, package.get("metric_recomputation_performed_in_review")),
        ("model_training_in_review_false", False, package.get("model_training_performed_in_review")),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
        ("limitations_recorded", LIMITATIONS, package.get("limitations")),
        ("next_chain_defined", NEXT_CHAIN, package.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, package.get("risk_controls")),
        ("no_tracked_marketflow_files", True, package.get("no_tracked_marketflow_files")),
    ])
    return [_check(check_id, expected, actual) for check_id, expected, actual in specs]


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(row, dict)
        and row.get("per_ticker_additional_predictive_evidence_results_review_digest")
        == _per_ticker_review_digest(row)
        for row in entries
    )


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "results_review_ready": not failed,
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence": not failed,
        "predictive_usefulness_reassessment_using_improved_evidence_created": False,
        "predictive_usefulness_acceptance_readiness_using_improved_evidence_created": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "metric_recomputation_performed_in_review": False,
        "model_training_performed_in_review": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(package))
    payload.pop("additional_predictive_evidence_results_review_using_improved_evidence_digest", None)
    payload["output_root"] = DEFAULT_SOURCE_OUTPUT_ROOT.as_posix()
    return payload


def additional_predictive_evidence_results_review_using_improved_evidence_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    return semantic_digest(_digest_payload(review_package))


def _blocked_package(output_root: Path, reason: str) -> dict[str, Any]:
    package = _base_package(output_root)
    package.update({
        "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_IMPROVED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS,
        "output_file_inspection_performed": False,
        "outputs_verified": False,
        "outputs_research_only_non_actionable": False,
        "additional_predictive_evidence_results_review_created": False,
        "additional_predictive_evidence_results_review_ready": False,
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence": False,
        "observed_output_count": 0,
        "output_digest_mismatch_count": None,
        "local_output_hashes": {},
        "output_digest_manifest": [],
        "verified_sections": {},
        "per_ticker_results_review_entries": [],
        "blocked_reason": reason,
        "review_checklist": [],
        "review_summary": {
            **_summary([]),
            "results_review_ready": False,
            "ready_for_predictive_usefulness_reassessment_using_improved_evidence": False,
        },
    })
    package["additional_predictive_evidence_results_review_using_improved_evidence_digest"] = (
        additional_predictive_evidence_results_review_using_improved_evidence_digest_v1(package)
    )
    return package


def build_additional_predictive_evidence_results_review_using_improved_evidence_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Inspect saved outputs and build a deterministic research-only review package."""
    root = DEFAULT_SOURCE_OUTPUT_ROOT if output_root is None else Path(output_root)
    try:
        verification = _verify_outputs(root)
    except (AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError, OSError) as exc:
        return _blocked_package(root, str(exc))
    package = _base_package(root)
    package.update({
        "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY,
        "output_file_inspection_performed": True,
        "outputs_verified": True,
        "outputs_research_only_non_actionable": True,
        "expected_output_count": 13,
        **deepcopy(verification),
    })
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["additional_predictive_evidence_results_review_using_improved_evidence_digest"] = (
        additional_predictive_evidence_results_review_using_improved_evidence_digest_v1(package)
    )
    validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            f"{field} mismatch"
        )


def validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
    review_package: dict,
) -> dict[str, Any]:
    """Reject source drift or any authority beyond a research-only results review."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "review_package must be an object"
        )
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_IMPROVED_EVIDENCE_V1,
        "schema_version",
    )
    digest = review_package.get(
        "additional_predictive_evidence_results_review_using_improved_evidence_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "review digest missing"
        )
    if review_package.get("review_status") == (
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_IMPROVED_EVIDENCE_MISSING_OR_INVALID_OUTPUTS
    ):
        _expect(review_package.get("output_file_inspection_performed"), False, "output inspection")
        _expect(review_package.get("additional_predictive_evidence_results_review_ready"), False, "review ready")
        _expect(review_package.get("ready_for_predictive_usefulness_reassessment_using_improved_evidence"), False, "reassessment readiness")
        _expect(
            digest,
            additional_predictive_evidence_results_review_using_improved_evidence_digest_v1(
                review_package
            ),
            "review digest",
        )
        return {"valid": True, "blocked": True, "review_status": review_package["review_status"]}

    _expect(
        review_package.get("review_status"),
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_IMPROVED_EVIDENCE_READY,
        "review_status",
    )
    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "additional_predictive_evidence_results_review_created",
        "additional_predictive_evidence_results_review_ready",
        "ready_for_predictive_usefulness_reassessment_using_improved_evidence",
        "meta_reduced_record_count_preserved", "leakage_control_passed",
        "output_file_inspection_performed", "outputs_verified",
        "outputs_research_only_non_actionable", "source_outputs_unchanged",
        "no_tracked_marketflow_files",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in FALSE_AUTHORITY_FIELDS:
        _expect(review_package.get(field), False, field)
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        "source_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_OUTPUT_BINDING_DIGEST,
        "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
        **SOURCE_EVIDENCE,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "generated_output_count": 13,
        "observed_output_count": 13,
        "output_digest_mismatch_count": 0,
        "matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_count": 1152,
        "oos_row_count": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "results_review_classification": "COMPLETED_RESEARCH_ONLY",
        "reassessment_readiness": "READY_FOR_FUTURE_REASSESSMENT_ONLY",
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)
    output_manifest = review_package.get("output_digest_manifest")
    if not isinstance(output_manifest, list) or len(output_manifest) != 13:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "output digest manifest mismatch"
        )
    if [row.get("filename") for row in output_manifest] != EXPECTED_OUTPUT_FILENAMES:
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "output digest filenames mismatch"
        )
    if any(row.get("digest_match") is not True for row in output_manifest):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "output digest mismatch"
        )
    entries = review_package.get("per_ticker_results_review_entries")
    if not _per_ticker_digests_valid(entries):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "per-ticker digest mismatch"
        )
    _expect([row.get("ticker") for row in entries], TARGET_UNIVERSE, "per-ticker order")
    checklist = review_package.get("review_checklist")
    expected_checklist = _review_checklist(review_package)
    _expect(checklist, expected_checklist, "review checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "review checklist failed"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review summary")
    _expect(
        digest,
        additional_predictive_evidence_results_review_using_improved_evidence_digest_v1(
            review_package
        ),
        "review digest",
    )
    return {
        "valid": True,
        "blocked": False,
        "review_status": review_package["review_status"],
        "additional_predictive_evidence_results_review_using_improved_evidence_digest": digest,
        **{
            key: review_package["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_additional_predictive_evidence_results_review_using_improved_evidence_markdown_v1(
    review_package: dict,
) -> str:
    validation = validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        review_package
    )
    sections = [
        ("Title", "Optional Additional Predictive Evidence Results Review Using Improved Evidence v1."),
        ("Optional Additional Predictive Evidence Results Review Using Improved Evidence", f"Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`."),
        ("Source Execution", f"Execution digest: `{review_package['source_execution_digest']}`."),
        ("Bound Evidence", "Execution, output binding, approval, candidate, planning, redesign, target-definition, prior predictive, registry, and records digests are bound."),
        ("Dataset and Universe", "The frozen 12-ticker dataset remains 11,946 records; META remains 913."),
        ("Output Verification", "All 13 saved outputs and available recorded SHA-256 values were verified read-only."),
        ("Selected Redesign Direction", f"`{review_package['selected_redesign_direction']}` remains research context only."),
        ("Source Binding Review", f"`{review_package['verified_sections']['source_binding_manifest']}`."),
        ("Improved Label Schema Binding Review", f"`{review_package['label_schema_binding_review']}`."),
        ("Improved Feature-Label Matrix Report Review", f"Rows/evaluable/unavailable: `{review_package['matrix_row_count']} / {review_package['evaluable_matrix_row_count']} / {review_package['unavailable_target_count']}`."),
        ("Walk-Forward Results Review", f"`{review_package['walk_forward_review']}`; four chronological folds."),
        ("OOS Results Review", f"`{review_package['oos_review']}`; `{review_package['oos_row_count']}` rows."),
        ("Baseline and Model Comparison Review", f"Cross-sectional delta: `{review_package['cross_sectional_delta_vs_majority']}`; local equals majority."),
        ("Metric Family Results Review", f"`{review_package['metric_family_count']}` families reviewed without recomputation."),
        ("Calibration and Stability Review", f"`{review_package['calibration_stability_review']}`."),
        ("Leakage and Quality Controls Review", "Eight controls passed and zero failed."),
        ("Per-Ticker and META Review", "Twelve digest-bound entries; META's 913-record limitation is preserved."),
        ("Review Classification", f"`{review_package['results_review_classification']}`; review only, not acceptance."),
        ("Limitations", ", ".join(review_package["limitations"])),
        ("Next Chain", " ".join(review_package["next_chain"])),
        ("Next Gates", ", ".join(review_package["next_gates"])),
        ("Risk Controls", ", ".join(review_package["risk_controls"])),
        ("Predictive Usefulness Boundary", "Predictive usefulness remains `not accepted`; reassessment was not created."),
        ("Profitability Boundary", "Profitability remains `not accepted`."),
        ("Runtime Boundary", "Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."),
        ("Checklist Summary", f"Checks: `{validation['total_checks']}` passed; zero failed; zero blockers."),
        ("Guardrails", "No provider, acquisition, regeneration, recomputation, training, reassessment, acceptance, runtime, recommendation, or trading action occurred."),
    ]
    lines = ["# MarketFlow Additional Predictive Evidence Results Review Using Improved Evidence", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, ""])
    return "\n".join(lines)


def write_additional_predictive_evidence_results_review_using_improved_evidence_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write one canonical package without overwriting existing evidence."""
    package = build_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        output_root=output_root
    )
    validation = validate_additional_predictive_evidence_results_review_using_improved_evidence_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_results_review_using_improved_evidence_v1.json"
    if path.exists():
        raise AdditionalPredictiveEvidenceResultsReviewImprovedEvidenceError(
            "review package output already exists"
        )
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "additional_predictive_evidence_results_review_using_improved_evidence_digest": validation[
            "additional_predictive_evidence_results_review_using_improved_evidence_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
