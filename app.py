# app.py — FGS Dashboard | HSLU Informatik

import streamlit as st
import pandas as pd

from config import *
from preprocessing import load_data, calculate_belonging_scores
import plotly.graph_objects as go
import plotly.express as px
from charts import (chart_fgs_bar, chart_belonging_bars)

st.set_page_config(
    page_title="FGS Dashboard | HSLU Informatik",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SEITENSTATUS (kein Browser-Reload) ───────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
page = st.session_state.page

# nth-child-Index des aktiven Navbar-Buttons (Logo=1, Spacer=2, Home=3, Dashboard=4, Über=5, Kontakt=6)
_active_nth = 3 if page == "home" else (4 if page == "dashboard" else 5)
_bg = "linear-gradient(140deg,#EAF7F5 0%,#EBF5FF 55%,#EAF7F5 100%)" if page == "home" else "#F5F7FB"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""<style>
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"],
[data-testid="collapsedControl"],
#MainMenu, footer, header {{ display:none !important; visibility:hidden; }}

.stApp {{
    background:{_bg} !important;
}}
.main, .main .block-container,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    padding:0 !important; max-width:100% !important; margin:0 !important;
    background:transparent !important;
}}
[data-testid="stMainBlockContainer"] {{
    max-width:1400px !important;
    margin:0 auto !important;
    padding:0 2.5rem !important;
    background:transparent !important;
    box-sizing:border-box !important;
}}
div[data-testid="stVerticalBlock"],
div[data-testid="column"] {{
    background:transparent !important;
}}
div[data-testid="stHorizontalBlock"]:not(:first-of-type) {{
    background:{"transparent" if page == "home" else "#FFFFFF"} !important;
}}
/* Fallback ohne :has – Label über Selectbox bekommt mehr Luft nach oben */
div[data-baseweb="select"] {{
    margin-top:4px !important;
}}
div[data-testid="stMarkdown"],
div[data-testid="stMarkdownContainer"],
div[data-testid="stElementContainer"],
.stMarkdown {{
    background:transparent !important;
}}

