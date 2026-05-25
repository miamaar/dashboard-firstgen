import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import load_data
from config import COL_FGS, FGS_LIKERT, COL_SUPPORT_GEWUENSCHT, COL_HILFT, MIN_N

st.set_page_config(page_title="Unterstützung | FGS Dashboard", layout="wide")
df = load_data()
fgs_df = df[df[COL_FGS].str.lower() == "ja"]

st.title("Unterstützung")
st.markdown("Selbsteinschätzung, genutzte Angebote und Wünsche von FGS.")
st.divider()

# Likert-Items
st.subheader("Selbsteinschätzung (FGS, Skala 1–5)")
rows = []
for label, col in FGS_LIKERT.items():
    if col in fgs_df.columns:
        rows.append({"Aussage": label, "Mittelwert": round(fgs_df[col].mean(), 2)})
likert_df = pd.DataFrame(rows)
fig = px.bar(likert_df, x="Mittelwert", y="Aussage", orientation="h",
             range_x=[1, 5], color_discrete_sequence=["#1565C0"])
fig.add_vline(x=3, line_dash="dash", line_color="gray",
              annotation_text="Neutral (3)", annotation_position="top right")
fig.update_layout(yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Was hätten sich FGS gewünscht?")
    if COL_SUPPORT_GEWUENSCHT in fgs_df.columns:
        antworten = fgs_df[COL_SUPPORT_GEWUENSCHT].dropna()
        antworten = antworten[antworten.str.strip() != ""]
        if len(antworten) >= MIN_N:
            for a in antworten:
                st.markdown(f"> {a}")
        else:
            st.info("Zu wenige Antworten.")

with col2:
    st.subheader("Was hilft im Studium?")
    if COL_HILFT in fgs_df.columns:
        antworten2 = fgs_df[COL_HILFT].dropna()
        antworten2 = antworten2[antworten2.str.strip() != ""]
        if len(antworten2) >= MIN_N:
            for a in antworten2:
                st.markdown(f"> {a}")
        else:
            st.info("Zu wenige Antworten.")