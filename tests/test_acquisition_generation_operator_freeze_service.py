from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import acquisition_generation_operator_freeze_service as freeze


def _attestation(**overrides) -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-07T00:00:00Z",
        "operator_attestation_phrase": freeze.REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_acquisition_review_package_digest": freeze.EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_acquisition_candidate_digest": freeze.EXPECTED_ACQUISITION_CANDIDATE_DIGEST,
        "operator_confirms_chunk_manifest_digest": freeze.EXPECTED_CHUNK_MANIFEST_DIGEST,
        "operator_confirms_provider_raw_response_digest": freeze.EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST,
        "operator_confirms_normalized_source_rows_digest": freeze.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
        "operator_confirms_monthly_reconciliation_digest": freeze.EXPECTED_MONTHLY_RECONCILIATION_DIGEST,
        "operator_confirms_acquisition_receipt_digest": freeze.EXPECTED_ACQUISITION_RECEIPT_DIGEST,
        "operator_confirms_targeted_diagnostic_receipt_digest": freeze.EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST,
        "operator_confirms_per_session_diagnostics_digest": freeze.EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST,
        "operator_confirms_identity_frozen_digest": freeze.acquisition.EXPECTED_IDENTITY_SEGMENT_FROZEN_DIGEST,
        "operator_confirms_calendar_frozen_digest": freeze.acquisition.EXPECTED_EXCHANGE_CALENDAR_FROZEN_DIGEST,
        "operator_confirms_schedule_digest": freeze.acquisition.EXPECTED_SCHEDULE_SEMANTIC_DIGEST,
        "operator_confirms_split_event_frozen_digest": freeze.acquisition.EXPECTED_SPLIT_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_dividend_event_frozen_digest": freeze.acquisition.EXPECTED_DIVIDEND_EVENT_AUDIT_FROZEN_DIGEST,
        "operator_confirms_2025_01_cross_check_passed": True,
        "operator_confirms_all_monthly_mismatches_explained": True,
        "operator_confirms_dividend_implication": True,
    }
    values.update(overrides)
    return freeze.build_acquisition_generation_operator_attestation_v1(**values)


def _frozen(**attestation_overrides) -> dict:
    return freeze.build_acquisition_generation_frozen_v1(operator_attestation=_attestation(**attestation_overrides))


def _recompute(frozen: dict) -> None:
    frozen["freeze_checklist"] = freeze._freeze_checklist(frozen)
    failed = [check for check in frozen["freeze_checklist"] if check["status"] != freeze.PASS]
    frozen["freeze_summary"] = {
        "total_checks": len(frozen["freeze_checklist"]),
        "passed_checks": len(frozen["freeze_checklist"]) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for check in failed if check["severity"] == freeze.BLOCKER),
        "acquisition_generation_freeze_authorized_by_operator": not failed,
        "software_auto_approval": False,
    }
    frozen["acquisition_generation_frozen_semantic_digest"] = freeze.acquisition_generation_frozen_semantic_digest_v1(frozen)


def test_operator_attestation_builder_creates_required_fields():
    attestation = _attestation()

    assert attestation["operator_decision"] == "APPROVE_ACQUISITION_GENERATION_FREEZE"
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_phrase"] == freeze.REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_confirms_no_provider_requests_in_freeze"] is True
    assert attestation["operator_confirms_no_canonical_approval"] is True


def test_frozen_artifact_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*args, **kwargs):  # pragma: no cover - should never run
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(freeze.acquisition, "build_acquisition_generation_live_candidate_v1", fail_provider_call)

    artifact = _frozen()

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_freeze"] is False


def test_frozen_artifact_kind_and_status():
    artifact = _frozen()

    assert artifact["artifact_kind"] == "ACQUISITION_GENERATION_FROZEN"
    assert artifact["freeze_status"] == "ACQUISITION_GENERATION_FROZEN"


def test_acquisition_generation_freeze_true_and_prior_authorities_true():
    artifact = _frozen()

    assert artifact["acquisition_generation_freeze"] is True
    assert artifact["identity_segment_frozen"] is True
    assert artifact["calendar_operator_frozen"] is True
    assert artifact["split_event_audit_frozen"] is True
    assert artifact["dividend_event_audit_frozen"] is True


