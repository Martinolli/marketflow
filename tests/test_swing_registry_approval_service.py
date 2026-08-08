from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import swing_registry_approval_service as registry


def _candidate() -> dict:
    return registry.build_swing_registry_approval_candidate_v1()


def _recompute(candidate: dict) -> None:
    candidate["registry_candidate_checklist"] = registry._build_checklist(candidate)
    candidate["registry_candidate_summary"] = registry._summary(candidate["registry_candidate_checklist"])
    candidate["swing_registry_approval_candidate_semantic_digest"] = (
        registry.swing_registry_approval_candidate_semantic_digest_v1(candidate)
    )


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(registry.swing_freeze.swing.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    candidate = _candidate()

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False
    assert candidate["binding_mode"] == registry.SWING_FROZEN_STATUS_BINDING


def test_artifact_kind_is_swing_registry_approval_candidate():
    assert _candidate()["artifact_kind"] == registry.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE


def test_candidate_status_is_ready_for_operator_review():
    assert _candidate()["candidate_status"] == registry.SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW


def test_swing_frozen_digest_matches_expected():
    assert _candidate()["swing_canonical_dataset_frozen_digest"] == registry.EXPECTED_SWING_FROZEN_DIGEST


def test_dataset_rows_digest_matches_expected():
    assert _candidate()["dataset_rows_digest"] == registry.EXPECTED_DATASET_ROWS_DIGEST


def test_dataset_manifest_digest_matches_expected():
    assert _candidate()["dataset_manifest_digest"] == registry.EXPECTED_DATASET_MANIFEST_DIGEST


def test_proposed_registry_key_is_deterministic():
    assert _candidate()["proposed_registry_key"] == registry.PROPOSED_REGISTRY_KEY


def test_registry_scope_is_research_dataset():
    assert _candidate()["proposed_registry_scope"] == "RESEARCH_DATASET"


def test_runtime_use_is_not_authorized():
    assert _candidate()["proposed_runtime_use"] == "NOT_AUTHORIZED"


def test_strategy_use_is_not_authorized():
    assert _candidate()["proposed_strategy_use"] == "NOT_AUTHORIZED"


def test_registry_activation_is_false():
    assert _candidate()["proposed_registry_activation"] is False


def test_registry_approval_created_is_false():
    assert _candidate()["registry_approval_created"] is False


def test_canonical_eligibility_remains_false():
    assert _candidate()["canonical_eligibility"] is False


def test_registry_eligibility_remains_false():
    assert _candidate()["registry_eligibility"] is False


def test_runtime_migration_remains_false():
    assert _candidate()["strategy_runtime_migration"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    candidate = _candidate()

    assert candidate["predictive_usefulness"] == "not accepted"
    assert candidate["profitability"] == "not accepted"


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _candidate()["registry_candidate_checklist"]] == registry.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_swing_frozen_dataset():
    assert {item["status"] for item in _candidate()["registry_candidate_checklist"]} == {"PASS"}


def test_summary_counts_total_passed_failed_correctly():
    summary = _candidate()["registry_candidate_summary"]

    assert summary["total_checks"] == len(registry.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(registry.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_registry_review"] is True
    assert summary["software_registry_approval"] is False
    assert summary["runtime_migration_authorized"] is False


def test_candidate_digest_is_deterministic():
    first = _candidate()
    second = _candidate()

    assert first["swing_registry_approval_candidate_semantic_digest"] == second["swing_registry_approval_candidate_semantic_digest"]
    assert first["swing_registry_approval_candidate_semantic_digest"] == registry.swing_registry_approval_candidate_semantic_digest_v1(first)


def test_validator_accepts_valid_candidate():
    validation = registry.validate_swing_registry_approval_candidate_v1(_candidate())

    assert validation["status"] == "SWING_REGISTRY_APPROVAL_CANDIDATE_VALID"
    assert validation["ready_for_operator_registry_review"] is True


@pytest.mark.parametrize(
    ("path", "value", "match"),
    [
        (("artifact_kind",), "WRONG", "artifact_kind"),
        (("candidate_status",), "WRONG", "candidate_status"),
        (("swing_canonical_dataset_frozen_digest",), "0" * 64, "swing_canonical_dataset_frozen_digest"),
        (("dataset_rows_digest",), "0" * 64, "dataset_rows_digest"),
        (("dataset_manifest_digest",), "0" * 64, "dataset_manifest_digest"),
        (("identity_frozen_digest",), "0" * 64, "identity_frozen_digest"),
        (("calendar_frozen_digest",), "0" * 64, "calendar_frozen_digest"),
        (("schedule_digest",), "0" * 64, "schedule_digest"),
        (("split_event_frozen_digest",), "0" * 64, "split_event_frozen_digest"),
        (("dividend_event_frozen_digest",), "0" * 64, "dividend_event_frozen_digest"),
        (("acquisition_generation_frozen_digest",), "0" * 64, "acquisition_generation_frozen_digest"),
        (("swing_bar_count",), 1987, "swing_bar_count"),
        (("cross_check_2025_01_status",), "FAILED", "cross_check_2025_01_status"),
        (("special_session_policy",), "INCLUDE_SPECIAL_SESSIONS", "special_session_policy"),
        (("in_range_dividend_implication",), None, "in_range_dividend_implication"),
        (("registry_eligibility",), True, "registry_eligibility"),
        (("canonical_eligibility",), True, "canonical_eligibility"),
        (("strategy_runtime_migration",), True, "strategy_runtime_migration"),
        (("proposed_runtime_use",), "AUTHORIZED", "proposed_runtime_use"),
        (("proposed_strategy_use",), "AUTHORIZED", "proposed_strategy_use"),
        (("proposed_registry_activation",), True, "proposed_registry_activation"),
        (("predictive_usefulness",), "accepted", "predictive_usefulness"),
        (("profitability",), "accepted", "profitability"),
        (("provider_requests_made",), True, "provider_requests_made"),
    ],
)
def test_validator_rejects_invalid_mutations(path: tuple[str, ...], value, match: str):
    candidate = _candidate()
    cursor = candidate
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    _recompute(candidate)

    with pytest.raises(registry.SwingRegistryApprovalError, match=match):
        registry.validate_swing_registry_approval_candidate_v1(candidate)


def test_validator_rejects_runtime_use_authorized():
    candidate = _candidate()
    candidate["proposed_runtime_use"] = "AUTHORIZED"
    _recompute(candidate)

    with pytest.raises(registry.SwingRegistryApprovalError, match="proposed_runtime_use"):
        registry.validate_swing_registry_approval_candidate_v1(candidate)


def test_validator_rejects_strategy_use_authorized():
    candidate = _candidate()
    candidate["proposed_strategy_use"] = "AUTHORIZED"
    _recompute(candidate)

    with pytest.raises(registry.SwingRegistryApprovalError, match="proposed_strategy_use"):
        registry.validate_swing_registry_approval_candidate_v1(candidate)


def test_validator_rejects_registry_activation_true():
    candidate = _candidate()
    candidate["proposed_registry_activation"] = True
    _recompute(candidate)

    with pytest.raises(registry.SwingRegistryApprovalError, match="proposed_registry_activation"):
        registry.validate_swing_registry_approval_candidate_v1(candidate)


def test_candidate_can_bind_to_supplied_frozen_artifact():
    attestation = registry.swing_freeze.build_swing_canonical_dataset_operator_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-08T00:00:00Z",
        operator_attestation_phrase=registry.swing_freeze.REQUIRED_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE,
        operator_confirms_swing_review_package_digest=registry.swing_freeze.EXPECTED_SWING_REVIEW_PACKAGE_DIGEST,
        operator_confirms_swing_candidate_digest=registry.swing_freeze.EXPECTED_SWING_CANDIDATE_DIGEST,
        operator_confirms_dataset_rows_digest=registry.swing_freeze.EXPECTED_DATASET_ROWS_DIGEST,
        operator_confirms_dataset_manifest_digest=registry.swing_freeze.EXPECTED_DATASET_MANIFEST_DIGEST,
        operator_confirms_source_rows_digest=registry.swing_freeze.EXPECTED_SOURCE_ROWS_DIGEST,
        operator_confirms_materialization_receipt_digest=registry.swing_freeze.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        operator_confirms_acquisition_generation_frozen_digest=registry.swing_freeze.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        operator_confirms_identity_frozen_digest=registry.acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        operator_confirms_calendar_frozen_digest=registry.acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        operator_confirms_schedule_digest=registry.acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        operator_confirms_split_event_frozen_digest=registry.acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        operator_confirms_dividend_event_frozen_digest=registry.acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        operator_confirms_swing_bar_count=1988,
        operator_confirms_2025_01_cross_check_passed=True,
        operator_confirms_special_session_policy=True,
        operator_confirms_dividend_implication=True,
    )
    frozen = registry.swing_freeze.build_swing_canonical_dataset_frozen_v1(operator_attestation=attestation)

    candidate = registry.build_swing_registry_approval_candidate_v1(swing_frozen_artifact=frozen)

    assert candidate["binding_mode"] == registry.SWING_FROZEN_ARTIFACT_BINDING
    assert candidate["swing_canonical_dataset_frozen_digest"] == registry.EXPECTED_SWING_FROZEN_DIGEST


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = registry.build_swing_registry_approval_candidate_markdown_v1(_candidate())

    for heading in (
        "## Title",
        "## Proposed Registry Entry",
        "## Frozen SWING Dataset Evidence",
        "## Dataset Summary",
        "## 2025-01 Cross-Check",
        "## Special-Session Policy",
        "## Authority Bindings",
        "## Dividend Implication",
        "## Registry Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert heading in markdown
    assert "No SWING registry approval, registry eligibility, or runtime migration occurred." in markdown


def test_write_candidate_writes_json_without_overwrite(tmp_path: Path):
    result = registry.write_swing_registry_approval_candidate_v1(tmp_path)

    assert result["artifact_kind"] == registry.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE
    assert result["payload_sha256"]
    with pytest.raises(registry.SwingRegistryApprovalError, match="already exists"):
        registry.write_swing_registry_approval_candidate_v1(tmp_path)


def test_registry_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE == "SWING_REGISTRY_APPROVAL_CANDIDATE"
    assert services.SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW == "SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW"
    assert services.build_swing_registry_approval_candidate_v1 is registry.build_swing_registry_approval_candidate_v1
    assert services.validate_swing_registry_approval_candidate_v1 is registry.validate_swing_registry_approval_candidate_v1
    assert services.write_swing_registry_approval_candidate_v1 is registry.write_swing_registry_approval_candidate_v1
    assert services.build_swing_registry_approval_candidate_markdown_v1 is registry.build_swing_registry_approval_candidate_markdown_v1
