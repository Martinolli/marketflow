"""Offline results review for predictive evidence using redesigned labels."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import additional_predictive_evidence_execution_redesigned_labels_service as execution


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1 = (
    "additional_predictive_evidence_results_review_using_redesigned_labels_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS"
)

SOURCE_OUTPUT_ROOT = Path(
    ".marketflow/additional_predictive_evidence_using_redesigned_labels/expanded_universe_v1"
)
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_USING_REDESIGNED_LABELS_RESEARCH_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_EXECUTION_DIGEST = "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_APPROVAL_DIGEST = "cc45d6692f1f249cc76554f7019f148c8510efedeade22adb3ccb3fcbc54fe96"
EXPECTED_CANDIDATE_REVIEW_DIGEST = "dc4ae33cd0f40d84de33ce7e195d35696443fa5cd5dcb52dee4ce0c649ac06ec"
EXPECTED_CANDIDATE_DIGEST = "f11550ab63f21f2f08b896296324e0f0b1cb99a27ae186cfc347028e5ddf9cd5"
EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST = "e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3"
EXPECTED_FEATURE_EXECUTION_DIGEST = "d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_FEATURE_APPROVAL_DIGEST = "595bb9685936979810cfe6e3a814ea9ef38e0e3d89b804426a2d540ec77471c1"
EXPECTED_LABEL_RESULTS_REVIEW_DIGEST = "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
EXPECTED_LABEL_EXECUTION_DIGEST = "0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506"
EXPECTED_LABEL_APPROVAL_DIGEST = "280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"

EXPECTED_TARGET_UNIVERSE = [
    "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT",
]
EXPECTED_OUTPUT_FILENAMES = [
    "additional_predictive_evidence_execution_manifest.json",
    "source_feature_label_binding_manifest.json",
    "feature_label_matrix.jsonl",
    "chronological_split_profile.json",
    "walk_forward_results.json",
    "oos_holdout_results.json",
    "baseline_model_comparison_results.json",
    "metric_family_results.json",
    "calibration_stability_report.json",
    "leakage_quality_control_report.json",
    "per_ticker_cross_sectional_review.json",
    "operator_review_summary.json",
    "additional_predictive_evidence_digest_manifest.json",
]

LIMITATIONS = [
    "predictive_evidence_is_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "trade_recommendations_not_generated",
    "small_oos_cross_sectional_edge_requires_reassessment",
    "local_model_did_not_outperform_majority",
    "optional_tree_and_ensemble_unavailable",
    "meta_reduced_record_count_preserved",
    "operator_review_required_before_reassessment",
    "operator_approval_required_before_any_acceptance",
]
NEXT_CHAIN = [
    "Predictive Usefulness Reassessment Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]
NEXT_GATES = [
    "predictive_usefulness_reassessment_using_redesigned_evidence",
    "predictive_usefulness_acceptance_readiness_using_redesigned_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_rerun_predictive_evidence",
    "review_does_not_retrain_models",
    "review_does_not_recompute_metrics",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "execution_digest_bound", "feature_label_matrix_digest_bound", "approval_digest_bound",
    "candidate_review_digest_bound", "candidate_digest_bound", "feature_results_review_digest_bound",
    "feature_values_digest_bound", "redesigned_label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved", "records_digest_preserved",
    "label_values_digest_preserved", "feature_values_digest_preserved", "matrix_digest_preserved",
    "meta_913_preserved", "source_execution_status_research_only", "generated_output_count_13",
    "output_digests_bound", "output_digest_mismatch_count_zero", "outputs_research_only_non_actionable",
    "matrix_verified", "walk_forward_results_verified", "oos_holdout_results_verified",
    "baseline_model_comparison_verified", "metric_family_results_verified",
    "calibration_stability_report_verified", "leakage_quality_control_verified",
    "per_ticker_cross_sectional_review_verified", "operator_summary_verified",
    "feature_label_matrix_row_count_143352", "evaluable_matrix_row_count_142200",
    "unavailable_target_count_1152", "walk_forward_fold_count_4", "oos_holdout_year_2025",
    "oos_evaluated_rows_34848", "baseline_family_count_4", "model_family_count_5",
    "metric_family_count_10", "leakage_control_status_pass", "leakage_failed_control_count_zero",
    "oos_cross_sectional_delta_bound", "local_model_delta_bound", "optional_model_unavailability_recorded",
    "results_review_created_true", "results_review_ready_true",
    "ready_for_predictive_usefulness_reassessment_true",
    "predictive_usefulness_reassessment_created_false",
    "predictive_usefulness_acceptance_candidate_created_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized", "strategy_not_authorized",
    "broker_not_authorized", "trade_recommendations_false", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "redesigned_label_regeneration_false", "feature_regeneration_false",
    "predictive_evidence_rerun_false", "metric_recomputation_in_review_false",
    "model_training_in_review_false", "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created", "no_runtime_migration_approval_created",
    "limitations_recorded", "next_chain_defined", "next_gates_defined", "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(ValueError):
    """Raised when the digest-bound review package is invalid."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            f"{path.name} is not valid readable JSON"
        ) from exc
    if not isinstance(value, dict):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            f"{path.name} must contain a JSON object"
        )
    return value


