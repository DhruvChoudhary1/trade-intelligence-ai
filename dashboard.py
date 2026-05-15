import streamlit as st
import pandas as pd
import plotly.express as px

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
    "trade_anomaly_results.csv"
)

df = pd.read_csv(
    data_path
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "Global Trade Intelligence Dashboard"
)

st.markdown(
    """
    Bilateral trade mismatch and
    anomaly detection system using
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
# METRICS
# -----------------------------------

latest = filtered_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(

    "Latest Imports",

    f"${latest['india_import_value']:,.0f}"
)

col2.metric(

    "Latest Exports",

    f"${latest['china_export_value']:,.0f}"
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
# CHART 1
# IMPORTS VS EXPORTS
# ===================================

st.subheader(
    "Imports vs Exports"
)

fig1 = px.line(

    filtered_df,

    x="year",

    y=[
        "india_import_value",
        "china_export_value"
    ],

    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ===================================
# CHART 2
# MISMATCH %
# ===================================

st.subheader(
    "Mismatch Percentage Trend"
)

fig2 = px.line(

    filtered_df,

    x="year",

    y="mismatch_percent",

    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===================================
# CHART 3
# ANOMALY SCORES
# ===================================

st.subheader(
    "Anomaly Scores"
)

fig3 = px.bar(

    filtered_df,

    x="year",

    y="anomaly_score",

    color="anomaly_label"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ===================================
# ANOMALY TABLE
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
# FULL DATA
# ===================================

st.subheader(
    "Full Dataset"
)

st.dataframe(
    filtered_df
)