def test_source_review_and_acquisition_digests_match():
    artifact = _frozen()

    assert artifact["source_acquisition_review_package_semantic_digest"] == freeze.EXPECTED_ACQUISITION_REVIEW_PACKAGE_DIGEST
    assert artifact["source_acquisition_candidate_digest"] == freeze.EXPECTED_ACQUISITION_CANDIDATE_DIGEST


def test_full_generation_digests_match_exact_values():
    artifact = _frozen()

    assert artifact["source_chunk_manifest_digest"] == freeze.EXPECTED_CHUNK_MANIFEST_DIGEST
    assert artifact["source_provider_raw_response_digest"] == freeze.EXPECTED_PROVIDER_RAW_RESPONSE_DIGEST
    assert artifact["source_normalized_source_rows_digest"] == freeze.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST
    assert artifact["source_monthly_reconciliation_digest"] == freeze.EXPECTED_MONTHLY_RECONCILIATION_DIGEST
    assert artifact["source_acquisition_receipt_digest"] == freeze.EXPECTED_ACQUISITION_RECEIPT_DIGEST


def test_targeted_diagnostic_digests_match_exact_values():
    artifact = _frozen()

    assert artifact["targeted_diagnostic_receipt_digest"] == freeze.EXPECTED_TARGETED_DIAGNOSTIC_RECEIPT_DIGEST
    assert artifact["per_session_diagnostics_digest"] == freeze.EXPECTED_PER_SESSION_DIAGNOSTICS_DIGEST


def test_counts_match_full_generation():
    artifact = _frozen()

    assert (artifact["expected_chunk_count"], artifact["completed_chunk_count"], artifact["failed_chunk_count"]) == (48, 48, 0)
    assert artifact["total_raw_rows"] == 63804
    assert artifact["total_normalized_source_rows"] == 63804
    assert artifact["total_rth_rows"] == 25970
    assert artifact["total_extended_hours_rows"] == 37834
    assert artifact["out_of_calendar_or_unknown_rows"] == 0


def test_cross_check_mismatches_and_dividend_implication_preserved():
    artifact = _frozen()

    assert artifact["accepted_2025_01_cross_check"]["cross_check_status"] == "PASSED"
    assert artifact["all_monthly_mismatches_explained"] is True
    assert artifact["authority_bindings"]["in_range_dividend_implication"] == "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("operator_attestation_phrase", "wrong", "operator_attestation_phrase_matches"),
        ("operator_decision", "REJECT", "operator_decision_approved"),
        ("operator_confirms_acquisition_review_package_digest", "0" * 64, "operator_review_digest_confirmation_matches"),
        ("operator_confirms_acquisition_candidate_digest", "0" * 64, "operator_candidate_digest_confirmation_matches"),
        ("operator_confirms_provider_raw_response_digest", "0" * 64, "operator_raw_digest_confirmation_matches"),
        ("operator_confirms_normalized_source_rows_digest", "0" * 64, "operator_normalized_digest_confirmation_matches"),
        ("operator_confirms_monthly_reconciliation_digest", "0" * 64, "operator_monthly_digest_confirmation_matches"),
        ("operator_confirms_acquisition_receipt_digest", "0" * 64, "operator_receipt_digest_confirmation_matches"),
        ("operator_confirms_targeted_diagnostic_receipt_digest", "0" * 64, "operator_targeted_receipt_digest_confirmation_matches"),
        ("operator_confirms_per_session_diagnostics_digest", "0" * 64, "operator_per_session_digest_confirmation_matches"),
        ("operator_confirms_2025_01_cross_check_passed", False, "operator_confirms_2025_01_cross_check"),
        ("operator_confirms_all_monthly_mismatches_explained", False, "operator_confirms_all_mismatches_explained"),
        ("operator_confirms_dividend_implication", False, "operator_confirms_dividend_implication"),
    ],
)
def test_wrong_operator_attestation_values_are_rejected(field: str, value, match: str):
    with pytest.raises(freeze.AcquisitionGenerationOperatorFreezeError, match=match):
        _frozen(**{field: value})


def test_missing_attestation_is_rejected():
    with pytest.raises(freeze.AcquisitionGenerationOperatorFreezeError, match="operator_attestation"):
        freeze.build_acquisition_generation_frozen_v1(operator_attestation=None)  # type: ignore[arg-type]


