from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import dataset_file_availability_verification_operator_review_service as review


def _package() -> dict:
    return review.build_dataset_file_availability_verification_review_package_v1()


def _entry(package: dict, profile: str) -> dict:
    return next(item for item in package["verification_entries"] if item["dataset_profile"] == profile)


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_is_dataset_file_availability_verification_review_package():
    assert (
        _package()["artifact_kind"]
        == review.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == review.DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY


def test_verification_package_digest_is_bound():
    assert (
        _package()["reviewed_verification_package_digest"]
        == review.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE_DIGEST
    )


def test_verification_entry_count_is_two():
    assert _package()["verification_entry_count"] == 2


def test_dataset_file_count_and_digest_verified_count_are_two():
    package = _package()

    assert package["dataset_files_available_count"] == 2
    assert package["dataset_digests_verified_count"] == 2


def test_manifest_file_count_and_digest_verified_count_are_two():
    package = _package()

    assert package["manifest_files_available_count"] == 2
    assert package["manifest_digests_verified_count"] == 2


def test_missing_file_count_is_zero():
    assert _package()["missing_file_count"] == 0


def test_digest_mismatch_count_is_zero():
    assert _package()["digest_mismatch_count"] == 0


def test_swing_file_evidence_is_bound():
    entry = _entry(_package(), "SWING")

    assert entry["registry_key"] == review.verification.discovery.swing_registry.PROPOSED_REGISTRY_KEY
    assert entry["registry_approval_digest"] == review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    assert entry["dataset_rows_digest"] == review.verification.discovery.swing_registry.EXPECTED_DATASET_ROWS_DIGEST
    assert entry["dataset_manifest_digest"] == review.verification.discovery.swing_registry.EXPECTED_DATASET_MANIFEST_DIGEST
    assert entry["dataset_file_status"] == review.verification.AVAILABLE_AND_DIGEST_VERIFIED
    assert entry["manifest_file_status"] == review.verification.AVAILABLE_AND_DIGEST_VERIFIED
    assert entry["runtime_use"] == review.verification.NOT_AUTHORIZED
    assert entry["strategy_use"] == review.verification.NOT_AUTHORIZED


def test_position_swing_file_evidence_is_bound():
    entry = _entry(_package(), "POSITION_SWING")

    assert entry["registry_key"] == review.verification.discovery.position_registry.PROPOSED_REGISTRY_KEY
    assert entry["registry_approval_digest"] == review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    assert entry["dataset_rows_digest"] == review.verification.discovery.position_registry.EXPECTED_DATASET_ROWS_DIGEST
    assert entry["dataset_manifest_digest"] == review.verification.discovery.position_registry.EXPECTED_DATASET_MANIFEST_DIGEST
    assert entry["dataset_file_status"] == review.verification.AVAILABLE_AND_DIGEST_VERIFIED
    assert entry["manifest_file_status"] == review.verification.AVAILABLE_AND_DIGEST_VERIFIED
    assert entry["runtime_use"] == review.verification.NOT_AUTHORIZED
    assert entry["strategy_use"] == review.verification.NOT_AUTHORIZED


def test_read_only_discovery_candidate_digest_is_bound():
    assert (
        _package()["read_only_discovery_candidate_digest"]
        == review.verification.EXPECTED_READ_ONLY_DISCOVERY_CANDIDATE_DIGEST
    )


def test_read_only_discovery_review_package_digest_is_bound():
    assert (
        _package()["read_only_discovery_review_package_digest"]
        == review.verification.EXPECTED_READ_ONLY_DISCOVERY_REVIEW_PACKAGE_DIGEST
    )


def test_runtime_plan_digest_is_bound():
    assert (
        _package()["runtime_migration_plan_digest"]
        == review.verification.discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST
    )


def test_runtime_review_package_digest_is_bound():
    assert (
        _package()["runtime_migration_review_package_digest"]
        == review.verification.discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
    )


def test_ready_for_research_campaign_planning_is_true():
    assert _package()["ready_for_research_campaign_planning"] is True


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == review.verification.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == review.verification.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == review.verification.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == review.verification.NOT_AUTHORIZED


def test_automatic_stitching_remains_false():
    assert _package()["automatic_stitching"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == review.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert package["profitability"] == review.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_provider_requests_made_in_review_remains_false():
    assert _package()["provider_requests_made_in_review"] is False


def test_checklist_contains_all_required_check_ids():
    assert [item["check_id"] for item in _package()["review_checklist"]] == review.REQUIRED_CHECK_IDS


def test_all_checks_pass_for_accepted_verification():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_correctly():
    summary = _package()["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["ready_for_research_campaign_planning"] is True
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert (
        first["dataset_file_availability_verification_review_package_digest"]
        == second["dataset_file_availability_verification_review_package_digest"]
    )
    assert (
        first["dataset_file_availability_verification_review_package_digest"]
        == review.dataset_file_availability_verification_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package():
    validation = review.validate_dataset_file_availability_verification_review_package_v1(_package())

    assert validation["status"] == "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_VALID"
    assert validation["runtime_migration_approved"] is False


def test_validator_rejects_modified_verification_package_digest():
    package = _package()
    package["reviewed_verification_package_digest"] = "0" * 64

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="reviewed_verification_package_digest",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_verification_entry_count_not_two():
    package = _package()
    package["verification_entries"] = package["verification_entries"][:1]

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="verification entry count",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_missing_swing_verification_entry():
    package = _package()
    position_entry = _entry(package, "POSITION_SWING")
    package["verification_entries"] = [position_entry, dict(position_entry)]

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="missing SWING",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_missing_position_swing_verification_entry():
    package = _package()
    swing_entry = _entry(package, "SWING")
    package["verification_entries"] = [swing_entry, dict(swing_entry)]

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="missing POSITION_SWING",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_ready_status_with_missing_files():
    package = _package()
    _entry(package, "SWING")["dataset_file_status"] = review.verification.MISSING_DATASET_FILE

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="dataset_file_status",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_ready_status_with_digest_mismatch():
    package = _package()
    _entry(package, "SWING")["dataset_rows_digest_match"] = False

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="dataset_rows_digest_match",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_runtime_migration_approved_true():
    package = _package()
    package["runtime_migration_approved"] = True

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="runtime_migration_approved",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_runtime_migration_active_true():
    package = _package()
    package["runtime_migration_active"] = True

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="runtime_migration_active",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_strategy_runtime_migration_true():
    package = _package()
    package["strategy_runtime_migration"] = True

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="strategy_runtime_migration",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_runtime_use_authorized():
    package = _package()
    package["runtime_use"] = "AUTHORIZED"

    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="runtime_use"):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_strategy_use_authorized():
    package = _package()
    package["strategy_use"] = "AUTHORIZED"

    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="strategy_use"):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_paper_trading_authorized():
    package = _package()
    package["paper_trading"] = "AUTHORIZED"

    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="paper_trading"):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_broker_execution_authorized():
    package = _package()
    package["broker_execution"] = "AUTHORIZED"

    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="broker_execution"):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match=field):
            review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_wrong_artifact_kind():
    package = _package()
    package["artifact_kind"] = "WRONG"

    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="artifact_kind"):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_missing_read_only_discovery_review_digest():
    package = _package()
    package["read_only_discovery_review_package_digest"] = None

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="read_only_discovery_review_package_digest",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_validator_rejects_missing_runtime_review_package_digest():
    package = _package()
    package["runtime_migration_review_package_digest"] = None

    with pytest.raises(
        review.DatasetFileAvailabilityVerificationOperatorReviewError,
        match="runtime_migration_review_package_digest",
    ):
        review.validate_dataset_file_availability_verification_review_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_dataset_file_availability_verification_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed Dataset File Availability Verification",
        "## Verified Files",
        "## Digest Verification Summary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_dataset_file_availability_verification_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.DatasetFileAvailabilityVerificationOperatorReviewError, match="already exists"):
        review.write_dataset_file_availability_verification_review_package_v1(tmp_path)


def test_dataset_file_availability_verification_review_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE
        == "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE"
    )
    assert (
        services.DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY
        == "DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_READY"
    )
    assert services.build_dataset_file_availability_verification_review_package_v1 is review.build_dataset_file_availability_verification_review_package_v1
    assert services.validate_dataset_file_availability_verification_review_package_v1 is review.validate_dataset_file_availability_verification_review_package_v1
    assert services.write_dataset_file_availability_verification_review_package_v1 is review.write_dataset_file_availability_verification_review_package_v1
    assert services.build_dataset_file_availability_verification_review_markdown_v1 is review.build_dataset_file_availability_verification_review_markdown_v1
