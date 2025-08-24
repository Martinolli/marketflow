"""
This code retrieves and processes financial data from the Polygon API.
To calculate fair prices, it uses various data points from the API.
"""

from polygon import RESTClient
import numbers
import re
from typing import Any, Optional

# --- Best Practice: Use Environment Variables for API Keys ---
# It's safer to load your API key from an environment variable
# rather than hardcoding it directly in the script.
# You can set this in your terminal before running the script:
# export POLYGON_API_KEY="YOUR_API_KEY_HERE"

from marketflow.marketflow_config_manager import create_app_config
config_manager = create_app_config()
api_key = config_manager.get_api_key('polygon')
if not api_key:
    raise ValueError("Please set the POLYGON_API_KEY environment variable.")

TICKER = "AAPL"
client = RESTClient(api_key)

def _get_val(d, *path, default=0.0):
    """
    Safely navigates through a nested structure (objects / dicts) and returns a numeric value.
    Unwraps Polygon DataPoint objects (which expose a .value attribute) or dicts containing 'value'.
    Returns 'default' if the value is missing or non-numeric.
    """
    cur = d
    for p in path:
        if cur is None:
            return default
        if hasattr(cur, p):
            cur = getattr(cur, p)
        elif isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return default

    if cur is None:
        return default

    # Direct numeric
    if isinstance(cur, numbers.Number):
        return float(cur)

    # Polygon DataPoint (has .value)
    if hasattr(cur, "value"):
        val = getattr(cur, "value")
        if isinstance(val, numbers.Number):
            return float(val)
        # Sometimes value may be a string number
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    # Dict with 'value'
    if isinstance(cur, dict) and "value" in cur:
        val = cur.get("value")
        if isinstance(val, numbers.Number):
            return float(val)
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    # Last resort: try casting
    try:
        return float(cur)
    except (TypeError, ValueError):
        return default

def dump_non_null(section, title, limit=40):
    """Print non-null keys and sample values for quick inspection."""
    avail = keys_of(section)
    rows = []
    for k in sorted(avail):
        try:
            raw = getattr(section, k, None)
        except Exception:
            raw = None
        num = _coerce_number(raw)
        if num not in (None, 0, 0.0):
            rows.append((k, num))
    print(f"\n[DEBUG] Non-null keys in {title} (showing up to {limit}):")
    for k, v in rows[:limit]:
        print(f"   - {k}: {v:,.0f}")
    if len(rows) == 0:
        print("   (none)")

def keys_of(section):
    """Return visible keys on a Polygon statement object."""
    if section is None:
        return []
    if hasattr(section, "model_dump"):  # pydantic v2 models
        d = section.model_dump()
    elif hasattr(section, "dict"):       # pydantic v1
        d = section.dict()
    elif hasattr(section, "__dict__"):
        d = {k: v for k, v in section.__dict__.items() if not k.startswith("_")}
    else:
        d = {}
    return [k for k, v in d.items() if v is not None]

# --- Unified numeric coercion helpers (handle Polygon DataPoint) ---
def _coerce_number(val: Any) -> Optional[float]:
    """
    Try to convert Polygon DataPoint / dict / string to float.
    Returns None if cannot coerce.
    """
    if val is None:
        return None
    if isinstance(val, numbers.Number):
        return float(val)
    # Polygon DataPoint style object
    if hasattr(val, "value"):
        inner = getattr(val, "value")
        try:
            return float(inner)
        except (TypeError, ValueError):
            return None
    if isinstance(val, dict) and "value" in val:
        inner = val.get("value")
        try:
            return float(inner)
        except (TypeError, ValueError):
            return None
    # Last resort
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def _pick(section, *keys, default=0.0):
    """Exact-key picker (first non-zero after coercion)."""
    for key in keys:
        try:
            raw = getattr(section, key, None)
        except Exception:
            raw = None
        num = _coerce_number(raw)
        if num not in (None, 0, 0.0):
            return num, key
    return float(default), None

def _pick_smart(section, aliases=(), patterns=(), default=0.0, debug_label=""):
    """
    Try aliases; if none, scan available keys with regex patterns.
    Returns (value, chosen_key). Prints what it used.
    """
    val, key = _pick(section, *aliases, default=default)
    if key:
        print(f"    ✓ {debug_label}: using alias '{key}'")
        return val, key

    avail = keys_of(section)
    for pat in patterns:
        rx = re.compile(pat, re.I)
        for k in avail:
            if rx.search(k):
                try:
                    raw = getattr(section, k, None)
                except Exception:
                    raw = None
                num = _coerce_number(raw)
                if num not in (None, 0, 0.0):
                    print(f"    ✓ {debug_label}: matched pattern '{pat}' → '{k}'")
                    return num, k
    print(f"    ! {debug_label}: not found → default {default}")
    return float(default), None

