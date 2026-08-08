from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import position_swing_canonical_dataset_operator_freeze_service as freeze


def _attestation(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-08T00:00:00Z",
        "operator_attestation_phrase": freeze.REQUIRED_POSITION_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_position_swing_review_package_digest": freeze.EXPECTED_POSITION_SWING_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_position_swing_candidate_digest": freeze.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST,
        "operator_confirms_dataset_rows_digest": freeze.EXPECTED_DATASET_ROWS_DIGEST,
        "operator_confirms_dataset_manifest_digest": freeze.EXPECTED_DATASET_MANIFEST_DIGEST,
        "operator_confirms_source_rows_digest": freeze.EXPECTED_SOURCE_ROWS_DIGEST,
        "operator_confirms_materialization_receipt_digest": freeze.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        "operator_confirms_acquisition_generation_frozen_digest": freeze.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST,
        "operator_confirms_identity_frozen_digest": freeze.acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "operator_confirms_calendar_frozen_digest": freeze.acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "operator_confirms_schedule_digest": freeze.acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "operator_confirms_split_event_frozen_digest": freeze.acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_dividend_event_frozen_digest": freeze.acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_position_swing_bar_count": 994,
        "operator_confirms_2025_01_cross_check_passed": True,
        "operator_confirms_special_session_policy": True,
        "operator_confirms_dividend_implication": True,
    }
    values.update(overrides)
    return freeze.build_position_swing_canonical_dataset_operator_attestation_v1(**values)


def _frozen(**attestation_overrides) -> dict:
    return freeze.build_position_swing_canonical_dataset_frozen_v1(
        operator_attestation=_attestation(**attestation_overrides)
    )


