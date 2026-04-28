# import time
# import streamlit as st
# from graph import graph

# st.set_page_config(page_title="MarketMind", page_icon="🧠", layout="wide")
# st.title("🧠 MarketMind — Parallel Multi-Agent Analyst")

# col1, col2 = st.columns([3, 1])
# with col1:
#     ticker = st.text_input("Enter ticker (e.g. BTC, ETH, AAPL, TSLA)", value="BTC")
# with col2:
#     analyze = st.button("🔍 Analyze", use_container_width=True)

# if analyze and ticker:
#     with st.spinner("Running 5 agents in parallel..."):
#         start = time.time()
#         result = graph.invoke({
#             "ticker": ticker.upper(),
#             "asset_type": "crypto",
#             "agent_signals": [],
#             "final_verdict": None,
#             "final_confidence": None,
#             "final_reasoning": None,
#         })
#         elapsed = round(time.time() - start, 2)

#     verdict = result.get("final_verdict", "N/A")
#     confidence = result.get("final_confidence", 0)
#     reasoning = result.get("final_reasoning", "")

#     color = {"BUY": "green", "SELL": "red", "HOLD": "orange"}.get(verdict, "gray")
#     st.markdown(f"## Final Verdict: :{color}[**{verdict}**] ({confidence:.0%} confidence)")
#     st.info(reasoning)
#     st.caption(f"⏱ Completed in {elapsed}s")

#     st.divider()
#     st.subheader("Agent Signals")
#     cols = st.columns(5)
#     for i, signal in enumerate(result.get("agent_signals", [])):
#         with cols[i % 5]:
#             sig_color = {"BULLISH": "green", "BEARISH": "red", "NEUTRAL": "gray"}.get(signal["signal"], "gray")
#             st.markdown(f"**{signal['agent'].upper()}**")
#             st.markdown(f":{sig_color}[{signal['signal']}] ({signal['confidence']:.0%})")
#             st.caption(signal["summary"])



import time
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from graph import graph

