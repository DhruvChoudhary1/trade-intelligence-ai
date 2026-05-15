import pandas as pd
import numpy as np

from sklearn.ensemble import (
    IsolationForest
)

from sklearn.preprocessing import (
    StandardScaler
)

# -----------------------------------
# DISPLAY SETTINGS
# -----------------------------------

pd.set_option(
    'display.float_format',
    '{:,.2f}'.format
)

# -----------------------------------
# MAIN SERVICE
# -----------------------------------

def run_anomaly_detection(df):

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if df.empty:

        return df

    # -----------------------------------
    # SORT
    # -----------------------------------

    df = df.sort_values(
        by="period"
    )

    # -----------------------------------
    # FEATURE ENGINEERING
    # -----------------------------------

    # Rolling mean

    df["rolling_mean"] = (

        df["mismatch_percent"]

        .rolling(window=3)

        .mean()
    )

    # Rolling std

    df["rolling_std"] = (

        df["mismatch_percent"]

        .rolling(window=3)

        .std()
    )

    # Month-over-month change

    df["mom_change"] = (

        df["mismatch_percent"]

        .pct_change()
    )

    # Z-score

    mean_val = (
        df["mismatch_percent"]
        .mean()
    )

    std_val = (
        df["mismatch_percent"]
        .std()
    )

    # Avoid divide-by-zero

    if std_val == 0:

        std_val = 1

    df["z_score"] = (

        (
            df["mismatch_percent"]
            -
            mean_val
        )

        /

        std_val
    )

    # -----------------------------------
    # DROP NaN ROWS
    # -----------------------------------

    df = df.dropna()

    # -----------------------------------
    # FEATURES
    # -----------------------------------

    features = [

        "mismatch_percent",

        "trade_gap",

        "rolling_mean",

        "rolling_std",

        "mom_change",

        "z_score"
    ]

    X = df[features]

    # -----------------------------------
    # SCALE
    # -----------------------------------

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # -----------------------------------
    # MODEL
    # -----------------------------------

    model = IsolationForest(

        n_estimators=200,

        contamination=0.1,

        random_state=42
    )

    model.fit(X_scaled)

    # -----------------------------------
    # PREDICTIONS
    # -----------------------------------

    df["anomaly_label"] = (

        model.predict(X_scaled)
    )

    df["anomaly_score"] = (

        model.decision_function(
            X_scaled
        )
    )

    # -----------------------------------
    # LABEL MAPPING
    # -----------------------------------

    df["anomaly_label"] = (

        df["anomaly_label"]

        .map({

            1: "Normal",

            -1: "Anomaly"
        })
    )

    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    df = df.sort_values(
        by="period"
    )

    return df