import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import load_data
from config import COL_FGS, SOB_GROUPS, MIN_N

st.set_page_config(page_title="Belonging | FGS Dashboard", layout="wide")
df = load_data()
fgs_df  = df[df[COL_FGS].str.lower() == "ja"]
nfgs_df = df[df[COL_FGS].str.lower() == "nein"]

st.title("Sense of Belonging")
st.markdown("Vergleich des Zugehörigkeitsgefühls zwischen FGS und Non-FGS (Skala 1–5).")
st.divider()

results = []
for group_name, cols_dict in SOB_GROUPS.items():
    cols = [c for c in cols_dict.values() if c in df.columns]
    if cols:
        results.append({
            "Dimension": group_name,
            "FGS":     round(fgs_df[cols].mean().mean(), 2),
            "Non-FGS": round(nfgs_df[cols].mean().mean(), 2),
        })

res_df = pd.DataFrame(results)
res_df["Differenz"] = (res_df["FGS"] - res_df["Non-FGS"]).round(2)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Vergleich nach Dimension")
    melted = res_df.melt(id_vars="Dimension", value_vars=["FGS", "Non-FGS"],
                         var_name="Gruppe", value_name="Mittelwert")
    fig = px.bar(melted, x="Dimension", y="Mittelwert", color="Gruppe",
                 barmode="group", range_y=[1, 5],
                 color_discrete_map={"FGS": "#1565C0", "Non-FGS": "#90CAF9"})
    fig.update_layout(xaxis_tickangle=-20, xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Radar-Übersicht")
    dims = res_df["Dimension"].tolist()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(
        r=res_df["FGS"].tolist() + [res_df["FGS"].tolist()[0]],
        theta=dims + [dims[0]], fill="toself", name="FGS", line_color="#1565C0"
    ))
    fig2.add_trace(go.Scatterpolar(
        r=res_df["Non-FGS"].tolist() + [res_df["Non-FGS"].tolist()[0]],
        theta=dims + [dims[0]], fill="toself", name="Non-FGS",
        line_color="#90CAF9", opacity=0.7
    ))
    fig2.update_layout(polar=dict(radialaxis=dict(range=[1, 5])))
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Detailtabelle")
st.dataframe(res_df, use_container_width=True, hide_index=True)