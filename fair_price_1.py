
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
    
    # Extract value if it's a Polygon DataPoint-like object
    val = cur
    if hasattr(cur, "value"):
        val = getattr(cur, "value")
    elif isinstance(cur, dict) and "value" in cur:
        val = cur.get("value")
    
    # Try to convert to float
    if isinstance(val, numbers.Number):
        return float(val)
    try:
        return float(val)
    except (TypeError, ValueError):
        return default

def _pick(section, *keys, default=0.0):
    """Exact-key picker (first non-zero after coercion)."""
    for key in keys:
        try:
            raw = getattr(section, key, None)
        except Exception:
            raw = None
        
        # Use _get_val to handle the nested structure and coercion
        num = _get_val(section, key)
        
        if num not in (0.0, 0):
            return num, key
    return float(default), None

def fetch_financials_ttm(ticker: str):
    """
    Build a TTM snapshot by deriving CapEx from changes in Fixed Assets and Depreciation.
    """
    print(f"\nFetching last 5 quarterly reports for {ticker} (to derive TTM CapEx)...")
    # FIX: Fetch 5 quarters to calculate 4 periods of change in fixed assets.
    fin_q = list(client.vx.list_stock_financials(
        ticker=ticker,
        timeframe="quarterly",
        sort="filing_date",
        order="desc",
        limit=5,
    ))

    if len(fin_q) < 5:
        raise ValueError(f"Not enough quarterly data for {ticker} to derive CapEx (need 5, got {len(fin_q)}).")

    ocf_ttm = 0.0
    capex_ttm = 0.0

    print("Deriving TTM CapEx from Balance Sheet and Cash Flow Statement...")
    # FIX: Loop through the 4 most recent periods to calculate change.
    for i in range(4):
        current_report = fin_q[i]
        previous_report = fin_q[i+1] # The report from the prior quarter

        cf_curr = current_report.financials.cash_flow_statement
        bs_curr = current_report.financials.balance_sheet
        bs_prev = previous_report.financials.balance_sheet

        # 1. Get Operating Cash Flow for the current quarter
        ocf_quarter, ocf_key = _pick(cf_curr, "net_cash_flow_from_operating_activities")
        if not ocf_key:
             print(f"Warning: OCF not found for quarter ending {current_report.end_date}, using 0.")
        ocf_ttm += ocf_quarter

        # 2. Derive CapEx for the current quarter
        # CapEx = (Ending PP&E - Beginning PP&E) + Depreciation
        ending_fixed_assets = _get_val(bs_curr, "fixed_assets")
        beginning_fixed_assets = _get_val(bs_prev, "fixed_assets")
        depreciation = _get_val(cf_curr, "depreciation_and_amortization")
        
        # Change in fixed assets is a positive number if assets increase.
        change_in_assets = ending_fixed_assets - beginning_fixed_assets
        
        # Derived CapEx. It's a cash outflow, so it should be negative for our FCF calc.
        capex_quarter = - (change_in_assets + depreciation)
        capex_ttm += capex_quarter
        print(f"  - Q ending {current_report.end_date}: OCF ${ocf_quarter:,.0f}, Derived CapEx ${capex_quarter:,.0f}")

    print(f"\n  - OCF TTM:   ${ocf_ttm:,.0f}")
    print(f"  - CapEx TTM: ${capex_ttm:,.0f}")
    
    # FCF = OCF + CapEx (since we've stored CapEx as a negative value)
    fcf_ttm = ocf_ttm + capex_ttm
    print(f"  - FCF TTM:   ${fcf_ttm:,.0f}")

    # --- Use the most recent report (fin_q[0]) for Balance Sheet and Shares data ---
    latest_bs = fin_q[0].financials.balance_sheet
    latest_is = fin_q[0].financials.income_statement
    latest_cfs = fin_q[0].financials.cash_flow_statement
    latest_ci = fin_q[0].financials.comprehensive_income

    print("Latest Cash Flow Statement:")
    print(latest_cfs)
    print()
    print("Latest Comprehensive Income:")
    print(latest_ci)

    # Get Debt (Long Term + Short Term if available)
    long_term_debt, _ = _pick(latest_bs, "long_term_debt")
    # Note: short term debt isn't in your key list, so this will likely be 0
    short_term_debt, _ = _pick(latest_bs, "current_debt", "short_term_debt")
    latest_debt = long_term_debt + short_term_debt
    
    # Get Cash (using a broad key that might not be in the list, but is common)
    latest_cash, _ = _pick(
            latest_bs,
            "cash_and_cash_equivalents",
            "cash_and_cash_equivalents_at_carrying_value",
            "cash_cash_equivalents_and_short_term_investments",
            "cash_and_short_term_investments",
            "cash_cash_equivalents_and_marketable_securities",
            "restricted_cash_and_cash_equivalents",
            "net_cash_flow",
            "cash"
        )

    # Get Shares Outstanding
    shares, shares_key = _pick(latest_is, "diluted_average_shares", "basic_average_shares")
    if not shares_key:
        raise ValueError("Could not find shares outstanding in the income statement.")

    print(f"  - Latest Total Debt: ${latest_debt:,.0f}")
    print(f"  - Latest Cash: ${latest_cash:,.0f}")
    print(f"  - Shares Used: {shares:,.0f} (from report ending {fin_q[0].end_date})")

    return {
        "fcf": float(fcf_ttm),
        "shares": float(shares),
        "debt": float(latest_debt),
        "cash": float(latest_cash),
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
    present_terminal_value = terminal_value / ((1 + discount_rate)**5)
    return present_terminal_value

def ramp_fcf_path(current_fcf, target_fcf, years_to_target, post_target_growth=0.03, horizon=10):
    """
    Build an FCF path that linearly ramps from current_fcf to target_fcf over `years_to_target`,
    then grows at `post_target_growth` until `horizon`.
    Returns list of yearly FCFs [y1..yN].
    """
    path = []
    if years_to_target <= 0:
        years_to_target = 1
    step = (target_fcf - current_fcf) / years_to_target
    y = current_fcf
    for _ in range(years_to_target):
        y += step
        path.append(y)
    while len(path) < horizon:
        y *= (1 + post_target_growth)
        path.append(y)
    return path

def pv(values, r):
    return [v / ((1+r)**i) for i, v in enumerate(values, start=1)]

def terminal_value(last_fcf, g, r, years):
    if r <= g:
        raise ValueError("Discount rate must exceed terminal growth.")
    tv = last_fcf * (1+g) / (r - g)
    return tv / ((1+r)**years)

def venture_dcf(current_fcf, target_fcf=300e6, years_to_target=6, post_target_growth=0.03,
                discount_rate=0.12, terminal_growth=0.02, survival_prob=0.65, horizon=10):
    """
    Early-stage valuation: negative FCF ramps to a target, then stabilizes.
    survival_prob down-weights execution/financing risk.
    """
    path = ramp_fcf_path(current_fcf, target_fcf, years_to_target,
                         post_target_growth=post_target_growth, horizon=horizon)
    pv_fcf = sum(pv(path, discount_rate))
    tv = terminal_value(path[-1], terminal_growth, discount_rate, horizon)
    ev = (pv_fcf + tv) * survival_prob
    return ev, path


if __name__ == "__main__":
    try:
        ttm = fetch_financials_ttm(TICKER)

        if ttm["fcf"] < 0:
            print("\nRunning Venture-DCF (negative FCF ramp)...")
            ev, fcf_path = venture_dcf(
                current_fcf=ttm["fcf"],
                target_fcf=300e6,          # <— tune: steady-state FCF
                years_to_target=6,         # <— tune: years to break-even/scale
                post_target_growth=0.05,   # <— tune: mid-cycle growth
                discount_rate=0.12,        # <— tune: higher risk, higher r
                terminal_growth=0.02,      # <— conservative LT growth
                survival_prob=0.60,        # <— execution/financing risk
                horizon=10
            )
            equity_value = ev - ttm["debt"] + ttm["cash"]
            fair_price = equity_value / ttm["shares"] if ttm["shares"] else 0.0
        else:
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
