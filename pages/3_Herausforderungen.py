import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import load_data
from config import COL_FGS, CHALLENGES, MIN_N

st.set_page_config(page_title="Herausforderungen | FGS Dashboard", layout="wide")
df = load_data()
fgs_df  = df[df[COL_FGS].str.lower() == "ja"]
nfgs_df = df[df[COL_FGS].str.lower() == "nein"]

st.sidebar.title("Filter")
gruppe = st.sidebar.radio("Gruppe", ["FGS & Non-FGS", "Nur FGS", "Nur Non-FGS"])

st.title("Herausforderungen")
st.markdown("Wie stark erleben Studierende verschiedene Barrieren im Studium? (Skala 1–5)")
st.divider()

ch_cols   = list(CHALLENGES.values())
ch_labels = list(CHALLENGES.keys())

avg_fgs  = [fgs_df[c].mean()  for c in ch_cols if c in df.columns]
avg_nfgs = [nfgs_df[c].mean() for c in ch_cols if c in df.columns]

# Radar
st.subheader("Radar-Übersicht")
fig = go.Figure()
if gruppe in ["FGS & Non-FGS", "Nur FGS"]:
    fig.add_trace(go.Scatterpolar(
        r=avg_fgs + [avg_fgs[0]],
        theta=ch_labels + [ch_labels[0]],
        fill="toself", name="FGS", line_color="#1565C0"
    ))
if gruppe in ["FGS & Non-FGS", "Nur Non-FGS"]:
    fig.add_trace(go.Scatterpolar(
        r=avg_nfgs + [avg_nfgs[0]],
        theta=ch_labels + [ch_labels[0]],
        fill="toself", name="Non-FGS", line_color="#90CAF9", opacity=0.7
    ))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])))
st.plotly_chart(fig, use_container_width=True)

# Balkendiagramm
st.subheader("Detailvergleich")
rows = []
if gruppe in ["FGS & Non-FGS", "Nur FGS"]:
    for label, val in zip(ch_labels, avg_fgs):
        rows.append({"Herausforderung": label, "Mittelwert": round(val, 2), "Gruppe": "FGS"})
if gruppe in ["FGS & Non-FGS", "Nur Non-FGS"]:
    for label, val in zip(ch_labels, avg_nfgs):
        rows.append({"Herausforderung": label, "Mittelwert": round(val, 2), "Gruppe": "Non-FGS"})

comp_df = pd.DataFrame(rows)
fig2 = px.bar(comp_df, x="Herausforderung", y="Mittelwert", color="Gruppe",
              barmode="group", range_y=[1, 5],
              color_discrete_map={"FGS": "#1565C0", "Non-FGS": "#90CAF9"})
fig2.update_layout(xaxis_tickangle=-25)
st.plotly_chart(fig2, use_container_width=True)