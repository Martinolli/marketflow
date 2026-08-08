from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import position_swing_canonical_dataset_operator_review_service as review


def _package() -> dict:
    return review.build_position_swing_canonical_dataset_candidate_review_package_v1()


def _evidence(package: dict) -> dict:
    return package["reviewed_position_swing_candidate_evidence"]


def _check_ids(package: dict) -> list[str]:
    return [item["check_id"] for item in package["review_checklist"]]


def test_review_package_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(review.position.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    package = _package()

    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_artifact_kind_is_position_swing_review_package():
    assert (
        _package()["artifact_kind"]
        == review.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE
    )


def test_review_status_is_ready():
    assert _package()["review_status"] == review.POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY


def test_reviewed_position_swing_candidate_digest_matches_expected():
    assert _evidence(_package())["reviewed_candidate_digest"] == review.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST


def test_dataset_rows_digest_matches_expected():
    assert _evidence(_package())["reviewed_dataset_rows_digest"] == review.EXPECTED_POSITION_SWING_DATASET_ROWS_DIGEST


def test_dataset_manifest_digest_matches_expected():
    assert (
        _evidence(_package())["reviewed_dataset_manifest_digest"]
        == review.EXPECTED_POSITION_SWING_DATASET_MANIFEST_DIGEST
    )


def test_source_rows_digest_matches_expected():
    assert _evidence(_package())["reviewed_source_rows_digest"] == review.EXPECTED_SOURCE_ROWS_DIGEST


def test_materialization_receipt_digest_matches_expected():
    assert (
        _evidence(_package())["reviewed_materialization_receipt_digest"]
        == review.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST
    )


def test_position_swing_bar_count_is_expected():
    assert _evidence(_package())["position_swing_bar_count"] == 994


def test_source_rth_consumed_and_excluded_are_expected():
    evidence = _evidence(_package())

    assert evidence["source_rth_rows_consumed"] == 25844
    assert evidence["source_rth_rows_excluded"] == 126


def test_full_sessions_used_is_expected():
    assert _evidence(_package())["full_sessions_used"] == 994


def test_special_sessions_excluded_is_expected():
    assert _evidence(_package())["special_sessions_excluded"] == 9


def test_special_session_rows_excluded_is_expected():
    assert _evidence(_package())["special_session_rows_excluded"] == 126


def test_2025_01_cross_check_passed():
    assert _evidence(_package())["cross_check_status"] == "PASSED"


def test_2025_01_position_swing_bars_are_expected():
    assert _evidence(_package())["cross_check_position_swing_bars"] == 20


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
    assert summary["operator_decision_required_before_freeze"] is True
    assert summary["software_freeze_authorized"] is False
    assert summary["registry_approval_authorized"] is False
    assert summary["runtime_migration_authorized"] is False


def test_position_swing_canonical_dataset_frozen_remains_false():
    package = _package()

    assert package["position_swing_canonical_dataset_frozen"] is False
    assert package["authority_boundary"]["position_swing_canonical_dataset_frozen"] is False


def test_position_swing_registry_approval_created_remains_false():
    package = _package()

    assert package["position_swing_registry_approval_created"] is False
    assert package["authority_boundary"]["position_swing_registry_approval_created"] is False


def test_position_swing_registry_eligibility_remains_false():
    package = _package()

    assert package["position_swing_registry_eligibility"] is False
    assert package["authority_boundary"]["position_swing_registry_eligibility"] is False


def test_runtime_migration_remains_false():
    package = _package()

    assert package["strategy_runtime_migration"] is False
    assert package["authority_boundary"]["strategy_runtime_migration"] is False


def test_runtime_use_remains_not_authorized():
    package = _package()

    assert package["runtime_use"] == review.position.NOT_AUTHORIZED
    assert package["authority_boundary"]["runtime_use"] == review.position.NOT_AUTHORIZED


def test_strategy_use_remains_not_authorized():
    package = _package()

    assert package["strategy_use"] == review.position.NOT_AUTHORIZED
    assert package["authority_boundary"]["strategy_use"] == review.position.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_remain_not_accepted():
    package = _package()

    assert package["predictive_usefulness"] == "not accepted"
    assert package["profitability"] == "not accepted"
    assert package["authority_boundary"]["predictive_usefulness"] == "not accepted"
    assert package["authority_boundary"]["profitability"] == "not accepted"


def test_provider_requests_made_in_review_remains_false():
    assert _package()["provider_requests_made_in_review"] is False


def test_no_position_swing_frozen_artifact_or_status_is_produced():
    package = _package()

    assert package["artifact_kind"] != "POSITION_SWING_CANONICAL_DATASET_FROZEN"
    assert package["review_status"] != "POSITION_SWING_CANONICAL_DATASET_FROZEN"
    assert package["freeze_status"] is None
    assert package["position_swing_canonical_dataset_frozen_artifact_created"] is False


def test_no_registry_approval_is_produced():
    package = _package()

    assert package["position_swing_registry_approval_created"] is False
    assert "POSITION_SWING_REGISTRY_APPROVED" not in repr(package)


def test_operator_decision_and_freeze_fields_remain_null():
    package = _package()

    assert package["operator_decision"] is None
    assert package["operator_approved_by"] is None
    assert package["operator_freeze_timestamp"] is None
    assert package["operator_freeze_digest"] is None
    assert package["operator_signature"] is None


def test_review_package_digest_is_deterministic():
    assert (
        _package()["position_swing_canonical_dataset_review_package_semantic_digest"]
        == _package()["position_swing_canonical_dataset_review_package_semantic_digest"]
    )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("reviewed_candidate_digest", "0" * 64, "reviewed_candidate_digest"),
        ("reviewed_dataset_rows_digest", "0" * 64, "reviewed_dataset_rows_digest"),
        ("reviewed_dataset_manifest_digest", "0" * 64, "reviewed_dataset_manifest_digest"),
        ("reviewed_source_rows_digest", "0" * 64, "reviewed_source_rows_digest"),
        ("reviewed_materialization_receipt_digest", "0" * 64, "reviewed_materialization_receipt_digest"),
        ("position_swing_bar_count", 993, "position_swing_bar_count"),
        ("cross_check_position_swing_bars", 19, "cross_check_position_swing_bars"),
    ],
)
def test_validator_rejects_modified_reviewed_evidence(field: str, value, match: str):
    package = _package()
    package["reviewed_position_swing_candidate_evidence"][field] = value

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match=match):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_2025_01_cross_check_not_passed():
    package = _package()
    package["reviewed_position_swing_candidate_evidence"]["cross_check_status"] = "FAILED"

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="cross_check_status"):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_missing_dividend_implication():
    package = _package()
    package["authority_bindings"]["in_range_dividend_implication"] = None

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="authority_bindings"):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