def test_review_package_blocker_count_is_rejected():
    package = freeze.review.build_acquisition_generation_candidate_review_package_v1()
    package["review_summary"]["blocker_count"] = 1
    package["review_summary"]["failed_checks"] = 1
    package["review_summary"]["ready_for_operator_assessment"] = False
    package["acquisition_generation_review_package_semantic_digest"] = freeze.review.acquisition_generation_review_package_semantic_digest_v1(package)

    with pytest.raises(freeze.AcquisitionGenerationOperatorFreezeError, match="source acquisition review package invalid"):
        freeze.build_acquisition_generation_frozen_v1(acquisition_review_package=package, operator_attestation=_attestation())


def test_downstream_authority_flags_remain_false():
    artifact = _frozen()

    assert artifact["canonical_eligibility"] is False
    assert artifact["registry_eligibility"] is False
    assert artifact["strategy_runtime_migration"] is False
    assert artifact["automatic_stitching"] is False
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_frozen_artifact_digest_is_deterministic():
    first = _frozen()
    second = _frozen()

    assert first["acquisition_generation_frozen_semantic_digest"] == second["acquisition_generation_frozen_semantic_digest"]
    assert first["acquisition_generation_frozen_semantic_digest"] == freeze.acquisition_generation_frozen_semantic_digest_v1(first)


@pytest.mark.parametrize(
    ("path", "value", "match"),
    [
        (("acquisition_generation_freeze",), False, "acquisition_generation_freeze"),
        (("canonical_eligibility",), True, "canonical_eligibility"),
        (("registry_eligibility",), True, "registry_eligibility"),
        (("strategy_runtime_migration",), True, "strategy_runtime_migration"),
        (("authority_bindings", "fixed_segment", "composite_figi"), "WRONG", "authority_bindings"),
        (("authority_bindings", "fixed_segment", "segment_end"), "2025-01-01", "authority_bindings"),
        (("authority_bindings", "fixed_segment", "security_type"), "ETF", "authority_bindings"),
        (("authority_bindings", "acquisition_contract_digest"), "0" * 64, "authority_bindings"),
        (("authority_bindings", "identity_segment_frozen_digest"), "0" * 64, "authority_bindings"),
        (("provider_requests_made_in_freeze",), True, "provider_requests_made_in_freeze"),
    ],
)
def test_validator_rejects_invalid_frozen_artifact_mutations(path: tuple[str, ...], value, match: str):
    artifact = _frozen()
    cursor = artifact
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    _recompute(artifact)

    with pytest.raises(freeze.AcquisitionGenerationOperatorFreezeError, match=match):
        freeze.validate_acquisition_generation_frozen_v1(artifact)


def test_remaining_roadmap_includes_required_future_work():
    roadmap = _frozen()["remaining_roadmap"]

    assert "SWING canonical dataset candidate." in roadmap
    assert "SWING registry approval." in roadmap
    assert "POSITION_SWING canonical dataset candidate." in roadmap
    assert "POSITION_SWING registry approval." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails(tmp_path: Path):
    artifact = _frozen()
    text = freeze.build_acquisition_generation_frozen_markdown_v1(artifact)
    result = freeze.write_acquisition_generation_frozen_v1(tmp_path, operator_attestation=_attestation())
    written = Path(result["markdown_path"]).read_text(encoding="utf-8")

    for heading in [
        "## Frozen Acquisition Generation",
        "## Operator Attestation",
        "## Source Acquisition Review Package",
        "## Full Generation Evidence",
        "## 2025-01 Cross-Check",
        "## Targeted Per-Session Triage",
        "## Frozen Authority Bindings",
        "## Dividend Adjustment Implication",
        "## Freeze Checklist Summary",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ]:
        assert heading in text
    assert "Provider requests made in freeze: `False`" in written
    assert "No canonical, registry, runtime, predictive, or profitability approval occurred." in written


def test_freeze_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_ACQUISITION_GENERATION_FROZEN == "ACQUISITION_GENERATION_FROZEN"
    assert services.REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE == freeze.REQUIRED_ACQUISITION_GENERATION_OPERATOR_ATTESTATION_PHRASE
    assert services.build_acquisition_generation_operator_attestation_v1 is freeze.build_acquisition_generation_operator_attestation_v1
    assert services.build_acquisition_generation_frozen_v1 is freeze.build_acquisition_generation_frozen_v1
    assert services.validate_acquisition_generation_frozen_v1 is freeze.validate_acquisition_generation_frozen_v1
    assert services.write_acquisition_generation_frozen_v1 is freeze.write_acquisition_generation_frozen_v1