def fetch_financials_ttm(ticker: str):
    """
    Build a TTM snapshot: sum last 4 quarters OCF & CapEx; grab latest Debt & Cash.
    """
    print(f"\nFetching last 4 quarterly reports for {ticker} (TTM)...")
    fin_q = list(client.vx.list_stock_financials(
        ticker=ticker,
        timeframe="quarterly",
        sort="filing_date",
        order="desc",
        limit=6,   # grab a few extra in case of missing quarters
    ))

    if not fin_q:
        raise ValueError(f"No quarterly financials for {ticker}.")

    ocf_ttm = 0.0
    capex_ttm = 0.0
    taken = 0

    latest_debt = 0.0
    latest_cash = 0.0
    latest_seen = False

    for f in fin_q:
        fin = f.financials
        cf  = fin.cash_flow_statement
        bs  = fin.balance_sheet
        inc = fin.income_statement

        # OCF (aliases kept simple; your existing _pick is fine here)
        ocf, _ = _pick_smart(
            cf,
            aliases=("net_cash_flow_from_operating_activities",
                     "net_cash_provided_by_used_in_operating_activities"),
            patterns=(r"net.*cash.*operat",),
            debug_label="OCF (quarter)"
        )

        # CapEx via smart picker
        capex, capex_key = _pick_smart(
            cf,
            aliases=(
                # Common us-gaap variants
                "purchase_of_property_plant_and_equipment",
                "payments_to_acquire_property_plant_and_equipment",
                "acquisition_of_property_plant_and_equipment",
                "additions_to_property_plant_and_equipment",

                # Other publisher wordings we often see
                "purchases_of_property_and_equipment",
                "payments_for_property_and_equipment",
                "capital_expenditure",
                "capital_expenditures",
            ),
            patterns=(
                # FIX 1: Broadened the main regex to be more flexible. It now looks
                # for a verb (purchase, payment, etc.) followed by any common
                # fixed asset noun (property, plant, equipment, etc.).
                r"(purchase|payment|acquisition|addition)s?.*(property|plant|equipment|pp&e|ppe|fixed_asset)s?",
                r"capital[_\s]?expend",  # capital_expenditure / capital expenditures
            ),
            # FIX 4 (minor): Simplified the debug label logic.
            debug_label="CapEx (quarter)"
        )
        if capex_key is None:
            dump_non_null(cf, "Cash Flow Statement (quarter)", limit=80)

        # TTM accumulation
        ocf_ttm += ocf
        # handle sign: if capex negative (outflow), adding is fine; else subtract
        capex_ttm += capex

        taken += 1
        if taken == 4:
            # store latest balance sheet once (from most recent f)
            if not latest_seen:
                # FIX 2: Added debug labels to all pickers for clarity.
                ltd, _ = _pick_smart(bs,
                    aliases=("long_term_debt","long_term_debt_noncurrent"),
                    patterns=(r"long.*term.*debt",),
                    debug_label="L/T Debt")
                std, _ = _pick_smart(bs,
                    aliases=("current_debt","short_term_debt",
                             "current_portion_of_long_term_debt"),
                    patterns=(r"(current|short).*debt",),
                    debug_label="S/T Debt")
                latest_debt = (ltd or 0.0) + (std or 0.0)

                # FIX 3: Used the more comprehensive list of aliases/patterns for cash.
                cash, _ = _pick_smart(bs,
                    aliases=(
                        "cash_and_cash_equivalents",
                        "cash_and_cash_equivalents_at_carrying_value",
                        "cash_cash_equivalents_and_short_term_investments",
                        "cash_and_short_term_investments",
                        "cash_cash_equivalents_and_marketable_securities",
                    ),
                    patterns=(
                        r"cash.*equivalents.*short.*invest",
                        r"cash.*equivalents.*marketable.*secur",
                        r"cash.*short.*invest",
                        r"^cash.*equivalents$",
                    ),
                    debug_label="Cash & Equiv")
                latest_cash = cash
                latest_seen = True
            break

    print(f"  - OCF TTM:   ${ocf_ttm:,.0f}")
    print(f"  - CapEx TTM: ${capex_ttm:,.0f}")
    fcf_ttm = ocf_ttm + capex_ttm if capex_ttm < 0 else ocf_ttm - capex_ttm
    print(f"  - FCF TTM:   ${fcf_ttm:,.0f}")

    # Shares: use latest balance-sheet shares if available; else diluted avg shares (quarter)
    shares, key = _pick_smart(fin_q[0].financials.balance_sheet,
                              aliases=("common_stock_shares_outstanding",),
                              patterns=(r"common.*shares.*outstanding",),
                              debug_label="Shares (balance sheet)")
    if shares in (0.0, 0):
        shares, key = _pick_smart(fin_q[0].financials.income_statement,
                                  aliases=("diluted_average_shares","basic_average_shares"),
                                  patterns=(r"dilut.*average.*shares|basic.*average.*shares",),
                                  debug_label="Shares (income stmt)")

    print(f"  - Shares Used: {shares:,.0f}")

    return {
        "fcf": float(fcf_ttm),
        "shares": float(shares),
        "debt": float(latest_debt),
        "cash": float(latest_cash),
    }

