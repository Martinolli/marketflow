from __future__ import annotations

from copy import deepcopy
from typing import Any


FAST_TEST_PROFILE = "fast_test"
DAILY_SWING_PROFILE = "daily_swing"
INTRADAY_TACTICAL_PROFILE = "intraday_tactical"
CONSERVATIVE_RESEARCH_PROFILE = "conservative_research"
LOW_TIMEFRAME_REVIEW_PROFILE = "low_timeframe_review"

DEFAULT_PROFILE_NAME = FAST_TEST_PROFILE

POSTURE_PREFERRED = "preferred"
POSTURE_ALLOWED = "allowed"
POSTURE_CAUTION = "caution"
POSTURE_REVIEW_ONLY = "review_only"
POSTURE_AVOID = "avoid"

VALID_POSTURES = {
    POSTURE_PREFERRED,
    POSTURE_ALLOWED,
    POSTURE_CAUTION,
    POSTURE_REVIEW_ONLY,
    POSTURE_AVOID,
}

PARAMETER_PROFILES: dict[str, dict[str, Any]] = {
    FAST_TEST_PROFILE: {
        "name": FAST_TEST_PROFILE,
        "label": "Fast Test",
        "description": "Quick app/runtime validation only.",
        "purpose": "quick app testing and sanity checks",
        "eigen_window": 40,
        "backtest_horizon": 20,
        "monte_carlo_horizon": 20,
        "monte_carlo_paths": 10000,
        "monte_carlo_block_len": 8,
        "minimum_rows_floor": 100,
        "timeframe_posture": {
            "1mo": POSTURE_CAUTION,
            "1w": POSTURE_ALLOWED,
            "1d": POSTURE_PREFERRED,
            "4h": POSTURE_PREFERRED,
            "2h": POSTURE_ALLOWED,
            "1h": POSTURE_ALLOWED,
            "30m": POSTURE_CAUTION,
            "15m": POSTURE_CAUTION,
            "5m": POSTURE_REVIEW_ONLY,
            "1m": POSTURE_REVIEW_ONLY,
        },
        "guardrails": [
            "runtime_validation_only",
            "not_for_serious_calibration_conclusions",
        ],
    },
    DAILY_SWING_PROFILE: {
        "name": DAILY_SWING_PROFILE,
        "label": "Daily / Swing",
        "description": "Daily and 4h swing-oriented analysis.",
        "purpose": "1d and 4h swing context",
        "eigen_window": 80,
        "backtest_horizon": 20,
        "monte_carlo_horizon": 20,
        "monte_carlo_paths": 30000,
        "monte_carlo_block_len": 10,
        "minimum_rows_floor": 150,
        "preferred_timeframes": ["1d", "4h"],
        "timeframe_posture": {
            "1mo": POSTURE_CAUTION,
            "1w": POSTURE_ALLOWED,
            "1d": POSTURE_PREFERRED,
            "4h": POSTURE_PREFERRED,
            "2h": POSTURE_ALLOWED,
            "1h": POSTURE_CAUTION,
            "30m": POSTURE_CAUTION,
            "15m": POSTURE_REVIEW_ONLY,
            "5m": POSTURE_REVIEW_ONLY,
            "1m": POSTURE_REVIEW_ONLY,
        },
        "guardrails": [
            "swing_context_only",
            "confirm_data_sufficiency",
        ],
    },
    INTRADAY_TACTICAL_PROFILE: {
        "name": INTRADAY_TACTICAL_PROFILE,
        "label": "Intraday Tactical",
        "description": "1h, 30m, and 15m tactical analysis.",
        "purpose": "intraday tactical candidate review",
        "eigen_window": 80,
        "backtest_horizon": 60,
        "monte_carlo_horizon": 60,
        "monte_carlo_paths": 30000,
        "monte_carlo_block_len": 12,
        "minimum_rows_floor": 240,
        "preferred_timeframes": ["1h", "30m", "15m"],
        "timeframe_posture": {
            "1mo": POSTURE_AVOID,
            "1w": POSTURE_CAUTION,
            "1d": POSTURE_ALLOWED,
            "4h": POSTURE_ALLOWED,
            "2h": POSTURE_ALLOWED,
            "1h": POSTURE_PREFERRED,
            "30m": POSTURE_PREFERRED,
            "15m": POSTURE_PREFERRED,
            "5m": POSTURE_REVIEW_ONLY,
            "1m": POSTURE_REVIEW_ONLY,
        },
        "guardrails": [
            "noise_caution",
            "horizon_alignment_required_for_calibration",
        ],
    },
    CONSERVATIVE_RESEARCH_PROFILE: {
        "name": CONSERVATIVE_RESEARCH_PROFILE,
        "label": "Conservative Research",
        "description": "Slower, broader research/calibration review.",
        "purpose": "higher-stability research review",
        "eigen_window": 120,
        "backtest_horizon": 60,
        "monte_carlo_horizon": 60,
        "monte_carlo_paths": 50000,
        "monte_carlo_block_len": 16,
        "minimum_rows_floor": 300,
        "preferred_timeframes": ["1d", "4h", "1h", "30m"],
        "timeframe_posture": {
            "1mo": POSTURE_CAUTION,
            "1w": POSTURE_ALLOWED,
            "1d": POSTURE_PREFERRED,
            "4h": POSTURE_PREFERRED,
            "2h": POSTURE_ALLOWED,
            "1h": POSTURE_PREFERRED,
            "30m": POSTURE_ALLOWED,
            "15m": POSTURE_CAUTION,
            "5m": POSTURE_REVIEW_ONLY,
            "1m": POSTURE_REVIEW_ONLY,
        },
        "guardrails": [
            "longer_runtime",
            "confirm_provider_limits",
            "small_samples_not_conclusive",
        ],
    },
    LOW_TIMEFRAME_REVIEW_PROFILE: {
        "name": LOW_TIMEFRAME_REVIEW_PROFILE,
        "label": "Review-Only Low-Timeframe",
        "description": "5m and 1m exploratory visual review only.",
        "purpose": "diagnostic visual review only",
        "eigen_window": 40,
        "backtest_horizon": 20,
        "monte_carlo_horizon": 20,
        "monte_carlo_paths": 10000,
        "monte_carlo_block_len": 8,
        "minimum_rows_floor": 200,
        "preferred_timeframes": ["5m", "1m"],
        "timeframe_posture": {
            "1mo": POSTURE_AVOID,
            "1w": POSTURE_AVOID,
            "1d": POSTURE_AVOID,
            "4h": POSTURE_CAUTION,
            "2h": POSTURE_CAUTION,
            "1h": POSTURE_ALLOWED,
            "30m": POSTURE_ALLOWED,
            "15m": POSTURE_CAUTION,
            "5m": POSTURE_REVIEW_ONLY,
            "1m": POSTURE_REVIEW_ONLY,
        },
        "guardrails": [
            "review_only",
            "high_noise",
            "not_for_first_pass_calibration",
        ],
    },
}

