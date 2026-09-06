from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_service
    as source,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_service
    as review,
)


def _build() -> dict:
    return review.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1()


def _validate(value: dict) -> dict:
    return review.validate_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(value)


def _assert_rejected(value: dict) -> None:
    with pytest.raises(review.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError):
        _validate(value)


def test_builds_offline_without_calling_source_candidate_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("source candidate builder must not be called")

    monkeypatch.setattr(
        source,
        "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1",
        forbidden,
    )
    artifact = _build()
    assert artifact["created_offline"] is True
    assert artifact["operator_review_only"] is True


def test_artifact_identity_and_review_philosophy_are_exact() -> None:
    artifact = _build()
    assert artifact["artifact_kind"] == review.ARTIFACT_KIND
    assert artifact["operator_review_status"] == review.OPERATOR_REVIEW_STATUS
    assert artifact["operator_review_scope"] == review.OPERATOR_REVIEW_SCOPE
    assert artifact["review_status"] == "REVIEWED_CANDIDATE_ONLY"
    assert "must not select" in artifact["operator_review_philosophy"]
    assert "must not create or supply" in artifact["operator_review_boundary"]


@pytest.mark.parametrize("key, expected", tuple(review.SOURCE_CANDIDATE_BINDINGS.items()))
def test_source_candidate_identity_and_digests_are_bound(key: str, expected: object) -> None:
    assert _build()[key] == expected


@pytest.mark.parametrize(
    "key, expected",
    tuple(review.SOURCE_FAILURE_BINDINGS.items()) + tuple(source.SOURCE_BINDINGS.items()),
)
def test_source_failure_completion_and_historical_chains_are_bound(key: str, expected: object) -> None:
    assert _build()[key] == expected


def test_source_failure_classes_and_blocked_execution_are_preserved() -> None:
    artifact = _build()
    assert artifact["primary_failure_class"] == "NO_OPERATOR_SOURCE_AUTHORITY_EVIDENCE_PACKAGE_COMPLETION_INPUTS_PROVIDED"
    assert artifact["secondary_failure_classes"] == list(source.SECONDARY_FAILURE_CLASSES)
    assert artifact["source_completion_execution_blocked_reason"] == artifact["primary_failure_class"]
    assert artifact["source_completion_execution_success_digests_absent"] is True
    assert artifact["source_durable_receipt_path"].endswith("RECEIPT_V1.json")
    assert artifact["durable_receipt_not_parsed"] is True


@pytest.mark.parametrize("key, expected", tuple(source.SOURCE_CONTEXT.items()))
def test_retry_priority1_and_diagnostic_context_is_bound(key: str, expected: object) -> None:
    assert _build()[key] == expected


def test_priority1_families_workstreams_and_template_are_reviewed_only() -> None:
    artifact = _build()
    assert sum(item["failed_or_errored_nodeid_count"] for item in artifact["priority_1_target_modules"]) == 612
    assert len(artifact["reviewed_observable_failure_families"]) == 4
    assert sum(item["observable_evidence_count"] for item in artifact["reviewed_observable_failure_families"]) == 188
    assert {item["confidence"] for item in artifact["reviewed_observable_failure_families"]} == {"HIGH"}
    assert len(artifact["reviewed_workstreams"]) == 4
    assert artifact["reviewed_template_structure"]["template_only"] is True
    assert artifact["reviewed_template_structure"]["actual_evidence_package_created"] is False
    assert len(artifact["missing_authority_mapping"]) == 30
    assert {item["current_status"] for item in artifact["missing_authority_mapping"]} == {"MISSING_NOT_ACQUIRED"}


@pytest.mark.parametrize("key, expected", tuple(review.COUNTS.items()))
def test_required_counts_and_count_label_distinctions_are_preserved(key: str, expected: object) -> None:
    assert _build()[key] == expected


@pytest.mark.parametrize("field", review.TRUE_FIELDS)
def test_review_only_positive_boundary_fields_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", review.FALSE_FIELDS)
def test_selection_execution_authority_and_action_fields_are_false(field: str) -> None:
    assert _build()[field] is False


@pytest.mark.parametrize("index", range(12))
def test_exact_package_options_are_reviewed_and_never_selected(index: int) -> None:
    item = _build()["package_options"][index]
    expected = review.PACKAGE_OPTIONS[index]
    assert item["package_id"] == expected[0]
    assert item["source_status"] == expected[1]
    assert item["operator_review_status"] == expected[2]
    assert item["selected"] is False
    assert item["approved"] is False
    assert item["authorized"] is False
    assert item["executed"] is False