def fetch_financials(ticker: str):
    """
    Fetches the most recent financial data required for a DCF analysis,
    using multiple Polygon key aliases per metric.
    """
    print(f"\nFetching latest financial report for {ticker}...")

    financials_list = list(client.vx.list_stock_financials(
        ticker=ticker,
        sort="filing_date",
        order="desc",
        limit=1,
    ))
    if not financials_list:
        raise ValueError(f"No recent financial data found for {ticker}.")

    latest_financials = financials_list[0]
    fin = latest_financials.financials

    cash_flow  = fin.cash_flow_statement
    income     = fin.income_statement
    balance    = fin.balance_sheet

    # --- Operating Cash Flow (OCF) ---
    # Primary and common aliases
    ocf, ocf_key = _pick(
        cash_flow,
        "net_cash_flow_from_operating_activities",
        "net_cash_provided_by_used_in_operating_activities",   # alternate taxonomy
    )
    print(f"  - Operating Cash Flow ({ocf_key or 'not found'}): ${ocf:,.0f}")

    # --- CapEx (may come as different labels and sign conventions) ---
    capex, capex_key = _pick_smart(
        cash_flow,
        aliases=(
            # Common us-gaap variants
            "purchase_of_property_plant_and_equipment",
            "payments_to_acquire_property_plant_and_equipment",
            "acquisition_of_property_plant_and_equipment",
            "additions_to_property_plant_and_equipment",

            # Other publisher wordings we often see
            "purchases_of_property_and_equipment",
            "payments_for_property_and_equipment",
            "capital_expenditure",
            "capital_expenditures",
        ),
        patterns=(
            r"(purchase|payment|acquisition|addition)s?.*(property|plant|equipment|pp&e|ppe|fixed_asset)s?",
            r"capital[_\s]?expend",  # capital_expenditure / capital expenditures
        ),
        debug_label="CapEx"
    )
    # If CapEx missing, treat as 0 but warn
    if capex_key is None:
        print("  ! CapEx not found via common keys; assuming $0 (conservative).")
    else:
        print(f"  - Capital Expenditures ({capex_key}): ${capex:,.0f}")

    # Sign-aware FCF: many providers store CapEx as negative outflow
    fcf = ocf + capex if capex < 0 else ocf - capex
    print(f"  - Free Cash Flow (FCF): ${fcf:,.0f}")

    # --- Shares Outstanding (average, prefer diluted then basic) ---
    shares, shares_key = _pick(
        income,
        "weighted_average_shares_outstanding",            # if present
        "weighted_average_shares_outstanding_diluted",    # alt
        "diluted_average_shares",                         # Polygon common
        "weighted_average_shares_outstanding_basic",
        "basic_average_shares",                           # Polygon common
    )
    # Fallback to balance sheet period-end shares if averages not present
    if shares in (0.0, 0) or shares_key is None:
        bs_shares, bs_key = _pick(balance, "common_stock_shares_outstanding")
        if bs_shares not in (0.0, 0):
            shares, shares_key = bs_shares, bs_key

    print(f"  - Shares Outstanding ({shares_key or 'not found'}): {shares:,.0f}")
    if shares == 0:
        raise ValueError(f"Shares outstanding is zero or missing for {ticker}.")

    # --- Net Income (simple) ---
    net_income, ni_key = _pick(
        income,
        "net_income_loss",
        "net_income_loss_attributable_to_parent",
        "net_income",    # some taxonomies
    )
    print(f"  - Net Income ({ni_key or 'not found'}): ${net_income:,.0f}")

    # --- Debt (short + long) ---
    long_term_debt, ltd_key = _pick(
        balance,
        "long_term_debt",
        "long_term_debt_noncurrent",
    )
    short_term_debt, std_key = _pick(
        balance,
        "current_debt",
        "short_term_debt",
        "current_portion_of_long_term_debt",
    )
    debt = (long_term_debt or 0.0) + (short_term_debt or 0.0)
    print(f"  - Long Term Debt ({ltd_key or 'not found'}): ${long_term_debt:,.0f}")
    print(f"  - Short Term Debt ({std_key or 'not found'}): ${short_term_debt:,.0f}")
    print(f"  - Total Debt: ${debt:,.0f}")

    # --- Cash & Equivalents ---
    cash, cash_key = _pick_smart(
    balance,
    aliases=(
        "cash_and_cash_equivalents",
        "cash_and_cash_equivalents_at_carrying_value",
        "cash_cash_equivalents_and_short_term_investments",
        # add a couple of broader aggregates:
        "cash_and_short_term_investments",
        "cash_cash_equivalents_and_marketable_securities",
        "restricted_cash_and_cash_equivalents",
    ),
    patterns=(
        r"cash.*equivalents.*short.*invest",
        r"cash.*equivalents.*marketable.*secur",
        r"cash.*short.*invest",
        r"^cash.*equivalents$",
        r"^cash$",
        r"restricted.*cash.*equivalents",
    ),
    debug_label="Cash & Equivalents"
)

    print(f"  - Cash & Equivalents ({cash_key or 'not found'}): ${cash:,.0f}")

    print(f"\nSuccessfully fetched data from report filed on: {latest_financials.filing_date}")
    return {
        "fcf": float(fcf),
        "shares": float(shares),
        "net_income": float(net_income),
        "debt": float(debt),
        "cash": float(cash)
    }


