import os
import json
import requests
from agents import llm, safe_parse_json
from state import MarketMindState, AgentSignal

def fetch_fred(series_id: str, api_key: str, limit: int = 5) -> list:
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id, "api_key": api_key,
        "file_type": "json", "sort_order": "desc", "limit": limit,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return [
        {"date": o["date"], "value": round(float(o["value"]), 4)}
        for o in resp.json().get("observations", [])
        if o["value"] != "."
    ]

def macro_agent(state: MarketMindState) -> dict:
    ticker = state["ticker"]
    asset_type = state["asset_type"]
    fred_key = os.getenv("FRED_API_KEY")

    try:
        raw_data = {}

        try:
            dxy = fetch_fred("DTWEXBGS", fred_key, limit=5)
            if dxy:
                raw_data["dxy_recent"] = dxy[0]["value"]
                raw_data["dxy_trend"] = "rising" if dxy[0]["value"] > dxy[-1]["value"] else "falling"
        except Exception:
            raw_data["dxy"] = "unavailable"

        try:
            fed = fetch_fred("FEDFUNDS", fred_key, limit=2)
            if fed:
                raw_data["fed_rate"] = fed[0]["value"]
        except Exception:
            raw_data["rate"] = "unavailable"

        try:
            yc = fetch_fred("T10Y2Y", fred_key, limit=2)
            if yc:
                raw_data["yield_curve"] = yc[0]["value"]
                raw_data["yield_curve_inverted"] = yc[0]["value"] < 0
        except Exception:
            raw_data["yield_curve"] = "unavailable"

        if asset_type == "crypto":
            try:
                fg_resp = requests.get("https://api.alternative.me/fng/?limit=1", timeout=5)
                fg_data = fg_resp.json()
                raw_data["fear_greed_index"] = int(fg_data["data"][0]["value"])
                raw_data["fear_greed_label"] = fg_data["data"][0]["value_classification"]
            except Exception:
                raw_data["fear_greed"] = "unavailable"

        prompt = f"""You are a macro economist. Analyze these conditions for {ticker} ({asset_type}):
{json.dumps(raw_data, indent=2)}

Key rules:
- DXY rising = Bearish for risk assets
- Fed rate above 4.5% = restrictive, Bearish pressure
- Inverted yield curve = recession risk, Bearish
- Fear & Greed below 30 = Extreme Fear (contrarian Bullish)

Return ONLY valid JSON:
{{"signal": "BULLISH" or "BEARISH" or "NEUTRAL", "confidence": 0.0 to 1.0, "summary": "one sentence under 20 words"}}"""

        result_raw = llm.invoke(prompt)
        result = safe_parse_json(result_raw.content)

        return {"agent_signals": [AgentSignal(
            agent="macro", signal=result["signal"],
            confidence=float(result["confidence"]),
            summary=result["summary"], raw_data=raw_data)]}

    except Exception as e:
        return {"agent_signals": [AgentSignal(
            agent="macro", signal="NEUTRAL", confidence=0.0,
            summary=f"Macro agent error: {str(e)[:60]}", raw_data={})]}