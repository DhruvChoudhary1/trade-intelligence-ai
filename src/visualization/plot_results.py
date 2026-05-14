import os
import pandas as pd
import matplotlib.pyplot as plt

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

results_path = (
    "data/results/"
    "trade_anomaly_results.csv"
)

df = pd.read_csv(
    results_path
)

print(
    "\nLoaded Results:\n"
)

print(df)

# -----------------------------------
# CREATE OUTPUT DIRECTORY
# -----------------------------------

os.makedirs(
    "outputs/plots",
    exist_ok=True
)

# ===================================
# CHART 1
# IMPORTS VS EXPORTS
# ===================================

plt.figure(figsize=(10, 6))

plt.plot(

    df["year"],

    df["india_import_value"],

    marker='o',

    linewidth=2,

    label="India Imports"
)

plt.plot(

    df["year"],

    df["china_export_value"],

    marker='o',

    linewidth=2,

    label="China Exports"
)

plt.title(
    "India-China Telecom Trade"
)

plt.xlabel("Year")

plt.ylabel("Trade Value (USD)")

plt.legend()

plt.grid(True)

chart1_path = (
    "outputs/plots/"
    "imports_vs_exports.png"
)

plt.savefig(
    chart1_path,
    bbox_inches='tight'
)

plt.close()

# ===================================
# CHART 2
# MISMATCH PERCENT
# ===================================

plt.figure(figsize=(10, 6))

plt.plot(

    df["year"],

    df["mismatch_percent"],

    marker='o',

    linewidth=2
)

plt.title(
    "Mirror Trade Mismatch %"
)

plt.xlabel("Year")

plt.ylabel("Mismatch %")

plt.grid(True)

chart2_path = (
    "outputs/plots/"
    "mismatch_percent.png"
)

plt.savefig(
    chart2_path,
    bbox_inches='tight'
)

plt.close()

# ===================================
# CHART 3
# ANOMALY SCORES
# ===================================

plt.figure(figsize=(10, 6))

plt.bar(

    df["year"].astype(str),

    df["anomaly_score"]
)

plt.title(
    "Trade Anomaly Scores"
)

plt.xlabel("Year")

plt.ylabel("Anomaly Score")

plt.grid(True)

chart3_path = (
    "outputs/plots/"
    "anomaly_scores.png"
)

plt.savefig(
    chart3_path,
    bbox_inches='tight'
)

plt.close()

# ===================================
# SHOW ANOMALIES
# ===================================

anomalies = df[
    df["anomaly_label"]
    == "Anomaly"
]

print(
    "\nDetected Anomalies:\n"
)

print(

    anomalies[
        [
            "year",

            "mismatch_percent",

            "anomaly_score"
        ]
    ]
)

# ===================================
# FINAL OUTPUT
# ===================================

print(
    "\nPlots Saved:\n"
)

print(chart1_path)

print(chart2_path)

print(chart3_path)