# charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import COLORS, CHALLENGES, SOB_GROUPS, COL_FGS, MIN_N

_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10, l=10, r=10),
    font=dict(family="Inter, sans-serif", size=12, color="#374151"),
)

# Kurze Dimensionsnamen fuer Radar und Balken
SOB_SHORT_NAMES = {
    "Allgemeine Zugehörigkeit":  "Allgemein",
    "Soziale Integration":       "Sozial",
    "Akademische Zugehörigkeit": "Akademisch",
    "Identität & Vielfalt":      "Identität",
}


def chart_fgs_donut(df):
    counts = df[COL_FGS].value_counts().reset_index()
    counts.columns = ["Gruppe", "Anzahl"]
    fig = px.pie(
        counts, values="Anzahl", names="Gruppe", hole=0.55,
        color_discrete_sequence=[COLORS["blue"], COLORS["teal"], COLORS["orange"]]
    )
    fig.update_traces(
        textinfo="percent",
        textfont_size=12,
        textposition="inside",
        insidetextorientation="radial",
    )
    # Kein **_LAYOUT hier — margin nur einmal angeben
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        height=200,
        margin=dict(t=10, b=40, l=10, r=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
    )
    return fig


def chart_challenges_bar(df_fgs, df_nfgs=None):
    rows = []
    for label, col in CHALLENGES.items():
        if col in df_fgs.columns:
            rows.append({
                "Herausforderung": label,
                "Mittelwert": round(df_fgs[col].mean(), 1),
                "Gruppe": "FGS"
            })
        if df_nfgs is not None and col in df_nfgs.columns and len(df_nfgs) >= MIN_N:
            rows.append({
                "Herausforderung": label,
                "Mittelwert": round(df_nfgs[col].mean(), 1),
                "Gruppe": "Non-FGS"
            })
    fig = px.bar(
        pd.DataFrame(rows),
        x="Mittelwert", y="Herausforderung",
        color="Gruppe", barmode="group", orientation="h",
        range_x=[1, 5], text="Mittelwert",
        color_discrete_map={"FGS": COLORS["blue"], "Non-FGS": COLORS["teal"]}
    )
    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        height=260,
        margin=dict(t=10, b=10, l=10, r=60),
        yaxis_title="",
        xaxis_title="Mittelwert (1-5)",
        legend=dict(
            orientation="h", yanchor="bottom",
            y=1.02, xanchor="right", x=1
        )
    )
    fig.update_xaxes(gridcolor="#E5E7EB", dtick=1, showgrid=True)
    fig.update_yaxes(showgrid=False)
    return fig


def chart_belonging_radar(scores_fgs, scores_nfgs=None):
    dims_long  = [k for k in scores_fgs if k != "Gesamt"]
    dims_short = [SOB_SHORT_NAMES.get(d, d) for d in dims_long]

    fig = go.Figure()
    vals_fgs = [scores_fgs[d] for d in dims_long]
    fig.add_trace(go.Scatterpolar(
        r=vals_fgs + [vals_fgs[0]],
        theta=dims_short + [dims_short[0]],
        fill="toself",
        name="FGS",
        line_color=COLORS["blue"],
        fillcolor="rgba(45,156,219,0.15)"
    ))
    if scores_nfgs:
        vals_nfgs = [scores_nfgs.get(d, 0) for d in dims_long]
        fig.add_trace(go.Scatterpolar(
            r=vals_nfgs + [vals_nfgs[0]],
            theta=dims_short + [dims_short[0]],
            fill="toself",
            name="Non-FGS",
            line_color=COLORS["teal"],
            fillcolor="rgba(0,168,150,0.12)"
        ))
    fig.update_layout(
        height=220,
        margin=dict(t=30, b=50, l=60, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5],
                gridcolor="#E0E0E0",
                tickfont=dict(size=10),
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="#374151"),
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def chart_belonging_bars(df_fgs, df_nfgs=None):
    rows = []
    for group_name, group_cols in SOB_GROUPS.items():
        short  = SOB_SHORT_NAMES.get(group_name, group_name)
        cols_f = [c for c in group_cols if c in df_fgs.columns]
        if cols_f:
            rows.append({
                "Dimension": short,
                "Mittelwert": round(df_fgs[cols_f].mean().mean(), 1),
                "Gruppe": "FGS"
            })
        if df_nfgs is not None and len(df_nfgs) >= MIN_N:
            cols_n = [c for c in group_cols if c in df_nfgs.columns]
            if cols_n:
                rows.append({
                    "Dimension": short,
                    "Mittelwert": round(df_nfgs[cols_n].mean().mean(), 1),
                    "Gruppe": "Non-FGS"
                })
    fig = px.bar(
        pd.DataFrame(rows),
        x="Dimension", y="Mittelwert",
        color="Gruppe", barmode="group",
        range_y=[1, 5], text="Mittelwert",
        color_discrete_map={"FGS": COLORS["blue"], "Non-FGS": COLORS["teal"]}
    )
    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        height=220,
        margin=dict(t=10, b=10, l=10, r=20),
        xaxis_title="",
        yaxis_title="Mittelwert (1-5)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig.update_yaxes(gridcolor="#E5E7EB", dtick=1, showgrid=True)
    fig.update_xaxes(showgrid=False)
    return fig