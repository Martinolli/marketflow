from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import acquisition_generation_operator_review_service as review


EXPECTED_ACQUISITION_DIGEST = "5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb"
EXPECTED_CHUNK_DIGEST = "8a4bf37f501fb7da5ea23e04d5ebe90da2cdfda1bf9e06e55e4c459be53fa374"
EXPECTED_RAW_DIGEST = "aea820006bb458b9e51a1cda23ae24be02f476aafb36bec6c65d3740812d06c7"
EXPECTED_NORMALIZED_DIGEST = "0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc"
EXPECTED_MONTHLY_DIGEST = "d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4"
EXPECTED_RECEIPT_DIGEST = "63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed"
EXPECTED_TARGETED_RECEIPT_DIGEST = "82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8"


def _package() -> dict:
    return review.build_acquisition_generation_candidate_review_package_v1()


def _recompute(package: dict) -> None:
    package["review_checklist"] = review._build_checklist(package)
    failed = [item for item in package["review_checklist"] if item["status"] != "PASS"]
    package["review_summary"] = {
        "total_checks": len(package["review_checklist"]),
        "passed_checks": len(package["review_checklist"]) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for item in failed if item["severity"] == "BLOCKER"),
        "ready_for_operator_assessment": not failed,
        "operator_decision_required_before_freeze": True,
        "software_freeze_authorized": False,
    }
    package["acquisition_generation_review_package_semantic_digest"] = (
        review.acquisition_generation_review_package_semantic_digest_v1(package)
    )


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*args, **kwargs):  # pragma: no cover - exercised only on bug
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.acquisition, "build_acquisition_generation_live_candidate_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_package_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE
        == "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE"
    )
    assert (
        services.ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY
        == "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY"
    )
    assert services.build_acquisition_generation_candidate_review_package_v1 is review.build_acquisition_generation_candidate_review_package_v1
    assert services.validate_acquisition_generation_candidate_review_package_v1 is review.validate_acquisition_generation_candidate_review_package_v1
    assert services.write_acquisition_generation_candidate_review_package_v1 is review.write_acquisition_generation_candidate_review_package_v1
    assert services.build_acquisition_generation_candidate_review_markdown_v1 is review.build_acquisition_generation_candidate_review_markdown_v1


def test_review_package_artifact_kind_and_status_ready():
    package = _package()

    assert package["artifact_kind"] == "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE"
    assert package["review_status"] == "ACQUISITION_GENERATION_CANDIDATE_REVIEW_PACKAGE_READY"


def test_review_package_binds_acquisition_candidate_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_acquisition_candidate_digest"] == EXPECTED_ACQUISITION_DIGEST


def test_review_package_binds_chunk_manifest_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_chunk_manifest_digest"] == EXPECTED_CHUNK_DIGEST


def test_review_package_binds_provider_raw_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_provider_raw_response_digest"] == EXPECTED_RAW_DIGEST


def test_review_package_binds_normalized_rows_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_normalized_source_rows_digest"] == EXPECTED_NORMALIZED_DIGEST


def test_review_package_binds_monthly_reconciliation_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_monthly_reconciliation_digest"] == EXPECTED_MONTHLY_DIGEST


def test_review_package_binds_acquisition_receipt_digest():
    assert _package()["reviewed_acquisition_evidence"]["reviewed_acquisition_receipt_digest"] == EXPECTED_RECEIPT_DIGEST


def test_review_package_counts_match_full_generation():
    evidence = _package()["reviewed_acquisition_evidence"]

    assert (evidence["expected_chunk_count"], evidence["completed_chunk_count"], evidence["failed_chunk_count"]) == (48, 48, 0)
    assert evidence["total_raw_rows"] == 63804
    assert evidence["total_normalized_source_rows"] == 63804
    assert evidence["total_rth_rows"] == 25970
    assert evidence["total_extended_hours_rows"] == 37834
    assert evidence["out_of_calendar_or_unknown_rows"] == 0


def test_review_package_2025_01_cross_check_passed():
    assert _package()["reviewed_acquisition_evidence"]["accepted_2025_01_cross_check"]["cross_check_status"] == "PASSED"


def test_review_package_monthly_reconciliation_counts_are_39_9():
    evidence = _package()["reviewed_acquisition_evidence"]

    assert evidence["monthly_reconciled_count"] == 39
    assert evidence["monthly_not_reconciled_count"] == 9


def test_review_package_targeted_diagnostics_ready_after_triage():
    assert _package()["targeted_diagnostic_evidence"]["targeted_diagnostic_status"] == "READY_AFTER_TRIAGE"


def test_review_package_all_monthly_mismatches_explained():
    assert _package()["targeted_diagnostic_evidence"]["all_monthly_mismatches_explained"] is True


def test_review_package_per_session_issue_summary_all_reconciled():
    assert _package()["targeted_diagnostic_evidence"]["per_session_issue_summary"] == {"RECONCILED": 188}


def test_review_package_per_session_severity_summary_info_only():
    assert _package()["targeted_diagnostic_evidence"]["per_session_severity_summary"] == {"INFO": 188}


