import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# LOAD ANOMALY RESULTS
# -----------------------------------

df = pd.read_csv(
    "data/processed/anomaly_results.csv"
)

# -----------------------------------
# CREATE FIGURE
# -----------------------------------

plt.figure(figsize=(12, 6))

# -----------------------------------
# PLOT MISMATCH PERCENTAGE
# -----------------------------------

normal_data = df[df["anomaly_label"] == "Normal"]
anomaly_data = df[df["anomaly_label"] == "Anomaly"]

# Plot normal years
plt.plot(
    normal_data["refYear"],
    normal_data["mismatch_percent"],
    marker="o",
    linewidth=2,
    label="Normal"
)

# Plot anomaly years
plt.scatter(
    anomaly_data["refYear"],
    anomaly_data["mismatch_percent"],
    s=200,
    marker="X",
    label="Anomaly"
)

# -----------------------------------
# ADD LABELS
# -----------------------------------

for _, row in df.iterrows():

    plt.text(
        row["refYear"],
        row["mismatch_percent"] + 1,
        f'{row["mismatch_percent"]:.1f}%',
        ha="center"
    )

# -----------------------------------
# CHART FORMATTING
# -----------------------------------

plt.title(
    "India-China Trade Mismatch Analysis (HS 8517)",
    fontsize=16
)

plt.xlabel("Year", fontsize=12)

plt.ylabel("Mismatch Percentage", fontsize=12)

plt.xticks(df["refYear"])

plt.grid(True)

plt.legend()

# -----------------------------------
# SAVE PLOT
# -----------------------------------

plt.savefig(
    "data/processed/trade_mismatch_plot.png",
    bbox_inches="tight"
)

# -----------------------------------
# SHOW PLOT
# -----------------------------------

plt.show()

print("\nVisualization Complete.")