def _expect_source_boundaries(payload: Mapping[str, Any], filename: str) -> None:
    expected = {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }
    for field, value in expected.items():
        if payload.get(field) != value:
            raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                f"{filename} {field} mismatch"
            )
    if _contains_sensitive_value(payload):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            f"{filename} contains an unredacted sensitive value"
        )
    forbidden = _forbidden_authority_field(payload)
    if forbidden:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            f"{filename} contains forbidden field {forbidden}"
        )


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() == "authorization" and item != "<redacted>":
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


def _forbidden_authority_field(payload: Mapping[str, Any]) -> str | None:
    forbidden_true = {
        "raw_provider_payloads_committed",
        "raw_provider_payload_committed",
        "api_keys_stored_or_printed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "runtime_migration_approved",
        "runtime_migration_active",
    }
    forbidden_keys = {"provider_response_body", "raw_provider_payload", "raw_provider_payloads"}
    for key, value in payload.items():
        if key in forbidden_keys or (key in forbidden_true and value is True):
            return key
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            return key
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            return key
        if isinstance(value, Mapping):
            nested = _forbidden_authority_field(value)
            if nested:
                return f"{key}.{nested}"
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Mapping):
                    nested = _forbidden_authority_field(item)
                    if nested:
                        return f"{key}[{index}].{nested}"
    return None


def _inspect_matrix(path: Path) -> dict[str, Any]:
    row_count = 0
    evaluable_count = 0
    unavailable_count = 0
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                    f"feature_label_matrix.jsonl line {line_number} is invalid"
                ) from exc
            if not isinstance(row, dict):
                raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                    f"feature_label_matrix.jsonl line {line_number} is not an object"
                )
            _expect_source_boundaries(row, "feature_label_matrix.jsonl")
            for field in (
                "future_label_values_used_as_features",
                "forward_return_used_as_feature",
                "label_value_used_as_feature",
                "threshold_value_used_as_numeric_predictor",
            ):
                if row.get(field) is not False:
                    raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                        f"feature_label_matrix.jsonl {field} must be false"
                    )
            row_count += 1
            if row.get("label_available") is True:
                evaluable_count += 1
            else:
                unavailable_count += 1
    return {
        "row_count": row_count,
        "evaluable_count": evaluable_count,
        "unavailable_count": unavailable_count,
        "verified": row_count == 143352 and evaluable_count == 142200 and unavailable_count == 1152,
    }