@pytest.mark.parametrize(
    "field",
    [
        "canonical_dataset_frozen",
        "canonical_eligibility",
        "registry_eligibility",
        "position_swing_canonical_dataset_frozen",
        "position_swing_registry_approval_created",
        "position_swing_registry_eligibility",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_validator_rejects_forbidden_true_flags(field: str):
    package = _package()
    package[field] = True

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match=field):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_position_swing_registry_eligibility_true_in_boundary():
    package = _package()
    package["authority_boundary"]["position_swing_registry_eligibility"] = True

    with pytest.raises(
        review.PositionSwingCanonicalDatasetOperatorReviewError,
        match="position_swing_registry_eligibility",
    ):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_runtime_use_authorized():
    package = _package()
    package["runtime_use"] = "AUTHORIZED"

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="runtime_use"):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_strategy_use_authorized():
    package = _package()
    package["strategy_use"] = "AUTHORIZED"

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="strategy_use"):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_accepted_predictive_or_profitability():
    for field in ("predictive_usefulness", "profitability"):
        package = _package()
        package[field] = "accepted"

        with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match=field):
            review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_provider_requests_made_in_review():
    package = _package()
    package["provider_requests_made_in_review"] = True

    with pytest.raises(
        review.PositionSwingCanonicalDatasetOperatorReviewError,
        match="provider_requests_made_in_review",
    ):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_frozen_artifact_or_status():
    for field in ("artifact_kind", "review_status", "freeze_status"):
        package = _package()
        package[field] = "POSITION_SWING_CANONICAL_DATASET_FROZEN"

        with pytest.raises(
            review.PositionSwingCanonicalDatasetOperatorReviewError,
            match="POSITION_SWING_CANONICAL_DATASET_FROZEN|freeze_status",
        ):
            review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_validator_rejects_registry_approval_present():
    package = _package()
    package["registry_approval_created"] = True

    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="registry_approval_created"):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_remaining_roadmap_contains_required_future_work():
    roadmap = _package()["remaining_roadmap"]

    assert "Digest-bound POSITION_SWING canonical dataset operator freeze ceremony." in roadmap
    assert "POSITION_SWING registry approval candidate." in roadmap
    assert "POSITION_SWING registry operator review package." in roadmap
    assert "POSITION_SWING registry approval ceremony." in roadmap
    assert "Normal runtime migration planning." in roadmap
    assert "Applicability/research campaign." in roadmap
    assert "Predictive and profitability evaluation." in roadmap


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = review.build_position_swing_canonical_dataset_candidate_review_markdown_v1(_package())

    for section in (
        "## Title",
        "## Reviewed POSITION_SWING Candidate",
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
    assert "No `POSITION_SWING_CANONICAL_DATASET_FROZEN` artifact or status is created." in markdown


def test_write_review_package_writes_json_without_overwrite(tmp_path):
    result = review.write_position_swing_canonical_dataset_candidate_review_package_v1(tmp_path)

    assert result["artifact_kind"] == review.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE
    assert result["payload_sha256"]
    with pytest.raises(review.PositionSwingCanonicalDatasetOperatorReviewError, match="already exists"):
        review.write_position_swing_canonical_dataset_candidate_review_package_v1(tmp_path)


def test_validator_rejects_mutated_digest_field():
    package = _package()
    package["position_swing_canonical_dataset_review_package_semantic_digest"] = "0" * 64

    with pytest.raises(
        review.PositionSwingCanonicalDatasetOperatorReviewError,
        match="position_swing_canonical_dataset_review_package_semantic_digest",
    ):
        review.validate_position_swing_canonical_dataset_candidate_review_package_v1(package)


def test_local_ignored_dataset_manifest_and_candidate_are_verified_when_available():
    package = _package()
    binding = package["local_artifact_binding"]

    assert binding["candidate_file_available"] is True
    assert binding["candidate_file_verified"] is True
    assert binding["manifest_file_available"] is True
    assert binding["manifest_file_verified"] is True
    assert binding["dataset_file_available"] is True
    assert binding["dataset_file_verified"] is True
    assert binding["dataset_row_count"] == 994


def test_build_uses_status_binding_by_default():
    package = _package()

    assert package["binding_mode"] == review.POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING
    assert _evidence(package)["reviewed_candidate_digest"] == review.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST


def test_build_from_candidate_object_uses_object_binding():
    candidate_path = review.DEFAULT_POSITION_SWING_CANDIDATE_PATH
    candidate = review.json.loads(candidate_path.read_text(encoding="utf-8"))

    package = review.build_position_swing_canonical_dataset_candidate_review_package_v1(deepcopy(candidate))

    assert package["binding_mode"] == review.POSITION_SWING_CANONICAL_DATASET_CANDIDATE_OBJECT_BINDING
    assert _evidence(package)["reviewed_candidate_digest"] == review.EXPECTED_POSITION_SWING_CANDIDATE_DIGEST
