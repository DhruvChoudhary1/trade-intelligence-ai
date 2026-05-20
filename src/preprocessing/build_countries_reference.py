import pandas as pd
import os

# ===================================
# LOAD SOURCE DATA
# ===================================

reporter_df = pd.read_csv(
    "data/reference/reporter_countries.csv"
)

# ===================================
# KEEP REQUIRED COLUMNS
# ===================================

countries_df = reporter_df[[
    "reporterCode",
    "reporterDesc",
    "reporterCodeIsoAlpha2",
    "reporterCodeIsoAlpha3"
]].copy()

# ===================================
# RENAME COLUMNS
# ===================================

countries_df = countries_df.rename(columns={

    "reporterCode": "comtrade_code",

    "reporterDesc": "country_name",

    "reporterCodeIsoAlpha2": "iso2",

    "reporterCodeIsoAlpha3": "iso3"
})

# ===================================
# CLEAN DATA
# ===================================
countries_df["country_name"] = (

    countries_df["country_name"]

    .astype(str)

    .str.strip()
)

countries_df["iso2"] = (

    countries_df["iso2"]

    .astype(str)

    .str.strip()
)
countries_df["iso3"] = (

    countries_df["iso3"]

    .astype(str)

    .str.strip()
)

countries_df["comtrade_code"] = (

    countries_df["comtrade_code"]

    .astype(str)

    .str.strip()
)

# ===================================
# REMOVE EMPTY ISO3
# ===================================
countries_df = countries_df[

    countries_df["iso3"] != ""
]

# ===================================
# REMOVE DUPLICATES
# ===================================

countries_df = countries_df.drop_duplicates(

    subset=["country_name"]
)

# ===================================
# SORT
# ===================================

countries_df = countries_df.sort_values(

    by="country_name"
)

# ===================================
# OUTPUT DIRECTORY
# ===================================

os.makedirs(
    "data/reference",
    exist_ok=True
)

# ===================================
# SAVE FILE
# ===================================

output_path = (
    "data/reference/countries.csv"
)

countries_df.to_csv(

    output_path,

    index=False
)

# ===================================
# FINAL INFO
# ===================================

print("\nMaster country dataset created.\n")

print(countries_df.head())

print(
    f"\nSaved to:\n{output_path}"
)