def _verify_outputs(output_root: Path) -> dict[str, Any]:
    if not output_root.is_dir():
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("output root missing")
    actual_names = sorted(path.name for path in output_root.iterdir() if path.is_file())
    if actual_names != sorted(EXPECTED_OUTPUT_FILENAMES):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("expected 13 output files")

    digest_payload = _load_json(output_root / "additional_predictive_evidence_digest_manifest.json")
    _expect_source_boundaries(digest_payload, "additional_predictive_evidence_digest_manifest.json")
    entries = digest_payload.get("output_digest_entries")
    if not isinstance(entries, list) or len(entries) != 13:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("source digest manifest mismatch")
    recorded = {row.get("filename"): row for row in entries if isinstance(row, dict)}
    if set(recorded) != set(EXPECTED_OUTPUT_FILENAMES):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("source digest filenames mismatch")

    payloads: dict[str, dict[str, Any]] = {}
    output_manifest: list[dict[str, Any]] = []
    mismatch_count = 0
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = output_root / filename
        local_digest = _sha256_file(path)
        source_entry = recorded[filename]
        if filename == "additional_predictive_evidence_digest_manifest.json":
            expected_digest = None
            matched = (
                source_entry.get("digest_kind") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
                and source_entry.get("sha256") is None
                and digest_payload.get("self_reference_policy") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
            )
        else:
            expected_digest = source_entry.get("sha256")
            matched = source_entry.get("digest_kind") == "FILE_SHA256" and local_digest == expected_digest
        if not matched:
            mismatch_count += 1
        output_manifest.append(
            {
                "filename": filename,
                "local_sha256": local_digest,
                "recorded_sha256": expected_digest,
                "digest_kind": source_entry.get("digest_kind"),
                "digest_match": matched,
            }
        )
        if filename.endswith(".json"):
            payload = digest_payload if filename == "additional_predictive_evidence_digest_manifest.json" else _load_json(path)
            _expect_source_boundaries(payload, filename)
            payloads[filename] = payload
    if mismatch_count:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            f"output digest mismatch count {mismatch_count}"
        )

    matrix = _inspect_matrix(output_root / "feature_label_matrix.jsonl")
    if not matrix["verified"]:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("feature-label matrix profile mismatch")

    manifest = payloads["additional_predictive_evidence_execution_manifest.json"]
    try:
        execution.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(manifest)
    except execution.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError as exc:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            "source execution manifest validation failed"
        ) from exc
    required_manifest_values = {
        "artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS,
        "execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_FEATURE_EXECUTION_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "redesigned_label_row_count": 143352,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_value_row_count": 203082,
        "available_feature_value_count": 190848,
        "unavailable_feature_value_count": 12234,
        "generated_output_count": 13,
        "feature_label_matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152,
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
    }
    for field, value in required_manifest_values.items():
        if manifest.get(field) != value:
            raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                f"source execution {field} mismatch"
            )

    walk = payloads["walk_forward_results.json"]
    oos = payloads["oos_holdout_results.json"]
    comparison = payloads["baseline_model_comparison_results.json"]
    metrics = payloads["metric_family_results.json"]
    leakage = payloads["leakage_quality_control_report.json"]
    per_ticker = payloads["per_ticker_cross_sectional_review.json"]
    operator = payloads["operator_review_summary.json"]
    calibration = payloads["calibration_stability_report.json"]
    split = payloads["chronological_split_profile.json"]

    method_metrics = oos.get("method_metrics", {})
    majority = method_metrics.get("BASELINE_MAJORITY_CLASS", {})
    cross = method_metrics.get("BASELINE_TICKER_CROSS_SECTIONAL", {})
    local = method_metrics.get("MODEL_FAMILY_REGULARIZED_LINEAR", {})
    baselines = comparison.get("baseline_families", [])
    models = comparison.get("model_families", [])
    optional_statuses = {
        row.get("model_family"): row.get("evaluation_status") for row in models if isinstance(row, dict)
    }
    per_ticker_entries = per_ticker.get("per_ticker_entries", [])
    if [row.get("ticker") for row in per_ticker_entries] != EXPECTED_TARGET_UNIVERSE:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("per-ticker universe mismatch")
    expected_oos = {
        "majority": (majority, "0.58626033", "0.21557412", "0.04867526"),
        "ticker cross-sectional": (cross, "0.58935950", "0.28155252", "0.04831065"),
        "regularized local model": (local, "0.58626033", "0.21557412", "0.04867526"),
    }
    for name, (row, accuracy, macro_f1, brier) in expected_oos.items():
        if (
            row.get("accuracy") != accuracy
            or row.get("macro_f1") != macro_f1
            or row.get("brier_score") != brier
        ):
            raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
                f"{name} OOS metrics mismatch"
            )
    deltas = metrics.get("baseline_outperformance_delta", {})
    if (
        deltas.get("BASELINE_TICKER_CROSS_SECTIONAL") != "0.00309917"
        or deltas.get("MODEL_FAMILY_REGULARIZED_LINEAR") != "0.00000000"
    ):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            "baseline outperformance delta mismatch"
        )
    if list(optional_statuses.values()).count("NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE") != 2:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(
            "optional model unavailability mismatch"
        )

    verified_sections = {
        "feature_label_matrix": matrix["verified"],
        "walk_forward_results": walk.get("walk_forward_fold_count") == 4 and len(walk.get("folds", [])) == 4,
        "oos_holdout_results": oos.get("oos_holdout_year") == 2025 and oos.get("evaluation_count") == 34848,
        "baseline_model_comparison": comparison.get("baseline_family_count") == 4 and comparison.get("model_family_count") == 5,
        "metric_family_results": metrics.get("metric_family_count") == 10,
        "calibration_stability_report": calibration.get("calibration_status") == "RESEARCH_ONLY_HARD_CLASS_CALIBRATION_SUMMARY",
        "leakage_quality_control": leakage.get("leakage_control_status") == PASS and leakage.get("leakage_failed_control_count") == 0,
        "per_ticker_cross_sectional_review": len(per_ticker_entries) == 12,
        "operator_summary": operator.get("generated_output_count") == 13,
        "chronological_split_profile": split.get("walk_forward_folds") == ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"],
    }
    if not all(verified_sections.values()):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review section verification failed")

    return {
        "payloads": payloads,
        "output_digest_manifest": output_manifest,
        "output_digest_mismatch_count": mismatch_count,
        "matrix": matrix,
        "manifest": manifest,
        "verified_sections": verified_sections,
        "walk_forward_results": deepcopy(walk.get("folds", [])),
        "oos_metrics": {
            "majority_class": deepcopy(majority),
            "ticker_cross_sectional": deepcopy(cross),
            "regularized_local_model": deepcopy(local),
        },
        "baseline_family_count": len(baselines),
        "model_family_count": len(models),
        "metric_families": deepcopy(metrics.get("metric_families", [])),
        "walk_forward_stability": deepcopy(calibration.get("walk_forward_stability", {})),
        "per_ticker_entries": deepcopy(per_ticker_entries),
        "optional_model_statuses": optional_statuses,
        "self_reference_policy": digest_payload.get("self_reference_policy"),
    }


