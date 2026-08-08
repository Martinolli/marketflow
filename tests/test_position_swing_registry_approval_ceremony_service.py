from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import position_swing_registry_approval_ceremony_service as approval


def _attestation(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-08T00:00:00Z",
        "operator_attestation_phrase": approval.REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_registry_review_package_digest": approval.EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_registry_candidate_digest": approval.EXPECTED_REGISTRY_CANDIDATE_DIGEST,
        "operator_confirms_registry_key": approval.registry.PROPOSED_REGISTRY_KEY,
        "operator_confirms_position_swing_frozen_digest": approval.registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST,
        "operator_confirms_dataset_rows_digest": approval.registry.EXPECTED_DATASET_ROWS_DIGEST,
        "operator_confirms_dataset_manifest_digest": approval.registry.EXPECTED_DATASET_MANIFEST_DIGEST,
        "operator_confirms_identity_frozen_digest": approval.acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "operator_confirms_calendar_frozen_digest": approval.acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "operator_confirms_schedule_digest": approval.acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "operator_confirms_split_event_frozen_digest": approval.acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_dividend_event_frozen_digest": approval.acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_acquisition_generation_frozen_digest": (
            approval.registry.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST
        ),
        "operator_confirms_swing_frozen_digest": approval.registry.EXPECTED_SWING_CANONICAL_DATASET_FROZEN_DIGEST,
        "operator_confirms_swing_registry_approval_digest": approval.registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_registry_scope_research_dataset": True,
        "operator_confirms_runtime_use_not_authorized": True,
        "operator_confirms_strategy_use_not_authorized": True,
        "operator_confirms_no_strategy_runtime_migration": True,
        "operator_confirms_no_predictive_usefulness": True,
        "operator_confirms_no_profitability_acceptance": True,
    }
    values.update(overrides)
    return approval.build_position_swing_registry_approval_attestation_v1(**values)


def _approved() -> dict:
    return approval.build_position_swing_registry_approved_v1(operator_attestation=_attestation())


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == approval.OPERATOR_DECISION_APPROVE_POSITION_SWING_REGISTRY_ENTRY
    assert attestation["operator_attestation_phrase"] == (
        approval.REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE
    )
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_confirms_registry_review_package_digest"] == (
        approval.EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST
    )
    assert attestation["operator_confirms_registry_candidate_digest"] == approval.EXPECTED_REGISTRY_CANDIDATE_DIGEST
    assert attestation["operator_confirms_registry_key"] == approval.registry.PROPOSED_REGISTRY_KEY


def test_approved_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(
        approval.review.registry.position_freeze.position.acquisition,
        "fetch_massive_custom_bars_v1",
        fail_provider_call,
    )

    artifact = _approved()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_approval"] is False


def test_artifact_kind_is_position_swing_registry_approved():
    assert _approved()["artifact_kind"] == approval.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED


def test_approval_status_is_position_swing_registry_approved():
    assert _approved()["approval_status"] == approval.POSITION_SWING_REGISTRY_APPROVED


def test_position_swing_registry_approval_created_is_true():
    assert _approved()["position_swing_registry_approval_created"] is True


def test_position_swing_registry_eligibility_is_true():
    assert _approved()["position_swing_registry_eligibility"] is True


def test_position_swing_registry_activation_is_true():
    assert _approved()["position_swing_registry_activation"] is True


def test_runtime_use_remains_not_authorized():
    assert _approved()["runtime_use"] == "NOT_AUTHORIZED"


def test_strategy_use_remains_not_authorized():
    assert _approved()["strategy_use"] == "NOT_AUTHORIZED"


