import pandas as pd
import numpy as np

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

india_imports = pd.read_csv(
    "data/raw/india_imports_8517.csv"
)

china_exports = pd.read_csv(
    "data/raw/china_exports_8517_clean.csv"
)

# -----------------------------------
# SELECT IMPORTANT COLUMNS
# -----------------------------------

columns_needed = [
    "refYear",
    "cmdCode",
    "cmdDesc",
    "qty",
    "primaryValue",
    "cifvalue",
    "fobvalue"
]

india_imports = india_imports[columns_needed]
china_exports = china_exports[columns_needed]

# -----------------------------------
# CONVERT NUMERIC COLUMNS
# -----------------------------------

numeric_cols = [
    "qty",
    "primaryValue",
    "cifvalue",
    "fobvalue"
]

for col in numeric_cols:

    india_imports[col] = pd.to_numeric(
        india_imports[col],
        errors="coerce"
    )

    china_exports[col] = pd.to_numeric(
        china_exports[col],
        errors="coerce"
    )

# -----------------------------------
# RENAME COLUMNS
# -----------------------------------

india_imports = india_imports.rename(columns={
    "qty": "india_qty",
    "primaryValue": "india_import_value",
    "cifvalue": "india_cif",
    "fobvalue": "india_fob"
})

china_exports = china_exports.rename(columns={
    "qty": "china_qty",
    "primaryValue": "china_export_value",
    "cifvalue": "china_cif",
    "fobvalue": "china_fob"
})

# -----------------------------------
# MERGE MIRROR TRADE DATA
# -----------------------------------

merged = pd.merge(
    india_imports,
    china_exports,
    on=["refYear", "cmdCode"],
    how="inner"
)

# -----------------------------------
# FEATURE ENGINEERING
# -----------------------------------

# Trade Gap
merged["trade_gap"] = (
    merged["china_export_value"] -
    merged["india_import_value"]
)

# Mismatch Percentage
merged["mismatch_percent"] = (
    abs(merged["trade_gap"]) /
    merged[
        [
            "china_export_value",
            "india_import_value"
        ]
    ].max(axis=1)
) * 100

# Safe Unit Price Calculation
merged["india_unit_price"] = np.where(
    merged["india_qty"] > 0,
    merged["india_import_value"] /
    merged["india_qty"],
    np.nan
)

merged["china_unit_price"] = np.where(
    merged["china_qty"] > 0,
    merged["china_export_value"] /
    merged["china_qty"],
    np.nan
)

# Unit Price Gap
merged["unit_price_gap"] = (
    abs(
        merged["china_unit_price"] -
        merged["india_unit_price"]
    )
)

# -----------------------------------
# SORT DATA
# -----------------------------------

merged = merged.sort_values("refYear")

# -----------------------------------
# SAVE PROCESSED DATA
# -----------------------------------

merged.to_csv(
    "data/processed/processed_trade_data.csv",
    index=False
)

# -----------------------------------
# OUTPUT RESULTS
# -----------------------------------

print("\nProcessed Dataset Shape:")
print(merged.shape)

print("\nTrade Intelligence Output:\n")

print(
    merged[
        [
            "refYear",
            "cmdCode",
            "india_import_value",
            "china_export_value",
            "trade_gap",
            "mismatch_percent"
        ]
    ]
)

print("\nProcessing Complete.")