REQUIRED_PROFILE_FIELDS = (
    "name",
    "label",
    "eigen_window",
    "backtest_horizon",
    "monte_carlo_horizon",
    "monte_carlo_paths",
    "monte_carlo_block_len",
    "minimum_rows_floor",
    "timeframe_posture",
)

NUMERIC_PROFILE_FIELDS = (
    "eigen_window",
    "backtest_horizon",
    "monte_carlo_horizon",
    "monte_carlo_paths",
    "monte_carlo_block_len",
    "minimum_rows_floor",
)


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _to_int(value: Any) -> int | None:
    if isinstance(value, bool) or _is_missing(value):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _json_safe_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(profile)


def _normalize_profile_name(profile_name: str | None = None) -> str:
    if _is_missing(profile_name):
        return DEFAULT_PROFILE_NAME
    return str(profile_name).strip().lower()


def _profile_summary(profile: dict[str, Any], *, include_description: bool = True) -> dict[str, Any]:
    summary = {
        "name": profile.get("name"),
        "label": profile.get("label"),
        "eigen_window": profile.get("eigen_window"),
        "backtest_horizon": profile.get("backtest_horizon"),
        "monte_carlo_horizon": profile.get("monte_carlo_horizon"),
        "monte_carlo_paths": profile.get("monte_carlo_paths"),
        "monte_carlo_block_len": profile.get("monte_carlo_block_len"),
        "minimum_rows_floor": profile.get("minimum_rows_floor"),
        "preferred_timeframes": profile.get("preferred_timeframes", []),
        "guardrails": profile.get("guardrails", []),
    }
    if include_description:
        summary["description"] = profile.get("description")
        summary["purpose"] = profile.get("purpose")
    return _json_safe_profile(summary)


def list_parameter_profiles() -> list[dict[str, Any]]:
    return [
        _profile_summary(profile)
        for profile in PARAMETER_PROFILES.values()
    ]


