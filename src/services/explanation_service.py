import pandas as pd

# -----------------------------------
# MAIN EXPLANATION SERVICE
# -----------------------------------

def generate_explanation(df):

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if df.empty:

        return (
            "No trade data available "
            "for analysis."
        )

    # -----------------------------------
    # BASIC METRICS
    # -----------------------------------

    avg_mismatch = (
        df["mismatch_percent"]
        .mean()
    )

    max_mismatch = (
        df["mismatch_percent"]
        .max()
    )

    volatility = (
        df["mismatch_percent"]
        .std()
    )

    anomaly_count = len(

        df[
            df["anomaly_label"]
            == "Anomaly"
        ]
    )

    total_periods = len(df)

    anomaly_frequency = (

        anomaly_count
        /
        total_periods
    )

    latest_mismatch = (
        df.iloc[-1][
            "mismatch_percent"
        ]
    )

    # -----------------------------------
    # RISK CLASSIFICATION
    # -----------------------------------

    if avg_mismatch >= 40:

        risk_level = "Critical"

    elif avg_mismatch >= 25:

        risk_level = "High"

    elif avg_mismatch >= 10:

        risk_level = "Medium"

    else:

        risk_level = "Low"

    # -----------------------------------
    # TREND ANALYSIS
    # -----------------------------------

    first_half = df[
        "mismatch_percent"
    ].iloc[
        :len(df)//2
    ].mean()

    second_half = df[
        "mismatch_percent"
    ].iloc[
        len(df)//2:
    ].mean()

    if second_half > first_half:

        trend = (
            "Mismatch levels appear "
            "to be increasing over time."
        )

    else:

        trend = (
            "Mismatch levels appear "
            "relatively stable over time."
        )

    # -----------------------------------
    # VOLATILITY INTERPRETATION
    # -----------------------------------

    if volatility >= 20:

        volatility_text = (

            "Trade behavior shows "
            "high volatility and "
            "structural instability."
        )

    elif volatility >= 10:

        volatility_text = (

            "Trade behavior shows "
            "moderate volatility."
        )

    else:

        volatility_text = (

            "Trade behavior appears "
            "comparatively stable."
        )

    # -----------------------------------
    # ANOMALY INTERPRETATION
    # -----------------------------------

    if anomaly_frequency >= 0.2:

        anomaly_text = (

            "Frequent anomaly detection "
            "suggests persistent "
            "trade asymmetry."
        )

    elif anomaly_frequency >= 0.1:

        anomaly_text = (

            "Periodic anomalies were "
            "detected across the "
            "selected periods."
        )

    else:

        anomaly_text = (

            "Only limited anomaly "
            "activity was observed."
        )

    # -----------------------------------
    # FINAL REPORT
    # -----------------------------------

    explanation = f"""
Trade Intelligence Summary

Risk Level: {risk_level}

Key Metrics:
- Average Mismatch: {avg_mismatch:.2f}%
- Maximum Mismatch: {max_mismatch:.2f}%
- Latest Mismatch: {latest_mismatch:.2f}%
- Volatility: {volatility:.2f}
- Anomaly Frequency: {anomaly_frequency:.2f}

Analysis:
{trend}

{volatility_text}

{anomaly_text}

Potential contributing factors may include:
- reporting asymmetry,
- freight and insurance differences,
- supply-chain rerouting,
- transshipment effects,
- classification inconsistencies,
- geopolitical trade distortions.
"""

    return explanation