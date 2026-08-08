from __future__ import annotations

from pathlib import Path

import pytest

from marketflow.services import swing_registry_approval_service as candidate_service
from marketflow.services import swing_registry_operator_review_service as review


def _package() -> dict:
    return review.build_swing_registry_approval_candidate_review_package_v1()


def _check_ids(package: dict) -> list[str]:
    return [item["check_id"] for item in package["review_checklist"]]


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.registry.swing_freeze.swing.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False
    assert package["binding_mode"] == review.SWING_REGISTRY_CANDIDATE_STATUS_BINDING


def test_artifact_kind_is_swing_registry_review_package():
    assert _package()["artifact_kind"] == review.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE


def test_review_status_is_ready():
    assert _package()["review_status"] == review.SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY


def test_reviewed_registry_candidate_digest_matches_expected():
    assert _package()["reviewed_registry_candidate_digest"] == review.EXPECTED_REGISTRY_CANDIDATE_DIGEST


def test_proposed_registry_key_matches_expected():
    assert _package()["reviewed_proposed_registry_key"] == candidate_service.PROPOSED_REGISTRY_KEY


def test_registry_scope_is_research_dataset():
    assert _package()["reviewed_registry_scope"] == "RESEARCH_DATASET"


def test_runtime_use_is_not_authorized():
    package = _package()

    assert package["reviewed_runtime_use"] == "NOT_AUTHORIZED"
    assert package["runtime_use"] == "NOT_AUTHORIZED"


def test_strategy_use_is_not_authorized():
    package = _package()

    assert package["reviewed_strategy_use"] == "NOT_AUTHORIZED"
    assert package["strategy_use"] == "NOT_AUTHORIZED"


def test_registry_activation_is_false():
    package = _package()

    assert package["reviewed_registry_activation"] is False
    assert package["registry_activation"] is False


def test_registry_approval_created_is_false():
    assert _package()["registry_approval_created"] is False


def test_swing_frozen_digest_matches_expected():
    assert _package()["swing_canonical_dataset_frozen_digest"] == candidate_service.EXPECTED_SWING_FROZEN_DIGEST


def test_dataset_rows_digest_matches_expected():
    assert _package()["dataset_rows_digest"] == candidate_service.EXPECTED_DATASET_ROWS_DIGEST


def test_dataset_manifest_digest_matches_expected():
    assert _package()["dataset_manifest_digest"] == candidate_service.EXPECTED_DATASET_MANIFEST_DIGEST


def test_swing_bar_count_is_expected():
    assert _package()["swing_bar_count"] == 1988


