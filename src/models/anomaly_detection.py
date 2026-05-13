import pandas as pd
from sklearn.ensemble import IsolationForest

# -----------------------------------
# LOAD PROCESSED DATA
# -----------------------------------

df = pd.read_csv(
    "data/processed/processed_trade_data.csv"
)

# -----------------------------------
# SELECT FEATURES
# -----------------------------------

features = df[
    [
        "india_import_value",
        "china_export_value",
        "trade_gap",
        "mismatch_percent"
    ]
]

# -----------------------------------
# BUILD MODEL
# -----------------------------------

model = IsolationForest(
    contamination=0.2,
    random_state=42
)

# Train model
model.fit(features)

# Predict anomalies
df["anomaly"] = model.predict(features)

# Convert labels
df["anomaly_label"] = df["anomaly"].map({
    -1: "Anomaly",
     1: "Normal"
})

# Anomaly score
df["anomaly_score"] = model.decision_function(features)

# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------

print("\nTrade Anomaly Detection Results:\n")

print(
    df[
        [
            "refYear",
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

df.to_csv(
    "data/processed/anomaly_results.csv",
    index=False
)

print("\nAnomaly Detection Complete.")