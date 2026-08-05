from __future__ import annotations

import json
import os

import pytest

from marketflow.services import split_event_provider_adapter_service as adapter


def _page(events: list[dict], *, next_url: str | None = None) -> dict:
    payload: dict = {
        "status": "OK",
        "request_id": "test-request-not-public",
        "results": events,
    }
    if next_url is not None:
        payload["next_url"] = next_url
    return payload


def test_live_request_metadata_builds_without_api_key_leakage():
    request = adapter.build_massive_split_events_request_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-secret-key",
        request_timestamp_utc="2026-08-05T00:00:00Z",
    )
    rendered = json.dumps(request, sort_keys=True)

    assert request["provider_endpoint"] == "/stocks/v1/splits"
    assert request["provider_endpoint_stability"] == "CURRENT_STOCKS_V1_SPLITS"
    assert request["provider_request_mode"] == "LIVE_PROVIDER_REQUEST"
    assert "fictional-secret-key" not in rendered
    assert "api_key" not in rendered.lower()
    assert "apikey" not in rendered.lower()
    assert request["headers"]["Authorization"] == "<redacted>"


def test_fake_transport_is_used_for_live_adapter_tests():
    calls: list[dict] = []

    def fake_transport(request):
        calls.append(dict(request))
        return _page([])

    raw = adapter.fetch_massive_split_events_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-secret-key",
        transport=fake_transport,
        request_timestamp_utc="2026-08-05T00:00:00Z",
    )

    assert len(calls) == 1
    assert calls[0]["sanitized_url"].startswith("https://api.massive.com/stocks/v1/splits?")
    assert raw["provider_requests_made"] is True
    assert raw["provider_response_injected"] is False
    assert raw["provider_response_page_count"] == 1
    assert raw["provider_raw_response_row_count"] == 0


def test_fake_transport_pagination_uses_sanitized_continuation_url():
    next_url = (
        "https://api.massive.com/stocks/v1/splits?"
        "ticker=AAPL&execution_date.gte=2022-01-01&execution_date.lte=2025-12-31"
        "&sort=execution_date.asc&limit=5000&cursor=opaque-provider-cursor"
    )
    calls: list[dict] = []

    def fake_transport(request):
        calls.append(dict(request))
        if len(calls) == 1:
            return _page([{"execution_date": "2021-12-31", "ticker": "AAPL"}], next_url=next_url)
        return _page([{"execution_date": "2024-06-10", "ticker": "AAPL"}])

    raw = adapter.fetch_massive_split_events_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-secret-key",
        transport=fake_transport,
        request_timestamp_utc="2026-08-05T00:00:00Z",
    )

    assert len(calls) == 2
    assert raw["provider_response_page_count"] == 2
    assert raw["provider_raw_response_row_count"] == 2
    assert "opaque-provider-cursor" not in calls[1]["sanitized_url"]
    assert "cursor-" in calls[1]["sanitized_url"]


def test_pagination_rejects_untrusted_next_url_host():
    def fake_transport(request):
        return _page([], next_url="https://example.com/stocks/v1/splits?cursor=x")

    with pytest.raises(adapter.SplitEventProviderAdapterError, match="host or scheme"):
        adapter.fetch_massive_split_events_v1(
            ticker="AAPL",
            start_date="2022-01-01",
            end_date="2025-12-31",
            api_key="fictional-secret-key",
            transport=fake_transport,
            request_timestamp_utc="2026-08-05T00:00:00Z",
        )


def test_raw_response_digest_is_deterministic():
    def fake_transport(request):
        return _page([{"execution_date": "2024-06-10", "split_from": 1, "split_to": 4, "ticker": "AAPL"}])

    first = adapter.fetch_massive_split_events_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-secret-key",
        transport=fake_transport,
        request_timestamp_utc="2026-08-05T00:00:00Z",
    )
    second = adapter.fetch_massive_split_events_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key="fictional-secret-key",
        transport=fake_transport,
        request_timestamp_utc="2026-08-05T00:00:00Z",
    )

    assert first == second
    assert len(first["provider_raw_response_digest"]) == 64


@pytest.mark.skipif(
    os.environ.get("MARKETFLOW_ENABLE_LIVE_SPLIT_AUDIT") != "1" or not (os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")),
    reason="live split audit smoke requires MARKETFLOW_ENABLE_LIVE_SPLIT_AUDIT=1 and a provider API key",
)
def test_optional_live_split_event_provider_smoke():
    raw = adapter.fetch_massive_split_events_v1(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2025-12-31",
        api_key=os.environ.get("MASSIVE_API_KEY") or os.environ["POLYGON_API_KEY"],
    )

    assert raw["provider_requests_made"] is True
    assert raw["provider_response_injected"] is False
