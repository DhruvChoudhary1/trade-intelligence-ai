import os
import pandas as pd

from comtrade_client import fetch_trade_data

# -----------------------------------
# DISPLAY SETTINGS
# -----------------------------------

pd.set_option(
    'display.float_format',
    '{:,.2f}'.format
)

# -----------------------------------
# CONFIGURATION
# -----------------------------------

IMPORTING_COUNTRY = "India"

EXPORTING_COUNTRY = "China"

HS_CODE = "8517"

YEARS = [
    "2020",
    "2021",
    "2022",
    "2023",
    "2024"
]

# -----------------------------------
# RESULTS STORAGE
# -----------------------------------

results = []

# -----------------------------------
# PROCESS EACH YEAR
# -----------------------------------

for year in YEARS:

    print(
        f"\n{'=' * 50}"
    )

    print(
        f"\nProcessing Year: {year}\n"
    )

    # -----------------------------------
    # FETCH IMPORT DATA
    # -----------------------------------

    imports_df = fetch_trade_data(

        reporter_country=IMPORTING_COUNTRY,

        partner_country=EXPORTING_COUNTRY,

        period=year,

        flow_code="M",

        cmd_code=HS_CODE,

        freq_code="A"
    )

    # -----------------------------------
    # FETCH EXPORT DATA
    # -----------------------------------

    exports_df = fetch_trade_data(

        reporter_country=EXPORTING_COUNTRY,

        partner_country=IMPORTING_COUNTRY,

        period=year,

        flow_code="X",

        cmd_code=HS_CODE,

        freq_code="A"
    )

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if (
        imports_df is None
        or imports_df.empty
        or exports_df is None
        or exports_df.empty
    ):

        print(
            f"\nSkipping {year} "
            f"due to missing data."
        )

        continue

    # -----------------------------------
    # EXTRACT VALUES
    # -----------------------------------

    india_import_value = float(

        imports_df.iloc[0][
            "primaryValue"
        ]
    )

    china_export_value = float(

        exports_df.iloc[0][
            "primaryValue"
        ]
    )

    # -----------------------------------
    # COMPUTE TRADE GAP
    # -----------------------------------

    trade_gap = (

        india_import_value
        -
        china_export_value
    )

    # -----------------------------------
    # SYMMETRIC MISMATCH %
    # -----------------------------------

    mismatch_percent = (

        abs(trade_gap)

        /

        (
            (
                india_import_value
                +
                china_export_value
            ) / 2
        )

    ) * 100

    # -----------------------------------
    # PRINT VALUES
    # -----------------------------------

    print(
        f"India Imports: "
        f"{india_import_value:,.2f}"
    )

    print(
        f"China Exports: "
        f"{china_export_value:,.2f}"
    )

    print(
        f"Trade Gap: "
        f"{trade_gap:,.2f}"
    )

    print(
        f"Mismatch %: "
        f"{mismatch_percent:.2f}%"
    )

    # -----------------------------------
    # STORE RESULTS
    # -----------------------------------

    results.append({

        "year": int(year),

        "hs_code": HS_CODE,

        "importing_country":
            IMPORTING_COUNTRY,

        "exporting_country":
            EXPORTING_COUNTRY,

        "india_import_value":
            india_import_value,

        "china_export_value":
            china_export_value,

        "trade_gap":
            trade_gap,

        "mismatch_percent":
            mismatch_percent
    })

# -----------------------------------
# CREATE FINAL DATAFRAME
# -----------------------------------

mirror_df = pd.DataFrame(
    results
)

# -----------------------------------
# SAVE OUTPUT
# -----------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)

output_path = (

    "data/processed/"
    "mirror_analysis_all_years.csv"
)

mirror_df.to_csv(
    output_path,
    index=False
)

# -----------------------------------
# FINAL OUTPUT
# -----------------------------------

print(
    f"\n{'=' * 50}"
)

print(
    "\nFINAL MULTI-YEAR ANALYSIS:\n"
)

print(mirror_df)

print(
    f"\nSaved dataset to:\n"
    f"{output_path}"
)