st.set_page_config(
    page_title="MarketMind Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Modern SaaS Theme ─────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --bg:        #0a0a0f;
        --surface:   #111118;
        --surface2:  #18181f;
        --border:    #25252e;
        --border2:   #2e2e3a;
        --text:      #f0f0f5;
        --muted:     #6b6b80;
        --subtle:    #3a3a4a;
        --green:     #22c55e;
        --green-dim: rgba(34,197,94,0.12);
        --red:       #ef4444;
        --red-dim:   rgba(239,68,68,0.12);
        --amber:     #f59e0b;
        --amber-dim: rgba(245,158,11,0.12);
        --blue:      #6366f1;
        --blue-dim:  rgba(99,102,241,0.12);
    }

    * { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
    code, .mono { font-family: 'DM Mono', monospace; }

    .stApp { background-color: var(--bg); color: var(--text); }

    /* hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    h1,h2,h3,h4,h5,h6 { color: var(--text) !important; font-weight: 600 !important; }
    p, label { color: var(--muted) !important; }

    /* ── Topbar ── */
    .topbar {
        position: sticky; top: 0; z-index: 100;
        background: rgba(10,10,15,0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
        padding: 0 32px;
        height: 56px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .topbar-left { display: flex; align-items: center; gap: 32px; }
    .brand {
        font-size: 15px; font-weight: 700; color: var(--text);
        display: flex; align-items: center; gap: 8px; letter-spacing: -0.3px;
    }
    .brand-dot {
        width: 8px; height: 8px; background: var(--green);
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px var(--green);
    }
    .nav-items { display: flex; gap: 4px; }
    .nav-item {
        color: var(--muted); font-size: 13px; font-weight: 500;
        padding: 6px 14px; border-radius: 6px; cursor: pointer;
        transition: all 0.15s;
    }
    .nav-item.active { background: var(--surface2); color: var(--text); }
    .topbar-right { display: flex; align-items: center; gap: 12px; }
    .badge-live {
        background: var(--green-dim); color: var(--green);
        border: 1px solid rgba(34,197,94,0.25);
        border-radius: 20px; padding: 3px 10px;
        font-size: 11px; font-weight: 600; letter-spacing: 0.3px;
    }

    /* ── Page padding ── */
    .page { padding: 32px 40px; }

    /* ── Hero ── */
    .hero {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 56px 48px;
        margin-bottom: 28px;
        position: relative; overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute; inset: 0;
        background: radial-gradient(ellipse 60% 50% at 50% -10%, rgba(99,102,241,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        display: inline-flex; align-items: center; gap: 6px;
        background: var(--blue-dim); color: var(--blue);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 20px; padding: 4px 12px;
        font-size: 11px; font-weight: 600; letter-spacing: 0.8px;
        text-transform: uppercase; margin-bottom: 20px;
    }
    .hero h1 {
        font-size: 44px !important; font-weight: 700 !important;
        color: var(--text) !important; line-height: 1.15 !important;
        letter-spacing: -1px !important; margin-bottom: 14px !important;
    }
    .hero h1 span { color: var(--green); }
    .hero-sub {
        color: var(--muted) !important; font-size: 15px !important;
        max-width: 520px; line-height: 1.65 !important;
        margin: 0 0 28px 0 !important;
    }
    .hero-stats {
        display: flex; gap: 32px; padding-top: 24px;
        border-top: 1px solid var(--border); margin-top: 8px;
    }
    .hero-stat-val { color: var(--text); font-size: 20px; font-weight: 700; }
    .hero-stat-lbl { color: var(--muted); font-size: 11px; margin-top: 2px; letter-spacing: 0.3px; }

    /* ── Inputs ── */
    .stTextInput > div > div > input {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        padding: 11px 14px !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    }
    .stTextInput > div > div > input::placeholder { color: var(--subtle) !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--blue) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 20px !important;
        letter-spacing: 0.2px !important;
        transition: opacity 0.15s, transform 0.1s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Section headers ── */
    .sec-head {
        display: flex; align-items: center; justify-content: space-between;
        padding-bottom: 14px; border-bottom: 1px solid var(--border);
        margin-bottom: 20px;
    }
    .sec-title {
        color: var(--text); font-size: 14px; font-weight: 600;
        display: flex; align-items: center; gap: 8px;
    }
    .sec-count {
        background: var(--surface2); color: var(--muted);
        border: 1px solid var(--border); border-radius: 20px;
        padding: 2px 9px; font-size: 11px; font-weight: 600;
    }

    /* ── Verdict ── */
    .verdict {
        border-radius: 12px; padding: 36px 40px;
        margin-bottom: 8px; text-align: center; position: relative; overflow: hidden;
    }
    .verdict-buy  { background: var(--surface); border: 1px solid var(--green); }
    .verdict-sell { background: var(--surface); border: 1px solid var(--red); }
    .verdict-hold { background: var(--surface); border: 1px solid var(--amber); }
    .verdict-eyebrow {
        color: var(--muted); font-size: 11px; letter-spacing: 1.5px;
        text-transform: uppercase; margin-bottom: 12px;
        font-family: 'DM Mono', monospace;
    }
    .verdict-label {
        font-size: 60px; font-weight: 800; line-height: 1;
        letter-spacing: 4px; margin-bottom: 10px;
        font-family: 'DM Mono', monospace;
    }
    .verdict-conf {
        font-size: 13px; color: var(--muted); margin-bottom: 18px;
    }
    .verdict-reason {
        color: var(--text); font-size: 14px; line-height: 1.7;
        max-width: 580px; margin: 0 auto;
        background: rgba(255,255,255,0.03); border-radius: 8px;
        padding: 14px 18px; border: 1px solid var(--border);
    }

    /* ── Pill badges ── */
    .pill {
        border-radius: 20px; padding: 3px 10px;
        font-size: 11px; font-weight: 700; letter-spacing: 0.4px;
        display: inline-block;
    }
    .pill-bull { background: var(--green-dim); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
    .pill-bear { background: var(--red-dim);   color: var(--red);   border: 1px solid rgba(239,68,68,0.3); }
    .pill-neut { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,158,11,0.3); }

    /* ── Agent cards ── */
    .agent-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
    .agent-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 10px; padding: 18px; transition: border-color 0.2s, transform 0.15s;
    }
    .agent-card:hover { border-color: var(--border2); transform: translateY(-2px); }
    .agent-icon { font-size: 22px; margin-bottom: 10px; }
    .agent-name {
        color: var(--muted); font-size: 10px; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;
    }
    .agent-conf {
        color: var(--text); font-size: 26px; font-weight: 700;
        font-family: 'DM Mono', monospace; margin: 8px 0;
    }
    .agent-summary { color: var(--muted); font-size: 11px; line-height: 1.5; margin-top: 8px; }

    /* ── Metric strip ── */
    .metric-strip { display: flex; gap: 12px; margin: 20px 0; }
    .metric-tile {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 10px; padding: 18px 22px; flex: 1;
    }
    .metric-val { color: var(--text); font-size: 22px; font-weight: 700; font-family: 'DM Mono', monospace; }
    .metric-lbl { color: var(--muted); font-size: 11px; margin-top: 4px; letter-spacing: 0.3px; }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; opacity: 1 !important; margin: 28px 0 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important; border-radius: 8px !important;
    }

    /* ── Dataframe ── */
    .stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }
    [data-testid="stMetricValue"] { color: var(--text) !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--blue) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

    /* ── Footer ── */
    .footer {
        text-align: center; padding: 32px 20px;
        border-top: 1px solid var(--border); margin-top: 40px;
    }
    .footer-warn { color: var(--muted); font-size: 12px; }
    .footer-brand { color: var(--subtle); font-size: 11px; margin-top: 6px; font-family: 'DM Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ─── Topbar ────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="brand">
            <span class="brand-dot"></span> MarketMind
        </div>
        <div class="nav-items">
            <div class="nav-item active">Dashboard</div>
            <div class="nav-item">Opportunities</div>
            <div class="nav-item">Reports</div>
            <div class="nav-item">Settings</div>
        </div>
    </div>
    <div class="topbar-right">
        <span class="badge-live">● LIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='page'>", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">⚡ AI-Powered Analysis</div>
    <h1>Trade Smarter with<br><span>Intelligent Insights</span></h1>
    <p class="hero-sub">
        5 specialized AI agents analyze price action, sentiment, on-chain data,
        macro trends, and risk — delivering a unified verdict in seconds.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">5</div>
            <div class="hero-stat-lbl">AI Agents</div>
        </div>
        <div>
            <div class="hero-stat-val">90d</div>
            <div class="hero-stat-lbl">Price History</div>
        </div>
        <div>
            <div class="hero-stat-val">Real-time</div>
            <div class="hero-stat-lbl">Market Data</div>
        </div>
        <div>
            <div class="hero-stat-val">LLaMA 3.3</div>
            <div class="hero-stat-lbl">70B Model</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Input ─────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    ticker = st.text_input(
        "",
        value="BTC",
        placeholder="Enter ticker symbol — BTC, ETH, AAPL, TSLA, NVDA…"
    )
    c1, c2 = st.columns(2)
    with c1:
        analyze = st.button("📊  Analyze Asset", use_container_width=True)
    with c2:
        st.button("⚙️  Manage Strategies", use_container_width=True)

st.markdown("---")

# ─── Chart helpers ─────────────────────────────────────────
def make_price_chart(ticker, asset_type):
    try:
        yfin_ticker = f"{ticker}-USD" if asset_type == "crypto" else ticker
        data = yf.download(yfin_ticker, period="90d", interval="1d", progress=False)
        if data.empty:
            return None
        close = data["Close"].squeeze()
        dates = data.index
        sma   = close.rolling(20).mean()
        std   = close.rolling(20).std()
        upper = sma + 2 * std
        lower = sma - 2 * std

        fig = go.Figure()
        # Bollinger band fill
        fig.add_trace(go.Scatter(
            x=list(dates) + list(dates[::-1]),
            y=list(upper) + list(lower[::-1]),
            fill='toself', fillcolor='rgba(99,102,241,0.06)',
            line=dict(color='rgba(0,0,0,0)'),
            name='Bollinger Band', showlegend=False
        ))
        # SMA line
        fig.add_trace(go.Scatter(
            x=dates, y=sma,
            line=dict(color='#3a3a4a', width=1, dash='dot'),
            name='SMA 20'
        ))
        # Price line
        fig.add_trace(go.Scatter(
            x=dates, y=close,
            line=dict(color='#22c55e', width=2),
            name='Price', fill='tonexty',
            fillcolor='rgba(34,197,94,0.04)'
        ))
        fig.update_layout(
            paper_bgcolor='#0a0a0f',
            plot_bgcolor='#111118',
            font=dict(color='#6b6b80', family='DM Sans'),
            xaxis=dict(gridcolor='#18181f', color='#6b6b80',
                       showgrid=True, zeroline=False),
            yaxis=dict(gridcolor='#18181f', color='#6b6b80',
                       showgrid=True, zeroline=False),
            legend=dict(bgcolor='#18181f', bordercolor='#25252e',
                        font=dict(color='#f0f0f5'), borderwidth=1),
            margin=dict(l=8, r=8, t=8, b=8),
            height=320,
        )
        return fig
    except Exception:
        return None


def make_gauge(value, title):
    color = "#22c55e" if value >= 0.7 else "#f59e0b" if value >= 0.5 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        title={"text": title, "font": {"color": "#6b6b80", "size": 11, "family": "DM Sans"}},
        number={"suffix": "%", "font": {"color": color, "size": 22, "family": "DM Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#25252e",
                     "tickfont": {"color": "#6b6b80", "size": 9}},
            "bar": {"color": color, "thickness": 0.6},
            "bgcolor": "#111118",
            "bordercolor": "#25252e",
            "borderwidth": 1,
            "steps": [
                {"range": [0,  40], "color": "#110d0d"},
                {"range": [40, 70], "color": "#111008"},
                {"range": [70,100], "color": "#0a110d"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="#0a0a0f", plot_bgcolor="#0a0a0f",
        margin=dict(l=16, r=16, t=44, b=8), height=170,
    )
    return fig


def make_bar_chart(signals):
    agents      = [s["agent"].upper() for s in signals]
    confidences = [s["confidence"] * 100 for s in signals]
    colors = []
    for s in signals:
        if   s["signal"] == "BULLISH": colors.append("#22c55e")
        elif s["signal"] == "BEARISH": colors.append("#ef4444")
        else:                          colors.append("#f59e0b")

    fig = go.Figure(go.Bar(
        x=agents, y=confidences,
        marker_color=colors,
        marker_line_color='#25252e', marker_line_width=1,
        text=[f"{c:.0f}%" for c in confidences],
        textposition='outside',
        textfont=dict(color='#f0f0f5', family='DM Mono', size=11),
    ))
    fig.update_layout(
        paper_bgcolor='#0a0a0f', plot_bgcolor='#111118',
        font=dict(color='#6b6b80', family='DM Sans'),
        xaxis=dict(gridcolor='#18181f', color='#6b6b80'),
        yaxis=dict(gridcolor='#18181f', color='#6b6b80', range=[0, 118]),
        margin=dict(l=8, r=8, t=8, b=8), height=260, showlegend=False,
    )
    return fig


def make_radar(signals):
    agents = [s["agent"].upper() for s in signals]
    scores = []
    for s in signals:
        if   s["signal"] == "BULLISH": scores.append(s["confidence"] * 100)
        elif s["signal"] == "BEARISH": scores.append((1 - s["confidence"]) * 100)
        else:                          scores.append(50)

    fig = go.Figure(go.Scatterpolar(
        r=scores + [scores[0]], theta=agents + [agents[0]],
        fill='toself', fillcolor='rgba(99,102,241,0.12)',
        line=dict(color='#6366f1', width=2),
        marker=dict(color='#6366f1', size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='#111118',
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor='#25252e', color='#6b6b80',
                            tickfont=dict(size=9)),
            angularaxis=dict(gridcolor='#25252e', color='#f0f0f5',
                             tickfont=dict(size=11)),
        ),
        paper_bgcolor='#0a0a0f',
        font=dict(color='#f0f0f5', family='DM Sans'),
        margin=dict(l=40, r=40, t=40, b=40), height=290, showlegend=False,
    )
    return fig


# ─── Main Analysis ─────────────────────────────────────────
if analyze and ticker:
    with st.spinner("Running parallel agents…"):
        start  = time.time()
        result = graph.invoke({
            "ticker":           ticker.upper(),
            "asset_type":       "crypto",
            "agent_signals":    [],
            "final_verdict":    None,
            "final_confidence": None,
            "final_reasoning":  None,
        })
        elapsed = round(time.time() - start, 2)

    verdict    = result.get("final_verdict",    "N/A")
    confidence = result.get("final_confidence", 0)
    reasoning  = result.get("final_reasoning",  "")
    signals    = result.get("agent_signals",     [])

    crypto_list = {"BTC","ETH","SOL","BNB","DOGE","ADA","AVAX","DOT","MATIC","LINK","XRP","LTC"}
    asset_type  = "crypto" if ticker.upper() in crypto_list else "stock"

    # ── Verdict ──
    v_map = {
        "BUY":  ("#22c55e", "verdict-buy"),
        "SELL": ("#ef4444", "verdict-sell"),
        "HOLD": ("#f59e0b", "verdict-hold"),
    }
    vc, vcls = v_map.get(verdict, ("#6b6b80", "verdict-hold"))

    st.markdown(f"""
    <div class="verdict {vcls}">
        <div class="verdict-eyebrow">{ticker.upper()} · Analysis Complete · {elapsed}s</div>
        <div class="verdict-label" style="color:{vc}">{verdict}</div>
        <div class="verdict-conf">{confidence:.0%} Confidence</div>
        <div class="verdict-reason">{reasoning}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metric strip ──
    bull = sum(1 for s in signals if s["signal"] == "BULLISH")
    bear = sum(1 for s in signals if s["signal"] == "BEARISH")
    avg  = sum(s["confidence"] for s in signals) / len(signals) if signals else 0

    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-tile">
            <div class="metric-val">{confidence:.0%}</div>
            <div class="metric-lbl">Overall Confidence</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val" style="color:#22c55e">{bull}</div>
            <div class="metric-lbl">Bullish Agents</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val" style="color:#ef4444">{bear}</div>
            <div class="metric-lbl">Bearish Agents</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val">{avg:.0%}</div>
            <div class="metric-lbl">Avg Agent Confidence</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val">{elapsed}s</div>
            <div class="metric-lbl">Analysis Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Agent signals table ──
    st.markdown("""
    <div class="sec-head">
        <div class="sec-title">📅 Today's Trading Opportunities <span class="sec-count">5 Agents</span></div>
    </div>
    """, unsafe_allow_html=True)

    icons = {"price":"📈","sentiment":"📰","onchain":"🔗","macro":"🌍","risk":"⚠️"}
    table_data = [{
        "Agent":      f"{icons.get(s['agent'],'🤖')} {s['agent'].upper()}",
        "Signal":     s["signal"],
        "Confidence": f"{s['confidence']:.0%}",
        "Summary":    s["summary"],
    } for s in signals]

    if table_data:
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Price chart + gauges ──
    st.markdown("""
    <div class="sec-title" style="margin-bottom:16px;">📈 Price Analysis — 90 Day Chart</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        price_fig = make_price_chart(ticker, asset_type)
        if price_fig:
            st.plotly_chart(price_fig, use_container_width=True)
    with col2:
        st.plotly_chart(make_gauge(confidence, "OVERALL CONFIDENCE"), use_container_width=True)
        for s in signals[:2]:
            st.plotly_chart(make_gauge(s["confidence"], s["agent"].upper()), use_container_width=True)

    st.markdown("---")

    # ── Radar + Bar ──
    st.markdown("""
    <div class="sec-title" style="margin-bottom:16px;">🎯 Agent Signal Overview</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_radar(signals), use_container_width=True)
    with col2:
        st.plotly_chart(make_bar_chart(signals), use_container_width=True)

    st.markdown("---")

    # ── Agent cards ──
    st.markdown("""
    <div class="sec-head">
        <div class="sec-title">🤖 Active Agent Signals <span class="sec-count">5</span></div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, signal in enumerate(signals):
        with cols[i % 5]:
            sig    = signal["signal"]
            pill   = "pill-bull" if sig == "BULLISH" else "pill-bear" if sig == "BEARISH" else "pill-neut"
            icon   = icons.get(signal["agent"], "🤖")
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-icon">{icon}</div>
                <div class="agent-name">{signal['agent']}</div>
                <span class="pill {pill}">{sig}</span>
                <div class="agent-conf">{signal['confidence']:.0%}</div>
                <div class="agent-summary">{signal['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Raw metrics ──
    st.markdown("""
    <div class="sec-title" style="margin-bottom:16px;">📊 Raw Agent Metrics</div>
    """, unsafe_allow_html=True)

    for signal in signals:
        if signal["raw_data"]:
            with st.expander(f"{icons.get(signal['agent'],'🤖')} {signal['agent'].upper()} — Detailed Metrics"):
                df = pd.DataFrame(signal["raw_data"].items(), columns=["Metric", "Value"])
                st.dataframe(df, use_container_width=True, hide_index=True)

# ─── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-warn">⚠️ Not financial advice · For research purposes only</div>
    <div class="footer-brand">MarketMind Pro · LangGraph + Groq + LLaMA 3.3 70B</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close .page