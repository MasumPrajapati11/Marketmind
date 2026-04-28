import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Reports — MarketMind",
    page_icon="📈",
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
        --green:#22c55e; --red:#ef4444; --blue:#6366f1;
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
    .nav-item { color: var(--muted); font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 6px; }
    .nav-item.active { background: var(--surface2); color: var(--text); }
    .page-title { font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 6px; letter-spacing: -0.5px; }
    .page-sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }
    .metric-strip { display: flex; gap: 12px; margin-bottom: 24px; }
    .metric-tile { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px 22px; flex: 1; }
    .metric-val { color: var(--text); font-size: 24px; font-weight: 700; font-family: 'DM Mono', monospace; }
    .metric-lbl { color: var(--muted); font-size: 11px; margin-top: 4px; }
    .metric-up { color: var(--green); font-size: 12px; font-weight: 600; margin-top: 4px; }
    .metric-dn { color: var(--red); font-size: 12px; font-weight: 600; margin-top: 4px; }
    .sec-title { color: var(--text); font-size: 15px; font-weight: 600; margin-bottom: 16px; }
    hr { border-color: var(--border) !important; opacity: 1 !important; margin: 24px 0 !important; }
    .stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }
    ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: var(--bg); } ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="brand"><span class="brand-dot"></span> MarketMind</div>
        <div class="nav-items">
            <a href="/" style="text-decoration:none"><div class="nav-item">Dashboard</div></a>
            <a href="/Opportunities" style="text-decoration:none"><div class="nav-item">Opportunities</div></a>
            <div class="nav-item active">Reports</div>
            <a href="/Settings" style="text-decoration:none"><div class="nav-item">Settings</div></a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='page-title'>📈 Performance Reports</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>Historical signal accuracy and agent performance analytics</div>", unsafe_allow_html=True)

st.markdown("""
<div class="metric-strip">
    <div class="metric-tile"><div class="metric-val">73%</div><div class="metric-lbl">Signal Accuracy</div><div class="metric-up">↑ +4% this month</div></div>
    <div class="metric-tile"><div class="metric-val">142</div><div class="metric-lbl">Total Signals</div><div class="metric-up">↑ +18 this week</div></div>
    <div class="metric-tile"><div class="metric-val">89</div><div class="metric-lbl">BUY Signals</div><div class="metric-up">↑ 63%</div></div>
    <div class="metric-tile"><div class="metric-val">31</div><div class="metric-lbl">SELL Signals</div><div class="metric-dn">↓ 22%</div></div>
    <div class="metric-tile"><div class="metric-val">22</div><div class="metric-lbl">HOLD Signals</div><div class="metric-lbl">15%</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='sec-title'>📊 Monthly Accuracy Trend</div>", unsafe_allow_html=True)
months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
accuracy = [61, 65, 68, 70, 69, 73]
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=months, y=accuracy, mode='lines+markers',
    line=dict(color='#6366f1', width=2),
    marker=dict(color='#6366f1', size=7),
    fill='tozeroy', fillcolor='rgba(99,102,241,0.07)',
))
fig.update_layout(
    paper_bgcolor='#0a0a0f', plot_bgcolor='#111118',
    font=dict(color='#6b6b80', family='DM Sans'),
    xaxis=dict(gridcolor='#18181f', color='#6b6b80'),
    yaxis=dict(gridcolor='#18181f', color='#6b6b80', range=[50, 90]),
    margin=dict(l=8, r=8, t=8, b=8), height=280, showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<div class='sec-title'>🤖 Agent Performance</div>", unsafe_allow_html=True)
st.dataframe(pd.DataFrame({
    "Agent":    ["📈 PRICE", "📰 SENTIMENT", "🔗 ONCHAIN", "🌍 MACRO", "⚠️ RISK"],
    "Accuracy": ["78%", "71%", "69%", "74%", "72%"],
    "Avg Conf": ["82%", "74%", "70%", "76%", "73%"],
    "Best At":  ["Trend detection", "News impact", "Whale moves", "Rate changes", "Drawdown avoidance"],
}), use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("<div class='sec-title'>🕐 Recent Signal History</div>", unsafe_allow_html=True)
st.dataframe(pd.DataFrame({
    "Date":       ["2026-04-28", "2026-04-27", "2026-04-26", "2026-04-25", "2026-04-24"],
    "Ticker":     ["BTC", "ETH", "NVDA", "SOL", "TSLA"],
    "Signal":     ["BUY", "BUY", "BUY", "HOLD", "SELL"],
    "Confidence": ["84%", "76%", "71%", "60%", "68%"],
    "Outcome":    ["✅ Correct", "✅ Correct", "✅ Correct", "⏳ Pending", "✅ Correct"],
}), use_container_width=True, hide_index=True)