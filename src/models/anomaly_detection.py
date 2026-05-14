import os
import pandas as pd

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
# LOAD DATA
# -----------------------------------

data_path = (
    "data/processed/"
    "mirror_analysis_all_years.csv"
)

df = pd.read_csv(
    data_path
)

print(
    "\nLoaded Dataset:\n"
)

print(df)

# -----------------------------------
# FEATURES
# -----------------------------------

features = [

    "india_import_value",

    "china_export_value",

    "trade_gap",

    "mismatch_percent"
]

X = df[features]

# -----------------------------------
# SCALE FEATURES
# -----------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# -----------------------------------
# ISOLATION FOREST
# -----------------------------------

model = IsolationForest(

    n_estimators=100,

    contamination=0.2,

    random_state=42
)

model.fit(X_scaled)

# -----------------------------------
# PREDICTIONS
# -----------------------------------

df["anomaly_label"] = model.predict(
    X_scaled
)

df["anomaly_score"] = model.decision_function(
    X_scaled
)

# -----------------------------------
# LABEL CONVERSION
# -----------------------------------

df["anomaly_label"] = df[
    "anomaly_label"
].map({

    1: "Normal",

    -1: "Anomaly"
})

# -----------------------------------
# SORT BY SCORE
# -----------------------------------

df = df.sort_values(
    by="anomaly_score"
)

# -----------------------------------
# OUTPUT
# -----------------------------------

print(
    "\nTrade Anomaly Detection Results:\n"
)

print(

    df[
        [
            "year",

            "trade_gap",

            "mismatch_percent",

            "anomaly_label",

            "anomaly_score"
        ]
    ]
)

# -----------------------------------
# SAVE RESULTS
# -----------------------------------

os.makedirs(
    "data/results",
    exist_ok=True
)

output_path = (
    "data/results/"
    "trade_anomaly_results.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nSaved results to:\n"
    f"{output_path}"
)