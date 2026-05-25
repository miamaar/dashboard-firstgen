import streamlit as st
import plotly.express as px
from src.data_loader import load_data
from config import COL_FGS, COL_STUDIENGANG, COL_GESCHLECHT, COL_ALTER, COL_MIGRATION, COL_ARBEIT, MIN_N

st.set_page_config(page_title="FGS Profil | FGS Dashboard", layout="wide")
df = load_data()
fgs_df = df[df[COL_FGS].str.lower() == "ja"].copy()

st.sidebar.title("Filter")
sg_opts = ["Alle"] + sorted(df[COL_STUDIENGANG].dropna().unique().tolist())
sel_sg = st.sidebar.selectbox("Studiengang", sg_opts)
if sel_sg != "Alle":
    fgs_df = fgs_df[fgs_df[COL_STUDIENGANG] == sel_sg]

st.title("FGS Profil")
st.markdown("Wer sind First-Generation-Studierende an der HSLU Informatik?")
st.divider()

if len(fgs_df) < MIN_N:
    st.warning(f"Zu wenige Antworten für diese Auswahl (n={len(fgs_df)}).")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Geschlecht")
    g = fgs_df[COL_GESCHLECHT].value_counts().reset_index()
    g.columns = ["Geschlecht", "Anzahl"]
    fig = px.pie(g, values="Anzahl", names="Geschlecht",
                 color_discrete_sequence=["#1565C0", "#42A5F5", "#BBDEFB"])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Migrationshintergrund")
    m = fgs_df[COL_MIGRATION].value_counts().reset_index()
    m.columns = ["Migration", "Anzahl"]
    fig2 = px.pie(m, values="Anzahl", names="Migration",
                  color_discrete_sequence=["#1565C0", "#90CAF9"])
    fig2.update_traces(textinfo="percent+label")
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Studiengang")
    sg = fgs_df[COL_STUDIENGANG].value_counts().reset_index()
    sg.columns = ["Studiengang", "Anzahl"]
    fig3 = px.bar(sg, x="Anzahl", y="Studiengang", orientation="h",
                  color_discrete_sequence=["#1565C0"])
    fig3.update_layout(showlegend=False, yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Arbeit neben Studium")
    a = fgs_df[COL_ARBEIT].value_counts().reset_index()
    a.columns = ["Arbeit", "Anzahl"]
    fig4 = px.bar(a, x="Arbeit", y="Anzahl",
                  color_discrete_sequence=["#1565C0"])
    fig4.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Altersverteilung")
fig5 = px.histogram(fgs_df, x=COL_ALTER, nbins=10,
                    color_discrete_sequence=["#1565C0"],
                    labels={COL_ALTER: "Alter"})
fig5.update_layout(bargap=0.1, yaxis_title="Anzahl")
st.plotly_chart(fig5, use_container_width=True)