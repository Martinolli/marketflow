from __future__ import annotations

from decimal import Decimal
import json
from typing import Any

import pytest

from marketflow.services import acquisition_provider_evidence_adapter_service as adapter


def _transport(request: dict[str, Any]) -> dict[str, Any]:
    assert request["provider_query_ticker"] == "MSFT"
    return {
        "status": "OK",
        "results": [
            {
                "t": 1641168000000,
                "o": 101.2500,
                "h": Decimal("102.500"),
                "l": "100.000",
                "c": 102.0,
                "v": 1250000.0,
                "n": 4000,
                "vw": 101.875,
            }
        ],
    }


def test_request_metadata_is_sanitized_and_daily():
    request = adapter.build_massive_daily_bars_request_v1(
        ticker="MSFT",
        start_date="2022-01-01",
        end_date="2025-12-31",
        request_timestamp_utc="2026-08-13T00:00:00Z",
    )

    assert request["provider_timespan"] == "day"
    assert request["provider_multiplier"] == 1
    assert request["headers"]["Authorization"] == "<redacted>"
    assert "apikey" not in request["url"].lower()
    assert len(request["request_semantic_digest"]) == 64


def test_fake_transport_returns_sanitized_rows_without_raw_payload():
    result = adapter.fetch_massive_daily_bars_evidence_v1(
        ticker="MSFT",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-test-key",
        transport=_transport,
        request_timestamp_utc="2026-08-13T00:00:00Z",
    )

    assert result["provider_request_mode"] == adapter.FAKE_TRANSPORT_PROVIDER_RESPONSE_INJECTION
    assert result["raw_response_stored"] is False
    assert result["raw_payload_exposed"] is False
    assert "provider_response_body" not in result
    assert "fictional-test-key" not in json.dumps(result, sort_keys=True)


def test_numeric_values_are_deterministic_text_before_digest():
    result = adapter.fetch_massive_daily_bars_evidence_v1(
        ticker="MSFT",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-test-key",
        transport=_transport,
        request_timestamp_utc="2026-08-13T00:00:00Z",
    )
    bar = result["sanitized_rows"][0]

    assert bar["open"] == "101.25"
    assert bar["high"] == "102.5"
    assert bar["low"] == "100"
    assert bar["close"] == "102"
    assert bar["volume"] == "1250000"
    assert all(value is None or isinstance(value, (str, int)) for value in bar.values())


def test_fake_transport_digest_is_deterministic():
    kwargs = {
        "ticker": "MSFT",
        "start_date": "2022-01-01",
        "end_date": "2025-12-31",
        "api_key": "fictional-test-key",
        "transport": _transport,
        "request_timestamp_utc": "2026-08-13T00:00:00Z",
    }
    first = adapter.fetch_massive_daily_bars_evidence_v1(**kwargs)
    second = adapter.fetch_massive_daily_bars_evidence_v1(**kwargs)

    assert first["provider_response_digest"] == second["provider_response_digest"]


def test_live_transport_is_refused_without_gate(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(adapter.MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE, raising=False)

    with pytest.raises(adapter.AcquisitionProviderEvidenceAdapterError, match="gate is not enabled"):
        adapter.fetch_massive_daily_bars_evidence_v1(
            ticker="MSFT",
            start_date="2022-01-01",
            end_date="2025-12-31",
            api_key="fictional-test-key",
        )


@pytest.mark.parametrize("field,value", [("o", float("nan")), ("v", object())])
def test_invalid_numeric_values_fail_closed(field: str, value: Any):
    def invalid_transport(_: dict[str, Any]) -> dict[str, Any]:
        row = {"t": 1641168000000, "o": 1, "h": 1, "l": 1, "c": 1, "v": 1}
        row[field] = value
        return {"status": "OK", "results": [row]}

    with pytest.raises(adapter.AcquisitionProviderEvidenceAdapterError, match="must be"):
        adapter.fetch_massive_daily_bars_evidence_v1(
            ticker="MSFT",
            start_date="2022-01-01",
            end_date="2025-12-31",
            api_key="fictional-test-key",
            transport=invalid_transport,
        )
