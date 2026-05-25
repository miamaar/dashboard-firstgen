# app.py — FGS Dashboard | HSLU Informatik
# Vollständige Version mit allen Fixes
 
import streamlit as st
import pandas as pd
import numpy as np
 
from config import *
from preprocessing import load_data, apply_privacy_threshold, calculate_belonging_scores
from charts import (chart_fgs_donut, chart_challenges_bar,
                    chart_belonging_radar, chart_belonging_bars)
 
st.set_page_config(
    page_title="FGS Dashboard | HSLU Informatik",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""<style>
[data-testid="stSidebarNav"]     { display:none !important; }
section[data-testid="stSidebar"] { display:none !important; }
[data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header        { visibility:hidden; }
 
.stApp { background-color:#F5F7FB; }
.main .block-container { max-width:1280px; padding:1.5rem 2rem 3rem 2rem; }
 
/* Tabs oben */
.stTabs [data-baseweb="tab-list"] {
    background:#FFFFFF; border-radius:10px; padding:4px 8px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-bottom:1.5rem; gap:4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:8px; padding:8px 24px;
    font-size:14px; font-weight:500; color:#6B7280;
}
.stTabs [aria-selected="true"] {
    background-color:#1E2A44 !important; color:#FFFFFF !important;
}
 
/* Cards mit sichtbarer Umrandung */
.card {
    background:#FFFFFF;
    border-radius:12px;
    padding:1rem 1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07);
    margin-bottom:1rem;
    border:1px solid #E5E7EB;
}
 
/* Abschnittstitel */
.section-title {
    font-size:17px; font-weight:600; color:#1E2A44;
    margin:2rem 0 1rem 0; padding-bottom:0.5rem;
    border-bottom:2px solid #EFEFEF;
}
 
/* KPI-Karten */
.kpi-card {
    background:#FFFFFF; border-radius:12px; padding:1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); text-align:center;
    border:1px solid #E5E7EB;
}
.kpi-value { font-size:2rem; font-weight:700; line-height:1.2; }
.kpi-label { font-size:12px; color:#6B7280; margin-top:4px; }
 
/* Kontext-Cards */
.ctx-card {
    background:#FFFFFF; border-radius:12px; padding:1rem 1.25rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.07); border-left:4px solid;
    border-right:1px solid #E5E7EB;
    border-top:1px solid #E5E7EB;
    border-bottom:1px solid #E5E7EB;
}
 
/* Insight-Box */
.insight-box {
    background:#F0F9FF; border-left:4px solid #2D9CDB;
    border-radius:8px; padding:1rem 1.25rem; margin-top:0.5rem;
}
 
[data-testid="metric-container"] {
    background:#FFFFFF; border-radius:12px; padding:1rem;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
}
</style>""", unsafe_allow_html=True)
 
# ── DATEN LADEN ──────────────────────────────────────────────────────────────
df_raw = load_data()
 
# ── TABS ─────────────────────────────────────────────────────────────────────
tab_dash, tab_methodik, tab_hinweise = st.tabs(["Dashboard", "Methodik", "Datenhinweise"])
 
# ════════════════════════════════════════════════════════════════════════════
with tab_dash:
 
    # HEADER
    n_total = len(df_raw)
    st.markdown(f"""
    <div style="background:#FFFFFF; border-radius:16px; padding:1.5rem 2rem;
                box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:1.5rem;
                border:1px solid #E5E7EB;
                display:flex; justify-content:space-between; align-items:flex-start;">
      <div>
        <h1 style="font-size:26px;font-weight:700;color:#1E2A44;margin:0 0 4px 0;">
          FGS Dashboard</h1>
        <p style="font-size:15px;color:#4B5563;margin:0 0 6px 0;">
          Studienerfahrungen, Herausforderungen und Unterstützungsbedarfe
          von First-Generation Studierenden</p>
        <p style="font-size:13px;color:#9CA3AF;margin:0;">
          Das Dashboard macht zentrale Aspekte der Situation von First-Generation
          Studierenden sichtbar und unterstützt die datenbasierte Weiterentwicklung
          von Hochschulangeboten.</p>
      </div>
      <div style="text-align:right;flex-shrink:0;padding-left:2rem;">
        <div style="font-size:12px;color:#9CA3AF;">Teilnehmende</div>
        <div style="font-size:28px;font-weight:700;color:#1E2A44;">{n_total} Antworten</div>
        <div style="font-size:12px;color:#9CA3AF;">Datenstand 2025</div>
      </div>
    </div>""", unsafe_allow_html=True)
 
    # KONTEXT-CARDS
    cc1, cc2, cc3 = st.columns(3)
    for col_w, color, title, text in [
        (cc1, "#2D9CDB", "Projektziel",
         "Bildungsbiografien, Herausforderungen und Ressourcen von Studierenden sichtbar machen."),
        (cc2, "#00A896", "Definition FGS",
         "Personen, deren Eltern keinen Hochschulabschluss besitzen und die als erste in ihrer Familie studieren."),
        (cc3, "#7B61FF", "Datenquelle",
         "Google-Forms-Befragung, bereinigt, anonymisiert aggregiert und interaktiv visualisiert."),
    ]:
        with col_w:
            st.markdown(f"""
            <div class="ctx-card" style="border-left-color:{color};">
              <div style="font-size:11px;font-weight:700;color:{color};
                          text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">
                {title}</div>
              <p style="font-size:13px;color:#374151;margin:0;line-height:1.5;">{text}</p>
            </div>""", unsafe_allow_html=True)
 
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
 
    # FILTER-LEISTE
    st.markdown('<div style="background:#FFFFFF;border-radius:12px;padding:0.75rem 1.25rem;'
                'box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:1.5rem;'
                'border:1px solid #E5E7EB;">',
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
    if sel_gruppe == "FGS":     df = df[df[COL_FGS].str.lower() == "ja"]
    if sel_gruppe == "Non-FGS": df = df[df[COL_FGS].str.lower() == "nein"]
    if sel_sg != "Alle" and COL_STUDIENGANG  in df.columns: df = df[df[COL_STUDIENGANG]   == sel_sg]
    if sel_g  != "Alle" and COL_GESCHLECHT   in df.columns: df = df[df[COL_GESCHLECHT]    == sel_g]
    if sel_a  != "Alle" and COL_ARBEIT       in df.columns: df = df[df[COL_ARBEIT]        == sel_a]
    if sel_m  != "Alle" and COL_MIGRATION    in df.columns: df = df[df[COL_MIGRATION]     == sel_m]
    if sel_j  != "Alle" and COL_ABSCHLUSSJAHR in df.columns: df = df[df[COL_ABSCHLUSSJAHR] == sel_j]
 
    df_fgs  = df[df[COL_FGS].str.lower() == "ja"].copy()  if COL_FGS in df.columns else df.copy()
    df_nfgs = df[df[COL_FGS].str.lower() == "nein"].copy() if COL_FGS in df.columns else pd.DataFrame()
 
    if apply_privacy_threshold(df) is None:
        st.warning(f"Die Fallzahl ist zu klein für eine datenschutzkonforme Auswertung "
                   f"(n={len(df)} < {MIN_N}).")
        st.stop()
 
    # KPI-KARTEN
    n_fgs    = int((df[COL_FGS].str.lower() == "ja").sum()) if COL_FGS in df.columns else 0
    pct_fgs  = round(n_fgs / len(df) * 100) if len(df) > 0 else 0
    all_sob  = [c for g in SOB_GROUPS.values() for c in g if c in df.columns]
    sob_score = round(df[all_sob].mean().mean(), 1) if all_sob else 0
    pct_fin  = round((df["ch_finanzen"] >= 4).mean() * 100) if "ch_finanzen" in df.columns else 0
    pct_zeit = round((df["ch_zeitdruck"] >= 4).mean() * 100) if "ch_zeitdruck" in df.columns else 0
 
    k1, k2, k3, k4, k5 = st.columns(5)
    for col_w, val, label, color in [
        (k1, str(len(df)),   "Teilnehmende",           COLORS["blue"]),
        (k2, f"{pct_fgs} %", "FGS-Anteil",             COLORS["teal"]),
        (k3, f"{sob_score}", "Belonging-Score Ø",      COLORS["violet"]),
        (k4, f"{pct_fin} %", "Hohe finanz. Belastung", COLORS["orange"]),
        (k5, f"{pct_zeit} %","Hoher Zeitdruck",        COLORS["coral"]),
    ]:
        with col_w:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color};">
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-label">{label}</div>
            </div>""", unsafe_allow_html=True)
 
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
 
    # ── A: FGS PROFIL ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">FGS Profil</div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
 
    with a1:
        st.markdown('<div class="card"><b>FGS vs. Non-FGS</b>', unsafe_allow_html=True)
        st.plotly_chart(chart_fgs_donut(df_raw), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with a2:
        st.markdown('<div class="card"><b>FGS nach Studiengang</b>', unsafe_allow_html=True)
        if COL_STUDIENGANG in df_raw.columns:
            import plotly.express as px
            sg_f = (df_raw[df_raw[COL_FGS].str.lower() == "ja"][COL_STUDIENGANG]
                    .value_counts().reset_index())
            sg_f.columns = ["Studiengang", "Anzahl"]
            fig = px.bar(sg_f, x="Anzahl", y="Studiengang", orientation="h",
                         color_discrete_sequence=[COLORS["blue"]], text="Anzahl")
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(t=0, b=0), height=200,
                              showlegend=False, yaxis_title="")
            fig.update_xaxes(gridcolor="#E5E7EB", dtick=5, showgrid=True)
            fig.update_yaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with a3:
        st.markdown('<div class="card"><b>Erwerbstätigkeit (FGS)</b>', unsafe_allow_html=True)
        if COL_ARBEIT in df_fgs.columns and len(df_fgs) >= MIN_N:
            import plotly.express as px
            arb = df_fgs[COL_ARBEIT].value_counts().reset_index()
            arb.columns = ["Pensum", "Anzahl"]
            fig = px.pie(arb, values="Anzahl", names="Pensum", hole=0.5,
                         color_discrete_sequence=[COLORS["blue"], COLORS["teal"], COLORS["violet"]])
            fig.update_traces(textinfo="percent+label", textfont_size=11)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                              margin=dict(t=10, b=10), height=200)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    # ── B: HERAUSFORDERUNGEN ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">Herausforderungen</div>', unsafe_allow_html=True)
    b1, b2 = st.columns([3, 2])
 
    with b1:
        st.markdown('<div class="card"><b>Vergleich FGS vs. Non-FGS (Mittelwert 1–5)</b>',
                    unsafe_allow_html=True)
        if len(df_fgs) >= MIN_N:
            st.plotly_chart(
                chart_challenges_bar(df_fgs, df_nfgs if len(df_nfgs) >= MIN_N else None),
                use_container_width=True)
        else:
            st.info("Zu wenige Daten für diese Auswahl.")
        st.markdown('</div>', unsafe_allow_html=True)
 
    with b2:
        st.markdown('<div class="card"><b>Selbsteinschätzung FGS (Likert 1–5)</b>',
                    unsafe_allow_html=True)
        if len(df_fgs) >= MIN_N:
            import plotly.express as px
            rows = [{"Aussage": lbl, "Mittelwert": round(df_fgs[col].mean(), 1)}
                    for lbl, col in FGS_LIKERT.items() if col in df_fgs.columns]
            if rows:
                ldf = pd.DataFrame(rows)
                fig = px.bar(ldf, x="Mittelwert", y="Aussage", orientation="h",
                             range_x=[1, 5], color_discrete_sequence=[COLORS["violet"]],
                             text="Mittelwert")
                fig.update_traces(textposition="outside", textfont_size=11)
                fig.add_vline(x=3, line_dash="dash", line_color="#D1D5DB",
                              annotation_text="Neutral", annotation_position="top right",
                              annotation_font_size=10)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(t=0, b=0), height=200,
                                  yaxis_title="", showlegend=False)
                fig.update_xaxes(gridcolor="#E5E7EB", dtick=1, showgrid=True)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    # ── C: KRITISCHE STUDIENPHASE ─────────────────────────────────────────────
    st.markdown('<div class="section-title">Kritische Studienphasen</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card"><b>Wann war das Studium bisher besonders herausfordernd?</b>',
                unsafe_allow_html=True)
 
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
                             color_discrete_map={"FGS": COLORS["blue"],
                                                 "Non-FGS": COLORS["teal"]})
                fig.update_traces(textposition="outside", textfont_size=11)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(t=0, b=0), height=240, xaxis_title="")
                fig.update_yaxes(gridcolor="#E5E7EB", dtick=2, showgrid=True)
                fig.update_xaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if len(df_fgs) >= MIN_N and COL_HERAUSFORDERND in df_fgs.columns:
                top = df_fgs[COL_HERAUSFORDERND].mode()[0]
                st.markdown(f"""
                <div class="insight-box">
                  <div style="font-size:11px;font-weight:700;color:#2D9CDB;margin-bottom:4px;">
                    KRITISCHSTE PHASE (FGS)</div>
                  <div style="font-size:18px;font-weight:700;color:#1E2A44;">{top}</div>
                  <div style="font-size:12px;color:#6B7280;margin-top:6px;">
                    Häufigste Nennung</div>
                </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
    # ── D: UNTERSTÜTZUNG ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Unterstützung & Support-Gaps</div>',
                unsafe_allow_html=True)
 
    def _text_bar(series, color):
        import plotly.express as px
        s = series.dropna()
        s = s[s.str.strip() != ""]
        if len(s) < MIN_N:
            return None
        counts = s.value_counts().head(6).reset_index()
        counts.columns = ["Antwort", "Anzahl"]
        fig = px.bar(counts, x="Anzahl", y="Antwort", orientation="h",
                     color_discrete_sequence=[color], text="Anzahl")
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          margin=dict(t=0, b=0), height=220,
                          yaxis_title="", showlegend=False)
        fig.update_xaxes(gridcolor="#E5E7EB", dtick=2, showgrid=True)
        fig.update_yaxes(showgrid=False)
        return fig
 
    d1, d2 = st.columns(2)
    with d1:
        st.markdown('<div class="card"><b>Was hätten sich FGS gewünscht?</b>',
                    unsafe_allow_html=True)
        if COL_SUPPORT_GEWUENSCHT in df_fgs.columns and len(df_fgs) >= MIN_N:
            fig = _text_bar(df_fgs[COL_SUPPORT_GEWUENSCHT], COLORS["orange"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Zu wenige Antworten.")
        st.markdown('</div>', unsafe_allow_html=True)
 
    with d2:
        st.markdown('<div class="card"><b>Was hilft FGS im Studium?</b>',
                    unsafe_allow_html=True)
        if COL_HILFT in df_fgs.columns and len(df_fgs) >= MIN_N:
            fig = _text_bar(df_fgs[COL_HILFT], COLORS["teal"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Zu wenige Antworten.")
        st.markdown('</div>', unsafe_allow_html=True)
 
    # ── E: SENSE OF BELONGING ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">Sense of Belonging</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
 
    with e1:
        st.markdown('<div class="card"><b>Vergleich nach Dimension</b>',
                    unsafe_allow_html=True)
        if len(df_fgs) >= MIN_N:
            st.plotly_chart(
                chart_belonging_bars(df_fgs, df_nfgs if len(df_nfgs) >= MIN_N else None),
                use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with e2:
        st.markdown('<div class="card"><b>Radar-Übersicht</b>', unsafe_allow_html=True)
        if len(df_fgs) >= MIN_N:
            sc_fgs  = calculate_belonging_scores(df_fgs)
            sc_nfgs = calculate_belonging_scores(df_nfgs) if len(df_nfgs) >= MIN_N else None
            st.plotly_chart(chart_belonging_radar(sc_fgs, sc_nfgs), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    # ── F: QUALITATIVE EINBLICKE ──────────────────────────────────────────────
    st.markdown('<div class="section-title">Qualitative Einblicke</div>',
                unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
 
    for col_w, col_data, title, color in [
        (q1, COL_ZUGEHOERIG_POS, "Was hilft für Zugehörigkeit?",         COLORS["teal"]),
        (q2, COL_ZUGEHOERIG_NEG, "Wann fühlen Sie sich nicht zugehörig?", COLORS["coral"]),
        (q3, COL_WUENSCHE,       "Was wünschen Sie sich?",                COLORS["violet"]),
    ]:
        with col_w:
            st.markdown(f'<div style="font-size:13px;font-weight:600;color:{color};'
                        f'margin-bottom:8px;">{title}</div>', unsafe_allow_html=True)
            if col_data in df_fgs.columns and len(df_fgs) >= MIN_N:
                antworten = df_fgs[col_data].dropna()
                antworten = antworten[antworten.str.strip() != ""]
                if len(antworten) >= MIN_N:
                    for answer, count in antworten.value_counts().head(5).items():
                        st.markdown(
                            f'<div style="background:#F9FAFB;border-radius:6px;'
                            f'padding:7px 10px;margin-bottom:5px;font-size:12px;'
                            f'color:#374151;">{answer} '
                            f'<span style="float:right;color:#9CA3AF;">{count}x</span>'
                            f'</div>', unsafe_allow_html=True)
                else:
                    st.caption("Zu wenige Antworten.")
 
# ════════════════════════════════════════════════════════════════════════════
with tab_methodik:
    st.markdown('<div class="section-title">Methodik & Datenpipeline</div>',
                unsafe_allow_html=True)
 
    st.markdown('<div class="card"><b>Datenfluss</b>', unsafe_allow_html=True)
    steps = ["CSV-Import", "Spalten bereinigen", "Likert numerisch",
             "FGS-Status", "Aggregation", "Visualisierung"]
    step_colors = [COLORS["blue"], COLORS["teal"], COLORS["violet"],
                   COLORS["orange"], COLORS["coral"], COLORS["dark_blue"]]
    cols_s = st.columns(len(steps))
    for i, (step, color) in enumerate(zip(steps, step_colors)):
        with cols_s[i]:
            st.markdown(f"""
            <div style="text-align:center;">
              <div style="background:{color};color:#FFF;border-radius:8px;
                          padding:8px 4px;font-size:11px;font-weight:600;
                          margin-bottom:4px;">{i+1}</div>
              <div style="font-size:11px;color:#374151;line-height:1.4;">{step}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="card"><b>Datenschutz</b>', unsafe_allow_html=True)
    st.markdown(f"""
- Nur aggregierte Darstellung — keine Einzelantworten sichtbar
- Mindestfallzahl: **n ≥ {MIN_N}** — Gruppen darunter werden nicht ausgewiesen
- Keine Rückverfolgbarkeit einzelner Personen
- Anonymisierung vor jeder Analyse
    """)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ════════════════════════════════════════════════════════════════════════════
with tab_hinweise:
    st.markdown('<div class="section-title">Datenhinweise</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="card"><b>Skalierbarkeit</b>', unsafe_allow_html=True)
    st.markdown("""
Zukünftige Survey-Wellen ab 2025 können direkt integriert werden:
- Jahr als Filterdimension vorhanden
- CSV einfach in `data/raw/survey.csv` ersetzen
- Spaltenmapping zentral in `config.py` anpassbar
    """)
    st.markdown('</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="card"><b>Interpretation der Werte</b>', unsafe_allow_html=True)
    st.markdown(f"""
- Likert-Skala: 1 = trifft gar nicht zu, 5 = trifft voll zu
- FGS-Status basiert auf Selbstauskunft der Befragten
- Belonging-Score: Mittelwert aller Items der jeweiligen Dimension
- Gruppen mit n < {MIN_N} werden aus Datenschutzgründen nicht ausgewiesen
    """)
    st.markdown('</div>', unsafe_allow_html=True)