def test_2025_01_cross_check_passed_and_bar_count_matches():
    package = _package()

    assert package["cross_check_2025_01_status"] == "PASSED"
    assert package["cross_check_2025_01_swing_bars"] == 40


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
    assert summary["ready_for_operator_registry_assessment"] is True
    assert summary["operator_decision_required_before_registry_approval"] is True
    assert summary["software_registry_approval_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_canonical_eligibility_remains_false():
    assert _package()["canonical_eligibility"] is False


def test_registry_eligibility_remains_false():
    assert _package()["registry_eligibility"] is False


def test_runtime_migration_remains_false():
    assert _package()["strategy_runtime_migration"] is False


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"


def test_provider_requests_made_in_review_remains_false():
    assert _package()["provider_requests_made_in_review"] is False


def test_no_registry_approved_artifact_or_status_is_produced():
    package = _package()

    assert package["artifact_kind"] != "SWING_REGISTRY_APPROVED"
    assert package["review_status"] != "SWING_REGISTRY_APPROVED"
    assert package["approval_status"] is None


def test_no_registry_activation_is_produced():
    assert _package()["registry_activation"] is False


def test_operator_decision_remains_null_and_not_approved():
    package = _package()

    assert package["operator_decision_required"] is True
    assert package["operator_decision"] is None


def test_approval_fields_remain_null():
    package = _package()

    assert package["operator_approved_by"] is None
    assert package["operator_approval_timestamp"] is None
    assert package["operator_approval_digest"] is None
    assert package["operator_signature"] is None
    assert package["approval_status"] is None


def test_review_package_digest_is_deterministic():
    first = _package()
    second = _package()

    assert first["swing_registry_review_package_semantic_digest"] == second["swing_registry_review_package_semantic_digest"]
    assert first["swing_registry_review_package_semantic_digest"] == review.swing_registry_review_package_semantic_digest_v1(first)


def test_build_can_bind_to_supplied_registry_candidate_object():
    candidate = candidate_service.build_swing_registry_approval_candidate_v1()

    package = review.build_swing_registry_approval_candidate_review_package_v1(candidate)

    assert package["binding_mode"] == review.SWING_REGISTRY_CANDIDATE_OBJECT_BINDING
    assert package["reviewed_registry_candidate_digest"] == review.EXPECTED_REGISTRY_CANDIDATE_DIGEST


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("reviewed_registry_candidate_digest", "0" * 64, "reviewed_registry_candidate_digest"),
        ("reviewed_proposed_registry_key", "AAPL:WRONG", "reviewed_proposed_registry_key"),
        ("reviewed_registry_scope", "RUNTIME_DATASET", "reviewed_registry_scope"),
        ("reviewed_runtime_use", "AUTHORIZED", "reviewed_runtime_use"),
        ("reviewed_strategy_use", "AUTHORIZED", "reviewed_strategy_use"),
        ("reviewed_registry_activation", True, "reviewed_registry_activation"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("registry_activation", True, "registry_activation"),
        ("registry_approval_created", True, "registry_approval_created"),
        ("canonical_eligibility", True, "canonical_eligibility"),
        ("registry_eligibility", True, "registry_eligibility"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("predictive_usefulness", "accepted", "predictive_usefulness"),
        ("profitability", "accepted", "profitability"),
        ("provider_requests_made_in_review", True, "provider_requests_made_in_review"),
        ("swing_canonical_dataset_frozen_digest", "0" * 64, "swing_canonical_dataset_frozen_digest"),
        ("dataset_rows_digest", "0" * 64, "dataset_rows_digest"),
        ("dataset_manifest_digest", "0" * 64, "dataset_manifest_digest"),
        ("swing_bar_count", 1987, "swing_bar_count"),
        ("cross_check_2025_01_status", "FAILED", "cross_check_2025_01_status"),
        ("cross_check_2025_01_swing_bars", 39, "cross_check_2025_01_swing_bars"),
        ("identity_frozen_digest", "0" * 64, "identity_frozen_digest"),
        ("calendar_frozen_digest", "0" * 64, "calendar_frozen_digest"),
        ("schedule_digest", "0" * 64, "schedule_digest"),
        ("split_event_frozen_digest", "0" * 64, "split_event_frozen_digest"),
        ("dividend_event_frozen_digest", "0" * 64, "dividend_event_frozen_digest"),
        ("acquisition_generation_frozen_digest", "0" * 64, "acquisition_generation_frozen_digest"),
        ("in_range_dividend_implication", None, "in_range_dividend_implication"),
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("review_status", "WRONG", "review_status"),
    ],
)
def test_validator_rejects_invalid_mutations(field: str, value, match: str):
    package = _package()
    package[field] = value

    with pytest.raises(review.SwingRegistryOperatorReviewError, match=match):
        review.validate_swing_registry_approval_candidate_review_package_v1(package)


def test_validator_rejects_registry_approved_artifact_or_status():
    for field in ("artifact_kind", "review_status", "approval_status"):
        package = _package()
        package[field] = "SWING_REGISTRY_APPROVED"

        with pytest.raises(review.SwingRegistryOperatorReviewError, match="SWING_REGISTRY_APPROVED"):
            review.validate_swing_registry_approval_candidate_review_package_v1(package)


def test_validator_rejects_populated_approval_fields():
    for field in (
        "operator_approved_by",
        "operator_approval_timestamp",
        "operator_approval_digest",
        "operator_signature",
    ):
        package = _package()
        package[field] = "not-null"

        with pytest.raises(review.SwingRegistryOperatorReviewError, match=field):
            review.validate_swing_registry_approval_candidate_review_package_v1(package)


def test_validator_rejects_mutated_digest_field():
    package = _package()
    package["swing_registry_review_package_semantic_digest"] = "0" * 64

    with pytest.raises(review.SwingRegistryOperatorReviewError, match="swing_registry_review_package_semantic_digest"):
        review.validate_swing_registry_approval_candidate_review_package_v1(package)


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _package()["remaining_roadmap"]

    assert roadmap == review.REMAINING_ROADMAP
    assert "Digest-bound SWING registry approval ceremony." in roadmap
    assert "POSITION_SWING canonical dataset candidate." in roadmap
    assert "POSITION_SWING canonical dataset operator review/freeze." in roadmap
    assert "POSITION_SWING registry approval chain." in roadmap
    assert "Normal runtime migration." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_swing_registry_approval_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed Registry Candidate",
        "## Proposed Registry Entry",
        "## Frozen SWING Dataset Evidence",
        "## Dataset Summary",
        "## Registry Boundary",
        "## Authority Bindings",
        "## Checklist Summary",
        "## Remaining Required Tasks",
        "## Guardrails",
    ):
        assert section in markdown
    assert "No `SWING_REGISTRY_APPROVED` artifact or status is created." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path: Path):
    result = review.write_swing_registry_approval_candidate_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.SwingRegistryOperatorReviewError, match="already exists"):
        review.write_swing_registry_approval_candidate_review_package_v1(tmp_path)


def test_registry_review_service_exports_are_public():
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE
        == "SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE"
    )
    assert (
        services.SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY
        == "SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY"
    )
    assert services.build_swing_registry_approval_candidate_review_package_v1 is review.build_swing_registry_approval_candidate_review_package_v1
    assert services.validate_swing_registry_approval_candidate_review_package_v1 is review.validate_swing_registry_approval_candidate_review_package_v1
    assert services.write_swing_registry_approval_candidate_review_package_v1 is review.write_swing_registry_approval_candidate_review_package_v1
    assert services.build_swing_registry_approval_candidate_review_markdown_v1 is review.build_swing_registry_approval_candidate_review_markdown_v1