def _recompute(artifact: dict) -> None:
    artifact["freeze_checklist"] = freeze._freeze_checklist(artifact)
    artifact["freeze_summary"] = freeze._summary(artifact["freeze_checklist"])
    artifact["position_swing_canonical_dataset_frozen_semantic_digest"] = (
        freeze.position_swing_canonical_dataset_frozen_semantic_digest_v1(artifact)
    )


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == "APPROVE_POSITION_SWING_CANONICAL_DATASET_FREEZE"
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert (
        attestation["operator_attestation_phrase"]
        == freeze.REQUIRED_POSITION_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE
    )
    assert attestation["operator_confirms_position_swing_review_package_digest"] == (
        freeze.EXPECTED_POSITION_SWING_REVIEW_PACKAGE_DIGEST
    )
    assert attestation["operator_confirms_no_provider_requests_in_freeze"] is True
    assert attestation["operator_confirms_no_registry_approval"] is True


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(freeze.position.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    artifact = _frozen()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_freeze"] is False


def test_artifact_kind_is_position_swing_canonical_dataset_frozen():
    assert _frozen()["artifact_kind"] == "POSITION_SWING_CANONICAL_DATASET_FROZEN"


def test_freeze_status_is_position_swing_canonical_dataset_frozen():
    assert _frozen()["freeze_status"] == "POSITION_SWING_CANONICAL_DATASET_FROZEN"


def test_position_swing_canonical_dataset_frozen_is_true():
    assert _frozen()["position_swing_canonical_dataset_frozen"] is True


def test_position_swing_registry_approval_created_remains_false():
    assert _frozen()["position_swing_registry_approval_created"] is False


def test_position_swing_registry_eligibility_remains_false():
    assert _frozen()["position_swing_registry_eligibility"] is False


def test_registry_eligibility_remains_false():
    assert _frozen()["registry_eligibility"] is False


def test_runtime_use_remains_not_authorized():
    assert _frozen()["runtime_use"] == freeze.position.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _frozen()["strategy_use"] == freeze.position.NOT_AUTHORIZED


def test_strategy_runtime_migration_remains_false():
    assert _frozen()["strategy_runtime_migration"] is False


def test_position_swing_review_package_digest_matches_expected():
    assert (
        _frozen()["source_position_swing_review_package_semantic_digest"]
        == freeze.EXPECTED_POSITION_SWING_REVIEW_PACKAGE_DIGEST
    )


def test_position_swing_candidate_digest_matches_expected():
    assert _frozen()["source_position_swing_candidate_digest"] == freeze.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST


def test_dataset_rows_digest_matches_expected():
    assert _frozen()["source_dataset_rows_digest"] == freeze.EXPECTED_DATASET_ROWS_DIGEST


def test_dataset_manifest_digest_matches_expected():
    assert _frozen()["source_dataset_manifest_digest"] == freeze.EXPECTED_DATASET_MANIFEST_DIGEST


def test_source_rows_and_materialization_digest_match_expected():
    artifact = _frozen()

    assert artifact["source_normalized_rows_digest"] == freeze.EXPECTED_SOURCE_ROWS_DIGEST
    assert artifact["source_materialization_receipt_digest"] == freeze.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST


def test_authority_digests_match_expected():
    bindings = _frozen()["authority_bindings"]

    assert bindings["identity_frozen_digest"] == freeze.acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST
    assert bindings["calendar_frozen_digest"] == freeze.acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST
    assert bindings["schedule_digest"] == freeze.acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST
    assert bindings["split_event_frozen_digest"] == freeze.acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST
    assert bindings["dividend_event_frozen_digest"] == freeze.acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST
    assert bindings["acquisition_generation_frozen_digest"] == freeze.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST


def test_position_swing_bar_count_is_994():
    assert _frozen()["position_swing_bar_count"] == 994


def test_2025_01_cross_check_passed_and_has_20_bars():
    artifact = _frozen()

    assert artifact["cross_check_2025_01_status"] == "PASSED"
    assert artifact["cross_check_2025_01_position_swing_bars"] == 20


def test_special_session_policy_is_preserved():
    artifact = _frozen()

    assert artifact["special_session_policy"] == "FULL_ORDINARY_SESSIONS_ONLY"
    assert artifact["special_sessions_excluded"] == 9
    assert artifact["special_session_rows_excluded"] == 126


def test_dividend_implication_is_preserved():
    artifact = _frozen()

    assert artifact["in_range_dividends_found"] is True
    assert artifact["in_range_dividend_count"] == 16
    assert artifact["in_range_dividend_implication"] == "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"
    assert artifact["source_adjusted_data_used"] is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_attestation_phrase", "wrong", "operator_attestation_phrase_matches"),
        ("operator_decision", "REJECT", "operator_decision_approved"),
        ("operator_confirms_position_swing_review_package_digest", "0" * 64, "operator_review_digest_confirmation_matches"),
        ("operator_confirms_position_swing_candidate_digest", "0" * 64, "operator_candidate_digest_confirmation_matches"),
        ("operator_confirms_dataset_rows_digest", "0" * 64, "operator_dataset_rows_digest_confirmation_matches"),
        ("operator_confirms_dataset_manifest_digest", "0" * 64, "operator_dataset_manifest_digest_confirmation_matches"),
        ("operator_confirms_source_rows_digest", "0" * 64, "operator_source_rows_digest_confirmation_matches"),
        ("operator_confirms_materialization_receipt_digest", "0" * 64, "operator_materialization_receipt_confirmation_matches"),
        ("operator_confirms_acquisition_generation_frozen_digest", "0" * 64, "operator_acquisition_digest_confirmation_matches"),
        ("operator_confirms_identity_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_calendar_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_schedule_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_split_event_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_dividend_event_frozen_digest", "0" * 64, "operator_authority_digest_confirmations_match"),
        ("operator_confirms_position_swing_bar_count", 993, "operator_confirms_position_swing_bar_count"),
        ("operator_confirms_2025_01_cross_check_passed", False, "operator_confirms_2025_01_cross_check"),
        ("operator_confirms_special_session_policy", False, "operator_confirms_special_session_policy"),
        ("operator_confirms_dividend_implication", False, "operator_confirms_dividend_implication"),
        ("operator_confirms_no_provider_requests_in_freeze", False, "operator_confirms_no_provider_requests_in_freeze"),
        ("operator_confirms_no_registry_approval", False, "operator_confirms_no_registry_approval"),
        ("operator_confirms_no_strategy_runtime_migration", False, "operator_confirms_no_strategy_runtime_migration"),
        ("operator_confirms_no_predictive_usefulness", False, "operator_confirms_no_predictive_usefulness"),
        ("operator_confirms_no_profitability_acceptance", False, "operator_confirms_no_profitability_acceptance"),
    ],
)
def test_wrong_operator_attestation_values_are_rejected(field: str, value, match: str):
    with pytest.raises(freeze.PositionSwingCanonicalDatasetOperatorFreezeError, match=match):
        _frozen(**{field: value})


