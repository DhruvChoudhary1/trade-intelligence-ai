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

from src.services.explanation_service import (
    generate_explanation
)

from src.services.hs_service import (

    get_all_hs_options,

    extract_hs_code
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title=
    "AI Trade Intelligence Platform",

    layout="wide"
)

# ===================================
# LOAD COUNTRY DATA
# ===================================

reporter_df = pd.read_csv(
    "data/reference/reporter_countries.csv"
)

partner_df = pd.read_csv(
    "data/reference/partner_countries.csv"
)

# -----------------------------------
# CLEAN COUNTRY NAMES
# -----------------------------------

reporter_df["text"] = (

    reporter_df["text"]

    .astype(str)

    .str.strip()
)

partner_df["text"] = (

    partner_df["text"]

    .astype(str)

    .str.strip()
)

# ===================================
# COUNTRY OPTIONS
# ===================================

reporter_options = sorted(

    reporter_df["text"]
    .unique()
)

partner_options = sorted(

    partner_df["text"]
    .unique()
)

# ===================================
# HS OPTIONS
# ===================================

hs_options = get_all_hs_options()

# ===================================
# TITLE
# ===================================

st.title(
    "AI-Powered Trade Intelligence Platform"
)

st.markdown(
    """
    Dynamic bilateral trade analytics,
    anomaly detection,
    and AI-generated intelligence
    using UN Comtrade mirror statistics.
    """
)

# ===================================
# SIDEBAR
# ===================================

st.sidebar.header(
    "Trade Query"
)

# -----------------------------------
# REPORTER COUNTRY
# -----------------------------------

reporter_country = st.sidebar.selectbox(

    "Reporter Country",

    reporter_options,

    index=reporter_options.index(
        "India"
    )
    if "India" in reporter_options
    else 0
)

# -----------------------------------
# PARTNER COUNTRY
# -----------------------------------

partner_country = st.sidebar.selectbox(

    "Partner Country",

    partner_options,

    index=partner_options.index(
        "China"
    )
    if "China" in partner_options
    else 0
)

# ===================================
# HS DROPDOWN
# ===================================

selected_hs = st.sidebar.selectbox(

    "Select Commodity (HS Code)",

    hs_options
)

# -----------------------------------
# EXTRACT HS CODE
# -----------------------------------

hs_code = extract_hs_code(
    selected_hs
)

# ===================================
# FREQUENCY
# ===================================

frequency = st.sidebar.selectbox(

    "Frequency",

    ["M", "A"]
)

# ===================================
# YEAR RANGE
# ===================================

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

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if reporter_country == partner_country:

        st.error(
            "Reporter and partner "
            "countries cannot be the same."
        )

    else:

        # -----------------------------------
        # FETCH DATA
        # -----------------------------------

        with st.spinner(
            "Fetching trade data..."
        ):

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
        # NO DATA
        # -----------------------------------

        if df.empty:

            st.error(
                "No trade data found."
            )

        else:

            # -----------------------------------
            # RUN ANOMALY DETECTION
            # -----------------------------------

            with st.spinner(
                "Running anomaly detection..."
            ):

                df = run_anomaly_detection(
                    df
                )

            # -----------------------------------
            # AI SUMMARY
            # -----------------------------------

            explanation = generate_explanation(
                df
            )

            # -----------------------------------
            # SUCCESS
            # -----------------------------------

            st.success(
                "Analysis Complete"
            )

            # ===================================
            # QUERY INFO
            # ===================================

            st.subheader(
                "Query Details"
            )

            st.write(
                f"Reporter: "
                f"{reporter_country}"
            )

            st.write(
                f"Partner: "
                f"{partner_country}"
            )

            st.write(
                f"HS Code: "
                f"{hs_code}"
            )

            st.write(
                f"Commodity: "
                f"{selected_hs}"
            )

            # ===================================
            # AI SUMMARY
            # ===================================

            st.subheader(
                "AI Intelligence Summary"
            )

            st.info(
                explanation
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
            # Z-SCORE ANALYSIS
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
            # DETECTED ANOMALIES
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
            # FULL DATASET
            # ===================================

            st.subheader(
                "Full Dataset"
            )

            st.dataframe(df)