def test_recommended_and_blocked_package_dispositions_are_exact() -> None:
    artifact = _build()
    assert artifact["recommended_operator_completion_inputs_preparation_or_supply_package"] == review.RECOMMENDED_PACKAGE
    assert artifact["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert sum(item["source_status"] != "BLOCKED_NOT_ALLOWED" for item in artifact["package_options"]) == 7
    assert sum(item["operator_review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in artifact["package_options"]) == 5


@pytest.mark.parametrize("requirement_id", review.FUTURE_INPUT_REQUIREMENT_IDS)
def test_all_future_input_requirements_are_reviewed_not_executed(requirement_id: str) -> None:
    items = {item["requirement_id"]: item for item in _build()["future_input_preparation_requirements"]}
    assert items[requirement_id]["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_EXECUTION"
    assert items[requirement_id]["execution_status"] == "NOT_EXECUTED"


def test_future_input_supply_contract_is_reviewed_planning_only_and_non_secret() -> None:
    contract = _build()["future_input_supply_contract"]
    assert contract["contract_status"] == "REVIEWED_PLANNING_ONLY_NOT_EXECUTED"
    assert len(contract["evidence_items"]) == 30
    assert len({item["mapped_missing_authority_id"] for item in contract["evidence_items"]}) == 30
    for declaration in (
        "package_declares_no_secrets", "package_declares_no_api_keys",
        "package_declares_no_broker_credentials", "package_declares_no_personal_financial_credentials",
        "package_declares_no_market_data_credentials", "package_declares_no_private_tokens",
        "package_distinguishes_specification_from_observation",
        "package_distinguishes_expected_from_actual",
        "package_distinguishes_source_authority_from_diagnostic_output",
    ):
        assert contract["package_header"][declaration] is True
    assert contract["operator_review_inspects_secrets"] is False


@pytest.mark.parametrize("index", range(17))
def test_all_future_plan_steps_are_reviewed_not_executed(index: int) -> None:
    item = _build()["future_plan"][index]
    assert item["step"] == index + 1
    assert item["action"] == review.FUTURE_PLAN_STEPS[index]
    assert item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED"


@pytest.mark.parametrize("output_id", review.PLANNED_OUTPUT_IDS)
def test_all_candidate_planned_outputs_are_reviewed_not_generated(output_id: str) -> None:
    items = {item["output_id"]: item for item in _build()["planned_outputs"]}
    assert items[output_id]["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED"
    assert items[output_id]["generation_status"] == "NOT_GENERATED"


@pytest.mark.parametrize("non_goal", review.NON_GOALS)
def test_all_source_non_goals_are_reviewed_and_active(non_goal: str) -> None:
    items = {item["non_goal_id"]: item for item in _build()["non_goals"]}
    assert items[non_goal]["review_status"] == "REVIEWED_ACTIVE"
    assert items[non_goal]["active"] is True


@pytest.mark.parametrize("output_id", review.OUTPUT_IDS)
def test_all_required_review_outputs_are_generated(output_id: str) -> None:
    items = {item["output_id"]: item for item in _build()["outputs"]}
    assert items[output_id]["status"] == "GENERATED_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_ONLY"


@pytest.mark.parametrize("risk_control", review.RISK_CONTROLS)
def test_all_review_risk_controls_are_defined(risk_control: str) -> None:
    assert risk_control in _build()["risk_controls"]


@pytest.mark.parametrize("gate", review.NEXT_GATES)
def test_all_next_gates_are_defined_without_authority(gate: str) -> None:
    artifact = _build()
    assert gate in artifact["next_gates"]
    assert artifact["ready_for_operator_completion_inputs_preparation_or_supply_approval_if_selected"] is True
    assert artifact["ready_for_operator_completion_inputs_preparation_or_supply_execution"] is False


def test_recommendation_and_next_chain_are_review_only() -> None:
    artifact = _build()
    assert artifact["recommended_next_task"].endswith("_V1_IF_SELECTED")
    assert artifact["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert artifact["recommended_action"] == "OPTIONAL_OPERATOR_SELECTION_AND_SEPARATE_APPROVAL_REQUIRED_BEFORE_ANY_INPUT_PREPARATION_OR_SUPPLY_EXECUTION"
    assert len(artifact["next_chain"]) == 13
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_use"] == "NOT_AUTHORIZED"
    assert artifact["broker_execution"] == "NOT_AUTHORIZED"


@pytest.mark.parametrize(
    "digest_key",
    (
        review.OPERATOR_REVIEW_DIGEST_KEY,
        review.PACKAGE_OPTIONS_REVIEW_DIGEST_KEY,
        review.INPUT_CONTRACT_REVIEW_DIGEST_KEY,
        review.SOURCE_BINDING_REVIEW_DIGEST_KEY,
        review.COVERAGE_REVIEW_DIGEST_KEY,
        review.MANIFEST_DIGEST_KEY,
    ),
)
def test_digests_are_deterministic_lowercase_sha256(digest_key: str) -> None:
    first = _build()[digest_key]
    second = _build()[digest_key]
    assert first == second
    assert len(first) == 64
    assert set(first) <= set("0123456789abcdef")


def test_validator_accepts_valid_review_and_reports_clean_checklist() -> None:
    result = _validate(_build())
    assert result["artifact_kind"] == review.ARTIFACT_KIND
    assert result["operator_review_status"] == review.OPERATOR_REVIEW_STATUS
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize("field", review.TRUE_FIELDS)
def test_validator_rejects_any_required_true_boundary_changed(field: str) -> None:
    artifact = _build()
    artifact[field] = False
    _assert_rejected(artifact)


@pytest.mark.parametrize("field", review.FALSE_FIELDS)
def test_validator_rejects_any_closed_boundary_changed(field: str) -> None:
    artifact = _build()
    artifact[field] = True
    _assert_rejected(artifact)


@pytest.mark.parametrize("key", tuple(review.SOURCE_CANDIDATE_BINDINGS))
def test_validator_rejects_source_candidate_identity_or_digest_drift(key: str) -> None:
    artifact = _build()
    artifact[key] = "changed"
    _assert_rejected(artifact)


@pytest.mark.parametrize(
    "key",
    tuple(dict.fromkeys((*review.SOURCE_FAILURE_BINDINGS, *source.SOURCE_BINDINGS))),
)
def test_validator_rejects_source_chain_drift(key: str) -> None:
    artifact = _build()
    artifact[key] = "changed" if not isinstance(artifact[key], bool) else not artifact[key]
    _assert_rejected(artifact)


@pytest.mark.parametrize("field", ("artifact_kind", "operator_review_status", "operator_review_scope"))
def test_validator_rejects_wrong_identity(field: str) -> None:
    artifact = _build()
    artifact[field] = "WRONG"
    _assert_rejected(artifact)


@pytest.mark.parametrize(
    "collection",
    (
        "package_options", "future_input_preparation_requirements", "future_plan",
        "planned_outputs", "non_goals", "outputs", "next_chain", "next_gates", "risk_controls",
    ),
)
def test_validator_rejects_missing_review_content(collection: str) -> None:
    artifact = _build()
    artifact[collection].pop()
    _assert_rejected(artifact)


def test_validator_rejects_changed_coverage_or_missing_authority_status() -> None:
    artifact = _build()
    artifact["actual_coverage"]["actual_covered_missing_authority_item_count"] = 1
    _assert_rejected(artifact)
    artifact = _build()
    artifact["missing_authority_mapping"][0]["current_status"] = "ACQUIRED"
    _assert_rejected(artifact)


def test_injected_source_candidate_is_digest_bound() -> None:
    injected = deepcopy(review.SOURCE_CANDIDATE_BINDINGS)
    assert _build() == review.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(source_candidate=injected)
    injected["source_candidate_digest"] = "0" * 64
    with pytest.raises(review.MarketFlowRepositoryIntegrationBranchRetryFailureOperatorCompletionInputsPreparationOrSupplyCandidateOperatorReviewError):
        review.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(source_candidate=injected)


def test_markdown_contains_every_required_section() -> None:
    markdown = review.build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_markdown_v1(_build())
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Operator Completion Inputs")
    for section in review.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown
    assert review.RECOMMENDED_PACKAGE in markdown
    assert "0/30" in markdown
    assert "MISSING_NOT_ACQUIRED" in markdown


def test_writer_uses_only_requested_output_file(tmp_path: Path) -> None:
    artifact = review.write_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_operator_review_after_blocked_completion_execution_v1(tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name == "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OPERATOR_COMPLETION_INPUTS_PREPARATION_OR_SUPPLY_CANDIDATE_OPERATOR_REVIEW_AFTER_BLOCKED_COMPLETION_EXECUTION_STATUS.md"
    assert artifact["operator_review_status"] == review.OPERATOR_REVIEW_STATUS


def test_service_source_has_no_forbidden_runtime_or_upstream_builder_calls() -> None:
    text = Path(review.__file__).read_text(encoding="utf-8")
    forbidden = (
        "subprocess.", "requests.", "httpx.", "os.environ", "dotenv", "pytest.main",
        "build_marketflow_repository_integration_branch_retry_failure_operator_completion_inputs_preparation_or_supply_candidate_after_blocked_completion_execution_v1(",
    )
    for marker in forbidden:
        if marker.startswith("build_marketflow"):
            assert f"source.{marker}" not in text
        else:
            assert marker not in text