def test_strategy_runtime_migration_remains_false():
    assert _approved()["strategy_runtime_migration"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    artifact = _approved()

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_registry_review_package_digest_matches_expected():
    assert _approved()["source_registry_review_package_digest"] == approval.EXPECTED_REGISTRY_REVIEW_PACKAGE_DIGEST


def test_registry_candidate_digest_matches_expected():
    assert _approved()["source_registry_candidate_digest"] == approval.EXPECTED_REGISTRY_CANDIDATE_DIGEST


def test_registry_key_matches_expected():
    artifact = _approved()

    assert artifact["proposed_registry_key"] == approval.registry.PROPOSED_REGISTRY_KEY
    assert artifact["registry_key"] == approval.registry.PROPOSED_REGISTRY_KEY


def test_position_swing_frozen_digest_matches_expected():
    assert (
        _approved()["position_swing_canonical_dataset_frozen_digest"]
        == approval.registry.EXPECTED_POSITION_SWING_FROZEN_DIGEST
    )


def test_dataset_rows_and_manifest_digests_match_expected():
    artifact = _approved()

    assert artifact["dataset_rows_digest"] == approval.registry.EXPECTED_DATASET_ROWS_DIGEST
    assert artifact["dataset_manifest_digest"] == approval.registry.EXPECTED_DATASET_MANIFEST_DIGEST


def test_registry_scope_is_research_dataset():
    assert _approved()["registry_scope"] == "RESEARCH_DATASET"


def test_swing_registry_approval_digest_is_bound():
    assert _approved()["swing_registry_approval_digest"] == approval.registry.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST


def test_approval_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _approved()["approval_checklist"]] == approval.REQUIRED_APPROVAL_CHECK_IDS


def test_all_approval_checks_pass():
    assert {item["status"] for item in _approved()["approval_checklist"]} == {"PASS"}


def test_approval_summary_counts_total_passed_failed_correctly():
    artifact = _approved()
    summary = artifact["approval_summary"]

    assert summary["total_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["passed_checks"] == len(approval.REQUIRED_APPROVAL_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["position_swing_registry_approval_authorized_by_operator"] is True
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_strategy_use_authorized"] is False


def test_operator_attestation_phrase_must_match_exactly():
    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match="operator_attestation_phrase_matches"):
        approval.build_position_swing_registry_approved_v1(
            operator_attestation=_attestation(operator_attestation_phrase="APPROVE POSITION_SWING REGISTRY ENTRY")
        )


def test_wrong_operator_decision_is_rejected():
    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match="operator_decision_approved"):
        approval.build_position_swing_registry_approved_v1(operator_attestation=_attestation(operator_decision="REJECT"))


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_confirms_registry_review_package_digest", "0" * 64, "operator_review_digest_confirmation_matches"),
        ("operator_confirms_registry_candidate_digest", "0" * 64, "operator_candidate_digest_confirmation_matches"),
        ("operator_confirms_registry_key", "AAPL:WRONG", "operator_registry_key_confirmation_matches"),
        (
            "operator_confirms_position_swing_frozen_digest",
            "0" * 64,
            "operator_position_swing_frozen_digest_confirmation_matches",
        ),
        ("operator_confirms_dataset_rows_digest", "0" * 64, "operator_dataset_rows_digest_confirmation_matches"),
        ("operator_confirms_dataset_manifest_digest", "0" * 64, "operator_dataset_manifest_digest_confirmation_matches"),
        ("operator_confirms_registry_scope_research_dataset", False, "operator_registry_scope_confirmation_research_dataset"),
        ("operator_confirms_runtime_use_not_authorized", False, "operator_runtime_use_not_authorized_confirmation"),
        ("operator_confirms_strategy_use_not_authorized", False, "operator_strategy_use_not_authorized_confirmation"),
        ("operator_confirms_no_strategy_runtime_migration", False, "operator_no_strategy_runtime_migration_confirmation"),
        ("operator_confirms_no_predictive_usefulness", False, "operator_no_predictive_usefulness_confirmation"),
        ("operator_confirms_no_profitability_acceptance", False, "operator_no_profitability_acceptance_confirmation"),
        ("operator_confirms_identity_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_calendar_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_schedule_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_split_event_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_dividend_event_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_acquisition_generation_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_swing_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_swing_registry_approval_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
    ],
)
def test_operator_attestation_rejects_bad_confirmations(field: str, value, match: str):
    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match=match):
        approval.build_position_swing_registry_approved_v1(operator_attestation=_attestation(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("approval_status", "WRONG", "approval_status"),
        ("source_registry_review_package_digest", "0" * 64, "source_registry_review_package_digest"),
        ("source_registry_candidate_digest", "0" * 64, "source_registry_candidate_digest"),
        ("registry_key", "AAPL:WRONG", "registry_key"),
        ("position_swing_canonical_dataset_frozen_digest", "0" * 64, "position_swing_canonical_dataset_frozen_digest"),
        ("dataset_rows_digest", "0" * 64, "dataset_rows_digest"),
        ("dataset_manifest_digest", "0" * 64, "dataset_manifest_digest"),
        ("identity_frozen_digest", "0" * 64, "identity_frozen_digest"),
        ("calendar_frozen_digest", "0" * 64, "calendar_frozen_digest"),
        ("schedule_digest", "0" * 64, "schedule_digest"),
        ("split_event_frozen_digest", "0" * 64, "split_event_frozen_digest"),
        ("dividend_event_frozen_digest", "0" * 64, "dividend_event_frozen_digest"),
        ("acquisition_generation_frozen_digest", "0" * 64, "acquisition_generation_frozen_digest"),
        ("swing_canonical_dataset_frozen_digest", "0" * 64, "swing_canonical_dataset_frozen_digest"),
        ("swing_registry_approval_digest", "0" * 64, "swing_registry_approval_digest"),
        ("registry_scope", "RUNTIME_DATASET", "registry_scope"),
        ("position_swing_registry_approval_created", False, "position_swing_registry_approval_created"),
        ("position_swing_registry_eligibility", False, "position_swing_registry_eligibility"),
        ("position_swing_registry_activation", False, "position_swing_registry_activation"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
    ],
)
def test_validator_rejects_invalid_approval_mutations(field: str, value, match: str):
    artifact = _approved()
    artifact[field] = value

    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match=match):
        approval.validate_position_swing_registry_approved_v1(artifact)


