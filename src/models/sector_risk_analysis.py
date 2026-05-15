import os
import pandas as pd
import numpy as np

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
    "data/results/"
    "trade_anomalies_results.csv"
)

df = pd.read_csv(
    data_path
)

print(
    "\nLoaded Dataset:\n"
)

print(df.head())

# -----------------------------------
# GROUP BY SECTOR
# -----------------------------------

sector_stats = (

    df.groupby(
        ["hs_code", "sector"]
    )

    .agg({

        "mismatch_percent": [

            "mean",
            "max",
            "std"
        ],

        "trade_gap": [

            "mean"
        ],

        "anomaly_label": [

            lambda x:
            (x == "Anomaly").sum(),

            lambda x:
            (
                (x == "Anomaly").sum()
                / len(x)
            )
        ]
    })
)

# -----------------------------------
# FLATTEN COLUMNS
# -----------------------------------

sector_stats.columns = [

    "avg_mismatch",

    "max_mismatch",

    "volatility",

    "avg_trade_gap",

    "anomaly_count",

    "anomaly_frequency"
]

sector_stats = (
    sector_stats
    .reset_index()
)

# -----------------------------------
# HANDLE NaN VOLATILITY
# -----------------------------------

sector_stats[
    "volatility"
] = (

    sector_stats[
        "volatility"
    ]

    .fillna(0)
)

# -----------------------------------
# NORMALIZATION
# -----------------------------------

def normalize(series):

    return (

        (
            series
            -
            series.min()
        )

        /

        (
            series.max()
            -
            series.min()
        )
    )

sector_stats[
    "norm_mismatch"
] = normalize(

    sector_stats[
        "avg_mismatch"
    ]
)

sector_stats[
    "norm_volatility"
] = normalize(

    sector_stats[
        "volatility"
    ]
)

sector_stats[
    "norm_anomaly_freq"
] = normalize(

    sector_stats[
        "anomaly_frequency"
    ]
)

# -----------------------------------
# RISK SCORE
# -----------------------------------

sector_stats[
    "risk_score"
] = (

    0.4
    *
    sector_stats[
        "norm_mismatch"
    ]

    +

    0.3
    *
    sector_stats[
        "norm_volatility"
    ]

    +

    0.3
    *
    sector_stats[
        "norm_anomaly_freq"
    ]
)

# -----------------------------------
# RISK LEVELS
# -----------------------------------

def classify_risk(score):

    if score >= 0.75:

        return "Critical"

    elif score >= 0.5:

        return "High"

    elif score >= 0.25:

        return "Medium"

    else:

        return "Low"

sector_stats[
    "risk_level"
] = sector_stats[
    "risk_score"
].apply(classify_risk)

# -----------------------------------
# SORT
# -----------------------------------

sector_stats = sector_stats.sort_values(

    by="risk_score",

    ascending=False
)

# -----------------------------------
# OUTPUT
# -----------------------------------

print(
    "\nSector Risk Intelligence:\n"
)

print(

    sector_stats[
        [
            "hs_code",

            "sector",

            "avg_mismatch",

            "volatility",

            "anomaly_frequency",

            "risk_score",

            "risk_level"
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
    "sector_risk_analysis.csv"
)

sector_stats.to_csv(

    output_path,

    index=False
)

# -----------------------------------
# FINAL MESSAGE
# -----------------------------------

print(
    f"\nSaved results to:\n"
    f"{output_path}"
)