def test_missing_attestation_is_rejected():
    with pytest.raises(freeze.PositionSwingCanonicalDatasetOperatorFreezeError, match="operator_attestation"):
        freeze.build_position_swing_canonical_dataset_frozen_v1(operator_attestation=None)  # type: ignore[arg-type]


def test_review_package_blocker_count_is_rejected():
    package = freeze.review.build_position_swing_canonical_dataset_candidate_review_package_v1()
    package["review_summary"]["blocker_count"] = 1
    package["review_summary"]["failed_checks"] = 1
    package["position_swing_canonical_dataset_review_package_semantic_digest"] = (
        freeze.review.position_swing_canonical_dataset_review_package_semantic_digest_v1(package)
    )

    with pytest.raises(
        freeze.PositionSwingCanonicalDatasetOperatorFreezeError,
        match="source POSITION_SWING review package invalid",
    ):
        freeze.build_position_swing_canonical_dataset_frozen_v1(
            position_swing_review_package=package,
            operator_attestation=_attestation(),
        )


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    artifact = _frozen()

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_frozen_artifact_digest_is_deterministic_across_repeated_builds():
    first = _frozen()
    second = _frozen()

    assert (
        first["position_swing_canonical_dataset_frozen_semantic_digest"]
        == second["position_swing_canonical_dataset_frozen_semantic_digest"]
    )
    assert first["position_swing_canonical_dataset_frozen_semantic_digest"] == (
        freeze.position_swing_canonical_dataset_frozen_semantic_digest_v1(first)
    )


@pytest.mark.parametrize(
    ("path", "value", "match"),
    [
        (("source_position_swing_review_package_semantic_digest",), "0" * 64, "source_position_swing_review_package_semantic_digest"),
        (("source_position_swing_review_status",), "NOT_READY", "source_position_swing_review_status"),
        (("source_position_swing_review_blocker_count",), 1, "source_position_swing_review_blocker_count"),
        (("source_position_swing_candidate_digest",), "0" * 64, "source_position_swing_candidate_digest"),
        (("source_dataset_rows_digest",), "0" * 64, "source_dataset_rows_digest"),
        (("source_dataset_manifest_digest",), "0" * 64, "source_dataset_manifest_digest"),
        (("source_normalized_rows_digest",), "0" * 64, "source_normalized_rows_digest"),
        (("source_materialization_receipt_digest",), "0" * 64, "source_materialization_receipt_digest"),
        (("authority_bindings", "identity_frozen_digest"), "0" * 64, "authority_bindings"),
        (("authority_bindings", "calendar_frozen_digest"), "0" * 64, "authority_bindings"),
        (("authority_bindings", "schedule_digest"), "0" * 64, "authority_bindings"),
        (("authority_bindings", "split_event_frozen_digest"), "0" * 64, "authority_bindings"),
        (("authority_bindings", "dividend_event_frozen_digest"), "0" * 64, "authority_bindings"),
        (("source_acquisition_generation_frozen_digest",), "0" * 64, "source_acquisition_generation_frozen_digest"),
        (("position_swing_bar_count",), 993, "position_swing_bar_count"),
        (("cross_check_2025_01_status",), "FAILED", "cross_check_2025_01_status"),
        (("cross_check_2025_01_position_swing_bars",), 19, "cross_check_2025_01_position_swing_bars"),
        (("special_session_policy",), "INCLUDE_SPECIAL_SESSIONS", "special_session_policy"),
        (("in_range_dividend_implication",), None, "in_range_dividend_implication"),
        (("provider_requests_made_in_freeze",), True, "provider_requests_made_in_freeze"),
        (("automatic_stitching",), True, "automatic_stitching"),
        (("position_swing_canonical_dataset_frozen",), False, "position_swing_canonical_dataset_frozen"),
        (("position_swing_registry_approval_created",), True, "position_swing_registry_approval_created"),
        (("position_swing_registry_eligibility",), True, "position_swing_registry_eligibility"),
        (("registry_eligibility",), True, "registry_eligibility"),
        (("strategy_runtime_migration",), True, "strategy_runtime_migration"),
        (("runtime_use",), "AUTHORIZED", "runtime_use"),
        (("strategy_use",), "AUTHORIZED", "strategy_use"),
        (("predictive_usefulness",), "accepted", "predictive_usefulness"),
        (("profitability",), "accepted", "profitability"),
        (("registry_approval_created",), True, "registry_approval_created"),
    ],
)
def test_validator_rejects_invalid_frozen_artifact_mutations(path: tuple[str, ...], value, match: str):
    artifact = _frozen()
    cursor = artifact
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    _recompute(artifact)

    with pytest.raises(freeze.PositionSwingCanonicalDatasetOperatorFreezeError, match=match):
        freeze.validate_position_swing_canonical_dataset_frozen_v1(artifact)


