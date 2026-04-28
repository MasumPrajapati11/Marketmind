import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Opportunities — MarketMind",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
    :root {
        --bg:#0a0a0f; --surface:#111118; --surface2:#18181f;
        --border:#25252e; --border2:#2e2e3a;
        --text:#f0f0f5; --muted:#6b6b80;
        --green:#22c55e; --green-dim:rgba(34,197,94,0.12);
        --red:#ef4444; --red-dim:rgba(239,68,68,0.12);
        --amber:#f59e0b; --amber-dim:rgba(245,158,11,0.12);
        --blue:#6366f1;
    }
    * { font-family: 'DM Sans', sans-serif; }
    .stApp { background-color: var(--bg); color: var(--text); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem !important; max-width: 100% !important; }
    h1,h2,h3 { color: var(--text) !important; font-weight: 600 !important; }
    p, label { color: var(--muted) !important; }
    .topbar {
        background: rgba(10,10,15,0.95); border-bottom: 1px solid var(--border);
        padding: 0 32px; height: 56px;
        display: flex; align-items: center;
        margin: -2rem -3rem 2rem -3rem;
    }
    .topbar-left { display: flex; align-items: center; gap: 32px; }
    .brand { font-size: 15px; font-weight: 700; color: var(--text); display: flex; align-items: center; gap: 8px; }
    .brand-dot { width: 8px; height: 8px; background: var(--green); border-radius: 50%; display: inline-block; box-shadow: 0 0 8px var(--green); }
    .nav-items { display: flex; gap: 4px; }
    .nav-item { color: var(--muted); font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 6px; cursor: pointer; }
    .nav-item.active { background: var(--surface2); color: var(--text); }
    .page-title { font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 6px; letter-spacing: -0.5px; }
    .page-sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }
    .opp-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 12px; padding: 20px 24px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .opp-ticker { font-size: 18px; font-weight: 700; color: var(--text); font-family: 'DM Mono', monospace; }
    .opp-name { color: var(--muted); font-size: 12px; margin-top: 2px; }
    .opp-conf { font-family: 'DM Mono', monospace; font-size: 20px; font-weight: 700; color: var(--text); }
    .opp-conf-lbl { color: var(--muted); font-size: 11px; }
    .pill { border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 700; display: inline-block; }
    .pill-bull { background: var(--green-dim); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
    .pill-bear { background: var(--red-dim); color: var(--red); border: 1px solid rgba(239,68,68,0.3); }
    .pill-neut { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,158,11,0.3); }
    .stSelectbox > div > div { background: var(--surface) !important; border-color: var(--border2) !important; color: var(--text) !important; }
    ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: var(--bg); } ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="brand"><span class="brand-dot"></span> MarketMind</div>
        <div class="nav-items">
            <a href="/" style="text-decoration:none"><div class="nav-item">Dashboard</div></a>
            <div class="nav-item active">Opportunities</div>
            <a href="/Reports" style="text-decoration:none"><div class="nav-item">Reports</div></a>
            <a href="/Settings" style="text-decoration:none"><div class="nav-item">Settings</div></a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='page-title'>📅 Trading Opportunities</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>Top opportunities detected by AI agents across crypto & stocks</div>", unsafe_allow_html=True)

opportunities = [
    {"ticker": "BTC",  "name": "Bitcoin",       "signal": "BUY",  "confidence": 0.84, "agents": 4, "type": "Crypto"},
    {"ticker": "ETH",  "name": "Ethereum",       "signal": "BUY",  "confidence": 0.76, "agents": 4, "type": "Crypto"},
    {"ticker": "NVDA", "name": "NVIDIA Corp",    "signal": "BUY",  "confidence": 0.71, "agents": 3, "type": "Stock"},
    {"ticker": "SOL",  "name": "Solana",         "signal": "HOLD", "confidence": 0.60, "agents": 3, "type": "Crypto"},
    {"ticker": "TSLA", "name": "Tesla Inc",      "signal": "SELL", "confidence": 0.68, "agents": 4, "type": "Stock"},
    {"ticker": "AAPL", "name": "Apple Inc",      "signal": "HOLD", "confidence": 0.55, "agents": 3, "type": "Stock"},
    {"ticker": "BNB",  "name": "Binance Coin",   "signal": "BUY",  "confidence": 0.72, "agents": 4, "type": "Crypto"},
    {"ticker": "AVAX", "name": "Avalanche",      "signal": "SELL", "confidence": 0.65, "agents": 3, "type": "Crypto"},
]

col1, col2 = st.columns([1, 1])
with col1:
    signal_filter = st.selectbox("Signal", ["All", "BUY", "SELL", "HOLD"])
with col2:
    type_filter = st.selectbox("Type", ["All", "Crypto", "Stock"])

filtered = opportunities
if signal_filter != "All":
    filtered = [o for o in filtered if o["signal"] == signal_filter]
if type_filter != "All":
    filtered = [o for o in filtered if o["type"] == type_filter]

st.markdown(f"<div style='color:var(--muted);font-size:13px;margin-bottom:16px;'>{len(filtered)} opportunities found</div>", unsafe_allow_html=True)

for opp in filtered:
    pill_cls = "pill-bull" if opp["signal"] == "BUY" else "pill-bear" if opp["signal"] == "SELL" else "pill-neut"
    conf_color = "#22c55e" if opp["confidence"] >= 0.7 else "#f59e0b" if opp["confidence"] >= 0.5 else "#ef4444"
    st.markdown(f"""
    <div class="opp-card">
        <div>
            <div class="opp-ticker">{opp['ticker']}</div>
            <div class="opp-name">{opp['name']} · {opp['type']}</div>
        </div>
        <span class="pill {pill_cls}">{opp['signal']}</span>
        <div style="text-align:center">
            <div class="opp-conf" style="color:{conf_color}">{opp['confidence']:.0%}</div>
            <div class="opp-conf-lbl">Confidence</div>
        </div>
        <div style="text-align:center">
            <div class="opp-conf">{opp['agents']}/5</div>
            <div class="opp-conf-lbl">Agents Agree</div>
        </div>
    </div>
    """, unsafe_allow_html=True)