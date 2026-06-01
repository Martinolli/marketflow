from __future__ import annotations

from copy import deepcopy

from marketflow.services.parameter_profile_service import (
    CONSERVATIVE_RESEARCH_PROFILE,
    DAILY_SWING_PROFILE,
    FAST_TEST_PROFILE,
    INTRADAY_TACTICAL_PROFILE,
    LOW_TIMEFRAME_REVIEW_PROFILE,
    PARAMETER_PROFILES,
    POSTURE_ALLOWED,
    build_parameter_context_from_profile,
    build_session_update_from_profile,
    get_parameter_profile,
    get_timeframe_posture,
    list_parameter_profiles,
    parameter_profile_summary_rows,
    validate_parameter_profile,
)


EXPECTED_PROFILE_NAMES = {
    FAST_TEST_PROFILE,
    DAILY_SWING_PROFILE,
    INTRADAY_TACTICAL_PROFILE,
    CONSERVATIVE_RESEARCH_PROFILE,
    LOW_TIMEFRAME_REVIEW_PROFILE,
}


def test_list_profiles_returns_expected_names():
    profiles = list_parameter_profiles()

    assert {profile["name"] for profile in profiles} == EXPECTED_PROFILE_NAMES


def test_returned_profiles_are_deep_copies():
    result = get_parameter_profile(FAST_TEST_PROFILE)
    assert result["success"] is True

    result["profile"]["guardrails"].append("mutated")
    result["profile"]["timeframe_posture"]["1d"] = "mutated"

    summary_rows = parameter_profile_summary_rows()
    summary_rows[0]["guardrails"].append("summary_mutated")

    assert "mutated" not in PARAMETER_PROFILES[FAST_TEST_PROFILE]["guardrails"]
    assert PARAMETER_PROFILES[FAST_TEST_PROFILE]["timeframe_posture"]["1d"] == "preferred"
    assert "summary_mutated" not in PARAMETER_PROFILES[FAST_TEST_PROFILE]["guardrails"]


def test_get_default_profile():
    result = get_parameter_profile()

    assert result["success"] is True
    assert result["profile"]["name"] == FAST_TEST_PROFILE


def test_unknown_profile_returns_safe_error():
    result = get_parameter_profile("missing_profile")

    assert result["success"] is False
    assert result["profile"] is None
    assert result["errors"] == ["Unknown parameter profile: missing_profile"]


def test_validate_built_in_profiles():
    for profile in PARAMETER_PROFILES.values():
        result = validate_parameter_profile(profile)
        assert result["success"] is True


def test_validation_catches_missing_required_field():
    profile = deepcopy(PARAMETER_PROFILES[FAST_TEST_PROFILE])
    profile.pop("monte_carlo_horizon")

    result = validate_parameter_profile(profile)

    assert result["success"] is False
    assert "Missing required profile field: monte_carlo_horizon" in result["errors"]


def test_validation_catches_horizon_mismatch():
    profile = deepcopy(PARAMETER_PROFILES[FAST_TEST_PROFILE])
    profile["monte_carlo_horizon"] = profile["backtest_horizon"] + 1

    result = validate_parameter_profile(profile)

    assert result["success"] is False
    assert "Monte Carlo horizon must match Backtest Outcome horizon." in result["errors"]


def test_validation_catches_invalid_posture():
    profile = deepcopy(PARAMETER_PROFILES[FAST_TEST_PROFILE])
    profile["timeframe_posture"]["1d"] = "unsupported"

    result = validate_parameter_profile(profile)

    assert result["success"] is False
    assert "Unsupported timeframe posture for 1d: unsupported" in result["errors"]


def test_build_parameter_context():
    result = build_parameter_context_from_profile(INTRADAY_TACTICAL_PROFILE)

    assert result["success"] is True
    assert result["parameter_context"]["eigen_window"] == 80
    assert result["parameter_context"]["backtest_horizon"] == 60
    assert result["parameter_context"]["monte_carlo_horizon"] == 60
    assert result["data_sufficiency_context"] == result["parameter_context"]
    assert result["monte_carlo_context"]["horizon"] == 60
    assert result["monte_carlo_context"]["paths"] == 30000
    assert result["monte_carlo_context"]["block_len"] == 12


def test_build_session_update():
    result = build_session_update_from_profile(DAILY_SWING_PROFILE)

    assert result["success"] is True
    assert result["session_updates"]["backtest_outcome_horizon_bars"] == 20
    assert result["session_updates"]["monte_carlo_horizon_bars"] == 20
    assert result["session_updates"]["monte_carlo_paths"] == 30000


def test_timeframe_posture_preferred():
    result = get_timeframe_posture(INTRADAY_TACTICAL_PROFILE, "30m")

    assert result["success"] is True
    assert result["posture"] == "preferred"
    assert result["is_preferred"] is True
    assert result["warning"] is None


def test_timeframe_posture_review_only():
    result = get_timeframe_posture(INTRADAY_TACTICAL_PROFILE, "5m")

    assert result["success"] is True
    assert result["posture"] == "review_only"
    assert result["is_review_only"] is True
    assert result["warning"] == "Timeframe is review-only for this profile."


def test_timeframe_posture_avoid():
    result = get_timeframe_posture(LOW_TIMEFRAME_REVIEW_PROFILE, "1d")

    assert result["success"] is True
    assert result["posture"] == "avoid"
    assert result["warning"] == "Timeframe is not recommended for this profile."


def test_missing_timeframe_posture_returns_warning():
    result = get_timeframe_posture(INTRADAY_TACTICAL_PROFILE, None)

    assert result["success"] is True
    assert result["posture"] is None
    assert result["warning"] == "Timeframe is missing."


def test_unknown_timeframe_posture_returns_warning():
    result = get_timeframe_posture(INTRADAY_TACTICAL_PROFILE, "10m")

    assert result["success"] is True
    assert result["posture"] is None
    assert result["warning"] == "Unknown timeframe for this profile: 10m"


def test_no_mutation_of_profile_templates_by_context_session_builders():
    before = deepcopy(PARAMETER_PROFILES)

    context = build_parameter_context_from_profile(INTRADAY_TACTICAL_PROFILE)
    context["parameter_context"]["eigen_window"] = 999
    context["monte_carlo_context"]["paths"] = 999

    session_update = build_session_update_from_profile(INTRADAY_TACTICAL_PROFILE)
    session_update["session_updates"]["monte_carlo_paths"] = 999

    assert PARAMETER_PROFILES == before


def test_all_built_in_profiles_keep_mc_horizon_equal_to_backtest_horizon():
    for profile in PARAMETER_PROFILES.values():
        assert profile["monte_carlo_horizon"] == profile["backtest_horizon"]


def test_validate_warns_for_low_timeframe_posture_not_cautious():
    profile = deepcopy(PARAMETER_PROFILES[FAST_TEST_PROFILE])
    profile["timeframe_posture"]["5m"] = POSTURE_ALLOWED

    result = validate_parameter_profile(profile)

    assert result["success"] is True
    assert "5m posture should be review_only, caution, or avoid." in result["warnings"]