def test_validator_rejects_missing_operator_attestation():
    artifact = _approved()
    artifact["operator_attestation"] = None

    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match="operator_attestation"):
        approval.validate_position_swing_registry_approved_v1(artifact)


def test_validator_rejects_mutated_digest_field():
    artifact = _approved()
    artifact["position_swing_registry_approved_semantic_digest"] = "0" * 64

    with pytest.raises(
        approval.PositionSwingRegistryApprovalCeremonyError,
        match="position_swing_registry_approved_semantic_digest",
    ):
        approval.validate_position_swing_registry_approved_v1(artifact)


def test_approved_artifact_digest_is_deterministic():
    first = _approved()
    second = _approved()

    assert (
        first["position_swing_registry_approved_semantic_digest"]
        == second["position_swing_registry_approved_semantic_digest"]
    )
    assert (
        first["position_swing_registry_approved_semantic_digest"]
        == approval.position_swing_registry_approved_semantic_digest_v1(first)
    )


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _approved()["remaining_roadmap"]

    assert roadmap == approval.REMAINING_ROADMAP_AFTER_POSITION_SWING_REGISTRY_APPROVAL
    assert "Normal runtime migration planning." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = approval.build_position_swing_registry_approved_markdown_v1(_approved())

    for section in (
        "## Title",
        "## Approved Registry Entry",
        "## Operator Attestation",
        "## Source Registry Review Package",
        "## Frozen POSITION_SWING Dataset Evidence",
        "## Registry Scope",
        "## Runtime Boundary",
        "## Authority Bindings",
        "## Approval Checklist Summary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Runtime use and strategy use remain `NOT_AUTHORIZED`." in markdown


def test_write_approved_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = approval.write_position_swing_registry_approved_v1(tmp_path, operator_attestation=_attestation())

    assert result["artifact_kind"] == approval.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED
    assert result["payload_sha256"]
    with pytest.raises(approval.PositionSwingRegistryApprovalCeremonyError, match="already exists"):
        approval.write_position_swing_registry_approved_v1(tmp_path, operator_attestation=_attestation())


def test_position_swing_registry_approval_ceremony_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_POSITION_SWING_REGISTRY_APPROVED == "POSITION_SWING_REGISTRY_APPROVED"
    assert services.POSITION_SWING_REGISTRY_APPROVED == "POSITION_SWING_REGISTRY_APPROVED"
    assert (
        services.REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE
        == approval.REQUIRED_POSITION_SWING_REGISTRY_APPROVAL_ATTESTATION_PHRASE
    )
    assert (
        services.build_position_swing_registry_approval_attestation_v1
        is approval.build_position_swing_registry_approval_attestation_v1
    )
    assert services.build_position_swing_registry_approved_v1 is approval.build_position_swing_registry_approved_v1
    assert services.validate_position_swing_registry_approved_v1 is approval.validate_position_swing_registry_approved_v1
    assert services.write_position_swing_registry_approved_v1 is approval.write_position_swing_registry_approved_v1
    assert (
        services.build_position_swing_registry_approved_markdown_v1
        is approval.build_position_swing_registry_approved_markdown_v1
    )
