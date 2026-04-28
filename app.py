import time
import streamlit as st
from graph import graph

st.set_page_config(page_title="MarketMind", page_icon="🧠", layout="wide")
st.title("🧠 MarketMind — Parallel Multi-Agent Analyst")

col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("Enter ticker (e.g. BTC, ETH, AAPL, TSLA)", value="BTC")
with col2:
    analyze = st.button("🔍 Analyze", use_container_width=True)

if analyze and ticker:
    with st.spinner("Running 5 agents in parallel..."):
        start = time.time()
        result = graph.invoke({
            "ticker": ticker.upper(),
            "asset_type": "crypto",
            "agent_signals": [],
            "final_verdict": None,
            "final_confidence": None,
            "final_reasoning": None,
        })
        elapsed = round(time.time() - start, 2)

    verdict = result.get("final_verdict", "N/A")
    confidence = result.get("final_confidence", 0)
    reasoning = result.get("final_reasoning", "")

    color = {"BUY": "green", "SELL": "red", "HOLD": "orange"}.get(verdict, "gray")
    st.markdown(f"## Final Verdict: :{color}[**{verdict}**] ({confidence:.0%} confidence)")
    st.info(reasoning)
    st.caption(f"⏱ Completed in {elapsed}s")

    st.divider()
    st.subheader("Agent Signals")
    cols = st.columns(5)
    for i, signal in enumerate(result.get("agent_signals", [])):
        with cols[i % 5]:
            sig_color = {"BULLISH": "green", "BEARISH": "red", "NEUTRAL": "gray"}.get(signal["signal"], "gray")
            st.markdown(f"**{signal['agent'].upper()}**")
            st.markdown(f":{sig_color}[{signal['signal']}] ({signal['confidence']:.0%})")
            st.caption(signal["summary"])