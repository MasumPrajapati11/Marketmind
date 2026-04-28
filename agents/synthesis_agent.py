import json
from agents import llm, safe_parse_json
from state import MarketMindState

WEIGHTS = {
    "price": 0.30,
    "sentiment": 0.20,
    "onchain": 0.20,
    "macro": 0.15,
    "risk": 0.15,
}

def synthesis_agent(state: MarketMindState) -> dict:
    signals = state["agent_signals"]

    signal_summary = []
    weighted_score = 0.0

    for s in signals:
        score = {"BULLISH": 1.0, "NEUTRAL": 0.0, "BEARISH": -1.0}.get(s["signal"], 0.0)
        weight = WEIGHTS.get(s["agent"], 0.2)
        weighted_score += score * s["confidence"] * weight
        signal_summary.append(
            f"{s['agent'].upper()}: {s['signal']} ({s['confidence']:.0%}) — {s['summary']}"
        )

    prompt = f"""You are the Chief Investment Officer. Synthesize these agent signals:

{chr(10).join(signal_summary)}

Weighted sentiment score: {weighted_score:.3f} (positive=bullish, negative=bearish)

Return ONLY valid JSON:
{{"verdict": "BUY" or "HOLD" or "SELL", "confidence": 0.0 to 1.0, "reasoning": "2-3 sentences max"}}"""

    try:
        result_raw = llm.invoke(prompt)
        result = safe_parse_json(result_raw.content)
        return {
            "final_verdict": result["verdict"],
            "final_confidence": float(result["confidence"]),
            "final_reasoning": result["reasoning"],
        }
    except Exception as e:
        verdict = "BUY" if weighted_score > 0.1 else "SELL" if weighted_score < -0.1 else "HOLD"
        return {
            "final_verdict": verdict,
            "final_confidence": 0.5,
            "final_reasoning": f"Fallback verdict based on weighted score: {weighted_score:.3f}",
        }