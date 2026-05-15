import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.services.mirror_analysis_service import (
    run_mirror_analysis
)

from src.services.anomaly_service import (
    run_anomaly_detection
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title=
    "AI Trade Intelligence Platform",

    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "AI-Powered Trade Intelligence Platform"
)

st.markdown(
    """
    Dynamic mirror trade analytics,
    anomaly detection,
    and sector intelligence system
    powered by UN Comtrade.
    """
)

# ===================================
# SIDEBAR INPUTS
# ===================================

st.sidebar.header(
    "Trade Query"
)

# -----------------------------------
# COUNTRY INPUTS
# -----------------------------------

reporter_country = st.sidebar.text_input(

    "Reporter Country",

    value="India"
)

partner_country = st.sidebar.text_input(

    "Partner Country",

    value="China"
)

# -----------------------------------
# HS CODE
# -----------------------------------

hs_code = st.sidebar.text_input(

    "HS Code",

    value="8517"
)

# -----------------------------------
# FREQUENCY
# -----------------------------------

frequency = st.sidebar.selectbox(

    "Frequency",

    ["M", "A"]
)

# -----------------------------------
# YEAR RANGE
# -----------------------------------

start_year = st.sidebar.number_input(

    "Start Year",

    min_value=2000,

    max_value=2025,

    value=2020
)

end_year = st.sidebar.number_input(

    "End Year",

    min_value=2000,

    max_value=2025,

    value=2024
)

# ===================================
# RUN BUTTON
# ===================================

run_button = st.sidebar.button(
    "Run Analysis"
)

# ===================================
# MAIN EXECUTION
# ===================================

if run_button:

    with st.spinner(
        "Fetching trade data..."
    ):

        # -----------------------------
        # MIRROR ANALYSIS
        # -----------------------------

        df = run_mirror_analysis(

            reporter_country=
                reporter_country,

            partner_country=
                partner_country,

            hs_code=
                hs_code,

            start_year=
                start_year,

            end_year=
                end_year,

            frequency=
                frequency
        )

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if df.empty:

        st.error(
            "No trade data found."
        )

    else:

        # -----------------------------
        # ANOMALY DETECTION
        # -----------------------------

        df = run_anomaly_detection(df)

        # -----------------------------
        # SUCCESS MESSAGE
        # -----------------------------

        st.success(
            "Analysis Complete"
        )

        # ===================================
        # METRICS
        # ===================================

        latest = df.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "Imports",

            f"${latest['import_value']:,.0f}"
        )

        col2.metric(

            "Exports",

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
            "Imports vs Exports"
        )

        fig1 = go.Figure()

        fig1.add_trace(

            go.Scatter(

                x=df["period"],

                y=df["import_value"],

                mode='lines+markers',

                name='Imports'
            )
        )

        fig1.add_trace(

            go.Scatter(

                x=df["period"],

                y=df["export_value"],

                mode='lines+markers',

                name='Exports'
            )
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # ===================================
        # MISMATCH TREND
        # ===================================

        st.subheader(
            "Mismatch Trend"
        )

        fig2 = px.line(

            df,

            x="period",

            y="mismatch_percent",

            markers=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ===================================
        # Z-SCORE
        # ===================================

        st.subheader(
            "Z-Score Analysis"
        )

        fig3 = px.bar(

            df,

            x="period",

            y="z_score",

            color="anomaly_label"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # ===================================
        # ANOMALY SCORES
        # ===================================

        st.subheader(
            "Anomaly Scores"
        )

        fig4 = px.bar(

            df,

            x="period",

            y="anomaly_score",

            color="anomaly_label"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        # ===================================
        # ANOMALY TABLE
        # ===================================

        st.subheader(
            "Detected Anomalies"
        )

        anomalies = df[

            df["anomaly_label"]
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

        st.dataframe(df)