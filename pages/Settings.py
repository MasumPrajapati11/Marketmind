import streamlit as st

st.set_page_config(
    page_title="Settings — MarketMind",
    page_icon="⚙️",
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
    .nav-item { color: var(--muted); font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 6px; }
    .nav-item.active { background: var(--surface2); color: var(--text); }
    .page-title { font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 6px; letter-spacing: -0.5px; }
    .page-sub { color: var(--muted); font-size: 14px; margin-bottom: 28px; }
    .settings-section {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 12px; padding: 24px 28px; margin-bottom: 16px;
    }
    .settings-title { color: var(--text); font-size: 14px; font-weight: 600; margin-bottom: 4px; }
    .settings-sub { color: var(--muted); font-size: 12px; margin-bottom: 20px; }
    .stTextInput > div > div > input {
        background-color: var(--surface2) !important; color: var(--text) !important;
        border: 1px solid var(--border2) !important; border-radius: 8px !important;
        font-family: 'DM Mono', monospace !important;
    }
    .stTextInput > div > div > input:focus { border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important; }
    .stSelectbox > div > div { background: var(--surface2) !important; border-color: var(--border2) !important; color: var(--text) !important; }
    .stButton > button {
        background: var(--blue) !important; color: #fff !important;
        border: none !important; border-radius: 8px !important;
        font-weight: 600 !important; font-size: 13px !important; padding: 10px 24px !important;
    }
    .badge-saved { background: var(--green-dim); color: var(--green); border: 1px solid rgba(34,197,94,0.3); border-radius: 6px; padding: 8px 16px; font-size: 13px; font-weight: 600; }
    hr { border-color: var(--border) !important; opacity: 1 !important; margin: 24px 0 !important; }
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
            <a href="/Reports" style="text-decoration:none"><div class="nav-item">Reports</div></a>
            <div class="nav-item active">Settings</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='page-title'>⚙️ Settings</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>Configure API keys, model preferences, and agent behaviour</div>", unsafe_allow_html=True)

st.markdown("""
<div class="settings-section">
    <div class="settings-title">🔑 API Keys</div>
    <div class="settings-sub">Stored securely — never committed to GitHub</div>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.text_input("News API Key", type="password", placeholder="newsapi_...")
with col2:
    st.text_input("FRED API Key", type="password", placeholder="fred_...")
    st.text_input("CoinGecko API Key", type="password", placeholder="cg_...")

st.markdown("---")
st.markdown("""
<div class="settings-section">
    <div class="settings-title">🤖 Model Settings</div>
    <div class="settings-sub">Configure AI model and analysis parameters</div>
</div>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
with col2:
    st.selectbox("Default Asset Type", ["Auto Detect", "Crypto", "Stock"])
with col3:
    st.selectbox("Chart Period", ["90d", "30d", "60d", "180d", "1y"])

st.markdown("---")
st.markdown("""
<div class="settings-section">
    <div class="settings-title">⚡ Agent Configuration</div>
    <div class="settings-sub">Enable or disable individual analysis agents</div>
</div>
""", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.toggle("📈 Price", value=True)
with col2: st.toggle("📰 Sentiment", value=True)
with col3: st.toggle("🔗 On-chain", value=True)
with col4: st.toggle("🌍 Macro", value=True)
with col5: st.toggle("⚠️ Risk", value=True)

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("💾  Save Settings", use_container_width=True):
        st.markdown("<div class='badge-saved'>✅ Saved!</div>", unsafe_allow_html=True)
with col2:
    if st.button("↺  Reset", use_container_width=True):
        st.rerun()