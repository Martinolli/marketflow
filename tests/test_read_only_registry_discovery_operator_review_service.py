from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import read_only_registry_discovery_operator_review_service as review
from marketflow.services import read_only_registry_discovery_service as discovery


def _package() -> dict:
    return review.build_read_only_registry_discovery_candidate_review_package_v1()


def _entry(package: dict, profile: str) -> dict:
    return next(item for item in package["registry_entries"] if item["dataset_profile"] == profile)


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.discovery.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["binding_mode"] == review.READ_ONLY_REGISTRY_DISCOVERY_STATUS_BINDING


def test_artifact_kind_is_read_only_registry_discovery_review_package():
    assert (
        _package()["artifact_kind"]
        == review.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == review.READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY


def test_discovery_candidate_digest_is_bound():
    assert (
        _package()["reviewed_discovery_candidate_digest"]
        == review.EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST
    )


def test_registry_entry_count_is_two():
    assert _package()["registry_entry_count"] == 2


def test_dataset_file_count_and_digest_verified_count_are_two():
    package = _package()

    assert package["available_dataset_file_count"] == 2
    assert package["verified_dataset_digest_count"] == 2


def test_manifest_file_count_and_digest_verified_count_are_two():
    package = _package()

    assert package["available_manifest_file_count"] == 2
    assert package["verified_manifest_digest_count"] == 2


def test_missing_file_count_is_zero():
    assert _package()["missing_file_count"] == 0


def test_swing_registry_entry_is_bound():
    entry = _entry(_package(), "SWING")

    assert entry["registry_key"] == discovery.swing_registry.PROPOSED_REGISTRY_KEY
    assert entry["registry_approval_digest"] == discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    assert entry["dataset_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED
    assert entry["manifest_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED


def test_position_swing_registry_entry_is_bound():
    entry = _entry(_package(), "POSITION_SWING")

    assert entry["registry_key"] == discovery.position_registry.PROPOSED_REGISTRY_KEY
    assert (
        entry["registry_approval_digest"]
        == discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert entry["dataset_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED
    assert entry["manifest_file_status"] == discovery.AVAILABLE_DIGEST_VERIFIED


def test_runtime_plan_digest_is_bound():
    assert _package()["runtime_migration_plan_digest"] == discovery.EXPECTED_RUNTIME_MIGRATION_PLAN_DIGEST


def test_runtime_review_package_digest_is_bound():
    assert (
        _package()["runtime_migration_review_package_digest"]
        == discovery.EXPECTED_RUNTIME_MIGRATION_REVIEW_PACKAGE_DIGEST
    )


def test_runtime_migration_approved_remains_false():
    assert _package()["runtime_migration_approved"] is False


def test_runtime_migration_active_remains_false():
    assert _package()["runtime_migration_active"] is False


def test_strategy_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    assert _package()["runtime_use"] == discovery.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    assert _package()["strategy_use"] == discovery.NOT_AUTHORIZED


def test_paper_trading_remains_not_authorized():
    assert _package()["paper_trading"] == discovery.NOT_AUTHORIZED


def test_broker_execution_remains_not_authorized():
    assert _package()["broker_execution"] == discovery.NOT_AUTHORIZED


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


def test_all_checks_pass_for_accepted_discovery():
    assert {item["status"] for item in _package()["review_checklist"]} == {review.PASS}


def test_summary_counts_total_passed_failed_correctly():
    package = _package()
    summary = package["review_summary"]

    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["passed_checks"] == len(review.REQUIRED_CHECK_IDS)
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_operator_assessment"] is True
    assert summary["operator_decision_required_before_next_gate"] is True
    assert summary["software_runtime_migration_authorized"] is False
    assert summary["software_runtime_activation_authorized"] is False


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["read_only_registry_discovery_review_package_digest"] == second[
        "read_only_registry_discovery_review_package_digest"
    ]
    assert (
        first["read_only_registry_discovery_review_package_digest"]
        == review.read_only_registry_discovery_review_package_digest_v1(first)
    )


def test_validator_accepts_valid_review_package():
    validation = review.validate_read_only_registry_discovery_candidate_review_package_v1(_package())

    assert validation["status"] == "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_VALID"
    assert validation["reviewed_discovery_candidate_digest"] == review.EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST
    assert validation["blocker_count"] == 0
    assert validation["runtime_migration_approved"] is False


def test_review_package_can_bind_supplied_discovery_candidate():
    candidate = discovery.build_read_only_registry_discovery_candidate_v1()

    package = review.build_read_only_registry_discovery_candidate_review_package_v1(candidate)

    assert package["binding_mode"] == review.READ_ONLY_REGISTRY_DISCOVERY_OBJECT_BINDING
    assert package["reviewed_discovery_candidate_digest"] == review.EXPECTED_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_DIGEST


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("review_status", "WRONG", "review_status"),
        ("reviewed_discovery_candidate_digest", "0" * 64, "reviewed_discovery_candidate_digest"),
        ("registry_entry_count", 1, "registry_entry_count"),
        ("available_dataset_file_count", 1, "available_dataset_file_count"),
        ("available_manifest_file_count", 1, "available_manifest_file_count"),
        ("verified_dataset_digest_count", 1, "verified_dataset_digest_count"),
        ("verified_manifest_digest_count", 1, "verified_manifest_digest_count"),
        ("missing_file_count", 1, "missing_file_count"),
        ("runtime_migration_review_package_digest", None, "runtime_migration_review_package_digest"),
        ("runtime_migration_plan_digest", None, "runtime_migration_plan_digest"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
        ("automatic_stitching", True, "automatic_stitching"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
    ],
)
def test_validator_rejects_invalid_mutations(field: str, value, match: str):
    package = _package()
    package[field] = value

    with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match=match):
        review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_missing_swing_registry_entry():
    package = _package()
    position_entry = deepcopy(_entry(package, "POSITION_SWING"))
    package["registry_entries"] = [position_entry, deepcopy(position_entry)]

    with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match="missing SWING"):
        review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_missing_position_swing_registry_entry():
    package = _package()
    swing_entry = deepcopy(_entry(package, "SWING"))
    package["registry_entries"] = [swing_entry, deepcopy(swing_entry)]

    with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match="missing POSITION_SWING"):
        review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_dataset_or_manifest_not_verified_when_ready():
    for field in ("dataset_digest_verified", "manifest_digest_verified"):
        package = _package()
        package["registry_entries"] = deepcopy(package["registry_entries"])
        package["registry_entries"][0][field] = False

        with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match=field):
            review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_predictive_and_profitability_accepted():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match=field):
            review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_runtime_activation_status_values():
    for status in ("RUNTIME_MIGRATION_APPROVED", "RUNTIME_MIGRATION_ACTIVE", "STRATEGY_RUNTIME_MIGRATION"):
        package = _package()
        package["review_status"] = status

        with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match=status):
            review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_validator_rejects_mutated_review_package_digest():
    package = _package()
    package["read_only_registry_discovery_review_package_digest"] = "0" * 64

    with pytest.raises(
        review.ReadOnlyRegistryDiscoveryOperatorReviewError,
        match="read_only_registry_discovery_review_package_digest",
    ):
        review.validate_read_only_registry_discovery_candidate_review_package_v1(package)


