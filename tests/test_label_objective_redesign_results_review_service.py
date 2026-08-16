from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import label_objective_redesign_execution_service as execution
from marketflow.services import label_objective_redesign_results_review_service as review


FIXED_TIMESTAMP = "2026-08-16T19:03:45Z"


def _verified_source() -> dict:
    return {
        "source_root": execution.DEFAULT_SOURCE_ROOT.as_posix(),
        "required_source_file_count": 9,
        "required_source_files": list(execution.REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "total_record_count_actual": 11946,
        "per_ticker_record_counts_actual": deepcopy(execution.EXPECTED_RECORD_COUNTS),
        "canonical_dataset_generation_digest": execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
    }


def _write_execution_fixture(output_root) -> None:
    reports = execution._build_reports(FIXED_TIMESTAMP)
    report_bytes = {
        filename: canonical_json_bytes(payload) for filename, payload in reports.items()
    }
    report_digests = {
        filename: sha256_bytes(payload) for filename, payload in report_bytes.items()
    }
    digest_manifest = [
        {
            "filename": filename,
            "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
            "sha256": None,
        }
        if filename == execution.OUTPUT_FILENAMES[0]
        else {
            "filename": filename,
            "digest_kind": "FILE_SHA256",
            "sha256": report_digests[filename],
        }
        for filename in execution.OUTPUT_FILENAMES
    ]
    artifact = execution._build_executed_artifact(
        run_timestamp_utc=FIXED_TIMESTAMP,
        source_root=execution.DEFAULT_SOURCE_ROOT,
        output_root=execution.DEFAULT_OUTPUT_ROOT,
        source_verification=_verified_source(),
        output_digest_manifest=digest_manifest,
    )
    assert artifact["label_objective_redesign_execution_digest"] == review.EXPECTED_EXECUTION_DIGEST
    report_bytes[execution.OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    output_root.mkdir(parents=True)
    for filename, payload in report_bytes.items():
        (output_root / filename).write_bytes(payload)


@pytest.fixture(scope="module")
def reviewed(tmp_path_factory):
    output_root = tmp_path_factory.mktemp("label_redesign_review") / "outputs"
    _write_execution_fixture(output_root)
    return review.build_label_objective_redesign_results_review_package_v1(
        output_root=output_root
    ), output_root


def test_review_package_builds_offline(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    output_root = tmp_path / "outputs"
    _write_execution_fixture(output_root)
    package = review.build_label_objective_redesign_results_review_package_v1(
        output_root=output_root
    )
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_blocks_when_output_root_is_missing(tmp_path) -> None:
    package = review.build_label_objective_redesign_results_review_package_v1(
        output_root=tmp_path / "missing"
    )
    assert package["review_status"] == review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["label_objective_redesign_results_review_ready"] is False
    assert package["ready_for_redesigned_label_generation_candidate"] is False
    assert package["blocker_count"] == 8


def test_artifact_kind_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE"


def test_review_status_is_correct(reviewed) -> None:
    package, _ = reviewed
    assert package["review_status"] == "LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_label_objective_redesign_execution_digest", review.EXPECTED_EXECUTION_DIGEST),
        ("source_label_objective_redesign_execution_approval_digest", execution.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("source_label_objective_redesign_execution_candidate_review_package_digest", execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("source_label_objective_redesign_execution_candidate_digest", execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("source_label_objective_redesign_approval_digest", execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_DIGEST),
        ("source_label_objective_redesign_candidate_review_package_digest", execution.EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("source_operator_method_path_selection_digest", execution.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST),
        ("source_research_registry_approval_digest", execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
    ],
)
def test_required_source_digests_are_bound(reviewed, field: str, expected: str) -> None:
    package, _ = reviewed
    assert package[field] == expected


def test_records_digest_is_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["records_digest"] == execution.EXPECTED_RECORDS_DIGEST


def test_universe_count_and_order_are_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["target_universe_count"] == 12
    assert package["target_universe"] == execution.TARGET_UNIVERSE


def test_meta_913_is_preserved(reviewed) -> None:
    package, _ = reviewed
    assert package["meta_record_count"] == 913
    assert package["per_ticker_record_counts"]["META"] == 913
    assert package["meta_reduced_record_count_preserved"] is True


def test_generated_output_count_is_eight(reviewed) -> None:
    package, _ = reviewed
    assert package["generated_output_count"] == 8
    assert package["generated_output_names"] == execution.OUTPUT_FILENAMES


def test_output_digests_are_bound(reviewed) -> None:
    package, _ = reviewed
    assert package["output_digests"] == review.EXPECTED_OUTPUT_DIGESTS
    assert package["non_self_output_digest_match_count"] == 7
    assert package["output_digest_mismatch_count"] == 0
    assert len(package["output_digest_bindings"]) == 8


def test_outputs_are_research_only_non_actionable(reviewed) -> None:
    package, _ = reviewed
    assert package["outputs_research_only_non_actionable"] is True
    assert package["outputs_evidence_scope"] == "LABEL_OBJECTIVE_REDESIGN_RESEARCH_ONLY"
    assert package["digest_manifest_self_reference_policy"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"


@pytest.mark.parametrize(
    "review_field",
    [
        "label_family_candidate_matrix_review",
        "threshold_design_matrix_review",
        "horizon_design_matrix_review",
        "per_ticker_label_objective_plan_review",
        "label_availability_boundary_plan_review",
        "meta_limitation_preservation_plan_review",
    ],
)
def test_each_required_planning_output_is_verified(reviewed, review_field: str) -> None:
    package, _ = reviewed
    assert package[review_field]["available"] is True
    assert package[review_field]["verified"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("candidate_label_family_count", 10),
        ("threshold_design_strategy_count", 7),
        ("horizon_design_candidate_count", 5),
        ("per_ticker_plan_count", 12),
    ],
)
def test_planning_output_counts_are_exact(reviewed, field: str, expected: int) -> None:
    package, _ = reviewed
    assert package[field] == expected


def test_review_created_ready_and_candidate_ready_are_true(reviewed) -> None:
    package, _ = reviewed
    assert package["label_objective_redesign_results_review_created"] is True
    assert package["label_objective_redesign_results_review_ready"] is True
    assert package["ready_for_redesigned_label_generation_candidate"] is True


@pytest.mark.parametrize(
    "field",
    [
        "redesigned_label_generation_candidate_created",
        "label_generation_performed",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_generation_evaluation_and_candidate_boundaries_remain_false(reviewed, field: str) -> None:
    package, _ = reviewed
    assert package[field] is False


def test_predictive_profitability_and_runtime_boundaries_remain_closed(reviewed) -> None:
    package, _ = reviewed
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert package[field] == "NOT_AUTHORIZED"


def test_limitations_are_recorded(reviewed) -> None:
    package, _ = reviewed
    assert package["limitations"] == review.LIMITATIONS


def test_next_chain_and_next_gates_are_defined(reviewed) -> None:
    package, _ = reviewed
    assert package["next_chain"] == review.NEXT_CHAIN
    assert package["next_gates"] == review.NEXT_GATES


def test_risk_controls_are_defined(reviewed) -> None:
    package, _ = reviewed
    assert package["risk_controls"] == review.RISK_CONTROLS


def test_checklist_passes(reviewed) -> None:
    package, _ = reviewed
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in package["review_checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in package["review_checklist"])
    assert package["review_summary"] == {
        "total_checks": 56,
        "passed_checks": 56,
        "failed_checks": 0,
        "blocker_count": 0,
        "results_review_ready": True,
        "ready_for_redesigned_label_generation_candidate": True,
        "redesigned_label_generation_candidate_created": False,
        "actual_labels_generated": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def test_review_digest_is_deterministic_and_output_location_independent(tmp_path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    _write_execution_fixture(first_root)
    _write_execution_fixture(second_root)
    first = review.build_label_objective_redesign_results_review_package_v1(output_root=first_root)
    second = review.build_label_objective_redesign_results_review_package_v1(output_root=second_root)
    assert first["label_objective_redesign_results_review_package_digest"] == second["label_objective_redesign_results_review_package_digest"]


def test_validator_accepts_valid_package(reviewed) -> None:
    package, _ = reviewed
    result = review.validate_label_objective_redesign_results_review_package_v1(package)
    assert result["status"] == review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_VALID


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_label_objective_redesign_execution_digest", "0" * 64),
        ("source_label_objective_redesign_execution_approval_digest", "0" * 64),
        ("target_universe", ["MSFT"]),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 914),
        ("generated_output_count", 7),
        ("candidate_label_family_count", 9),
        ("threshold_design_strategy_count", 6),
        ("horizon_design_candidate_count", 4),
        ("per_ticker_plan_count", 11),
        ("label_objective_redesign_results_review_ready", False),
        ("ready_for_redesigned_label_generation_candidate", False),
        ("redesigned_label_generation_candidate_created", True),
        ("label_generation_performed", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
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
        ("provider_requests_made_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("label_objective_redesign_execution_rerun_performed", True),
    ],
)
def test_validator_rejects_guardrail_mutations(reviewed, field: str, bad_value) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed[field] = bad_value
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewError):
        review.validate_label_objective_redesign_results_review_package_v1(changed)


@pytest.mark.parametrize("field", ["limitations", "next_chain", "risk_controls"])
def test_validator_rejects_missing_governance_lists(reviewed, field: str) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop(field)
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewError):
        review.validate_label_objective_redesign_results_review_package_v1(changed)


def test_validator_rejects_missing_review_digest(reviewed) -> None:
    package, _ = reviewed
    changed = deepcopy(package)
    changed.pop("label_objective_redesign_results_review_package_digest")
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewError):
        review.validate_label_objective_redesign_results_review_package_v1(changed)


def test_markdown_includes_required_sections(reviewed) -> None:
    package, _ = reviewed
    markdown = review.build_label_objective_redesign_results_review_markdown_v1(package)
    for heading in (
        "## Title",
        "## Label Objective Redesign Results Review",
        "## Source Execution",
        "## Dataset and Universe",
        "## Generated Planning Outputs",
        "## Label Family Candidate Matrix Review",
        "## Threshold Design Matrix Review",
        "## Horizon Design Matrix Review",
        "## Per-Ticker Label Objective Plan Review",
        "## Label Availability Boundary Plan Review",
        "## META Limitation Preservation Review",
        "## Limitations",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_writer_writes_canonical_package_once(reviewed, tmp_path) -> None:
    package, output_root = reviewed
    result = review.write_label_objective_redesign_results_review_package_v1(
        tmp_path, output_root=output_root
    )
    written = json.loads((tmp_path / result["filename"]).read_text(encoding="utf-8"))
    assert written == package
    with pytest.raises(review.LabelObjectiveRedesignResultsReviewError):
        review.write_label_objective_redesign_results_review_package_v1(
            tmp_path, output_root=output_root
        )


def test_service_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE == review.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE
    assert services.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY == review.LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_READY
    assert services.build_label_objective_redesign_results_review_package_v1 is review.build_label_objective_redesign_results_review_package_v1
    assert services.validate_label_objective_redesign_results_review_package_v1 is review.validate_label_objective_redesign_results_review_package_v1
    assert services.write_label_objective_redesign_results_review_package_v1 is review.write_label_objective_redesign_results_review_package_v1
    assert services.build_label_objective_redesign_results_review_markdown_v1 is review.build_label_objective_redesign_results_review_markdown_v1