def _base_package(output_root: Path) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1,
        "output_root": output_root.as_posix(),
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "metric_recomputation_performed_in_review": False,
        "model_training_performed_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "source_additional_predictive_evidence_execution_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_FEATURE_EXECUTION_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_APPROVAL_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "additional_predictive_evidence_executed": True,
        "predictive_evidence_results_created": True,
        "metric_recomputation_performed": True,
        "model_training_performed": True,
        "additional_predictive_evidence_results_review_created": True,
        "additional_predictive_evidence_results_review_ready": True,
        "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence": True,
        "predictive_usefulness_reassessment_review_created": False,
        "predictive_usefulness_acceptance_readiness_review_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "redesigned_label_row_count": 143352,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_value_row_count": 203082,
        "available_feature_value_count": 190848,
        "unavailable_feature_value_count": 12234,
        "feature_label_matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152,
        "generated_output_count": 13,
        "expected_output_count": 13,
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "oos_evaluated_rows": 34848,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
        "oos_majority_accuracy": "0.58626033",
        "oos_ticker_cross_sectional_accuracy": "0.58935950",
        "oos_regularized_local_model_accuracy": "0.58626033",
        "oos_cross_sectional_delta_vs_majority": "0.00309917",
        "oos_local_model_delta_vs_majority": "0.00000000",
        "oos_majority_macro_f1": "0.21557412",
        "oos_ticker_cross_sectional_macro_f1": "0.28155252",
        "oos_regularized_local_model_macro_f1": "0.21557412",
        "oos_majority_brier": "0.04867526",
        "oos_ticker_cross_sectional_brier": "0.04831065",
        "oos_regularized_local_model_brier": "0.04867526",
        "predictive_evidence_interpretation": "GENERATED_RESEARCH_ONLY",
        "baseline_outperformance_interpretation": "SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_interpretation": "MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE",
        "stability_interpretation": "REQUIRES_REASSESSMENT",
        "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_SEPARATE_REASSESSMENT",
        "profitability_interpretation": "NOT_EVALUATED_NOT_ACCEPTED",
        "runtime_interpretation": NOT_AUTHORIZED,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
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
        "message": "review evidence matches" if status == PASS else "review evidence mismatch",
    }