def test_markdown_writer_includes_required_sections():
    markdown = review.build_read_only_registry_discovery_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed Read-Only Discovery Candidate",
        "## Discovered Registry Entries",
        "## Dataset File Availability",
        "## Digest Verification",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_read_only_registry_discovery_candidate_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.ReadOnlyRegistryDiscoveryOperatorReviewError, match="already exists"):
        review.write_read_only_registry_discovery_candidate_review_package_v1(tmp_path)


def test_read_only_registry_discovery_operator_review_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE
        == "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE"
    )
    assert (
        services.READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY
        == "READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE_REVIEW_PACKAGE_READY"
    )
    assert (
        services.build_read_only_registry_discovery_candidate_review_package_v1
        is review.build_read_only_registry_discovery_candidate_review_package_v1
    )
    assert (
        services.validate_read_only_registry_discovery_candidate_review_package_v1
        is review.validate_read_only_registry_discovery_candidate_review_package_v1
    )
    assert (
        services.write_read_only_registry_discovery_candidate_review_package_v1
        is review.write_read_only_registry_discovery_candidate_review_package_v1
    )
    assert (
        services.build_read_only_registry_discovery_candidate_review_markdown_v1
        is review.build_read_only_registry_discovery_candidate_review_markdown_v1
    )