def test_remaining_roadmap_includes_required_future_work():
    roadmap = _frozen()["remaining_roadmap"]

    assert "POSITION_SWING registry approval candidate." in roadmap
    assert "POSITION_SWING registry operator review package." in roadmap
    assert "POSITION_SWING registry approval ceremony." in roadmap
    assert "Normal runtime migration planning." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_freeze_checklist_summary_counts_and_blockers():
    artifact = _frozen()
    summary = artifact["freeze_summary"]

    assert [item["check_id"] for item in artifact["freeze_checklist"]] == freeze.REQUIRED_FREEZE_CHECK_IDS
    assert summary["total_checks"] == len(freeze.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["passed_checks"] == len(freeze.REQUIRED_FREEZE_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["position_swing_canonical_dataset_freeze_authorized_by_operator"] is True
    assert summary["software_auto_approval"] is False
    assert summary["registry_approval_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = freeze.build_position_swing_canonical_dataset_frozen_markdown_v1(_frozen())

    for heading in (
        "## Title",
        "## Frozen POSITION_SWING Canonical Dataset",
        "## Operator Attestation",
        "## Source POSITION_SWING Review Package",
        "## Dataset Evidence",
        "## 2025-01 Cross-Check",
        "## Special-Session Policy",
        "## Frozen Authority Bindings",
        "## Dividend Adjustment Implication",
        "## Freeze Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert heading in markdown
    assert "No registry approval or Strategy runtime migration occurred." in markdown


def test_write_frozen_artifact_writes_json_without_overwrite(tmp_path: Path):
    result = freeze.write_position_swing_canonical_dataset_frozen_v1(tmp_path, operator_attestation=_attestation())

    assert result["artifact_kind"] == "POSITION_SWING_CANONICAL_DATASET_FROZEN"
    assert result["frozen_payload_digest"]
    with pytest.raises(freeze.PositionSwingCanonicalDatasetOperatorFreezeError, match="already exists"):
        freeze.write_position_swing_canonical_dataset_frozen_v1(tmp_path, operator_attestation=_attestation())


def test_freeze_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_FROZEN == "POSITION_SWING_CANONICAL_DATASET_FROZEN"
    assert services.POSITION_SWING_CANONICAL_DATASET_FROZEN == "POSITION_SWING_CANONICAL_DATASET_FROZEN"
    assert (
        services.REQUIRED_POSITION_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE
        == freeze.REQUIRED_POSITION_SWING_CANONICAL_DATASET_OPERATOR_ATTESTATION_PHRASE
    )
    assert (
        services.build_position_swing_canonical_dataset_operator_attestation_v1
        is freeze.build_position_swing_canonical_dataset_operator_attestation_v1
    )
    assert services.build_position_swing_canonical_dataset_frozen_v1 is freeze.build_position_swing_canonical_dataset_frozen_v1
    assert (
        services.validate_position_swing_canonical_dataset_frozen_v1
        is freeze.validate_position_swing_canonical_dataset_frozen_v1
    )
    assert services.write_position_swing_canonical_dataset_frozen_v1 is freeze.write_position_swing_canonical_dataset_frozen_v1
    assert (
        services.build_position_swing_canonical_dataset_frozen_markdown_v1
        is freeze.build_position_swing_canonical_dataset_frozen_markdown_v1
    )