def test_review_package_targeted_diagnostic_receipt_digest_matches():
    assert _package()["targeted_diagnostic_evidence"]["targeted_diagnostic_receipt_digest"] == EXPECTED_TARGETED_RECEIPT_DIGEST


def test_review_package_authority_digests_match():
    bindings = _package()["authority_bindings"]

    assert bindings["identity_segment_frozen_digest"] == "57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e"
    assert bindings["exchange_calendar_frozen_digest"] == "25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6"
    assert bindings["schedule_semantic_digest"] == "b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0"
    assert bindings["split_event_audit_frozen_digest"] == "9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae"
    assert bindings["dividend_event_audit_frozen_digest"] == "0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141"


def test_review_package_dividend_implication_preserved():
    bindings = _package()["authority_bindings"]

    assert bindings["in_range_dividends_found"] is True
    assert bindings["in_range_dividend_count"] == 16
    assert bindings["in_range_dividend_implication"] == "ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY"


def test_review_package_acquisition_freeze_remains_false():
    package = _package()

    assert package["acquisition_generation_freeze"] is False
    assert package["authority_boundary"]["acquisition_generation_freeze"] is False


def test_review_package_canonical_registry_runtime_remain_false():
    package = _package()

    assert package["canonical_eligibility"] is False
    assert package["registry_eligibility"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["automatic_stitching"] is False


def test_review_package_predictive_and_profitability_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"


def test_review_package_provider_requests_made_in_review_false():
    assert _package()["provider_requests_made_in_review"] is False


def test_review_package_does_not_emit_frozen_artifact_or_status():
    package = _package()

    assert package["artifact_kind"] != "ACQUISITION_GENERATION_FROZEN"
    assert package["freeze_status"] is None


def test_review_package_operator_decision_is_null_and_not_approved():
    package = _package()

    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None


def test_review_package_freeze_operator_timestamp_and_signature_are_null():
    package = _package()

    assert package["operator_approved_by"] is None
    assert package["operator_freeze_timestamp"] is None
    assert package["operator_freeze_digest"] is None
    assert package["operator_signature"] is None


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["acquisition_generation_review_package_semantic_digest"] == second["acquisition_generation_review_package_semantic_digest"]
    assert first["acquisition_generation_review_package_semantic_digest"] == review.acquisition_generation_review_package_semantic_digest_v1(first)


@pytest.mark.parametrize(
    ("path", "value", "match"),
    [
        (("reviewed_acquisition_evidence", "reviewed_acquisition_candidate_digest"), "0" * 64, "reviewed_acquisition_evidence"),
        (("reviewed_acquisition_evidence", "reviewed_normalized_source_rows_digest"), "1" * 64, "reviewed_acquisition_evidence"),
        (("reviewed_acquisition_evidence", "total_raw_rows"), 1, "reviewed_acquisition_evidence"),
        (("reviewed_acquisition_evidence", "accepted_2025_01_cross_check", "cross_check_status"), "FAILED", "reviewed_acquisition_evidence"),
        (("targeted_diagnostic_evidence", "all_monthly_mismatches_explained"), False, "targeted_diagnostic_evidence"),
        (("authority_bindings", "in_range_dividend_implication"), None, "authority_bindings"),
        (("acquisition_generation_freeze",), True, "acquisition_generation_freeze"),
        (("canonical_eligibility",), True, "canonical_eligibility"),
        (("registry_eligibility",), True, "registry_eligibility"),
        (("strategy_runtime_migration",), True, "strategy_runtime_migration"),
        (("predictive_usefulness",), "accepted", "predictive_usefulness"),
        (("profitability",), "accepted", "profitability"),
    ],
)
def test_review_package_validator_rejects_invalid_mutations(path: tuple[str, ...], value, match: str):
    package = _package()
    cursor = package
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    _recompute(package)

    with pytest.raises(review.AcquisitionGenerationOperatorReviewError, match=match):
        review.validate_acquisition_generation_candidate_review_package_v1(package)


def test_review_package_remaining_roadmap_includes_required_future_work():
    roadmap = _package()["remaining_roadmap"]

    assert "Digest-bound acquisition generation operator freeze ceremony." in roadmap
    assert "SWING canonical dataset candidate." in roadmap
    assert "SWING registry approval." in roadmap
    assert "POSITION_SWING canonical dataset candidate." in roadmap
    assert "POSITION_SWING registry approval." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_review_package_markdown_includes_required_sections_and_guardrails(tmp_path: Path):
    package = _package()
    text = review.build_acquisition_generation_candidate_review_markdown_v1(package)
    result = review.write_acquisition_generation_candidate_review_package_v1(tmp_path)
    written = Path(result["markdown_path"]).read_text(encoding="utf-8")

    for heading in [
        "## Reviewed Acquisition Candidate",
        "## Full Generation Summary",
        "## 2025-01 Cross-Check",
        "## Monthly Reconciliation Summary",
        "## Targeted Per-Session Triage",
        "## Frozen Authority Bindings",
        "## Dividend Adjustment Implication",
        "## Checklist Summary",
        "## Failed Checks",
        "## Authority Boundary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ]:
        assert heading in text
    assert "Provider requests made in review: `False`" in written
    assert "No acquisition-generation freeze was created." in written