/* ── NAVBAR: erster horizontaler Block ── */
div[data-testid="stHorizontalBlock"]:first-of-type {{
    background:#fff !important;
    padding:0 60px !important;
    min-height:52px !important;
    box-shadow:0 1px 8px rgba(0,0,0,0.06) !important;
    position:sticky !important; top:0 !important; z-index:100 !important;
    display:flex !important; align-items:center !important;
}}
/* Alle Column-, Block- und Element-Wrapper im Navbar auf null setzen */
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"],
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stElementContainer"],
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stMarkdown"],
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stMarkdownContainer"],
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] {{
    padding:0 !important;
    margin:0 !important;
    display:flex !important;
    align-items:center !important;
    line-height:1 !important;
}}
/* Alle Buttons im Navbar: Text-Link-Style */
div[data-testid="stHorizontalBlock"]:first-of-type button {{
    background:transparent !important; border:none !important;
    box-shadow:none !important; border-radius:0 !important;
    color:#6B7280 !important; font-size:12px !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:1px !important; padding:0 4px !important;
    width:100% !important; min-height:0 !important; min-width:0 !important;
    line-height:1 !important; position:relative !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type button:hover {{
    color:#1E2A44 !important; background:transparent !important;
    border:none !important;
}}
/* Aktiver Navbar-Button: nur Farbe ändern, kein Layout */
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child({_active_nth}) button {{
    color:#00A896 !important;
}}
/* Aktive Linie als ::after – ausserhalb des Layouts, kein Textversatz */
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child({_active_nth}) button::after {{
    content:"" !important;
    position:absolute !important;
    bottom:-12px !important;
    left:0 !important; right:0 !important;
    height:2px !important;
    background:#00A896 !important;
    border-radius:1px !important;
}}

/* ── CTA BUTTON (alle anderen Buttons = grosser dunkler Button) ── */
.stButton > button {{
    background:#1E2A44 !important; color:#fff !important;
    border:none !important; border-radius:10px !important;
    padding:18px 52px !important; font-size:13px !important;
    font-weight:700 !important; letter-spacing:1.5px !important;
    text-transform:uppercase !important; min-width:280px !important;
    transition:background 0.2s !important;
}}
.stButton > button:hover {{ background:#2D3D5C !important; }}

/* ── HOME ── */
.hero-wrap {{
    position:relative; overflow:hidden;
    min-height:70vh; display:flex; flex-direction:column;
}}
.blob {{
    position:absolute; border-radius:50%;
    filter:blur(70px); opacity:0.55; pointer-events:none;
}}
.blob-1 {{ width:550px;height:550px;background:#9EEAE0;top:-180px;left:-130px; }}
.blob-2 {{ width:420px;height:420px;background:#A8CFEE;bottom:-80px;right:-80px; }}
.blob-3 {{ width:320px;height:320px;background:#9EEAE0;top:120px;right:160px; }}

.hero-body {{
    text-align:center; padding:72px 40px 64px 40px;
    position:relative; z-index:5; flex:1;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}}
.badge {{
    display:inline-flex; align-items:center; gap:8px;
    background:#fff; border:1px solid #E5E7EB; border-radius:100px;
    padding:9px 22px; font-size:12px; font-weight:600; color:#6B7280;
    letter-spacing:0.8px; text-transform:uppercase; margin-bottom:44px;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); font-family:Inter,sans-serif;
}}
.badge-dot {{ color:#00A896; }}
.hero-title {{
    font-size:68px; font-weight:800; color:#1E2A44;
    line-height:1.1; margin:0 0 28px 0; font-family:Inter,sans-serif;
}}
.hero-title .ital {{ color:#00A896; font-style:italic; }}
.hero-sub {{
    font-size:18px; color:#6B7280; line-height:1.75;
    max-width:640px; margin:0 auto; font-family:Inter,sans-serif;
}}

.research-wrap {{
    background:#1E2A44; padding:96px 80px;
    display:flex; flex-direction:column; align-items:center; text-align:center;
}}
.res-label {{
    font-size:12px; font-weight:700; letter-spacing:2px;
    color:#00A896; text-transform:uppercase; margin-bottom:32px; font-family:Inter,sans-serif;
}}
.res-quote {{
    font-size:30px; font-style:italic; font-weight:700; color:#fff;
    max-width:680px; margin:0 0 48px 0; line-height:1.45; font-family:Inter,sans-serif;
    text-align:center !important;
}}
.res-tags {{ display:flex; flex-wrap:wrap; justify-content:center; gap:12px; max-width:800px; margin:0 auto; }}
.res-tag {{
    background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2);
    border-radius:100px; padding:10px 24px; font-size:14px; color:#fff; font-family:Inter,sans-serif;
}}

/* ── DASHBOARD ── */
.dash-wrap {{ background:#F5F7FB; padding:0 0 2rem 0; max-width:100%; margin:0; }}
.stTabs [data-baseweb="tab-list"] {{
    background:#FFFFFF; border-radius:10px; padding:4px 8px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-bottom:1.5rem; gap:4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius:8px; padding:8px 24px; font-size:14px; font-weight:500; color:#6B7280;
}}
.stTabs [aria-selected="true"] {{ background-color:#1E2A44 !important; color:#FFFFFF !important; }}
.card {{
    background:#FFFFFF; border-radius:12px; padding:1rem 1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); margin-bottom:1rem; border:1px solid #E5E7EB;
}}
.section-title {{
    font-size:17px; font-weight:600; color:#1E2A44;
    margin:2rem 0 1rem 0; padding-bottom:0.5rem; border-bottom:2px solid #EFEFEF;
}}
.kpi-card {{
    background:#FFFFFF; border-radius:12px; padding:1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); text-align:center; border:1px solid #E5E7EB;
}}
.kpi-value {{ font-size:2rem; font-weight:700; line-height:1.2; }}
.kpi-label {{ font-size:12px; color:#6B7280; margin-top:4px; }}
.ctx-card {{
    background:#FFFFFF; border-radius:12px; padding:1rem 1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); border-left:4px solid;
    border-right:1px solid #E5E7EB; border-top:1px solid #E5E7EB; border-bottom:1px solid #E5E7EB;
}}
.insight-box {{
    background:#F0F9FF; border-left:4px solid #2D9CDB;
    border-radius:8px; padding:1rem 1.25rem; margin-top:0.5rem;
}}
</style>""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
logo_col, spacer, c_home, c_dash, c_ueber = st.columns(
    [2.5, 3.8, 0.9, 1.1, 1.5]
)
with logo_col:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0;line-height:1;">
      <span style="font-size:12px;font-weight:700;color:#00A896;
                   font-family:Inter,sans-serif;letter-spacing:1px;text-transform:uppercase;">FGS</span>
      <span style="font-size:12px;font-weight:700;color:#1E2A44;
                   font-family:Inter,sans-serif;letter-spacing:1px;text-transform:uppercase;">&nbsp;Dashboard</span>
      <span style="font-size:11px;font-weight:500;color:#9CA3AF;font-family:Inter,sans-serif;
                   letter-spacing:1.2px;text-transform:uppercase;
                   margin-left:12px;padding-left:12px;border-left:1px solid #E5E7EB;">HSLU</span>
    </div>
    """, unsafe_allow_html=True)
with c_home:
    if st.button("Home", key="nav_home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
with c_dash:
    if st.button("Dashboard", key="nav_dash", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
with c_ueber:
    if st.button("Über die Daten", key="nav_ueber", use_container_width=True):
        st.session_state.page = "ueber"
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# HOME
# ════════════════════════════════════════════════════════════════════════════
if page == "home":
    st.markdown("""
    <div class="hero-wrap">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
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

    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("DASHBOARD ERKUNDEN  →", key="cta", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

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


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif page == "dashboard":
    df_raw = load_data()

    n_total = len(df_raw)
    st.markdown(f"""
    <div style="background:#FFFFFF;border-radius:16px;padding:1.5rem 2rem;
                box-shadow:0 2px 12px rgba(0,0,0,0.07);margin-bottom:1.5rem;
                border:1px solid #E5E7EB;
                display:flex;justify-content:space-between;align-items:flex-start;">
      <div>
        <h1 style="font-size:26px;font-weight:700;color:#1E2A44;margin:0 0 4px 0;">FGS Dashboard</h1>
        <p style="font-size:15px;color:#4B5563;margin:0 0 6px 0;">
          Studienerfahrungen, Herausforderungen und Unterstützungsbedarfe von First-Generation Studierenden</p>
        <p style="font-size:13px;color:#9CA3AF;margin:0;">
          Das Dashboard macht zentrale Aspekte der Situation von First-Generation Studierenden sichtbar.</p>
      </div>
      <div style="text-align:right;flex-shrink:0;padding-left:2rem;">
        <div style="font-size:12px;color:#9CA3AF;">Teilnehmende</div>
        <div style="font-size:28px;font-weight:700;color:#1E2A44;">{n_total} Antworten</div>
        <div style="font-size:12px;color:#9CA3AF;">Datenstand 2026</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
      <div class="ctx-card" style="border-left-color:#2D9CDB;">
        <div style="font-size:11px;font-weight:700;color:#2D9CDB;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Projektziel</div>
        <p style="font-size:13px;color:#374151;margin:0;line-height:1.5;">Bildungsbiografien, Herausforderungen und Ressourcen von Studierenden sichtbar machen.</p>
      </div>
      <div class="ctx-card" style="border-left-color:#00A896;">
        <div style="font-size:11px;font-weight:700;color:#00A896;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Definition FGS</div>
        <p style="font-size:13px;color:#374151;margin:0;line-height:1.5;">Personen, deren Eltern keinen Hochschulabschluss besitzen und die als erste in ihrer Familie studieren.</p>
      </div>
      <div class="ctx-card" style="border-left-color:#7B61FF;">
        <div style="font-size:11px;font-weight:700;color:#7B61FF;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Datenquelle</div>
        <p style="font-size:13px;color:#374151;margin:0;line-height:1.5;">Google-Forms-Befragung, bereinigt, anonymisiert, aggregiert und interaktiv visualisiert.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # FILTER
    st.markdown('<div style="padding:0.75rem 0;margin-bottom:1rem;">',
                unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;font-weight:700;color:#9CA3AF;'
                'text-transform:uppercase;letter-spacing:1.5px;margin:0 0 10px 0;">Filter</p>',
                unsafe_allow_html=True)
    f1, f2, f3, f4, f5, f6 = st.columns(6)
    _sp = '<div style="height:14px"></div>'
    with f1:
        st.markdown(_sp, unsafe_allow_html=True)
        sel_gruppe = st.selectbox("Gruppe", ["Alle", "FGS", "Non-FGS"], key="fg")
        st.markdown(_sp, unsafe_allow_html=True)
    with f2:
        st.markdown(_sp, unsafe_allow_html=True)
        sg_opts = (["Alle"] + sorted(df_raw[COL_STUDIENGANG].dropna().unique().tolist())
                   if COL_STUDIENGANG in df_raw.columns else ["Alle"])
        sel_sg = st.selectbox("Studiengang", sg_opts, key="fsg")
        st.markdown(_sp, unsafe_allow_html=True)
    with f3:
        st.markdown(_sp, unsafe_allow_html=True)
        g_opts = (["Alle"] + sorted(df_raw[COL_GESCHLECHT].dropna().unique().tolist())
                  if COL_GESCHLECHT in df_raw.columns else ["Alle"])
        sel_g = st.selectbox("Geschlecht", g_opts, key="fg2")
        st.markdown(_sp, unsafe_allow_html=True)
    with f4:
        st.markdown(_sp, unsafe_allow_html=True)
        a_opts = (["Alle"] + sorted(df_raw[COL_ARBEIT].dropna().unique().tolist())
                  if COL_ARBEIT in df_raw.columns else ["Alle"])
        sel_a = st.selectbox("Erwerbstätigkeit", a_opts, key="fa")
        st.markdown(_sp, unsafe_allow_html=True)
    with f5:
        st.markdown(_sp, unsafe_allow_html=True)
        m_opts = (["Alle"] + sorted(df_raw[COL_MIGRATION].dropna().unique().tolist())
                  if COL_MIGRATION in df_raw.columns else ["Alle"])
        sel_m = st.selectbox("Migration", m_opts, key="fm")
        st.markdown(_sp, unsafe_allow_html=True)
    with f6:
        st.markdown(_sp, unsafe_allow_html=True)
        j_opts = (["Alle"] + sorted(df_raw[COL_ABSCHLUSSJAHR].dropna().unique().tolist())
                  if COL_ABSCHLUSSJAHR in df_raw.columns else ["Alle"])
        sel_j = st.selectbox("Jahr", j_opts, key="fj")
        st.markdown(_sp, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # FILTER ANWENDEN
    df = df_raw.copy()
    if sel_gruppe == "FGS":      df = df[df[COL_FGS].str.lower() == "ja"]
    if sel_gruppe == "Non-FGS":  df = df[df[COL_FGS].str.lower() == "nein"]
    if sel_sg != "Alle" and COL_STUDIENGANG   in df.columns: df = df[df[COL_STUDIENGANG]    == sel_sg]
    if sel_g  != "Alle" and COL_GESCHLECHT    in df.columns: df = df[df[COL_GESCHLECHT]     == sel_g]
    if sel_a  != "Alle" and COL_ARBEIT        in df.columns: df = df[df[COL_ARBEIT]         == sel_a]
    if sel_m  != "Alle" and COL_MIGRATION     in df.columns: df = df[df[COL_MIGRATION]      == sel_m]
    if sel_j  != "Alle" and COL_ABSCHLUSSJAHR in df.columns: df = df[df[COL_ABSCHLUSSJAHR]  == sel_j]

    df_fgs  = df[df[COL_FGS].str.lower() == "ja"].copy()  if COL_FGS in df.columns else df.copy()
    df_nfgs = df[df[COL_FGS].str.lower() == "nein"].copy() if COL_FGS in df.columns else pd.DataFrame()

    # Non-FGS-Filter: df_fgs ist leer weil df nur "nein"-Zeilen enthält.
    # Tausch: Non-FGS-Daten in df_fgs laden, df_nfgs leer lassen.
    if sel_gruppe == "Non-FGS":
        df_fgs  = df_nfgs.copy()
        df_nfgs = pd.DataFrame()

    # ── KPI helpers ──────────────────────────────────────────────────────────
    from collections import Counter

    def _top_multiselect(series):
        """Splits comma-separated answers, returns (top_item, count) or (None, 0)."""
        items = []
        for val in series.dropna():
            for part in str(val).split(","):
                part = part.strip()
                if part:
                    items.append(part)
        if not items:
            return None, 0
        top, count = Counter(items).most_common(1)[0]
        return top, count

    # Numeric KPI values
    _n_total     = len(df_raw)
    _n_fgs_kpi   = len(df_fgs)
    _n_all_kpi   = len(df)
    _pct_fgs_kpi = round(_n_fgs_kpi / _n_all_kpi * 100) if _n_all_kpi > 0 else 0

    _sob_cols_fgs = [c for g in SOB_GROUPS.values() for c in g if c in df_fgs.columns]
    _sob_fgs_val  = df_fgs[_sob_cols_fgs].mean().mean() if (_sob_cols_fgs and len(df_fgs) > 0) else None
    _sob_fgs      = round(_sob_fgs_val, 1) if (_sob_fgs_val is not None and pd.notna(_sob_fgs_val)) else None

    # Insight values (multi-select aware)
    _krit_phase, _krit_n = None, 0
    if COL_HERAUSFORDERND in df_fgs.columns and len(df_fgs) >= MIN_N:
        _krit_phase, _krit_n = _top_multiselect(df_fgs[COL_HERAUSFORDERND])

    _top_support, _support_n = None, 0
    if COL_SUPPORT_GEWUENSCHT in df_fgs.columns and len(df_fgs) >= MIN_N:
        _top_support, _support_n = _top_multiselect(df_fgs[COL_SUPPORT_GEWUENSCHT])

    # ── 4 numeric KPI cards ───────────────────────────────────────────────────
    def _num_kpi(main, sub, label, color):
        return (
            f'<div style="background:#fff;border-radius:12px;padding:20px 18px 16px;'
            f'border-top:4px solid {color};box-shadow:0 1px 6px rgba(0,0,0,0.07);">'
            f'<div style="font-size:1.85rem;font-weight:700;color:{color};line-height:1.15;">{main}</div>'
            + (f'<div style="font-size:0.78rem;font-weight:600;color:#9CA3AF;margin-top:2px;">{sub}</div>' if sub else "")
            + f'<div style="font-size:0.75rem;font-weight:600;color:#6B7280;text-transform:uppercase;'
            f'letter-spacing:0.6px;margin-top:10px;">{label}</div>'
            f'</div>'
        )

    _sob_main = f"{_sob_fgs} / 5" if _sob_fgs is not None else "–"
    _kpi_row = (
        _num_kpi(str(_n_total), None, "Teilnehmende", COLORS["blue"])
        + _num_kpi(f"{_n_fgs_kpi} von {_n_all_kpi}", f"{_pct_fgs_kpi} %", "FGS in der Stichprobe", COLORS["teal"])
        + _num_kpi(_sob_main, None, "Belonging-Score Ø FGS", COLORS["violet"])
        + _num_kpi(f"n = {len(df_fgs)}", None, "Aktive Auswahl (FGS)", COLORS["dark_blue"])
    )
    st.markdown(
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem;">'
        + _kpi_row + "</div>",
        unsafe_allow_html=True
    )

    # ── 2 Insight cards ───────────────────────────────────────────────────────
    def _insight_card(label, main_text, sub_text):
        _body = (
            f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;text-transform:uppercase;'
            f'letter-spacing:1px;margin-bottom:10px;">{label}</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#1E2A44;line-height:1.45;">'
            f'{main_text if main_text else "–"}</div>'
            + (f'<div style="font-size:0.78rem;color:#9CA3AF;margin-top:8px;">{sub_text}</div>' if sub_text else "")
        )
        return (
            f'<div style="background:#fff;border-radius:12px;padding:20px 20px 18px;'
            f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);">'
            + _body + "</div>"
        )

    _ins_phase   = _insight_card(
        "Kritischste Studienphase bei FGS",
        _krit_phase,
        f"Häufigste Nennung · n = {_krit_n}" if _krit_phase else None
    )
    _ins_support = _insight_card(
        "Häufigster Unterstützungsbedarf bei FGS",
        _top_support,
        f"Häufigste Nennung · n = {_support_n}" if _top_support else None
    )
    st.markdown(
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">'
        + _ins_phase + _ins_support + "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

    # A: FGS PROFIL
    st.markdown('<div class="section-title">Wer sind die FGS?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div class="card" style="margin-bottom:0;"><b>FGS und Non-FGS im Vergleich</b></div>
      <div class="card" style="margin-bottom:0;"><b>FGS nach Studiengang</b></div>
      <div class="card" style="margin-bottom:0;"><b>Erwerbstätigkeit von FGS</b></div>
    </div>
    """, unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1:
        st.plotly_chart(chart_fgs_bar(df_raw), use_container_width=True)
    with a2:
        if COL_STUDIENGANG in df_fgs.columns and len(df_fgs) >= MIN_N:
            sg_f = df_fgs[COL_STUDIENGANG].value_counts().reset_index()
            sg_f.columns = ["Studiengang", "Anzahl"]
            fig = px.bar(sg_f, x="Anzahl", y="Studiengang", orientation="h",
                         color_discrete_sequence=[COLORS["blue"]], text="Anzahl")
            fig.update_traces(textposition="outside", textfont_size=11, cliponaxis=False)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=11, color="#374151"),
                height=200, showlegend=False, yaxis_title="",
                margin=dict(t=0, b=10, l=10, r=80),
            )
            fig.update_xaxes(gridcolor="#E5E7EB", showgrid=True, showticklabels=False,
                             zeroline=False)
            fig.update_yaxes(showgrid=False, tickfont=dict(size=11), automargin=True)
            st.plotly_chart(fig, use_container_width=True)
    with a3:
        if COL_ARBEIT in df_fgs.columns and len(df_fgs) >= MIN_N:
            arb = df_fgs[COL_ARBEIT].value_counts().reset_index()
            arb.columns = ["Pensum", "Anzahl"]
            total_arb = arb["Anzahl"].sum()
            arb["Label"] = arb.apply(
                lambda r: f"{r['Anzahl']}  ({round(r['Anzahl'] / total_arb * 100)} %)", axis=1
            )
            x_max_arb = arb["Anzahl"].max()
            fig = go.Figure(go.Bar(
                x=arb["Anzahl"], y=arb["Pensum"],
                orientation="h",
                text=arb["Label"], textposition="outside",
                marker_color=COLORS["teal"],
                textfont=dict(size=11),
                cliponaxis=False,
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", size=11, color="#374151"),
                height=200, showlegend=False,
                margin=dict(t=0, b=10, l=130, r=80),
                xaxis=dict(range=[0, x_max_arb * 1.45], showticklabels=False,
                           gridcolor="#E5E7EB", showgrid=True, zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=11), automargin=False),
            )
            st.plotly_chart(fig, use_container_width=True)

    # B: HERAUSFORDERUNGEN
    # Datenvalidierung: NaN-sicher, nur Kategorien mit genug validen Werten
    _ch_valid_fgs = {}
    for _lbl, _col in CHALLENGES.items():
        if _col in df_fgs.columns:
            _s = pd.to_numeric(df_fgs[_col], errors="coerce").dropna()
            if len(_s) >= MIN_N:
                _ch_valid_fgs[_lbl] = round(float(_s.mean()), 1)

    _ch_valid_nfgs = {}
    if len(df_nfgs) >= MIN_N:
        for _lbl, _col in CHALLENGES.items():
            if _col in df_nfgs.columns:
                _s = pd.to_numeric(df_nfgs[_col], errors="coerce").dropna()
                if len(_s) >= MIN_N:
                    _ch_valid_nfgs[_lbl] = round(float(_s.mean()), 1)

    _shared_cats = {lbl for lbl in _ch_valid_fgs if lbl in _ch_valid_nfgs}
    _can_compare = len(_shared_cats) >= 2

    if _can_compare:
        # ── Option A: FGS vs. Non-FGS ────────────────────────────────────────
        st.markdown('<div class="section-title">Welche Herausforderungen zeigen sich?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:grid;grid-template-columns:3fr 2fr;gap:1rem;margin-bottom:1rem;">
          <div class="card" style="margin-bottom:0;"><b>Wahrgenommene Herausforderungen nach Gruppe</b>
          <span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;margin-left:8px;">Skala 1–5</span></div>
          <div class="card" style="margin-bottom:0;"><b>Auffälligste Unterschiede</b></div>
        </div>
        """, unsafe_allow_html=True)
        b1, b2 = st.columns([3, 2])
        with b1:
            _rows_b = []
            for _lbl in CHALLENGES:
                if _lbl in _ch_valid_fgs:
                    _rows_b.append({"Herausforderung": _lbl, "Mittelwert": _ch_valid_fgs[_lbl], "Gruppe": "FGS"})
                if _lbl in _ch_valid_nfgs:
                    _rows_b.append({"Herausforderung": _lbl, "Mittelwert": _ch_valid_nfgs[_lbl], "Gruppe": "Non-FGS"})
            fig = px.bar(
                pd.DataFrame(_rows_b),
                x="Mittelwert", y="Herausforderung",
                color="Gruppe", barmode="group", orientation="h",
                range_x=[1, 5], text="Mittelwert",
                color_discrete_map={"FGS": COLORS["blue"], "Non-FGS": COLORS["teal"]}
            )
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, margin=dict(t=10, b=10, l=10, r=60),
                yaxis_title="", xaxis_title="Mittelwert (1–5)",
                font=dict(family="Inter, sans-serif", size=12, color="#374151"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig.update_xaxes(gridcolor="#E5E7EB", dtick=1, showgrid=True)
            fig.update_yaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True)
        with b2:
            _diffs = sorted(
                [(lbl, _ch_valid_fgs[lbl], _ch_valid_nfgs[lbl],
                  round(abs(_ch_valid_fgs[lbl] - _ch_valid_nfgs[lbl]), 1))
                 for lbl in _shared_cats],
                key=lambda x: x[3], reverse=True
            )
            _diff_html = ""
            for _i, (_lbl, _fv, _nv, _d) in enumerate(_diffs[:6]):
                _sep   = "border-bottom:1px solid #F3F4F6;" if _i < len(_diffs[:6]) - 1 else ""
                _arrow = "↑" if _fv > _nv else ("↓" if _fv < _nv else "–")
                _col   = COLORS["blue"] if _fv > _nv else (COLORS["teal"] if _fv < _nv else "#9CA3AF")
                _diff_html += (
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:7px 0;{_sep}">'
                    f'<span style="font-size:0.82rem;color:#374151;flex:1;padding-right:8px;">{_lbl}</span>'
                    f'<span style="font-size:0.82rem;font-weight:700;color:{_col};white-space:nowrap;">'
                    f'{_arrow}&thinsp;Δ&thinsp;{_d}</span></div>'
                )
            st.markdown(
                f'<div style="background:#fff;border-radius:12px;padding:20px 20px 16px;'
                f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);">'
                f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;text-transform:uppercase;'
                f'letter-spacing:1px;margin-bottom:4px;">Auffälligste Unterschiede</div>'
                f'<div style="font-size:0.75rem;color:#9CA3AF;margin-bottom:14px;">'
                f'FGS vs. Non-FGS · Skala 1–5 · ↑&thinsp;FGS höher</div>'
                + _diff_html + '</div>',
                unsafe_allow_html=True
            )
    else:
        # ── Option B: Nur FGS ────────────────────────────────────────────────
        st.markdown('<div class="section-title">Welche Herausforderungen erleben FGS?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:grid;grid-template-columns:3fr 2fr;gap:1rem;margin-bottom:1rem;">
          <div class="card" style="margin-bottom:0;">
            <b>Wie stark treffen folgende Herausforderungen auf FGS zu?</b><br>
            <span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;">
              Skala: 1 = trifft gar nicht zu &nbsp;·&nbsp; 5 = trifft voll und ganz zu
            </span>
          </div>
          <div class="card" style="margin-bottom:0;"><b>Zentrale Beobachtung</b></div>
        </div>
        """, unsafe_allow_html=True)
        b1, b2 = st.columns([3, 2])
        with b1:
            if _ch_valid_fgs:
                # Absteigend sortiert: stärkste Herausforderung oben
                _rows_b = sorted(
                    [{"Herausforderung": lbl, "Mittelwert": val}
                     for lbl, val in _ch_valid_fgs.items()],
                    key=lambda r: r["Mittelwert"]  # ascending so top bar is at top in horiz chart
                )
                fig = px.bar(
                    pd.DataFrame(_rows_b),
                    x="Mittelwert", y="Herausforderung", orientation="h",
                    range_x=[1, 5], text="Mittelwert",
                    color_discrete_sequence=[COLORS["blue"]]
                )
                fig.update_traces(
                    textposition="outside", textfont_size=11,
                    texttemplate="%{x:.1f}",
                )
                fig.add_vline(
                    x=3, line_dash="dash", line_color="#D1D5DB", line_width=1,
                    annotation_text="Teils", annotation_position="top",
                    annotation_font_size=10, annotation_font_color="#9CA3AF",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    height=290, margin=dict(t=20, b=10, l=10, r=70),
                    yaxis_title="", xaxis_title="", showlegend=False,
                    font=dict(family="Inter, sans-serif", size=12, color="#374151"),
                )
                fig.update_xaxes(gridcolor="#E5E7EB", dtick=1, showgrid=True, range=[1, 5.5])
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Keine validen Herausforderungsdaten vorhanden.")
        with b2:
            if _ch_valid_fgs:
                _sorted_ch = sorted(_ch_valid_fgs.items(), key=lambda x: x[1], reverse=True)
                _top2_html = "".join(
                    f'<div style="padding:8px 0;'
                    f'{"border-bottom:1px solid #F3F4F6;" if i == 0 else ""}">'
                    f'<div style="font-size:0.85rem;font-weight:600;color:#1E2A44;">{lbl}</div>'
                    f'<div style="font-size:0.78rem;color:{COLORS["blue"]};font-weight:700;">Ø {val} / 5</div>'
                    f'</div>'
                    for i, (lbl, val) in enumerate(_sorted_ch[:2])
                )
                # Count valid FGS responses (use first available challenge column)
                _n_fgs_ch = 0
                for _col in CHALLENGES.values():
                    if _col in df_fgs.columns:
                        _n_fgs_ch = int(pd.to_numeric(df_fgs[_col], errors="coerce").dropna().count())
                        break
                _above_mid = any(v > 3 for v in _ch_valid_fgs.values())
                _mid_note  = (
                    "Mindestens eine Herausforderung liegt über dem Skalenmittelpunkt."
                    if _above_mid else
                    "Keine Herausforderung liegt über dem Skalenmittelpunkt."
                )
                st.markdown(
                    f'<div style="background:#fff;border-radius:12px;padding:20px 20px 18px;'
                    f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);">'
                    f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;text-transform:uppercase;'
                    f'letter-spacing:1px;margin-bottom:12px;">Zentrale Beobachtung</div>'
                    f'<div style="font-size:0.78rem;font-weight:600;color:#6B7280;margin-bottom:6px;">'
                    f'Stärkste Herausforderungen</div>'
                    + _top2_html +
                    f'<div style="font-size:0.72rem;color:#9CA3AF;margin-top:14px;padding-top:10px;'
                    f'border-top:1px solid #F3F4F6;">Ausgewertete FGS-Antworten: n = {_n_fgs_ch}</div>'
                    f'<div style="font-size:0.72rem;color:#6B7280;margin-top:8px;font-style:italic;">'
                    f'{_mid_note}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.info("Keine Daten vorhanden.")

    # C: KRITISCHE PHASEN
    st.markdown('<div class="section-title">Wann entstehen kritische Studienphasen?</div>', unsafe_allow_html=True)

    # Kanonische Phasen-Reihenfolge und Schreibvarianten-Mapping
    _PHASE_ORDER = [
        "Studienstart",
        "Erste Prüfungsphase",
        "Mitte des Studiums",
        "Abschlussphase",
        "Bisher keine kritische Phase",
    ]
    _PHASE_ALIASES = {
        "studienstart":                 "Studienstart",
        "erste prüfungsphase":          "Erste Prüfungsphase",
        "prüfungsphase":                "Erste Prüfungsphase",
        "mitte des studiums":           "Mitte des Studiums",
        "mitte studium":                "Mitte des Studiums",
        "abschlussphase":               "Abschlussphase",
        "bisher keine kritische phase": "Bisher keine kritische Phase",
        "keine":                        "Bisher keine kritische Phase",
    }

    def _split_phases(series):
        """Zerlegt Komma-getrennte Mehrfachantworten und aggregiert je kanonischer Phase."""
        counts = {p: 0 for p in _PHASE_ORDER}
        for val in series.dropna():
            raw = str(val).strip()
            if not raw:
                continue
            for part in raw.split(","):
                part = part.strip()
                canonical = _PHASE_ALIASES.get(part.lower())
                if canonical:
                    counts[canonical] += 1
        return counts

    if COL_HERAUSFORDERND in df.columns and len(df) >= MIN_N:
        # Titelkarten – gleiche CSS-Klasse wie in Abschnitt A
        st.markdown("""
        <div style="display:grid;grid-template-columns:2.2fr 1fr;gap:1rem;margin-bottom:0.75rem;">
          <div class="card" style="margin-bottom:0;"><b>Kritische Phasen im Studienverlauf</b></div>
          <div class="card" style="margin-bottom:0;"><b>Zentrale Erkenntnis</b></div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2.2, 1])

        with c1:
            _src = df_fgs[COL_HERAUSFORDERND] if len(df_fgs) >= MIN_N else pd.Series(dtype=str)
            phase_counts = _split_phases(_src)
            # Umgekehrte Reihenfolge → Studienstart erscheint oben im horizontalen Balkendiagramm
            phase_df = pd.DataFrame(
                [{"Phase": p, "Anzahl": phase_counts[p]} for p in reversed(_PHASE_ORDER)]
            )
            if phase_df["Anzahl"].sum() > 0:
                _max_n = phase_df["Anzahl"].max()
                _colors = [
                    COLORS["teal"] if n == _max_n and n > 0 else COLORS["blue"]
                    for n in phase_df["Anzahl"]
                ]
                fig_c = go.Figure(go.Bar(
                    x=phase_df["Anzahl"],
                    y=phase_df["Phase"],
                    orientation="h",
                    text=phase_df["Anzahl"],
                    textposition="outside",
                    marker_color=_colors,
                    textfont=dict(size=12),
                    cliponaxis=False,
                ))
                fig_c.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", size=12, color="#374151"),
                    height=280,
                    margin=dict(t=0, b=10, l=10, r=60),
                    showlegend=False,
                    xaxis=dict(
                        range=[0, _max_n * 1.4 if _max_n > 0 else 10],
                        showticklabels=True,
                        gridcolor="#E5E7EB",
                        showgrid=True,
                        zeroline=False,
                        dtick=max(1, _max_n // 5),
                    ),
                    yaxis=dict(showgrid=False, tickfont=dict(size=11), automargin=True),
                )
                st.plotly_chart(fig_c, use_container_width=True)
                st.markdown(
                    '<p style="font-size:11px;color:#9CA3AF;margin-top:-8px;">'
                    'Mehrfachnennungen möglich; dargestellt ist die Anzahl der Nennungen je Studienphase.</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.info("Keine Daten vorhanden.")

        with c2:
            if len(df_fgs) >= MIN_N and COL_HERAUSFORDERND in df_fgs.columns:
                _pc = _split_phases(df_fgs[COL_HERAUSFORDERND])
                # Top-2 Phasen (ohne "Bisher keine kritische Phase") für die Insight-Karte
                _ranked = sorted(
                    [(p, _pc[p]) for p in _PHASE_ORDER if p != "Bisher keine kritische Phase"],
                    key=lambda x: x[1], reverse=True,
                )
                _top_phases = [p for p, n in _ranked[:2] if n > 0]
                _top_label = " & ".join(_top_phases) if _top_phases else "—"
                st.markdown(f"""
                <div class="insight-box">
                  <div style="font-size:10px;font-weight:700;color:#2D9CDB;text-transform:uppercase;
                              letter-spacing:1.2px;margin-bottom:8px;">Zentrale Erkenntnis</div>
                  <div style="font-size:15px;font-weight:700;color:#1E2A44;line-height:1.3;
                              margin-bottom:10px;">{_top_label}</div>
                  <div style="font-size:12px;color:#374151;margin-bottom:10px;line-height:1.5;">
                    In diesen frühen Studienphasen zeigen sich die häufigsten Herausforderungen.
                  </div>
                  <div style="font-size:11px;color:#6B7280;border-top:1px solid #BFDBFE;
                              padding-top:8px;line-height:1.5;">
                    Möglicher Ansatzpunkt: Orientierung, Peer-Mentoring und frühe Prüfungsberatung.
                  </div>
                </div>""", unsafe_allow_html=True)

        # Aufklappbare Detailansicht mit Originalantworten (Kombinationen)
        with st.expander("Detailansicht: Kombinationen genannter Studienphasen", expanded=False):
            _rows_d = []
            if len(df_fgs) >= MIN_N:
                for _phase, _cnt in df_fgs[COL_HERAUSFORDERND].value_counts().items():
                    _rows_d.append({"Antwort": _phase, "Anzahl": int(_cnt), "Gruppe": "FGS"})
            if len(df_nfgs) >= MIN_N:
                for _phase, _cnt in df_nfgs[COL_HERAUSFORDERND].value_counts().items():
                    _rows_d.append({"Antwort": _phase, "Anzahl": int(_cnt), "Gruppe": "Non-FGS"})
            if _rows_d:
                _df_d = pd.DataFrame(_rows_d)
                # Sortierung: häufigste Antwort oben
                _order = (
                    _df_d.groupby("Antwort")["Anzahl"].sum()
                    .sort_values().index.tolist()
                )
                _n_cats = len(_df_d["Antwort"].unique())
                _fig_d = px.bar(
                    _df_d,
                    x="Anzahl", y="Antwort", color="Gruppe",
                    barmode="group", text="Anzahl",
                    orientation="h",
                    category_orders={"Antwort": _order},
                    color_discrete_map={"FGS": COLORS["blue"], "Non-FGS": COLORS["teal"]},
                )
                _fig_d.update_traces(textposition="outside", textfont_size=11, cliponaxis=False)
                _fig_d.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", size=11, color="#374151"),
                    height=max(280, _n_cats * 38),
                    margin=dict(t=10, b=10, l=10, r=60),
                    xaxis_title="Anzahl", yaxis_title="",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                _fig_d.update_xaxes(gridcolor="#E5E7EB", showgrid=True, zeroline=False)
                _fig_d.update_yaxes(showgrid=False, automargin=True, tickfont=dict(size=11))
                st.plotly_chart(_fig_d, use_container_width=True)
            else:
                st.info("Keine Daten vorhanden.")

    # D: UNTERSTÜTZUNG
    st.markdown('<div class="section-title">Was hilft und was fehlt?</div>', unsafe_allow_html=True)

    # Bekannte Mehrfachauswahl-Kategorien je Frage
    _CATS_GEWUENSCHT = [
        "Mehr Mentoring",
        "Bessere Informationen zum Studium",
        "Finanzielle Unterstützung",
        "Karriereberatung",
        "Austausch mit anderen Studierenden",
    ]
    _CATS_HILFT = [
        "Austausch mit anderen Studierenden",
        "Unterstützung durch Freunde",
        "Unterstützung durch Familie",
        "Gute Organisation des Studiums",
        "Unterstützung durch Dozierende",
        "Mentoringprogramme",
    ]

    def _split_agg(series, known_cats):
        """Zerlegt Komma-getrennte Mehrfachantworten und aggregiert nach Kategorie."""
        items = []
        for val in series.dropna():
            raw = str(val).strip()
            if not raw:
                continue
            for part in raw.split(","):
                part = part.strip()
                if not part:
                    continue
                matched = next((k for k in known_cats if k.lower() == part.lower()), None)
                items.append(matched if matched else "Weitere Nennungen")
        return Counter(items)

    def _support_chart(counter, color, height=280):
        rows = sorted(
            [{"Kategorie": k, "Anzahl": v} for k, v in counter.items()
             if k != "Weitere Nennungen"],
            key=lambda r: r["Anzahl"]          # ascending → höchster Balken oben
        )
        if counter.get("Weitere Nennungen", 0) >= MIN_N:
            rows.insert(0, {"Kategorie": "Weitere Nennungen",
                             "Anzahl": counter["Weitere Nennungen"]})
        if not rows:
            return None
        df_p   = pd.DataFrame(rows)
        x_max  = df_p["Anzahl"].max()
        fig    = px.bar(df_p, x="Anzahl", y="Kategorie", orientation="h",
                        color_discrete_sequence=[color], text="Anzahl")
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=height, margin=dict(t=10, b=10, l=10, r=50),
            yaxis_title="", xaxis_title="Anzahl Nennungen", showlegend=False,
            font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        )
        fig.update_xaxes(gridcolor="#E5E7EB", dtick=2, showgrid=True,
                          range=[0, x_max * 1.4])
        fig.update_yaxes(showgrid=False, automargin=True)
        return fig

    # Aggregation
    _ct_gew = (
        _split_agg(df_fgs[COL_SUPPORT_GEWUENSCHT], _CATS_GEWUENSCHT)
        if COL_SUPPORT_GEWUENSCHT in df_fgs.columns and len(df_fgs) >= MIN_N
        else Counter()
    )
    _ct_hilft = (
        _split_agg(df_fgs[COL_HILFT], _CATS_HILFT)
        if COL_HILFT in df_fgs.columns and len(df_fgs) >= MIN_N
        else Counter()
    )

    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div class="card" style="margin-bottom:0;">
        <b>Gewünschte Unterstützung</b>
        <span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;margin-left:8px;">
          Mehrfachnennungen möglich
        </span>
      </div>
      <div class="card" style="margin-bottom:0;">
        <b>Hilfreiche Ressourcen im Studium</b>
        <span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;margin-left:8px;">
          Mehrfachnennungen möglich
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        _fig_gew = _support_chart(_ct_gew, COLORS["orange"])
        if _fig_gew:
            st.plotly_chart(_fig_gew, use_container_width=True)
        else:
            st.info("Keine auswertbaren Antworten vorhanden.")
    with d2:
        _fig_hilft = _support_chart(_ct_hilft, COLORS["teal"])
        if _fig_hilft:
            st.plotly_chart(_fig_hilft, use_container_width=True)
        else:
            st.info("Keine auswertbaren Antworten vorhanden.")

    # ── Insight-Karte: Hinweise auf Unterstützungsbedarfe ─────────────────────
    _top_gew   = _ct_gew.most_common(1)[0]   if _ct_gew   else (None, 0)
    _top_hilft = _ct_hilft.most_common(1)[0] if _ct_hilft else (None, 0)
    _n_gew_resp  = int(df_fgs[COL_SUPPORT_GEWUENSCHT].dropna().pipe(
        lambda s: s[s.str.strip() != ""]).count()) if COL_SUPPORT_GEWUENSCHT in df_fgs.columns else 0
    _n_hilft_resp = int(df_fgs[COL_HILFT].dropna().pipe(
        lambda s: s[s.str.strip() != ""]).count()) if COL_HILFT in df_fgs.columns else 0

    def _kpi_block(label, main_val, sub_val, main_color="#1E2A44"):
        if main_val:
            return (
                f'<div style="display:flex;flex-direction:column;">'
                f'<div style="font-size:0.72rem;font-weight:600;color:#6B7280;'
                f'margin-bottom:6px;">{label}</div>'
                f'<div style="font-size:0.95rem;font-weight:700;color:{main_color};'
                f'line-height:1.35;margin-bottom:4px;">{main_val}</div>'
                f'<div style="font-size:0.80rem;color:{COLORS["blue"]};">{sub_val}</div>'
                f'</div>'
            )
        return (
            f'<div style="display:flex;flex-direction:column;">'
            f'<div style="font-size:0.72rem;font-weight:600;color:#6B7280;margin-bottom:6px;">'
            f'{label}</div>'
            f'<div style="font-size:0.82rem;color:#9CA3AF;font-style:italic;">Keine Daten verfügbar.</div>'
            f'</div>'
        )

    _b1 = _kpi_block(
        "Häufigster Unterstützungswunsch",
        _top_gew[0],
        f"n = {_top_gew[1]}" if _top_gew[0] else "",
    )
    _b2 = _kpi_block(
        "Häufigste hilfreiche Ressource",
        _top_hilft[0],
        f"n = {_top_hilft[1]}" if _top_hilft[0] else "",
    )
    _b3 = (
        f'<div style="display:flex;flex-direction:column;">'
        f'<div style="font-size:0.72rem;font-weight:600;color:#6B7280;margin-bottom:6px;">'
        f'Ausgewertete FGS-Antworten</div>'
        f'<div style="font-size:0.88rem;color:#1E2A44;line-height:1.8;">'
        f'Wünsche: <b>n = {_n_gew_resp}</b><br>'
        f'Ressourcen: <b>n = {_n_hilft_resp}</b>'
        f'</div>'
        f'</div>'
    )
    _interp_line = (
        f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid #F3F4F6;'
        f'font-size:0.78rem;color:#6B7280;">'
        f'Hinweis: Besonders häufig genannt wurde ein Bedarf an '
        f'<span style="font-weight:600;color:#374151;">{_top_gew[0]}</span>.'
        f'</div>'
        if _top_gew[0] and _top_gew[1] >= MIN_N else ""
    )

    st.markdown(
        f'<div style="background:#fff;border-radius:12px;padding:18px 22px 16px;'
        f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);margin-top:0.25rem;">'
        f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;text-transform:uppercase;'
        f'letter-spacing:1px;margin-bottom:14px;">Hinweise auf Unterstützungsbedarfe</div>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;align-items:start;">'
        + _b1 + _b2 + _b3
        + f'</div>'
        + _interp_line
        + f'</div>',
        unsafe_allow_html=True
    )

    # E: BELONGING
    st.markdown('<div class="section-title">Sense of Belonging</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div class="card" style="margin-bottom:0;">
        <b>Zugehörigkeitsgefühl nach Dimension: FGS und Non-FGS</b><br>
        <span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;">
          Mittelwert &nbsp;·&nbsp; Skala: 1 = stimme gar nicht zu, 5 = stimme voll und ganz zu
        </span>
      </div>
      <div class="card" style="margin-bottom:0;"><b>Zentrale Beobachtungen</b></div>
    </div>
    """, unsafe_allow_html=True)
    e1, e2 = st.columns([2, 1])
    with e1:
        if len(df_fgs) >= MIN_N:
            st.plotly_chart(
                chart_belonging_bars(df_fgs, df_nfgs if len(df_nfgs) >= MIN_N else None),
                use_container_width=True)
        else:
            st.info("Zu wenige FGS-Antworten für diese Auswahl.")
    with e2:
        if len(df_fgs) >= MIN_N:
            _sc_fgs  = calculate_belonging_scores(df_fgs)
            _sc_nfgs = calculate_belonging_scores(df_nfgs) if len(df_nfgs) >= MIN_N else {}
            _dims    = {k: v for k, v in _sc_fgs.items()
                        if k != "Gesamt" and pd.notna(v)}

            if _dims:
                _top_dim = max(_dims, key=_dims.get)
                _top_val = _dims[_top_dim]
                _bot_dim = min(_dims, key=_dims.get)
                _bot_val = _dims[_bot_dim]

                # Gruppenvergleich
                _comp_text = None
                if _sc_nfgs:
                    _diffs = {
                        k: round(abs(_dims[k] - _sc_nfgs[k]), 2)
                        for k in _dims
                        if k in _sc_nfgs and pd.notna(_sc_nfgs.get(k))
                    }
                    if _diffs:
                        _max_dd = max(_diffs, key=_diffs.get)
                        _max_dv = _diffs[_max_dd]
                        _comp_text = (
                            "Die Unterschiede zwischen FGS und Non-FGS sind in allen Dimensionen gering."
                            if _max_dv <= 0.2 else
                            f"Grösster Unterschied: {_max_dd} · {_max_dv:.1f} Punkte"
                        )

                _comp_block = (
                    f'<div style="padding:8px 0;border-top:1px solid #F3F4F6;">'
                    f'<div style="font-size:0.75rem;font-weight:600;color:#6B7280;margin-bottom:4px;">'
                    f'Gruppenvergleich</div>'
                    f'<div style="font-size:0.82rem;color:#374151;line-height:1.5;">{_comp_text}</div>'
                    f'</div>'
                ) if _comp_text else ""

                _ansatz = (
                    f'<div style="padding-top:8px;">'
                    f'<div style="font-size:0.72rem;color:#9CA3AF;font-style:italic;line-height:1.5;">'
                    f'Möglicher Ansatzpunkt: Angebote zur Stärkung von <i>{_bot_dim}</i> prüfen.'
                    f'</div></div>'
                ) if _bot_dim else ""

                st.markdown(
                    f'<div style="background:#fff;border-radius:12px;padding:20px 20px 18px;'
                    f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);">'
                    f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;'
                    f'text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">'
                    f'Zentrale Beobachtungen</div>'
                    f'<div style="padding-bottom:10px;border-bottom:1px solid #F3F4F6;">'
                    f'<div style="font-size:0.75rem;font-weight:600;color:#6B7280;margin-bottom:4px;">'
                    f'Höchster Wert bei FGS</div>'
                    f'<div style="font-size:0.88rem;font-weight:700;color:#1E2A44;">{_top_dim}</div>'
                    f'<div style="font-size:0.82rem;color:{COLORS["blue"]};">Ø {_top_val:.1f} / 5</div>'
                    f'</div>'
                    f'<div style="padding:10px 0;border-bottom:1px solid #F3F4F6;">'
                    f'<div style="font-size:0.75rem;font-weight:600;color:#6B7280;margin-bottom:4px;">'
                    f'Niedrigster Wert bei FGS</div>'
                    f'<div style="font-size:0.88rem;font-weight:700;color:#1E2A44;">{_bot_dim}</div>'
                    f'<div style="font-size:0.82rem;color:{COLORS["blue"]};">Ø {_bot_val:.1f} / 5</div>'
                    f'</div>'
                    + _comp_block
                    + _ansatz
                    + '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.info("Keine validen Belonging-Daten vorhanden.")
        else:
            st.info("Zu wenige FGS-Antworten für diese Auswahl.")

    # F: QUALITATIVE EINBLICKE
    st.markdown('<div class="section-title">Qualitative Einblicke</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card">'
        '<b>Persönliche Erfahrungen und Wünsche von FGS</b><br>'
        '<span style="font-size:0.72rem;color:#9CA3AF;font-weight:400;">'
        'Offene Antworten, thematisch codiert · Mehrfachcodierungen möglich · anonymisierte Darstellung'
        '</span></div>',
        unsafe_allow_html=True
    )

    if len(df_fgs) < MIN_N:
        st.warning(
            "Detailauswertung nicht verfügbar: "
            "Die aktuelle Filterauswahl umfasst weniger als 5 FGS-Antworten."
        )
    else:
        def _code_answers(series, coding_dict):
            c = Counter()
            for v in series.dropna():
                theme = coding_dict.get(str(v).strip())
                if theme:
                    c[theme] += 1
            return c

        _cnt_pos = _code_answers(df_fgs[COL_ZUGEHOERIG_POS], CODING_POS) \
            if COL_ZUGEHOERIG_POS in df_fgs.columns else Counter()
        _cnt_neg = _code_answers(df_fgs[COL_ZUGEHOERIG_NEG], CODING_NEG) \
            if COL_ZUGEHOERIG_NEG in df_fgs.columns else Counter()
        _cnt_wun = _code_answers(df_fgs[COL_WUENSCHE], CODING_WUENSCHE) \
            if COL_WUENSCHE in df_fgs.columns else Counter()

        def _top(counter):
            return counter.most_common(1)[0] if counter else (None, 0)

        _tp, _np = _top(_cnt_pos)
        _tn, _nn = _top(_cnt_neg)
        _tw, _nw = _top(_cnt_wun)

        def _insight_row(label, theme, n, color):
            if theme:
                return (
                    f'<div style="padding:7px 0;border-bottom:1px solid #F3F4F6;">'
                    f'<span style="font-size:0.75rem;font-weight:600;color:#6B7280;">{label}</span><br>'
                    f'<span style="font-size:0.88rem;font-weight:700;color:{color};">{theme}</span>'
                    f'<span style="font-size:0.82rem;color:#9CA3AF;"> · n = {n}</span>'
                    f'</div>'
                )
            return (
                f'<div style="padding:7px 0;border-bottom:1px solid #F3F4F6;">'
                f'<span style="font-size:0.75rem;font-weight:600;color:#6B7280;">{label}</span><br>'
                f'<span style="font-size:0.82rem;color:#9CA3AF;font-style:italic;">'
                f'Noch keine codierte Auswertung verfügbar.</span>'
                f'</div>'
            )

        st.markdown(
            '<div style="background:#fff;border-radius:12px;padding:18px 20px 14px;'
            'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);margin-bottom:1rem;">'
            '<div style="font-size:0.72rem;font-weight:700;color:#00A896;'
            'text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">'
            'Zentrale qualitative Erkenntnisse</div>'
            + _insight_row("Häufig genannte Ressource", _tp, _np, COLORS["teal"])
            + _insight_row("Häufig genannte Barriere",  _tn, _nn, COLORS["coral"])
            + _insight_row("Häufig genannter Wunsch",   _tw, _nw, COLORS["violet"])
            + '</div>',
            unsafe_allow_html=True
        )

        def _theme_bars(counter, accent, max_themes=5):
            if not counter:
                return (
                    '<div style="font-size:0.82rem;color:#9CA3AF;font-style:italic;">'
                    'Keine codierten Themen verfügbar.</div>'
                )
            top  = counter.most_common(max_themes)
            maxn = top[0][1]
            html = ""
            for theme, n in top:
                pct = int(n / maxn * 100)
                html += (
                    f'<div style="margin-bottom:9px;">'
                    f'<div style="display:flex;justify-content:space-between;'
                    f'font-size:0.80rem;color:#374151;margin-bottom:3px;">'
                    f'<span>{theme}</span>'
                    f'<span style="color:#9CA3AF;white-space:nowrap;padding-left:8px;">'
                    f'n = {n}</span></div>'
                    f'<div style="background:#F3F4F6;border-radius:4px;height:7px;">'
                    f'<div style="background:{accent};border-radius:4px;height:7px;'
                    f'width:{pct}%;"></div></div>'
                    f'</div>'
                )
            return html

        _theme_cols = []
        for title, counter, color in [
            ("Was stärkt Zugehörigkeit?",    _cnt_pos, COLORS["teal"]),
            ("Was erschwert Zugehörigkeit?", _cnt_neg, COLORS["coral"]),
            ("Gewünschte Verbesserungen",    _cnt_wun, COLORS["violet"]),
        ]:
            _theme_cols.append(
                f'<div style="display:flex;flex-direction:column;">'
                f'<div style="font-size:13px;font-weight:600;color:{color};'
                f'min-height:2.2rem;padding-bottom:0.5rem;">{title}</div>'
                + _theme_bars(counter, color)
                + f'</div>'
            )
        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;'
            'gap:1.25rem;margin-bottom:1rem;">'
            + "".join(_theme_cols)
            + '</div>',
            unsafe_allow_html=True
        )

        with st.expander("Anonymisierte Beispielaussagen"):
            _ex_cols = []
            for examples, title, color in [
                (ANON_EXAMPLES["pos"],      "Was stärkt Zugehörigkeit?",    COLORS["teal"]),
                (ANON_EXAMPLES["neg"],      "Was erschwert Zugehörigkeit?", COLORS["coral"]),
                (ANON_EXAMPLES["wuensche"], "Gewünschte Verbesserungen",    COLORS["violet"]),
            ]:
                cards = "".join(
                    f'<div style="background:#F9FAFB;border-left:3px solid {color};'
                    f'border-radius:0 6px 6px 0;padding:8px 10px;margin-bottom:6px;'
                    f'font-size:0.82rem;color:#374151;font-style:italic;">«{ex}»</div>'
                    for ex in examples
                )
                _ex_cols.append(
                    f'<div style="display:flex;flex-direction:column;">'
                    f'<div style="font-size:0.75rem;font-weight:600;color:{color};'
                    f'min-height:2.2rem;padding-bottom:0.5rem;">{title}</div>'
                    + cards +
                    f'</div>'
                )
            st.markdown(
                '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;'
                'gap:1.25rem;padding:0.25rem 0 0.5rem 0;">'
                + "".join(_ex_cols)
                + '</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            '<div style="background:#fff;border-radius:12px;padding:18px 20px 16px;'
            'box-shadow:0 1px 6px rgba(0,0,0,0.07);margin-top:1rem;">'
            '<div style="font-size:0.72rem;font-weight:700;color:#7B61FF;'
            'text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">'
            'Mögliche Ansatzpunkte für Hochschulakteure</div>'
            '<div style="font-size:0.75rem;color:#6B7280;font-style:italic;margin-bottom:10px;">'
            'Vorsichtige Hinweise auf Basis der häufig genannten Themen – '
            'keine nachgewiesenen Wirkungen.</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:10px;">'
            '<div style="flex:1;min-width:180px;background:#F9FAFB;'
            'border-radius:8px;padding:10px 12px;">'
            '<div style="font-size:0.78rem;font-weight:700;color:#1E2A44;margin-bottom:4px;">'
            'Studienberatung</div>'
            '<div style="font-size:0.80rem;color:#374151;line-height:1.5;">'
            'Orientierungs- und Informationsangebote für Studieneinstieg und Modulwahl prüfen.'
            '</div></div>'
            '<div style="flex:1;min-width:180px;background:#F9FAFB;'
            'border-radius:8px;padding:10px 12px;">'
            '<div style="font-size:0.78rem;font-weight:700;color:#1E2A44;margin-bottom:4px;">'
            'Dozierende</div>'
            '<div style="font-size:0.80rem;color:#374151;line-height:1.5;">'
            'Mehr Transparenz zu Modulaufbau, Zielen und Abläufen – '
            'insbesondere für Teilzeitstudierende.'
            '</div></div>'
            '<div style="flex:1;min-width:180px;background:#F9FAFB;'
            'border-radius:8px;padding:10px 12px;">'
            '<div style="font-size:0.78rem;font-weight:700;color:#1E2A44;margin-bottom:4px;">'
            'Diversity & Soziales</div>'
            '<div style="font-size:0.80rem;color:#374151;line-height:1.5;">'
            'Niederschwellige Kennenlernangebote und soziale Vernetzungsmöglichkeiten ausbauen.'
            '</div></div>'
            '</div></div>',
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════════════════
# ÜBER DIE DATEN
# ════════════════════════════════════════════════════════════════════════════
elif page == "ueber":
    _ueber_html = (
        '<div class="dash-wrap">'
        '<div style="background:#ffffff;border-radius:16px;padding:1.5rem 2rem;position:relative;overflow:hidden;margin-bottom:1.5rem;display:flex;justify-content:space-between;align-items:flex-start;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.07);">'
        '<div style="position:absolute;width:280px;height:280px;background:#00A896;border-radius:50%;opacity:0.07;top:-100px;right:260px;pointer-events:none;"></div>'
        '<div style="position:absolute;width:200px;height:200px;background:#2D9CDB;border-radius:50%;opacity:0.07;bottom:-60px;right:80px;pointer-events:none;"></div>'
        '<div style="position:relative;z-index:1;">'
                '<h2 style="font-size:26px;font-weight:700;color:#1E2A44;margin:0 0 4px 0;line-height:1.2;font-family:Inter,sans-serif;">&#220;ber die Daten</h2>'
        '<p style="font-size:13px;color:#4B5563;margin:0;line-height:1.6;">Datengrundlage, Datenschutz und Hinweise zur Interpretation</p>'
        '</div>'
        '<div style="display:flex;align-items:center;gap:2.5rem;position:relative;z-index:1;flex-shrink:0;">'
        '<div style="text-align:center;">'
        '<div style="font-size:34px;font-weight:800;color:#00A896;line-height:1;font-family:Inter,sans-serif;">2026</div>'
        '<div style="font-size:10px;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.6px;margin-top:5px;">Datenstand</div>'
        '</div>'
        '<div style="width:1px;height:44px;background:#A8D5CC;"></div>'
        '<div style="text-align:center;">'
        '<div style="font-size:34px;font-weight:800;color:#7B61FF;line-height:1;font-family:Inter,sans-serif;">100%</div>'
        '<div style="font-size:10px;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.6px;margin-top:5px;">Anonymisiert</div>'
        '</div>'
        '</div>'
        '</div>'
        '<div style="background:#fff;border-bottom:1px solid #E5E7EB;border-radius:12px;padding:0.9rem 1.75rem;margin-bottom:1.25rem;display:flex;align-items:center;gap:0.7rem;flex-wrap:wrap;">'
        '<span style="font-size:9px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:1px;margin-right:0.5rem;">Datenpipeline</span>'
        '<span style="background:#2D9CDB;color:#fff;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">Google Forms (anonym)</span>'
        '<span style="color:#9CA3AF;font-size:13px;">&#8594;</span>'
        '<span style="background:#F5F7FB;color:#6B7280;border:0.5px solid #E5E7EB;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">CSV-Export</span>'
        '<span style="color:#9CA3AF;font-size:13px;">&#8594;</span>'
        '<span style="background:#F5F7FB;color:#6B7280;border:0.5px solid #E5E7EB;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">Datenbereinigung</span>'
        '<span style="color:#9CA3AF;font-size:13px;">&#8594;</span>'
        '<span style="background:#F5F7FB;color:#6B7280;border:0.5px solid #E5E7EB;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">Aggregation</span>'
        '<span style="color:#9CA3AF;font-size:13px;">&#8594;</span>'
        '<span style="background:#1E2A44;color:#fff;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">Dashboard</span>'
        '</div>'
        '<div style="background:#F5F7FB;padding:1.5rem 0;border-radius:12px;">'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;">'
        '<div style="background:#fff;border-radius:12px;border:1px solid #E5E7EB;box-shadow:0 1px 8px rgba(0,0,0,0.05);overflow:hidden;">'
        '<div style="height:3px;background:linear-gradient(90deg,#2D9CDB,#7B61FF);"></div>'
        '<div style="padding:1.25rem 1.5rem;">'
        '<div style="font-size:11px;font-weight:700;color:#2D9CDB;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Datengrundlage</div>'
        '<p style="font-size:13px;color:#374151;line-height:1.5;margin:0 0 14px 0;">Die dargestellten Ergebnisse basieren auf einer Studierendenbefragung zu Bildungsbiografien, Herausforderungen, Ressourcen und Unterstützungsbedarfen von First-Generation-Studierenden am Departement Informatik der HSLU. Die Daten wurden bereinigt und ausschliesslich aggregiert visualisiert.</p>'
        '<span style="display:inline-block;background:#EFF6FF;color:#2D9CDB;border-radius:6px;padding:4px 11px;font-size:10px;font-weight:600;">Google Forms · CSV-Export</span>'
        '</div>'
        '</div>'
        '<div style="background:#fff;border-radius:12px;border:1px solid #E5E7EB;box-shadow:0 1px 8px rgba(0,0,0,0.05);overflow:hidden;">'
        '<div style="height:3px;background:linear-gradient(90deg,#7B61FF,#00A896);"></div>'
        '<div style="padding:1.25rem 1.5rem;">'
        '<div style="font-size:11px;font-weight:700;color:#7B61FF;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Definition FGS</div>'
        '<p style="font-size:13px;color:#374151;line-height:1.5;margin:0 0 14px 0;">Als First-Generation-Studierende gelten in diesem Dashboard Studierende, deren Eltern keinen Hochschulabschluss besitzen und die somit als Erste in ihrer Familie studieren.</p>'
        '<div style="background:#F5F3FF;border-left:2px solid #7B61FF;border-radius:0 6px 6px 0;padding:9px 13px;font-size:11px;color:#5B21B6;font-weight:500;line-height:1.4;">Erste in der Familie, die studieren</div>'
        '</div>'
        '</div>'
        '</div>'
        '<div style="background:linear-gradient(135deg,#E6FAF8 0%,#F0FFF4 100%);border-radius:12px;border:0.5px solid #A7F3D0;box-shadow:0 1px 8px rgba(0,0,0,0.05);padding:1.25rem 1.5rem;margin-bottom:12px;position:relative;overflow:hidden;display:flex;gap:1.25rem;align-items:flex-start;">'
        '<div style="position:absolute;width:130px;height:130px;background:#00A896;border-radius:50%;opacity:0.06;top:-35px;right:-25px;pointer-events:none;"></div>'
        '<div style="flex-shrink:0;width:36px;height:36px;background:#00A896;border-radius:8px;display:flex;align-items:center;justify-content:center;">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
        '</div>'
        '<div style="flex:1;position:relative;z-index:1;">'
        '<div style="font-size:11px;font-weight:700;color:#00A896;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Datenschutz und Anonymisierung</div>'
        '<p style="font-size:13px;color:#065F46;line-height:1.5;margin:0;">Die Befragung erfolgte anonym über Google Forms — es wurden keine personenbezogenen Angaben erhoben. Die Visualisierungen zeigen ausschliesslich aggregierte Ergebnisse. Bei kritischen Filterkombinationen werden keine Detailwerte angezeigt, um Rückschlüsse auf einzelne Personen zu verhindern. Freitextaussagen werden nur anonymisiert und inhaltlich bereinigt dargestellt.</p>'
        '</div>'
        '</div>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'
        '<div style="background:#fff;border-radius:12px;border:1px solid #E5E7EB;box-shadow:0 1px 8px rgba(0,0,0,0.05);overflow:hidden;">'
        '<div style="height:3px;background:linear-gradient(90deg,#F2994A,#EB5757);"></div>'
        '<div style="padding:1.25rem 1.5rem;">'
        '<div style="font-size:11px;font-weight:700;color:#F2994A;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Hinweise zur Interpretation</div>'
        '<p style="font-size:13px;color:#374151;line-height:1.5;margin:0;">Die Ergebnisse zeigen Wahrnehmungen und Erfahrungen der befragten Studierenden. Sie ermöglichen die Identifikation von Mustern und möglichen Unterstützungsbedarfen, erlauben jedoch keine pauschalen Aussagen über alle First-Generation-Studierenden. Dargestellte Handlungshinweise sind als mögliche Ansatzpunkte für weitere Diskussionen zu verstehen.</p>'
        '</div>'
        '</div>'
        '<div style="background:#fff;border-radius:12px;border:1px solid #E5E7EB;box-shadow:0 1px 8px rgba(0,0,0,0.05);overflow:hidden;">'
        '<div style="height:3px;background:linear-gradient(90deg,#1E2A44,#2D9CDB);"></div>'
        '<div style="padding:1.25rem 1.5rem;">'
        '<div style="font-size:11px;font-weight:700;color:#1E2A44;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Stand und Weiterentwicklung</div>'
        '<p style="font-size:13px;color:#374151;line-height:1.5;margin:0 0 14px 0;">Datenstand: 2026. Das Dashboard ist so konzipiert, dass zukünftige Erhebungen integriert und Entwicklungen über mehrere Jahre hinweg verglichen werden können.</p>'
        '<div style="display:flex;gap:6px;flex-wrap:wrap;">'
        '<span style="background:#1E2A44;color:#fff;border-radius:5px;padding:4px 10px;font-size:10px;font-weight:600;">2026</span>'
        '<span style="background:#F5F7FB;color:#6B7280;border:0.5px solid #D1D5DB;border-radius:5px;padding:4px 10px;font-size:10px;font-weight:600;">2027 &#8594;</span>'
        '<span style="background:#F5F7FB;color:#6B7280;border:0.5px solid #D1D5DB;border-radius:5px;padding:4px 10px;font-size:10px;font-weight:600;">2028 &#8594;</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(_ueber_html, unsafe_allow_html=True)
