from __future__ import annotations

import pytest

from marketflow.services import swing_canonical_dataset_operator_review_service as review


def _package() -> dict:
    return review.build_swing_canonical_dataset_candidate_review_package_v1()


def _check_ids(package: dict) -> list[str]:
    return [item["check_id"] for item in package["review_checklist"]]


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.swing.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_is_swing_review_package():
    assert _package()["artifact_kind"] == review.ARTIFACT_KIND_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE


def test_review_status_is_ready():
    assert _package()["review_status"] == review.SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY


def test_reviewed_candidate_digest_matches_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["reviewed_candidate_digest"] == review.EXPECTED_REVIEWED_CANDIDATE_DIGEST


def test_dataset_rows_digest_matches_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["reviewed_dataset_rows_digest"] == review.EXPECTED_REVIEWED_DATASET_ROWS_DIGEST


def test_dataset_manifest_digest_matches_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["reviewed_dataset_manifest_digest"] == review.EXPECTED_REVIEWED_DATASET_MANIFEST_DIGEST


def test_source_rows_digest_matches_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["reviewed_source_rows_digest"] == review.EXPECTED_SOURCE_ROWS_DIGEST


def test_materialization_receipt_digest_matches_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["reviewed_materialization_receipt_digest"] == review.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST


def test_swing_bar_count_is_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["swing_bar_count"] == 1988


def test_source_rth_consumed_and_excluded_are_expected():
    evidence = _package()["reviewed_swing_candidate_evidence"]

    assert evidence["source_rth_rows_consumed"] == 25844
    assert evidence["source_rth_rows_excluded"] == 126


def test_full_sessions_used_is_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["full_sessions_used"] == 994


def test_special_sessions_excluded_is_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["special_sessions_excluded"] == 9


def test_special_session_rows_excluded_is_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["special_session_rows_excluded"] == 126


def test_2025_01_cross_check_passed():
    assert _package()["reviewed_swing_candidate_evidence"]["cross_check_status"] == "PASSED"


def test_2025_01_swing_bars_are_expected():
    assert _package()["reviewed_swing_candidate_evidence"]["cross_check_swing_bars"] == 40


def test_checklist_contains_all_required_check_ids():
    assert _check_ids(_package()) == review.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_candidate():
    assert {item["status"] for item in _package()["review_checklist"]} == {"PASS"}


def test_summary_counts_total_passed_failed_correctly():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True


def test_authority_flags_remain_false_or_not_accepted():
    package = _package()

    assert package["canonical_dataset_frozen"] is False
    assert package["canonical_eligibility"] is False
    assert package["registry_eligibility"] is False
    assert package["strategy_runtime_migration"] is False
    assert package["automatic_stitching"] is False
    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    assert package["provider_requests_made_in_review"] is False


def test_no_frozen_artifact_or_registry_approval_is_produced():
    package = _package()

    assert package["artifact_kind"] != "SWING_CANONICAL_DATASET_FROZEN"
    assert package["review_status"] != "SWING_CANONICAL_DATASET_FROZEN"
    assert package["freeze_status"] is None
    assert package["registry_approval_created"] is False


def test_operator_decision_and_freeze_fields_remain_null():
    package = _package()

    assert package["operator_decision"] is None
    assert package["operator_approved_by"] is None
    assert package["operator_freeze_timestamp"] is None
    assert package["operator_freeze_digest"] is None
    assert package["operator_signature"] is None


def test_review_package_digest_is_deterministic():
    assert _package()["swing_canonical_dataset_review_package_semantic_digest"] == _package()["swing_canonical_dataset_review_package_semantic_digest"]


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("reviewed_candidate_digest", "0" * 64, "reviewed_candidate_digest"),
        ("reviewed_dataset_rows_digest", "0" * 64, "reviewed_dataset_rows_digest"),
        ("reviewed_dataset_manifest_digest", "0" * 64, "reviewed_dataset_manifest_digest"),
        ("reviewed_source_rows_digest", "0" * 64, "reviewed_source_rows_digest"),
        ("reviewed_materialization_receipt_digest", "0" * 64, "reviewed_materialization_receipt_digest"),
        ("swing_bar_count", 1987, "swing_bar_count"),
        ("cross_check_swing_bars", 39, "cross_check_swing_bars"),
    ],
)
def test_validator_rejects_modified_reviewed_evidence(field: str, value, match: str):
    package = _package()
    package["reviewed_swing_candidate_evidence"][field] = value

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match=match):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_2025_01_cross_check_not_passed():
    package = _package()
    package["reviewed_swing_candidate_evidence"]["cross_check_status"] = "FAILED"

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="cross_check_status"):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_missing_dividend_implication():
    package = _package()
    package["authority_bindings"]["in_range_dividend_implication"] = None

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="authority_bindings"):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "canonical_dataset_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    package = _package()
    package[field] = True

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match=field):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_accepted_predictive_or_profitability():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match=field):
            review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_provider_requests_made_in_review():
    package = _package()
    package["provider_requests_made_in_review"] = True

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="provider_requests_made_in_review"):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_frozen_artifact_or_status():
    for field in ("artifact_kind", "review_status", "freeze_status"):
        package = _package()
        package[field] = "SWING_CANONICAL_DATASET_FROZEN"

        with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="SWING_CANONICAL_DATASET_FROZEN|freeze_status"):
            review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_registry_approval_present():
    package = _package()
    package["registry_approval_created"] = True

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="registry_approval_created"):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _package()["remaining_roadmap"]

    assert "Digest-bound SWING canonical dataset operator freeze ceremony." in roadmap
    assert "SWING registry approval." in roadmap
    assert "POSITION_SWING canonical dataset candidate." in roadmap
    assert "POSITION_SWING canonical dataset operator review/freeze." in roadmap
    assert "POSITION_SWING registry approval." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_swing_canonical_dataset_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed SWING Candidate",
        "## Dataset Summary",
        "## 2025-01 Cross-Check",
        "## Special-Session Policy",
        "## Frozen Authority Bindings",
        "## Dividend Adjustment Implication",
        "## Checklist Summary",
        "## Failed Checks",
        "## Authority Boundary",
        "## Remaining Roadmap",
        "## Guardrails",
    ):
        assert section in markdown
    assert "No `SWING_CANONICAL_DATASET_FROZEN` artifact or status is created." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path):
    result = review.write_swing_canonical_dataset_candidate_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="already exists"):
        review.write_swing_canonical_dataset_candidate_review_package_v1(tmp_path)


def test_validator_rejects_mutated_digest_field():
    package = _package()
    package["swing_canonical_dataset_review_package_semantic_digest"] = "0" * 64

    with pytest.raises(review.SwingCanonicalDatasetOperatorReviewError, match="swing_canonical_dataset_review_package_semantic_digest"):
        review.validate_swing_canonical_dataset_candidate_review_package_v1(package)


def test_local_ignored_dataset_and_manifest_are_verified_when_available():
    package = _package()
    binding = package["local_artifact_binding"]

    assert binding["manifest_file_available"] is True
    assert binding["manifest_file_verified"] is True
    assert binding["dataset_file_available"] is True
    assert binding["dataset_file_verified"] is True
    assert binding["dataset_row_count"] == 1988


def test_build_from_status_binding_when_local_candidate_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(review, "_load_local_candidate", lambda: None)
    package = review.build_swing_canonical_dataset_candidate_review_package_v1()

    assert package["binding_mode"] == review.SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING
    assert package["reviewed_swing_candidate_evidence"]["reviewed_candidate_digest"] == review.EXPECTED_REVIEWED_CANDIDATE_DIGEST