def get_parameter_profile(profile_name: str | None = None) -> dict[str, Any]:
    normalized_name = _normalize_profile_name(profile_name)
    profile = PARAMETER_PROFILES.get(normalized_name)
    if profile is None:
        return {
            "success": False,
            "profile": None,
            "errors": [f"Unknown parameter profile: {normalized_name}"],
            "warnings": [],
        }
    return {
        "success": True,
        "profile": _json_safe_profile(profile),
        "errors": [],
        "warnings": [],
    }


def validate_parameter_profile(profile: dict[str, Any] | None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(profile, dict):
        return {
            "success": False,
            "errors": ["Parameter profile must be a dictionary."],
            "warnings": [],
        }

    for field in REQUIRED_PROFILE_FIELDS:
        if field not in profile or _is_missing(profile.get(field)):
            errors.append(f"Missing required profile field: {field}")

    numeric_values: dict[str, int] = {}
    for field in NUMERIC_PROFILE_FIELDS:
        if field not in profile or _is_missing(profile.get(field)):
            continue
        value = _to_int(profile.get(field))
        if value is None or value <= 0:
            errors.append(f"Profile field must be a positive integer: {field}")
        else:
            numeric_values[field] = value

    backtest_horizon = numeric_values.get("backtest_horizon")
    monte_carlo_horizon = numeric_values.get("monte_carlo_horizon")
    if (
        backtest_horizon is not None
        and monte_carlo_horizon is not None
        and monte_carlo_horizon != backtest_horizon
    ):
        errors.append("Monte Carlo horizon must match Backtest Outcome horizon.")

    timeframe_posture = profile.get("timeframe_posture")
    if "timeframe_posture" in profile and not isinstance(timeframe_posture, dict):
        errors.append("Profile field must be a dictionary: timeframe_posture")
    elif isinstance(timeframe_posture, dict):
        for timeframe, posture in timeframe_posture.items():
            if posture not in VALID_POSTURES:
                errors.append(
                    f"Unsupported timeframe posture for {timeframe}: {posture}"
                )

        low_timeframe_safe_postures = {
            POSTURE_REVIEW_ONLY,
            POSTURE_CAUTION,
            POSTURE_AVOID,
        }
        for timeframe in ("5m", "1m"):
            posture = timeframe_posture.get(timeframe)
            if posture not in low_timeframe_safe_postures:
                warnings.append(
                    f"{timeframe} posture should be review_only, caution, or avoid."
                )

    if not profile.get("preferred_timeframes"):
        warnings.append("Profile has no preferred_timeframes.")

    monte_carlo_paths = numeric_values.get("monte_carlo_paths")
    if monte_carlo_paths is not None and monte_carlo_paths > 50000:
        warnings.append("Monte Carlo paths exceed 50000.")

    minimum_rows_floor = numeric_values.get("minimum_rows_floor")
    if minimum_rows_floor is not None and minimum_rows_floor < 100:
        warnings.append("Minimum rows floor is below 100.")

    return {
        "success": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def build_parameter_context_from_profile(profile_name: str | None = None) -> dict[str, Any]:
    profile_result = get_parameter_profile(profile_name)
    if not profile_result["success"]:
        return {
            "success": False,
            "profile_name": None,
            "profile_label": None,
            "parameter_context": {},
            "data_sufficiency_context": {},
            "monte_carlo_context": {},
            "backtest_context": {},
            "errors": profile_result["errors"],
            "warnings": profile_result["warnings"],
        }

    profile = profile_result["profile"]
    validation = validate_parameter_profile(profile)
    errors = [*profile_result["errors"], *validation["errors"]]
    warnings = [*profile_result["warnings"], *validation["warnings"]]
    if errors:
        return {
            "success": False,
            "profile_name": profile.get("name"),
            "profile_label": profile.get("label"),
            "parameter_context": {},
            "data_sufficiency_context": {},
            "monte_carlo_context": {},
            "backtest_context": {},
            "errors": errors,
            "warnings": warnings,
        }

    parameter_context = {
        "eigen_window": _to_int(profile["eigen_window"]),
        "backtest_horizon": _to_int(profile["backtest_horizon"]),
        "monte_carlo_horizon": _to_int(profile["monte_carlo_horizon"]),
        "minimum_rows_floor": _to_int(profile["minimum_rows_floor"]),
    }
    monte_carlo_context = {
        "horizon": _to_int(profile["monte_carlo_horizon"]),
        "paths": _to_int(profile["monte_carlo_paths"]),
        "block_len": _to_int(profile["monte_carlo_block_len"]),
    }
    backtest_context = {
        "horizon_bars": _to_int(profile["backtest_horizon"]),
    }

    return {
        "success": True,
        "profile_name": profile.get("name"),
        "profile_label": profile.get("label"),
        "parameter_context": _json_safe_profile(parameter_context),
        "data_sufficiency_context": _json_safe_profile(parameter_context),
        "monte_carlo_context": _json_safe_profile(monte_carlo_context),
        "backtest_context": _json_safe_profile(backtest_context),
        "errors": [],
        "warnings": warnings,
    }


def get_timeframe_posture(
    profile_name: str | None,
    timeframe: str | None,
) -> dict[str, Any]:
    profile_result = get_parameter_profile(profile_name)
    if not profile_result["success"]:
        return {
            "success": False,
            "profile_name": None,
            "timeframe": None if _is_missing(timeframe) else str(timeframe).strip().lower(),
            "posture": None,
            "is_preferred": False,
            "is_review_only": False,
            "warning": None,
            "errors": profile_result["errors"],
            "warnings": profile_result["warnings"],
        }

    profile = profile_result["profile"]
    normalized_timeframe = None if _is_missing(timeframe) else str(timeframe).strip().lower()
    warnings = [*profile_result["warnings"]]

    if normalized_timeframe is None:
        warning = "Timeframe is missing."
        warnings.append(warning)
        return {
            "success": True,
            "profile_name": profile.get("name"),
            "timeframe": None,
            "posture": None,
            "is_preferred": False,
            "is_review_only": False,
            "warning": warning,
            "errors": [],
            "warnings": warnings,
        }

    posture = profile.get("timeframe_posture", {}).get(normalized_timeframe)
    if posture is None:
        warning = f"Unknown timeframe for this profile: {normalized_timeframe}"
        warnings.append(warning)
        return {
            "success": True,
            "profile_name": profile.get("name"),
            "timeframe": normalized_timeframe,
            "posture": None,
            "is_preferred": False,
            "is_review_only": False,
            "warning": warning,
            "errors": [],
            "warnings": warnings,
        }

    warning = None
    if posture == POSTURE_REVIEW_ONLY:
        warning = "Timeframe is review-only for this profile."
    elif posture == POSTURE_AVOID:
        warning = "Timeframe is not recommended for this profile."
    if warning:
        warnings.append(warning)

    return {
        "success": True,
        "profile_name": profile.get("name"),
        "timeframe": normalized_timeframe,
        "posture": posture,
        "is_preferred": posture == POSTURE_PREFERRED,
        "is_review_only": posture == POSTURE_REVIEW_ONLY,
        "warning": warning,
        "errors": [],
        "warnings": warnings,
    }


def build_session_update_from_profile(profile_name: str | None = None) -> dict[str, Any]:
    profile_result = get_parameter_profile(profile_name)
    if not profile_result["success"]:
        return {
            "success": False,
            "profile_name": None,
            "session_updates": {},
            "errors": profile_result["errors"],
            "warnings": profile_result["warnings"],
        }

    profile = profile_result["profile"]
    validation = validate_parameter_profile(profile)
    errors = [*profile_result["errors"], *validation["errors"]]
    warnings = [*profile_result["warnings"], *validation["warnings"]]
    if errors:
        return {
            "success": False,
            "profile_name": profile.get("name"),
            "session_updates": {},
            "errors": errors,
            "warnings": warnings,
        }

    return {
        "success": True,
        "profile_name": profile.get("name"),
        "session_updates": {
            "data_sufficiency_eigen_window": _to_int(profile["eigen_window"]),
            "data_sufficiency_backtest_horizon": _to_int(profile["backtest_horizon"]),
            "data_sufficiency_monte_carlo_horizon": _to_int(profile["monte_carlo_horizon"]),
            "backtest_outcome_horizon_bars": _to_int(profile["backtest_horizon"]),
            "monte_carlo_horizon_bars": _to_int(profile["monte_carlo_horizon"]),
            "monte_carlo_paths": _to_int(profile["monte_carlo_paths"]),
            "monte_carlo_block_len": _to_int(profile["monte_carlo_block_len"]),
        },
        "errors": [],
        "warnings": warnings,
    }


def parameter_profile_summary_rows() -> list[dict[str, Any]]:
    return [
        _profile_summary(profile, include_description=False)
        for profile in PARAMETER_PROFILES.values()
    ]
