# app.py — FGS Dashboard | HSLU Informatik

import streamlit as st
import pandas as pd

from config import *
from preprocessing import load_data, calculate_belonging_scores
import plotly.graph_objects as go
import plotly.express as px
from charts import (chart_fgs_bar, chart_belonging_radar, chart_belonging_bars)

st.set_page_config(
    page_title="FGS Dashboard | HSLU Informatik",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SEITENSTATUS (kein Browser-Reload) ───────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
page = st.session_state.page

# nth-child-Index des aktiven Navbar-Buttons (Logo=1, Spacer=2, Home=3, Dashboard=4 ...)
_active_nth = 3 if page == "home" else 4
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
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {{
    padding:0 !important; max-width:100% !important; margin:0 !important;
    background:transparent !important;
}}
div[data-testid="stVerticalBlock"],
div[data-testid="column"] {{
    background:transparent !important;
}}
div[data-testid="stHorizontalBlock"]:not(:first-of-type) {{
    background:{"transparent" if page == "home" else "#FFFFFF"} !important;
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
    padding:12px 60px !important;
    box-shadow:0 1px 8px rgba(0,0,0,0.06) !important;
    position:sticky !important; top:0 !important; z-index:100 !important;
    align-items:center !important;
}}
/* Alle Buttons im Navbar: Text-Link-Style */
div[data-testid="stHorizontalBlock"]:first-of-type button {{
    background:transparent !important; border:none !important;
    box-shadow:none !important; border-radius:0 !important;
    color:#6B7280 !important; font-size:12px !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:1px !important; padding:6px 4px !important;
    width:100% !important; min-height:0 !important; min-width:0 !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type button:hover {{
    color:#1E2A44 !important; background:transparent !important;
    border:none !important;
}}
/* Aktiver Navbar-Button */
div[data-testid="stHorizontalBlock"]:first-of-type > div:nth-child({_active_nth}) button {{
    color:#00A896 !important;
    border-bottom:2px solid #00A896 !important;
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

.research-wrap {{ background:#1E2A44; padding:96px 80px; text-align:center; }}
.res-label {{
    font-size:12px; font-weight:700; letter-spacing:2px;
    color:#00A896; text-transform:uppercase; margin-bottom:32px; font-family:Inter,sans-serif;
}}
.res-quote {{
    font-size:30px; font-style:italic; font-weight:700; color:#fff;
    max-width:860px; margin:0 auto 48px auto; line-height:1.45; font-family:Inter,sans-serif;
    text-align:center;
}}
.res-tags {{ display:flex; flex-wrap:wrap; justify-content:center; gap:12px; max-width:800px; margin:0 auto; }}
.res-tag {{
    background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2);
    border-radius:100px; padding:10px 24px; font-size:14px; color:#fff; font-family:Inter,sans-serif;
}}

/* ── DASHBOARD ── */
.dash-wrap {{ background:#F5F7FB; padding:1.5rem 2rem 3rem 2rem; max-width:1280px; margin:0 auto; }}
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
logo_col, spacer, c_home, c_dash, c_kont = st.columns(
    [2.5, 4.2, 0.9, 1.1, 1.0]
)
with logo_col:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
      <span style="font-size:17px;font-weight:800;color:#1E2A44;font-family:Inter,sans-serif;">
        FGS Dashboard
      </span>
      <span style="background:#1E2A44;color:#fff;padding:4px 10px;
                   border-radius:5px;font-size:12px;font-weight:700;">HSLU</span>
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
with c_kont:
    st.button("Kontakt", key="nav_kont", use_container_width=True)


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
    st.markdown('<div class="dash-wrap">', unsafe_allow_html=True)

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
        <div style="font-size:12px;color:#9CA3AF;">Datenstand 2025</div>
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
    st.markdown('<p style="font-size:11px;font-weight:700;color:#9CA3AF;'
                'text-transform:uppercase;letter-spacing:0.5px;margin:0 0 8px 0;">Filter</p>',
                unsafe_allow_html=True)
    f1, f2, f3, f4, f5, f6 = st.columns(6)
    with f1:
        sel_gruppe = st.selectbox("Gruppe", ["Alle", "FGS", "Non-FGS"], key="fg")
    with f2:
        sg_opts = (["Alle"] + sorted(df_raw[COL_STUDIENGANG].dropna().unique().tolist())
                   if COL_STUDIENGANG in df_raw.columns else ["Alle"])
        sel_sg = st.selectbox("Studiengang", sg_opts, key="fsg")
    with f3:
        g_opts = (["Alle"] + sorted(df_raw[COL_GESCHLECHT].dropna().unique().tolist())
                  if COL_GESCHLECHT in df_raw.columns else ["Alle"])
        sel_g = st.selectbox("Geschlecht", g_opts, key="fg2")
    with f4:
        a_opts = (["Alle"] + sorted(df_raw[COL_ARBEIT].dropna().unique().tolist())
                  if COL_ARBEIT in df_raw.columns else ["Alle"])
        sel_a = st.selectbox("Erwerbstätigkeit", a_opts, key="fa")
    with f5:
        m_opts = (["Alle"] + sorted(df_raw[COL_MIGRATION].dropna().unique().tolist())
                  if COL_MIGRATION in df_raw.columns else ["Alle"])
        sel_m = st.selectbox("Migration", m_opts, key="fm")
    with f6:
        j_opts = (["Alle"] + sorted(df_raw[COL_ABSCHLUSSJAHR].dropna().unique().tolist())
                  if COL_ABSCHLUSSJAHR in df_raw.columns else ["Alle"])
        sel_j = st.selectbox("Jahr", j_opts, key="fj")
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
    _n_fgs_kpi   = int((df[COL_FGS].str.lower() == "ja").sum()) if COL_FGS in df.columns else 0
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
        if COL_STUDIENGANG in df_raw.columns:
            import plotly.express as px
            sg_f = (df_raw[df_raw[COL_FGS].str.lower() == "ja"][COL_STUDIENGANG]
                    .value_counts().reset_index())
            sg_f.columns = ["Studiengang", "Anzahl"]
            fig = px.bar(sg_f, x="Anzahl", y="Studiengang", orientation="h",
                         color_discrete_sequence=[COLORS["blue"]], text="Anzahl")
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(t=0,b=0), height=200, showlegend=False, yaxis_title="")
            fig.update_xaxes(gridcolor="#E5E7EB", dtick=5, showgrid=True)
            fig.update_yaxes(showgrid=False)
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
                height=180, showlegend=False,
                margin=dict(t=0, b=0, l=130, r=80),
                xaxis=dict(range=[0, x_max_arb * 1.45],
                           showticklabels=False, showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=11), automargin=False),
                font=dict(family="Inter, sans-serif", size=11, color="#374151"),
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
    st.markdown('<div class="card"><b>Wann war das Studium bisher besonders herausfordernd?</b></div>', unsafe_allow_html=True)
    if COL_HERAUSFORDERND in df.columns and len(df) >= MIN_N:
        import plotly.express as px
        c1, c2 = st.columns([3, 1])
        rows = []
        if len(df_fgs) >= MIN_N:
            for phase, cnt in df_fgs[COL_HERAUSFORDERND].value_counts().items():
                rows.append({"Phase": phase, "Anzahl": int(cnt), "Gruppe": "FGS"})
        if len(df_nfgs) >= MIN_N:
            for phase, cnt in df_nfgs[COL_HERAUSFORDERND].value_counts().items():
                rows.append({"Phase": phase, "Anzahl": int(cnt), "Gruppe": "Non-FGS"})
        with c1:
            if rows:
                fig = px.bar(pd.DataFrame(rows), x="Phase", y="Anzahl", color="Gruppe",
                             barmode="group", text="Anzahl",
                             color_discrete_map={"FGS": COLORS["blue"], "Non-FGS": COLORS["teal"]})
                fig.update_traces(textposition="outside", textfont_size=11)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(t=0,b=0), height=240, xaxis_title="")
                fig.update_yaxes(gridcolor="#E5E7EB", dtick=2, showgrid=True)
                fig.update_xaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if len(df_fgs) >= MIN_N and COL_HERAUSFORDERND in df_fgs.columns:
                top = df_fgs[COL_HERAUSFORDERND].mode()[0]
                st.markdown(f"""
                <div class="insight-box">
                  <div style="font-size:11px;font-weight:700;color:#2D9CDB;margin-bottom:4px;">KRITISCHSTE PHASE (FGS)</div>
                  <div style="font-size:18px;font-weight:700;color:#1E2A44;">{top}</div>
                  <div style="font-size:12px;color:#6B7280;margin-top:6px;">Häufigste Nennung</div>
                </div>""", unsafe_allow_html=True)

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

    _gew_line  = (f"<b>Häufigster Unterstützungswunsch:</b> {_top_gew[0]} · n&thinsp;=&thinsp;{_top_gew[1]}"
                  if _top_gew[0] else "Keine Daten für Unterstützungswünsche.")
    _hilft_line = (f"<b>Am häufigsten genannte Ressource:</b> {_top_hilft[0]} · n&thinsp;=&thinsp;{_top_hilft[1]}"
                   if _top_hilft[0] else "Keine Daten für hilfreiche Ressourcen.")
    _interp = (
        f"Die Antworten weisen auf einen erhöhten Bedarf im Bereich "
        f"<i>{_top_gew[0]}</i> hin."
        if _top_gew[0] and _top_gew[1] >= MIN_N else ""
    )

    st.markdown(
        f'<div style="background:#fff;border-radius:12px;padding:22px 24px 18px;'
        f'border-left:4px solid #1E2A44;box-shadow:0 1px 6px rgba(0,0,0,0.07);margin-top:0.25rem;">'
        f'<div style="font-size:0.72rem;font-weight:700;color:#00A896;text-transform:uppercase;'
        f'letter-spacing:1px;margin-bottom:14px;">Hinweise auf Unterstützungsbedarfe</div>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;align-items:start;">'
        f'<div style="font-size:0.88rem;color:#374151;line-height:1.6;">{_gew_line}</div>'
        f'<div style="font-size:0.88rem;color:#374151;line-height:1.6;">{_hilft_line}</div>'
        f'<div style="font-size:0.88rem;color:#374151;line-height:1.6;">'
        f'<b>Ausgewertete FGS-Antworten:</b><br>'
        f'<span style="font-size:0.82rem;color:#6B7280;">'
        f'Wünsche: n&thinsp;=&thinsp;{_n_gew_resp} &nbsp;|&nbsp; Ressourcen: n&thinsp;=&thinsp;{_n_hilft_resp}</span>'
        + (f'<br><span style="font-size:0.78rem;color:#6B7280;font-style:italic;margin-top:8px;display:block;">'
           f'{_interp}</span>' if _interp else "")
        + f'</div></div></div>',
        unsafe_allow_html=True
    )

    # E: BELONGING
    st.markdown('<div class="section-title">Sense of Belonging</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div class="card" style="margin-bottom:0;"><b>Zugehörigkeitsgefühl nach Dimension</b></div>
      <div class="card" style="margin-bottom:0;"><b>Vergleichsübersicht</b></div>
    </div>
    """, unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        if len(df_fgs) >= MIN_N:
            st.plotly_chart(
                chart_belonging_bars(df_fgs, df_nfgs if len(df_nfgs) >= MIN_N else None),
                use_container_width=True)
    with e2:
        if len(df_fgs) >= MIN_N:
            sc_fgs  = calculate_belonging_scores(df_fgs)
            sc_nfgs = calculate_belonging_scores(df_nfgs) if len(df_nfgs) >= MIN_N else None
            st.plotly_chart(chart_belonging_radar(sc_fgs, sc_nfgs), use_container_width=True)

    # F: QUALITATIVE EINBLICKE
    st.markdown('<div class="section-title">Qualitative Einblicke</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>Persönliche Erfahrungen und Wünsche von FGS</b></div>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    for col_w, col_data, title, color in [
        (q1, COL_ZUGEHOERIG_POS, "Was hilft für Zugehörigkeit?",          COLORS["teal"]),
        (q2, COL_ZUGEHOERIG_NEG, "Wann fühlen Sie sich nicht zugehörig?", COLORS["coral"]),
        (q3, COL_WUENSCHE,       "Was wünschen Sie sich?",                COLORS["violet"]),
    ]:
        with col_w:
            st.markdown(
                f'<div style="font-size:13px;font-weight:600;color:{color};'
                f'padding:0.25rem 0 0.75rem 0;">{title}</div>',
                unsafe_allow_html=True
            )
            if col_data in df_fgs.columns and len(df_fgs) >= MIN_N:
                antworten = df_fgs[col_data].dropna()
                antworten = antworten[antworten.str.strip() != ""]
                if len(antworten) >= MIN_N:
                    for answer, count in antworten.value_counts().head(5).items():
                        st.markdown(
                            f'<div style="background:#F9FAFB;border-radius:6px;padding:7px 10px;'
                            f'margin-bottom:5px;font-size:12px;color:#374151;">{answer}'
                            f'<span style="float:right;color:#9CA3AF;">{count}×</span></div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.caption("Zu wenige Antworten.")

    st.markdown('</div>', unsafe_allow_html=True)
