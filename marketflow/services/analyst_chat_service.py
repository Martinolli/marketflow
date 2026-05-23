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


def run_analyst_chat(
    prompt: str,
    *,
    provider: str | None = None,
    model: str | None = None,
    dry_run: bool = False,
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

    if not prompt or not str(prompt).strip():
        return {
            "success": False,
            "dry_run": dry_run,
            "provider": resolved_provider,
            "model": resolved_model,
            "response_markdown": None,
            "error": "No prompt was provided.",
            "notes": notes,
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
        }

    missing_text = ", ".join(str(item) for item in (config.get("missing") or [])) or "none"
    response = f"""# Wyckoff Analyst Response - Dry Run

This is a local placeholder response. No AI model or external API was called.

## Configuration Status

- Provider: {resolved_provider or "not configured"}
- Model: {resolved_model or "not configured"}
- Missing: {missing_text}

## Prompt Received

The prompt is available and ready for a future Analyst Chat execution step. Review the prompt before any real model call.

```markdown
{_prompt_preview(prompt)}
```

## Analytical Placeholder

- This dry run does not provide a market conclusion.
- Use the Analyst Packet, Monte Carlo metrics, P&F gate, and Wyckoff context for human review.
- Treat failed gates, weak confirmation, unclear phase context, or missing data as caution signals.

## Next Setup Step

Configure the intended provider and model in a future milestone, then keep execution behind an explicit Run Analyst click.
"""

    return {
        "success": True,
        "dry_run": True,
        "provider": resolved_provider,
        "model": resolved_model,
        "response_markdown": response,
        "error": None,
        "notes": notes,
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
    ticker = _safe_filename_part(summary.get("ticker") or packet.get("ticker") or candidate.get("ticker"), "marketflow")
    timeframe = _safe_filename_part(summary.get("selected_timeframe") or candidate.get("tf"), "selected")
    parts = [ticker, timeframe]
    if style:
        parts.append(_safe_filename_part(style, "response"))
    parts.append("wyckoff_analyst_response")
    filename = "_".join(parts)
    if include_timestamp:
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return f"{filename}.md"
