from __future__ import annotations

import pytest

from marketflow.services import live_ticker_validation_provider_adapter_service as adapter


def _payload(ticker: str) -> dict:
    return {
        "status": "OK",
        "results": {
            "ticker": ticker,
            "name": f"{ticker} Corporation",
            "market": "stocks",
            "locale": "us",
            "primary_exchange": "XNAS",
            "type": "CS",
            "active": True,
            "currency_name": "usd",
            "composite_figi": f"BBG{ticker}",
        },
        "raw_secret_like_field": "not retained",
    }


def test_request_metadata_redacts_api_key():
    request = adapter.build_massive_ticker_details_request_v1(
        ticker="MSFT",
        api_key="fictional-secret-key",
        request_timestamp_utc="2026-08-09T00:00:00Z",
    )

    rendered = str(request).lower()
    assert "fictional-secret-key" not in rendered
    assert request["api_key_supplied"] is True
    assert request["api_key_stored"] is False
    assert request["api_key_printed"] is False
    assert request["headers"]["Authorization"] == "<redacted>"


def test_fake_transport_returns_sanitized_ticker_evidence():
    seen = []

    def transport(request):
        seen.append(request)
        return _payload(request["provider_query_ticker"])

    result = adapter.fetch_massive_ticker_details_v1(
        ticker="MSFT",
        api_key="fictional-secret-key",
        transport=transport,
        request_timestamp_utc="2026-08-09T00:00:00Z",
    )

    assert seen[0]["provider_endpoint"] == "/v3/reference/tickers/MSFT"
    assert result["provider_response_injected"] is True
    assert result["provider_request_mode"] == adapter.INJECTED_PROVIDER_RESPONSE
    assert result["sanitized_response"]["ticker"] == "MSFT"
    assert result["sanitized_response"]["active"] is True
    assert result["raw_response_stored"] is False
    assert result["raw_payload_committed"] is False
    assert result["api_key_stored_or_printed"] is False
    assert "results" not in result
    assert "raw_secret_like_field" not in str(result)


def test_live_transport_refuses_call_when_gate_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(adapter.LIVE_TICKER_VALIDATION_GATE_ENV, raising=False)

    with pytest.raises(adapter.LiveTickerValidationProviderAdapterError, match="gate"):
        adapter.fetch_massive_ticker_details_v1(
            ticker="MSFT",
            api_key="fictional-secret-key",
            request_timestamp_utc="2026-08-09T00:00:00Z",
        )


def test_adapter_normalizes_supported_provider_fields():
    def transport(request):
        return _payload(request["provider_query_ticker"]) | {
            "results": _payload(request["provider_query_ticker"])["results"]
            | {"delisted_utc": None, "share_class_figi": "BBG001S5TD05"}
        }

    result = adapter.fetch_massive_ticker_details_v1(
        ticker="NVDA",
        api_key="fictional-secret-key",
        transport=transport,
        request_timestamp_utc="2026-08-09T00:00:00Z",
    )

    assert result["provider_name"] == adapter.PROVIDER_NAME
    assert result["provider_endpoint_mode"] == adapter.SELECTED_ENDPOINT_MODE
    assert result["sanitized_response"]["ticker"] == "NVDA"
    assert result["sanitized_response"]["type"] == "CS"
    assert result["sanitized_response"]["primary_exchange"] == "XNAS"
    assert result["sanitized_response"]["share_class_figi"] == "BBG001S5TD05"
    assert len(result["provider_response_digest"]) == 64


def test_adapter_records_sanitized_request_metadata_only():
    def transport(request):
        return _payload(request["provider_query_ticker"])

    result = adapter.fetch_massive_ticker_details_v1(
        ticker="GOOGL",
        api_key="fictional-secret-key",
        transport=transport,
        request_timestamp_utc="2026-08-09T00:00:00Z",
    )

    request = result["request"]
    assert "url" not in request
    assert request["sanitized_url"].endswith("/v3/reference/tickers/GOOGL")
    assert request["headers"]["Authorization"] == "<redacted>"
    rendered = str(result).lower()
    assert "fictional-secret-key" not in rendered
    assert "bearer " not in rendered


def test_adapter_never_exposes_raw_payload_by_default():
    def transport(request):
        return _payload(request["provider_query_ticker"])

    result = adapter.fetch_massive_ticker_details_v1(
        ticker="META",
        api_key="fictional-secret-key",
        transport=transport,
        request_timestamp_utc="2026-08-09T00:00:00Z",
    )

    assert "payload" not in result
    assert "raw_payload" not in result
    assert "raw_secret_like_field" not in str(result)