def project_cash_flows(fcf, growth_rate=0.08, years=5):
    """Projects future cash flows for a number of years."""
    return [fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]

def discount_cash_flows(cash_flows, discount_rate=0.10):
    """Discounts future cash flows to their present value."""
    return [cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows, start=1)]

def calculate_terminal_value(last_fcf, growth_rate=0.02, discount_rate=0.10):
    """Calculates the terminal value of the company after the projection period."""
    if discount_rate <= growth_rate:
        raise ValueError("Discount rate must be greater than perpetual growth rate for terminal value.")
    terminal_value = (last_fcf * (1 + growth_rate)) / (discount_rate - growth_rate)
    
    # Also discount the terminal value back to present day
    # Assuming a 5-year projection period.
    present_terminal_value = terminal_value / ((1 + discount_rate)**5)
    return present_terminal_value

def estimate_fair_price(ticker):
    """
    Performs a full Discounted Cash Flow (DCF) analysis to estimate fair price.
    """
    fin = fetch_financials(ticker)
    
    # --- DCF Calculation Steps ---
    print("\nStarting DCF calculation...")
    
    # 1. Project cash flows for the next 5 years
    projected = project_cash_flows(fin["fcf"])
    print(f"  - Projected FCFs (5 years): {[f'${p:,.0f}' for p in projected]}")

    # 2. Discount those cash flows to their present value
    discounted = discount_cash_flows(projected)
    sum_of_discounted_fcf = sum(discounted)
    print(f"  - Present Value of FCFs: ${sum_of_discounted_fcf:,.0f}")

    # 3. Calculate terminal value and discount it to its present value
    terminal = calculate_terminal_value(projected[-1])
    print(f"  - Present Value of Terminal Value: ${terminal:,.0f}")

    # 4. Calculate Enterprise Value = PV of FCFs + PV of Terminal Value
    enterprise_value = sum_of_discounted_fcf + terminal
    print(f"  - Total Enterprise Value: ${enterprise_value:,.0f}")

    # 5. Calculate Equity Value = Enterprise Value - Debt + Cash
    equity_value = enterprise_value - fin["debt"] + fin["cash"]
    print(f"  - Implied Equity Value: ${equity_value:,.0f}")

    # 6. Calculate Fair Price per Share = Equity Value / Shares Outstanding
    fair_price = equity_value / fin["shares"]
    print(f"  - Fair Price per Share: ${fair_price:.2f}")

    return round(fair_price, 2)


if __name__ == "__main__":
    try:
        # Educational example DCF using TTM FCF.
        ttm = fetch_financials_ttm(TICKER)
        print("\nRunning DCF using TTM FCF...")
        projected = project_cash_flows(ttm["fcf"])
        discounted = discount_cash_flows(projected)
        pv_fcf = sum(discounted)
        terminal = calculate_terminal_value(projected[-1])
        enterprise_value = pv_fcf + terminal
        equity_value = enterprise_value - ttm["debt"] + ttm["cash"]
        fair_price = equity_value / ttm["shares"] if ttm["shares"] else 0.0
        print("\n" + "="*40)
        print(f"Estimated Fair Price for {TICKER}: ${fair_price:,.2f}")
        print("="*40)
    except Exception as e:
        print(f"\nAn error occurred: {e}")