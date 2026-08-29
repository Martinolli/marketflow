from copy import deepcopy
import json

import pytest

from marketflow.services import marketflow_repository_tag_push_results_review_service as service


@pytest.fixture
def snapshot():
    return service.approved_marketflow_repository_tag_push_results_review_git_snapshot_v1()


@pytest.fixture
def review(snapshot):
    return service.build_marketflow_repository_tag_push_results_review_v1(git_snapshot=snapshot)


def test_review_builds_offline_deterministically(snapshot, review):
    assert service.build_marketflow_repository_tag_push_results_review_v1(git_snapshot=snapshot) == review


def test_review_can_use_read_only_snapshot_loader(monkeypatch, snapshot):
    monkeypatch.setattr(service, "_read_git_snapshot", lambda _root: deepcopy(snapshot))
    result = service.build_marketflow_repository_tag_push_results_review_v1()
    assert result["review_status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY


def test_injected_snapshot_does_not_invoke_git(monkeypatch, snapshot):
    monkeypatch.setattr(service, "_read_git_snapshot", lambda _root: pytest.fail("Git invoked"))
    assert service.build_marketflow_repository_tag_push_results_review_v1(git_snapshot=snapshot)["remote_tags_reviewed"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1),
        ("review_status", service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_READY),
        ("review_scope", service.REPOSITORY_TAG_PUSH_RESULTS_REVIEW_ONLY_NOT_ADDITIONAL_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN),
        ("source_tag_push_execution_digest", service.EXPECTED_SOURCE_EXECUTION_DIGEST),
        ("source_remote_tag_manifest_digest", service.EXPECTED_SOURCE_REMOTE_TAG_MANIFEST_DIGEST),
        ("source_tag_push_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("source_tag_push_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_tag_push_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_final_archive_digest", service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST),
        ("source_records_digest", service.EXPECTED_SOURCE_RECORDS_DIGEST),
        ("origin_main_commit_before_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_after_execution", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("origin_main_commit_at_review", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_execution_commit", service.EXPECTED_SOURCE_EXECUTION_COMMIT),
        ("repository_tag_push_results_review_created", True),
        ("repository_tag_push_results_review_ready", True),
        ("remote_tags_reviewed", True),
        ("remote_tag_targets_reviewed", True),
        ("remote_tag_objects_reviewed", True),
        ("remote_tag_manifest_reviewed", True),
        ("ready_for_repository_merge_strategy_candidate", True),
        ("additional_tag_push_performed", False),
        ("repository_tags_pushed_again", False),
        ("additional_tags_created", False),
        ("tags_modified", False),
        ("tags_deleted", False),
        ("git_merge_performed", False),
        ("git_rebase_performed", False),
        ("git_branch_delete_performed", False),
        ("git_remote_delete_performed", False),
        ("git_main_push_performed", False),
        ("git_force_push_performed", False),
        ("git_remote_prune_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("provider_requests_made_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_review_fields(review, field, expected):
    assert review[field] == expected


def test_remote_tag_review_records_match(review):
    records = review["remote_tag_review_records"]
    assert [row["tag_name"] for row in records] == [row["tag_name"] for row in service.EXPECTED_TAGS]
    assert [row["observed_remote_tag_object_sha"] for row in records] == [row["local_tag_object_sha"] for row in service.EXPECTED_TAGS]
    assert [row["observed_remote_peeled_target_commit"] for row in records] == [row["target_commit"] for row in service.EXPECTED_TAGS]
    assert all(row["remote_ref_exists"] for row in records)
    assert all(row["remote_tag_object_sha_verified"] for row in records)
    assert all(row["remote_peeled_target_commit_verified"] for row in records)
    assert all(row["local_tag_still_matches_source"] for row in records)
    assert all(row["tag_message_verified_locally"] for row in records)


def test_remote_tag_count_review(review):
    assert review["remote_tag_count_review"] == {
        "remote_candidate_namespace_tag_count_before_source_push": 0,
        "remote_candidate_namespace_tag_count_after_source_push": 4,
        "remote_candidate_namespace_tag_count_at_review": 4,
        "remote_approved_tag_count_at_review": 4,
        "verified_remote_terminal_tag_count": 4,
        "extra_remote_candidate_namespace_tag_count_at_review": 0,
        "remote_tag_count_observation_note": "Four approved remote tags verified; no extra namespace tags observed.",
    }


def test_tag_message_review(review):
    assert len(review["tag_message_review"]) == 6
    assert all(review["tag_message_review"].values())


def test_remote_publication_review(review):
    assert review["remote_publication_review"] == {
        "remote_publication_review_status": "VERIFIED_REMOTE_PUBLICATION_COMPLETE",
        "explicit_refspec_push_confirmed_from_source": True,
        "push_all_tags_not_used": True,
        "branch_push_not_used": True,
        "main_push_not_used": True,
        "force_push_not_used": True,
        "origin_main_unchanged": True,
    }


def test_next_chain_gates_and_risks(review):
    assert review["next_chain"] == service.NEXT_CHAIN
    assert review["next_gates"] == service.NEXT_GATES
    assert review["risk_controls"] == service.RISK_CONTROLS
    assert review["recommended_next_task"] == "MARKETFLOW_REPOSITORY_MERGE_STRATEGY_CANDIDATE_V1"


def test_checklist_passes(review):
    assert [row["check_id"] for row in review["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in review["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in review["checklist"])
    assert review["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert review["summary"]["failed_checks"] == 0
    assert review["summary"]["blocker_count"] == 0


def test_digests_are_deterministic(review):
    assert review["marketflow_repository_tag_push_results_review_digest"] == service.marketflow_repository_tag_push_results_review_digest_v1(review)
    assert review["marketflow_repository_tag_push_results_review_remote_tag_manifest_digest"] == service.marketflow_repository_tag_push_results_review_remote_tag_manifest_digest_v1(review)


def test_validator_accepts_review(review):
    result = service.validate_marketflow_repository_tag_push_results_review_v1(review)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_VALID
    assert result["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "bad_value"),
    [
        (("artifact_kind",), "WRONG"), (("review_status",), "WRONG"),
        (("review_scope",), "WRONG"), (("source_tag_push_execution_digest",), "0" * 64),
        (("source_remote_tag_manifest_digest",), "0" * 64),
        (("source_tag_push_approval_digest",), "0" * 64),
        (("origin_main_commit_before_execution",), "0" * 40),
        (("origin_main_commit_after_execution",), "0" * 40),
        (("origin_main_commit_at_review",), "0" * 40),
        (("repository_tag_push_results_review_created",), False),
        (("repository_tag_push_results_review_ready",), False),
        (("remote_tags_reviewed",), False), (("remote_tag_targets_reviewed",), False),
        (("remote_tag_objects_reviewed",), False), (("remote_tag_manifest_reviewed",), False),
        (("ready_for_repository_merge_strategy_candidate",), False),
        (("remote_tag_count_review", "remote_candidate_namespace_tag_count_at_review"), 3),
        (("remote_tag_count_review", "remote_approved_tag_count_at_review"), 3),
        (("remote_tag_count_review", "verified_remote_terminal_tag_count"), 3),
        (("remote_tag_count_review", "extra_remote_candidate_namespace_tag_count_at_review"), 1),
        (("remote_tag_review_records", 0, "tag_name"), "wrong"),
        (("remote_tag_review_records", 0, "observed_remote_tag_object_sha"), "0" * 40),
        (("remote_tag_review_records", 0, "observed_remote_peeled_target_commit"), "0" * 40),
        (("remote_tag_review_records", 0, "local_tag_object_sha"), "0" * 40),
        (("remote_tag_review_records", 0, "tag_message_verified_locally"), False),
        (("remote_publication_review", "remote_publication_review_status"), "WRONG"),
        (("remote_publication_review", "push_all_tags_not_used"), False),
        (("remote_publication_review", "branch_push_not_used"), False),
        (("remote_publication_review", "main_push_not_used"), False),
        (("remote_publication_review", "force_push_not_used"), False),
        (("additional_tag_push_performed",), True), (("repository_tags_pushed_again",), True),
        (("additional_tags_created",), True), (("tags_modified",), True),
        (("tags_deleted",), True), (("git_merge_performed",), True),
        (("git_rebase_performed",), True), (("git_branch_delete_performed",), True),
        (("git_remote_delete_performed",), True), (("git_remote_prune_performed",), True),
        (("origin_main_modified_by_this_task",), True), (("provider_requests_made_in_review",), True),
        (("market_data_acquisition_performed_in_review",), True),
        (("dataset_generation_performed_in_review",), True),
        (("metric_recomputation_from_raw_rows_performed",), True),
        (("model_training_performed",), True), (("strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True), (("predictive_usefulness_accepted",), True),
        (("profitability_accepted",), True), (("runtime_use",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"), (("risk_controls",), []),
    ],
)
def test_validator_rejects_mutations(review, path, bad_value):
    changed = deepcopy(review)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(service.MarketFlowRepositoryTagPushResultsReviewError):
        service.validate_marketflow_repository_tag_push_results_review_v1(changed)


@pytest.mark.parametrize(
    "field",
    ["marketflow_repository_tag_push_results_review_digest",
     "marketflow_repository_tag_push_results_review_remote_tag_manifest_digest"],
)
def test_validator_rejects_missing_digests(review, field):
    changed = deepcopy(review)
    changed.pop(field)
    with pytest.raises(service.MarketFlowRepositoryTagPushResultsReviewError):
        service.validate_marketflow_repository_tag_push_results_review_v1(changed)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda snapshot: snapshot.update(origin_main_commit="0" * 40),
        lambda snapshot: snapshot["remote_tags"].pop(service.EXPECTED_REMOTE_REFS[0]),
        lambda snapshot: snapshot["remote_tags"].update({"refs/tags/marketflow/expectancy-lab/extra/v1": {"object_sha": "0" * 40, "peeled_target": "1" * 40}}),
        lambda snapshot: snapshot["remote_tags"][service.EXPECTED_REMOTE_REFS[0]].update(object_sha="0" * 40),
        lambda snapshot: snapshot["remote_tags"][service.EXPECTED_REMOTE_REFS[0]].update(peeled_target="0" * 40),
        lambda snapshot: snapshot["local_tags"][service.EXPECTED_TAGS[0]["tag_name"]].update(object_type="commit"),
        lambda snapshot: snapshot["local_tags"][service.EXPECTED_TAGS[0]["tag_name"]].update(object_sha="0" * 40),
        lambda snapshot: snapshot["local_tags"][service.EXPECTED_TAGS[0]["tag_name"]].update(target_commit="0" * 40),
        lambda snapshot: snapshot["local_tags"][service.EXPECTED_TAGS[0]["tag_name"]].update(message="missing boundaries"),
        lambda snapshot: snapshot.update(tracked_marketflow_file_count=1),
    ],
)
def test_snapshot_mismatches_return_blocked(snapshot, mutation):
    mutation(snapshot)
    result = service.build_marketflow_repository_tag_push_results_review_v1(git_snapshot=snapshot)
    assert result["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED
    assert result["review_status"] == service.MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_BLOCKED_REMOTE_TAG_MISMATCH_OR_ORIGIN_MAIN_CHANGE
    assert result["additional_tag_push_performed"] is False


def test_writer_round_trip(tmp_path, snapshot):
    result = service.write_marketflow_repository_tag_push_results_review_v1(tmp_path, git_snapshot=snapshot)
    payload = json.loads((tmp_path / "marketflow_repository_tag_push_results_review_v1.json").read_text(encoding="utf-8"))
    assert result["marketflow_repository_tag_push_results_review_digest"] == payload["marketflow_repository_tag_push_results_review_digest"]
    assert len(result["payload_sha256"]) == 64


def test_writer_refuses_overwrite(tmp_path, snapshot):
    service.write_marketflow_repository_tag_push_results_review_v1(tmp_path, git_snapshot=snapshot)
    with pytest.raises(service.MarketFlowRepositoryTagPushResultsReviewError):
        service.write_marketflow_repository_tag_push_results_review_v1(tmp_path, git_snapshot=snapshot)


def test_writer_refuses_blocked_review(tmp_path, snapshot):
    snapshot["origin_main_commit"] = "0" * 40
    with pytest.raises(service.MarketFlowRepositoryTagPushResultsReviewError):
        service.write_marketflow_repository_tag_push_results_review_v1(tmp_path, git_snapshot=snapshot)


def test_markdown_contains_required_sections(review):
    markdown = service.build_marketflow_repository_tag_push_results_review_markdown_v1(review)
    for section in (
        "Title", "MarketFlow Repository Tag Push Results Review v1",
        "Source Tag Push Execution", "Bound Evidence", "Repository Context",
        "Review Scope", "Remote Tag Review", "Remote Tag Count Review",
        "Tag Message Review", "Remote Publication Review", "Origin/Main Protection",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ):
        assert section in markdown
