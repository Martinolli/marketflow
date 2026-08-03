"""CLI for MarketFlow source-authority evidence tooling."""

from __future__ import annotations

import argparse
import json

from marketflow.source_authority.instrument_identity import (
    instrument_identity_plan,
    instrument_identity_self_check,
    live_command,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MarketFlow source-authority tooling")
    parser.add_argument(
        "--instrument-identity-plan",
        action="store_true",
        help="Print the fixed offline AAPL instrument-identity evidence plan.",
    )
    parser.add_argument(
        "--instrument-identity-self-check",
        action="store_true",
        help="Run mock-only instrument-identity evidence self-check.",
    )
    parser.add_argument(
        "--instrument-identity-run",
        action="store_true",
        help="Run the controlled live Massive.com Ticker Overview identity evidence command.",
    )
    args = parser.parse_args(argv)
    selected = sum(
        1
        for item in (
            args.instrument_identity_plan,
            args.instrument_identity_self_check,
            args.instrument_identity_run,
        )
        if item
    )
    if selected > 1:
        parser.error("select exactly one source-authority command")
    if args.instrument_identity_plan:
        print(json.dumps(instrument_identity_plan(), sort_keys=True, indent=2))
        return 0
    if args.instrument_identity_self_check:
        print(json.dumps(instrument_identity_self_check(), sort_keys=True, indent=2))
        return 0
    if args.instrument_identity_run:
        return live_command()
    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
