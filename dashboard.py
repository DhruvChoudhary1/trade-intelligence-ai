import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title=
    "Trade Intelligence Dashboard",

    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

data_path = (

    "data/results/"
    "trade_anomalies_results.csv"
)

df = pd.read_csv(
    data_path
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "AI-Powered Trade Intelligence Dashboard"
)

st.markdown(
    """
    Interactive bilateral trade anomaly
    detection platform using
    UN Comtrade mirror statistics.
    """
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header(
    "Filters"
)

selected_hs = st.sidebar.selectbox(

    "Select HS Code",

    df["hs_code"].unique()
)

filtered_df = df[
    df["hs_code"] == selected_hs
]

# -----------------------------------
# PERIOD FORMATTING
# -----------------------------------

filtered_df["period"] = (
    filtered_df["period"]
    .astype(str)
)

# -----------------------------------
# LATEST VALUES
# -----------------------------------

latest = filtered_df.iloc[-1]

# -----------------------------------
# METRICS
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(

    "Latest Imports",

    f"${latest['import_value']:,.0f}"
)

col2.metric(

    "Latest Exports",

    f"${latest['export_value']:,.0f}"
)

col3.metric(

    "Trade Gap",

    f"${latest['trade_gap']:,.0f}"
)

col4.metric(

    "Mismatch %",

    f"{latest['mismatch_percent']:.2f}%"
)

# ===================================
# IMPORTS VS EXPORTS
# ===================================

st.subheader(
    "Monthly Imports vs Exports"
)

fig1 = go.Figure()

fig1.add_trace(

    go.Scatter(

        x=filtered_df["period"],

        y=filtered_df["import_value"],

        mode='lines+markers',

        name='Imports'
    )
)

fig1.add_trace(

    go.Scatter(

        x=filtered_df["period"],

        y=filtered_df["export_value"],

        mode='lines+markers',

        name='Exports'
    )
)

fig1.update_layout(

    xaxis_title="Period",

    yaxis_title="Trade Value",

    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ===================================
# MISMATCH TREND
# ===================================

st.subheader(
    "Mismatch Percentage Trend"
)

fig2 = px.line(

    filtered_df,

    x="period",

    y="mismatch_percent",

    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===================================
# ROLLING MEAN
# ===================================

st.subheader(
    "Rolling Mean of Mismatch %"
)

fig3 = px.line(

    filtered_df,

    x="period",

    y="rolling_mean",

    markers=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ===================================
# Z-SCORE ANALYSIS
# ===================================

st.subheader(
    "Z-Score Analysis"
)

fig4 = px.bar(

    filtered_df,

    x="period",

    y="z_score",

    color="anomaly_label"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ===================================
# ANOMALY SCORES
# ===================================

st.subheader(
    "Anomaly Scores"
)

fig5 = px.bar(

    filtered_df,

    x="period",

    y="anomaly_score",

    color="anomaly_label"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ===================================
# DETECTED ANOMALIES
# ===================================

st.subheader(
    "Detected Anomalies"
)

anomalies = filtered_df[
    filtered_df["anomaly_label"]
    == "Anomaly"
]

st.dataframe(
    anomalies
)

# ===================================
# FULL DATASET
# ===================================

st.subheader(
    "Full Monthly Dataset"
)

st.dataframe(
    filtered_df
)