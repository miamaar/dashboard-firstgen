# home.py — Home Page | FGS Dashboard HSLU

import streamlit as st

st.markdown("""<style>
[data-testid="stSidebarNav"]     { display:none !important; }
section[data-testid="stSidebar"] { display:none !important; }
[data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header        { visibility:hidden; }

.stApp { background: linear-gradient(140deg, #EAF7F5 0%, #EBF5FF 55%, #EAF7F5 100%) !important; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAVBAR ── */
.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 24px 80px; position: relative; z-index: 10;
}
.nav-logo {
    font-size: 18px; font-weight: 800; color: #1E2A44;
    display: flex; align-items: center; gap: 10px; font-family: Inter, sans-serif;
}
.nav-logo-badge {
    background: #1E2A44; color: #fff;
    padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: 700;
}
.nav-links { display: flex; gap: 40px; align-items: center; }
.nav-links a {
    text-decoration: none; font-size: 13px; font-weight: 600;
    color: #6B7280; text-transform: uppercase; letter-spacing: 0.8px;
    font-family: Inter, sans-serif;
}
.nav-links a.active { color: #00A896; border-bottom: 2px solid #00A896; padding-bottom: 3px; }

/* ── HERO ── */
.hero-wrap {
    position: relative; overflow: hidden;
    min-height: 65vh; display: flex; flex-direction: column;
}
.blob {
    position: absolute; border-radius: 50%;
    filter: blur(70px); opacity: 0.55; pointer-events: none;
}
.blob-1 { width:550px; height:550px; background:#9EEAE0; top:-180px; left:-130px; }
.blob-2 { width:420px; height:420px; background:#A8CFEE; bottom:-80px; right:-80px; }
.blob-3 { width:320px; height:320px; background:#9EEAE0; top:120px; right:160px; }

.hero-body {
    text-align: center; padding: 64px 40px 60px 40px;
    position: relative; z-index: 5; flex: 1;
    display: flex; flex-direction: column; align-items: center;
}
.badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #fff; border: 1px solid #E5E7EB; border-radius: 100px;
    padding: 9px 22px; font-size: 12px; font-weight: 600; color: #6B7280;
    letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 44px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07); font-family: Inter, sans-serif;
}
.badge-dot { color: #00A896; }
.hero-title {
    font-size: 68px; font-weight: 800; color: #1E2A44;
    line-height: 1.1; margin: 0 0 28px 0; font-family: Inter, sans-serif;
}
.hero-title .ital { color: #00A896; font-style: italic; }
.hero-sub {
    font-size: 18px; color: #6B7280; line-height: 1.75;
    max-width: 640px; margin: 0 auto 0 auto; font-family: Inter, sans-serif;
}

/* ── CTA BUTTON (Streamlit button override) ── */
.cta-wrap { padding: 48px 0 72px 0; display: flex; justify-content: center; }
.stButton > button {
    background: #1E2A44 !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    padding: 18px 52px !important; font-size: 13px !important;
    font-weight: 700 !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important; min-width: 280px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #2D3D5C !important; }

/* ── RESEARCH SECTION ── */
.research-wrap { background: #1E2A44; padding: 96px 80px; text-align: center; }
.res-label {
    font-size: 12px; font-weight: 700; letter-spacing: 2px;
    color: #00A896; text-transform: uppercase; margin-bottom: 32px;
    font-family: Inter, sans-serif;
}
.res-quote {
    font-size: 30px; font-style: italic; font-weight: 700; color: #fff;
    max-width: 860px; margin: 0 auto 48px auto; line-height: 1.45;
    font-family: Inter, sans-serif;
}
.res-tags { display:flex; flex-wrap:wrap; justify-content:center; gap:12px; max-width:800px; margin:0 auto; }
.res-tag {
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 100px; padding: 10px 24px; font-size: 14px; color: #fff;
    font-family: Inter, sans-serif;
}
</style>""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
  <div class="navbar">
    <div class="nav-logo">FGS Dashboard&nbsp;<span class="nav-logo-badge">HSLU</span></div>
    <div class="nav-links">
      <a href="#" class="active">Home</a>
      <a href="#">Dashboard</a>
      <a href="#">Forschung</a>
      <a href="#">Methodik</a>
      <a href="#">Kontakt</a>
    </div>
  </div>
  <div class="hero-body">
    <div class="badge"><span class="badge-dot">●</span> Diversity-Projekt FS26 &middot; HSLU Informatik</div>
    <h1 class="hero-title">
      Die unsichtbare<br><span class="ital">Studierendengruppe</span><br>sichtbar machen.
    </h1>
    <p class="hero-sub">
      First-Generation Studierende stehen vor einzigartigen Herausforderungen.
      Dieses Dashboard analysiert ihre Lebensrealitäten, Barrieren und
      Ressourcen&nbsp;— als Grundlage für gezielte Massnahmen.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA BUTTON ───────────────────────────────────────────────────────────────
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("DASHBOARD ERKUNDEN  →", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

# ── FORSCHUNGSFRAGE ───────────────────────────────────────────────────────────
st.markdown("""
<div class="research-wrap">
  <div class="res-label">Forschungsfrage</div>
  <p class="res-quote">
    &ldquo;Welche Faktoren prägen den Studienerfolg von First-Generation
    Studierenden &mdash; und wie können Hochschulen gezielt unterstützen?&rdquo;
  </p>
  <div class="res-tags">
    <span class="res-tag">Bildungsbiografien</span>
    <span class="res-tag">Herausforderungen &amp; Barrieren</span>
    <span class="res-tag">Unterstützungsbedarfe</span>
    <span class="res-tag">Sense of Belonging</span>
    <span class="res-tag">Ressourcen &amp; Erfolgsfaktoren</span>
  </div>
</div>
""", unsafe_allow_html=True)
