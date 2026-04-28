import numpy as np
import yfinance as yf
import requests
from agents import llm, safe_parse_json
from state import MarketMindState, AgentSignal

def risk_agent(state: MarketMindState) -> dict:
    ticker = state["ticker"]
    yfin_ticker = f"{ticker}-USD" if state["asset_type"] == "crypto" else ticker

    try:
        data = yf.download(yfin_ticker, period="90d", interval="1d", progress=False)
        if data.empty:
            return {"agent_signals": [AgentSignal(
                agent="risk", signal="NEUTRAL", confidence=0.0,
                summary=f"No data for {ticker}", raw_data={})]}

        close = data["Close"].squeeze()
        returns = close.pct_change().dropna()

        vol_30d = round(float(returns[-30:].std() * (252 ** 0.5) * 100), 2)
        peak = close.cummax()
        drawdown = round(float(((close - peak) / peak).min() * 100), 2)
        sharpe = round(float(returns.mean() / returns.std() * (252 ** 0.5)), 3) if returns.std() > 0 else 0

        raw_data = {
            "volatility_30d_annualized_pct": vol_30d,
            "max_drawdown_90d_pct": drawdown,
            "sharpe_ratio_approx": sharpe,
        }

        try:
            vix_data = yf.download("^VIX", period="5d", interval="1d", progress=False)
            if not vix_data.empty:
                raw_data["vix"] = round(float(vix_data["Close"].iloc[-1]), 2)
        except Exception:
            raw_data["vix"] = "unavailable"

        prompt = f"""You are a risk analyst. Evaluate risk for {ticker}:
{raw_data}

- High volatility (>60%) = elevated risk
- Deep drawdown (<-30%) = high risk
- VIX above 30 = market stress
- Sharpe below 0.5 = poor risk-adjusted returns

Return ONLY valid JSON:
{{"signal": "BULLISH" or "BEARISH" or "NEUTRAL", "confidence": 0.0 to 1.0, "summary": "one sentence under 20 words"}}"""

        result_raw = llm.invoke(prompt)
        result = safe_parse_json(result_raw.content)

        return {"agent_signals": [AgentSignal(
            agent="risk", signal=result["signal"],
            confidence=float(result["confidence"]),
            summary=result["summary"], raw_data=raw_data)]}

    except Exception as e:
        return {"agent_signals": [AgentSignal(
            agent="risk", signal="NEUTRAL", confidence=0.0,
            summary=f"Risk agent error: {str(e)[:60]}", raw_data={})]}