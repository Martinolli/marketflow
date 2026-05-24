"""Local-safe Analyst Chat skeleton helpers."""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_filename_part(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip() or fallback
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text.strip("._") or fallback


def get_analyst_chat_config_status() -> dict[str, Any]:
    """
    Return whether Analyst Chat is configured.

    This only inspects local environment/configuration. It does not call any
    external service.
    """
    provider = os.getenv("MARKETFLOW_ANALYST_PROVIDER") or os.getenv("OPENAI_PROVIDER") or "openai"
    model = os.getenv("MARKETFLOW_ANALYST_MODEL") or os.getenv("OPENAI_MODEL")
    missing: list[str] = []
    notes: list[str] = [
        "Analyst Chat skeleton is local-safe and does not run automatically.",
        "This milestone does not perform real API execution.",
    ]

    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    if not model:
        missing.append("MARKETFLOW_ANALYST_MODEL or OPENAI_MODEL")

    return {
        "configured": not missing,
        "provider": provider,
        "model": model,
        "missing": missing,
        "notes": notes,
    }


def _prompt_preview(prompt: str, limit: int = 1800) -> str:
    text = (prompt or "").strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}\n\n..."


def _created_at() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _metadata_line(label: str, value: Any) -> str:
    if value is None or value == "":
        value = "not available"
    return f"- {label}: {value}"


def _source_linkage_lines(source_metadata: dict[str, Any] | None) -> list[str]:
    metadata = _as_dict(source_metadata)
    keys = (
        ("Ticker", "ticker"),
        ("Timeframe", "timeframe"),
        ("Prompt style", "prompt_style"),
        ("Source prompt filename", "source_prompt_filename"),
        ("Packet version", "packet_version"),
        ("Dry run", "dry_run"),
        ("Created at", "created_at"),
    )
    return [_metadata_line(label, metadata.get(key)) for label, key in keys]


def run_analyst_chat(
    prompt: str,
    *,
    provider: str | None = None,
    model: str | None = None,
    dry_run: bool = False,
    source_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Run or simulate analyst chat.

    This first skeleton is dry-run/local-placeholder only. It does not call an
    external LLM/API.
    """
    config = get_analyst_chat_config_status()
    resolved_provider = provider or config.get("provider")
    resolved_model = model or config.get("model")
    notes = list(config.get("notes") or [])
    created_at = _created_at()
    prompt_text = str(prompt or "")
    prompt_chars = len(prompt_text)
    prompt_preview = _prompt_preview(prompt_text)
    prompt_preview_chars = len(prompt_preview)

    if not prompt or not str(prompt).strip():
        return {
            "success": False,
            "dry_run": dry_run,
            "provider": resolved_provider,
            "model": resolved_model,
            "response_markdown": None,
            "error": "No prompt was provided.",
            "notes": notes,
            "created_at": created_at,
            "prompt_chars": prompt_chars,
            "prompt_preview_chars": prompt_preview_chars,
            "execution_mode": "dry_run" if dry_run else "not_configured",
        }

    if not dry_run:
        missing = config.get("missing") or []
        if missing:
            return {
                "success": False,
                "dry_run": False,
                "provider": resolved_provider,
                "model": resolved_model,
                "response_markdown": None,
                "error": "Analyst Chat is not configured.",
                "notes": [
                    *notes,
                    f"Missing configuration: {', '.join(str(item) for item in missing)}.",
                    "Use dry-run mode or configure the provider/model before real execution in a future milestone.",
                ],
                "created_at": created_at,
                "prompt_chars": prompt_chars,
                "prompt_preview_chars": prompt_preview_chars,
                "execution_mode": "not_configured",
            }

        return {
            "success": False,
            "dry_run": False,
            "provider": resolved_provider,
            "model": resolved_model,
            "response_markdown": None,
            "error": "Real Analyst Chat execution is not implemented in this skeleton.",
            "notes": [
                *notes,
                "No external API call was made.",
                "Keep dry-run enabled until the explicit Analyst Chat execution milestone is implemented.",
            ],
            "created_at": created_at,
            "prompt_chars": prompt_chars,
            "prompt_preview_chars": prompt_preview_chars,
            "execution_mode": "not_implemented",
        }

    source_metadata = {
        **_as_dict(source_metadata),
        "dry_run": True,
        "created_at": created_at,
    }
    source_linkage = "\n".join(_source_linkage_lines(source_metadata))
    response = f"""# Wyckoff Analyst Response - Dry Run

## Execution Status

- No external API call was made.
- Execution mode: dry_run
- Provider: {resolved_provider or "not configured"}
- Model: {resolved_model or "not configured"}
- Created at: {created_at}

## Source Linkage

{source_linkage}

## Source Prompt

- Prompt characters: {prompt_chars}
- Prompt preview characters: {prompt_preview_chars}

## Analyst Review Placeholder

This is not a market conclusion.
Use the Analyst Packet, Monte Carlo metrics, P&F gate, and Wyckoff context for human review.

## Next Step

Configure real execution in a future milestone only after explicit user confirmation.
"""

    return {
        "success": True,
        "dry_run": True,
        "provider": resolved_provider,
        "model": resolved_model,
        "response_markdown": response,
        "error": None,
        "notes": notes,
        "created_at": created_at,
        "prompt_chars": prompt_chars,
        "prompt_preview_chars": prompt_preview_chars,
        "execution_mode": "dry_run",
    }


def build_response_filename(
    packet: dict[str, Any],
    style: str | None = None,
    include_timestamp: bool = True,
) -> str:
    """
    Return a safe markdown filename for an Analyst Chat response artifact.
    """
    packet = _as_dict(packet)
    summary = _as_dict(packet.get("packet_summary"))
    candidate = _as_dict(packet.get("strategy_candidate"))
    selected_timeframe_context = _as_dict(packet.get("selected_timeframe_context"))
    pnf = _as_dict(packet.get("pnf"))
    pnf_selection = _as_dict(pnf.get("selection"))
    pnf_sidecar = _as_dict(pnf.get("selected_sidecar"))
    ticker = _safe_filename_part(summary.get("ticker") or packet.get("ticker") or candidate.get("ticker"), "marketflow")
    timeframe = _safe_filename_part(
        summary.get("selected_timeframe")
        or candidate.get("tf")
        or selected_timeframe_context.get("tf")
        or pnf_selection.get("candidate_timeframe")
        or pnf_sidecar.get("inferred_timeframe")
        or pnf_sidecar.get("timeframe"),
        "selected",
    )
    parts = [ticker, timeframe]
    if style:
        parts.append(_safe_filename_part(style, "response"))
    parts.append("wyckoff_analyst_response")
    filename = "_".join(parts)
    if include_timestamp:
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return f"{filename}.md"