def _review_checklist(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    manifest = package.get("output_digest_manifest", [])
    sections = package.get("verified_sections", {})
    optional = package.get("optional_model_statuses", {})
    actuals = {
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest_bound": package.get("source_feature_label_matrix_digest"),
        "approval_digest_bound": package.get("source_additional_predictive_evidence_execution_approval_digest"),
        "candidate_review_digest_bound": package.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"),
        "candidate_digest_bound": package.get("additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"),
        "feature_results_review_digest_bound": package.get("feature_generation_results_review_using_redesigned_labels_digest"),
        "feature_values_digest_bound": package.get("feature_values_digest"),
        "redesigned_label_values_digest_bound": package.get("redesigned_label_values_digest"),
        "research_registry_digest_bound": package.get("research_registry_approval_digest"),
        "records_digest_bound": package.get("records_digest"),
        "target_universe_12_preserved": package.get("target_universe_count"),
        "records_digest_preserved": package.get("records_digest"),
        "label_values_digest_preserved": package.get("redesigned_label_values_digest"),
        "feature_values_digest_preserved": package.get("feature_values_digest"),
        "matrix_digest_preserved": package.get("feature_label_matrix_digest"),
        "meta_913_preserved": package.get("meta_record_count"),
        "source_execution_status_research_only": package.get("source_execution_status"),
        "generated_output_count_13": package.get("generated_output_count"),
        "output_digests_bound": len(manifest),
        "output_digest_mismatch_count_zero": package.get("output_digest_mismatch_count"),
        "outputs_research_only_non_actionable": package.get("outputs_research_only_non_actionable"),
        "matrix_verified": sections.get("feature_label_matrix"),
        "walk_forward_results_verified": sections.get("walk_forward_results"),
        "oos_holdout_results_verified": sections.get("oos_holdout_results"),
        "baseline_model_comparison_verified": sections.get("baseline_model_comparison"),
        "metric_family_results_verified": sections.get("metric_family_results"),
        "calibration_stability_report_verified": sections.get("calibration_stability_report"),
        "leakage_quality_control_verified": sections.get("leakage_quality_control"),
        "per_ticker_cross_sectional_review_verified": sections.get("per_ticker_cross_sectional_review"),
        "operator_summary_verified": sections.get("operator_summary"),
        "feature_label_matrix_row_count_143352": package.get("feature_label_matrix_row_count"),
        "evaluable_matrix_row_count_142200": package.get("evaluable_matrix_row_count"),
        "unavailable_target_count_1152": package.get("unavailable_target_matrix_row_count"),
        "walk_forward_fold_count_4": package.get("walk_forward_fold_count"),
        "oos_holdout_year_2025": package.get("oos_holdout_year"),
        "oos_evaluated_rows_34848": package.get("oos_evaluated_rows"),
        "baseline_family_count_4": package.get("baseline_family_count"),
        "model_family_count_5": package.get("model_family_count"),
        "metric_family_count_10": package.get("metric_family_count"),
        "leakage_control_status_pass": package.get("leakage_control_status"),
        "leakage_failed_control_count_zero": package.get("leakage_failed_control_count"),
        "oos_cross_sectional_delta_bound": package.get("oos_cross_sectional_delta_vs_majority"),
        "local_model_delta_bound": package.get("oos_local_model_delta_vs_majority"),
        "optional_model_unavailability_recorded": sorted(set(optional.values())),
        "results_review_created_true": package.get("additional_predictive_evidence_results_review_created"),
        "results_review_ready_true": package.get("additional_predictive_evidence_results_review_ready"),
        "ready_for_predictive_usefulness_reassessment_true": package.get("ready_for_predictive_usefulness_reassessment_using_redesigned_evidence"),
        "predictive_usefulness_reassessment_created_false": package.get("predictive_usefulness_reassessment_review_created"),
        "predictive_usefulness_acceptance_candidate_created_false": package.get("predictive_usefulness_acceptance_candidate_created"),
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness"),
        "profitability_not_accepted": package.get("profitability"),
        "runtime_not_authorized": package.get("runtime_use"),
        "strategy_not_authorized": package.get("strategy_use"),
        "broker_not_authorized": package.get("broker_execution"),
        "trade_recommendations_false": package.get("trade_recommendations_generated"),
        "provider_requests_made_false": package.get("provider_requests_made_in_review"),
        "market_data_acquisition_false": package.get("market_data_acquisition_performed_in_review"),
        "dataset_regeneration_false": package.get("dataset_generation_performed_in_review"),
        "redesigned_label_regeneration_false": package.get("redesigned_label_regeneration_performed"),
        "feature_regeneration_false": package.get("feature_regeneration_performed"),
        "predictive_evidence_rerun_false": package.get("predictive_evidence_execution_rerun_performed"),
        "metric_recomputation_in_review_false": package.get("metric_recomputation_performed_in_review"),
        "model_training_in_review_false": package.get("model_training_performed_in_review"),
        "no_predictive_usefulness_acceptance_artifact_created": package.get("predictive_usefulness_acceptance_artifact_created"),
        "no_profitability_acceptance_created": package.get("profitability_acceptance_created"),
        "no_runtime_migration_approval_created": package.get("runtime_migration_approval_created"),
        "limitations_recorded": package.get("limitations"),
        "next_chain_defined": package.get("next_chain"),
        "next_gates_defined": package.get("next_gates"),
        "risk_controls_defined": package.get("risk_controls"),
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files"),
    }
    expected = {
        "execution_digest_bound": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest_bound": EXPECTED_MATRIX_DIGEST,
        "approval_digest_bound": EXPECTED_APPROVAL_DIGEST,
        "candidate_review_digest_bound": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "candidate_digest_bound": EXPECTED_CANDIDATE_DIGEST,
        "feature_results_review_digest_bound": EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST,
        "feature_values_digest_bound": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest_bound": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_digest_bound": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest_bound": EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": 12,
        "records_digest_preserved": EXPECTED_RECORDS_DIGEST,
        "label_values_digest_preserved": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest_preserved": EXPECTED_FEATURE_VALUES_DIGEST,
        "matrix_digest_preserved": EXPECTED_MATRIX_DIGEST,
        "meta_913_preserved": 913,
        "source_execution_status_research_only": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "generated_output_count_13": 13,
        "output_digests_bound": 13,
        "output_digest_mismatch_count_zero": 0,
        "outputs_research_only_non_actionable": True,
        "matrix_verified": True, "walk_forward_results_verified": True,
        "oos_holdout_results_verified": True, "baseline_model_comparison_verified": True,
        "metric_family_results_verified": True, "calibration_stability_report_verified": True,
        "leakage_quality_control_verified": True, "per_ticker_cross_sectional_review_verified": True,
        "operator_summary_verified": True, "feature_label_matrix_row_count_143352": 143352,
        "evaluable_matrix_row_count_142200": 142200, "unavailable_target_count_1152": 1152,
        "walk_forward_fold_count_4": 4, "oos_holdout_year_2025": 2025,
        "oos_evaluated_rows_34848": 34848, "baseline_family_count_4": 4,
        "model_family_count_5": 5, "metric_family_count_10": 10,
        "leakage_control_status_pass": PASS, "leakage_failed_control_count_zero": 0,
        "oos_cross_sectional_delta_bound": "0.00309917", "local_model_delta_bound": "0.00000000",
        "optional_model_unavailability_recorded": [
            "EVALUATED_COMPARISON_REPORT",
            "EVALUATED_RESEARCH_ONLY",
            "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
        ],
        "results_review_created_true": True, "results_review_ready_true": True,
        "ready_for_predictive_usefulness_reassessment_true": True,
        "predictive_usefulness_reassessment_created_false": False,
        "predictive_usefulness_acceptance_candidate_created_false": False,
        "predictive_usefulness_not_accepted": NOT_ACCEPTED, "profitability_not_accepted": NOT_ACCEPTED,
        "runtime_not_authorized": NOT_AUTHORIZED, "strategy_not_authorized": NOT_AUTHORIZED,
        "broker_not_authorized": NOT_AUTHORIZED, "trade_recommendations_false": False,
        "provider_requests_made_false": False, "market_data_acquisition_false": False,
        "dataset_regeneration_false": False, "redesigned_label_regeneration_false": False,
        "feature_regeneration_false": False, "predictive_evidence_rerun_false": False,
        "metric_recomputation_in_review_false": False, "model_training_in_review_false": False,
        "no_predictive_usefulness_acceptance_artifact_created": False,
        "no_profitability_acceptance_created": False, "no_runtime_migration_approval_created": False,
        "limitations_recorded": LIMITATIONS, "next_chain_defined": NEXT_CHAIN,
        "next_gates_defined": NEXT_GATES, "risk_controls_defined": RISK_CONTROLS,
        "no_tracked_marketflow_files": True,
    }
    return [_check(check_id, expected[check_id], actuals[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "results_review_ready": not failed,
        "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence": not failed,
        "predictive_usefulness_reassessment_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("additional_predictive_evidence_results_review_using_redesigned_labels_digest", None)
    payload["output_root"] = SOURCE_OUTPUT_ROOT.as_posix()
    return payload


def additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return a deterministic, output-location-independent review digest."""
    return semantic_digest(_digest_payload(review_package))


def _blocked_package(output_root: Path, reason: str) -> dict[str, Any]:
    package = _base_package(output_root)
    package.update(
        {
            "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS,
            "output_file_inspection_performed": False,
            "outputs_verified": False,
            "outputs_research_only_non_actionable": False,
            "additional_predictive_evidence_results_review_created": False,
            "additional_predictive_evidence_results_review_ready": False,
            "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence": False,
            "blocked_reason": reason,
            "output_digest_manifest": [],
            "output_digest_mismatch_count": None,
            "verified_sections": {},
            "review_checklist": [],
            "review_summary": {
                **_summary([]),
                "results_review_ready": False,
                "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence": False,
            },
        }
    )
    package["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] = (
        additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(package)
    )
    return package


def build_additional_predictive_evidence_results_review_using_redesigned_labels_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Inspect saved outputs and build a fail-closed, research-only review package."""
    root = Path(output_root) if output_root is not None else SOURCE_OUTPUT_ROOT
    try:
        verification = _verify_outputs(root)
    except (AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError, OSError) as exc:
        return _blocked_package(root, str(exc))

    package = _base_package(root)
    package.update(
        {
            "review_status": ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY,
            "output_file_inspection_performed": True,
            "outputs_verified": True,
            "outputs_research_only_non_actionable": True,
            "output_digest_manifest": verification["output_digest_manifest"],
            "output_digest_mismatch_count": verification["output_digest_mismatch_count"],
            "digest_manifest_self_reference_policy": "SELF_REFERENCE_EXPLICIT_NULL_OR_NOT_APPLICABLE",
            "source_digest_manifest_self_reference_policy": verification["self_reference_policy"],
            "verified_sections": verification["verified_sections"],
            "walk_forward_results": verification["walk_forward_results"],
            "oos_method_metrics": verification["oos_metrics"],
            "metric_families": verification["metric_families"],
            "walk_forward_stability": verification["walk_forward_stability"],
            "per_ticker_cross_sectional_review": verification["per_ticker_entries"],
            "optional_model_statuses": verification["optional_model_statuses"],
        }
    )
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["additional_predictive_evidence_results_review_using_redesigned_labels_digest"] = (
        additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(package)
    )
    validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(package)
    return package


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError(f"{field} must be false")


def validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(
    review_package: dict,
) -> dict:
    """Validate source bindings, review facts, and every closed authority boundary."""
    if not isinstance(review_package, dict):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review_package must be an object")
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_USING_REDESIGNED_LABELS_V1,
        "schema_version",
    )
    digest = review_package.get("additional_predictive_evidence_results_review_using_redesigned_labels_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review digest missing")
    if review_package.get("review_status") == ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_USING_REDESIGNED_LABELS_MISSING_OR_INVALID_OUTPUTS:
        _expect_false(review_package.get("output_file_inspection_performed"), "output_file_inspection_performed")
        _expect_false(review_package.get("additional_predictive_evidence_results_review_ready"), "results review ready")
        _expect_false(review_package.get("ready_for_predictive_usefulness_reassessment_using_redesigned_evidence"), "ready for reassessment")
        _expect(digest, additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(review_package), "review digest")
        return {"status": "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_BLOCKED_VALID", "review_status": review_package["review_status"]}

    _expect(
        review_package.get("review_status"),
        ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY,
        "review_status",
    )
    true_fields = (
        "created_offline", "research_only", "operator_review_required",
        "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized",
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels",
        "additional_predictive_evidence_executed", "predictive_evidence_results_created",
        "metric_recomputation_performed", "model_training_performed",
        "additional_predictive_evidence_results_review_created",
        "additional_predictive_evidence_results_review_ready",
        "ready_for_predictive_usefulness_reassessment_using_redesigned_evidence",
        "meta_reduced_record_count_preserved", "output_file_inspection_performed", "outputs_verified",
        "outputs_research_only_non_actionable", "no_tracked_marketflow_files",
    )
    for field in true_fields:
        _expect_true(review_package.get(field), field)
    false_fields = (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_review", "model_training_performed_in_review",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "predictive_usefulness_reassessment_review_created",
        "predictive_usefulness_acceptance_readiness_review_created",
        "predictive_usefulness_acceptance_candidate_created", "predictive_usefulness_acceptance_artifact_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_created", "profitability_acceptance_ready",
        "profitability_acceptance_recommended", "runtime_migration_approval_created",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
    )
    for field in false_fields:
        _expect_false(review_package.get(field), field)
    expected = {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": EVIDENCE_SCOPE,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS,
        "source_execution_status": execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "source_additional_predictive_evidence_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "source_feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "source_additional_predictive_evidence_execution_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE, "target_universe_count": 12,
        "records_digest": EXPECTED_RECORDS_DIGEST, "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "meta_record_count": 913, "generated_output_count": 13,
        "feature_label_matrix_row_count": 143352, "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152, "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025, "oos_evaluated_rows": 34848,
        "baseline_family_count": 4, "model_family_count": 5, "metric_family_count": 10,
        "leakage_control_status": PASS, "leakage_failed_control_count": 0,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS, "next_chain": NEXT_CHAIN, "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS, "output_digest_mismatch_count": 0,
        "oos_cross_sectional_delta_vs_majority": "0.00309917",
        "oos_local_model_delta_vs_majority": "0.00000000",
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    manifest = review_package.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != 13:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("output_digest_manifest mismatch")
    if [row.get("filename") for row in manifest] != EXPECTED_OUTPUT_FILENAMES:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("output digest filenames mismatch")
    if any(row.get("digest_match") is not True for row in manifest):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("output digest mismatch")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list) or [row.get("check_id") for row in checklist] != REQUIRED_CHECK_IDS:
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review checklist mismatch")
    if any(row.get("status") != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review checklist failed")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    _expect(digest, additional_predictive_evidence_results_review_using_redesigned_labels_digest_v1(review_package), "review digest")
    return {
        "status": "ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": digest,
        **{key: review_package["review_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_additional_predictive_evidence_results_review_using_redesigned_labels_markdown_v1(
    review_package: dict,
) -> str:
    """Render the ready review package as sanitized Markdown."""
    validation = validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(review_package)
    sections = [
        ("Title", ["Additional Predictive Evidence Results Review Using Redesigned Labels"]),
        ("Source Execution", [f"Artifact/status: `{review_package['source_execution_artifact_kind']}` / `{review_package['source_execution_status']}`.", f"Execution digest: `{review_package['source_additional_predictive_evidence_execution_digest']}`.", f"Review digest: `{validation['additional_predictive_evidence_results_review_using_redesigned_labels_digest']}`."]),
        ("Dataset and Universe", [f"Dataset: `{review_package['dataset_name']}`; records: `{review_package['total_canonical_record_count']}`.", "Universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + ".", "META remains `913`; each non-META ticker remains `1003`."]),
        ("Source Redesigned Label Profile", [f"Rows/available/unavailable: `{review_package['redesigned_label_row_count']} / {review_package['available_label_value_count']} / {review_package['unavailable_label_value_count']}`."]),
        ("Source Feature Profile", [f"Rows/available/unavailable: `{review_package['feature_value_row_count']} / {review_package['available_feature_value_count']} / {review_package['unavailable_feature_value_count']}`."]),
        ("Feature / Label Matrix Review", [f"Rows/evaluable/unavailable: `{review_package['feature_label_matrix_row_count']} / {review_package['evaluable_matrix_row_count']} / {review_package['unavailable_target_matrix_row_count']}`.", f"Digest: `{review_package['feature_label_matrix_digest']}`."]),
        ("Walk-Forward Review", [f"Four chronological folds verified; fold records: `{len(review_package['walk_forward_results'])}`."]),
        ("OOS Holdout Review", [f"Holdout year/evaluated rows: `{review_package['oos_holdout_year']} / {review_package['oos_evaluated_rows']}`."]),
        ("Baseline and Model Comparison Review", [f"Cross-sectional delta versus majority: `{review_package['oos_cross_sectional_delta_vs_majority']}`.", f"Local-model delta versus majority: `{review_package['oos_local_model_delta_vs_majority']}`."]),
        ("Metric Family Review", [f"Metric families verified: `{review_package['metric_family_count']}`."]),
        ("Calibration and Stability Review", [f"Interpretation: `{review_package['stability_interpretation']}`."]),
        ("Leakage and Quality Control Review", [f"Status/failed controls: `{review_package['leakage_control_status']} / {review_package['leakage_failed_control_count']}`."]),
        ("Per-Ticker / Cross-Sectional Review", [f"Verified ticker entries: `{len(review_package['per_ticker_cross_sectional_review'])}`."]),
        ("Output Digest Manifest", [f"`{row['filename']}`: `{row['local_sha256']}`." for row in review_package["output_digest_manifest"]]),
        ("Review Interpretation", [review_package["baseline_outperformance_interpretation"], review_package["local_model_interpretation"], review_package["predictive_usefulness_interpretation"]]),
        ("Limitations", review_package["limitations"]),
        ("Next Chain", review_package["next_chain"]),
        ("Next Gates", review_package["next_gates"]),
        ("Risk Controls", review_package["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted; reassessment is a separate future gate."]),
        ("Profitability Boundary", ["Profitability was not evaluated and remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{review_package['review_summary']['total_checks']} / {review_package['review_summary']['passed_checks']} / {review_package['review_summary']['failed_checks']} / {review_package['review_summary']['blocker_count']}`."]),
        ("Guardrails", ["No provider, acquisition, regeneration, predictive-evidence rerun, metric recomputation, model training, runtime, or trading action occurred in review."]),
    ]
    lines = ["# Additional Predictive Evidence Results Review Using Redesigned Labels", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_additional_predictive_evidence_results_review_using_redesigned_labels_v1(
    output_dir: str | Path,
    *, output_root: str | Path | None = None,
) -> dict:
    """Write the canonical review JSON without overwriting an existing package."""
    package = build_additional_predictive_evidence_results_review_using_redesigned_labels_v1(
        output_root=output_root
    )
    validation = validate_additional_predictive_evidence_results_review_using_redesigned_labels_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "additional_predictive_evidence_results_review_using_redesigned_labels_v1.json"
    if path.exists():
        raise AdditionalPredictiveEvidenceResultsReviewRedesignedLabelsError("review package output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": validation[
            "additional_predictive_evidence_results_review_using_redesigned_labels_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
