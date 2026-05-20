import pandas as pd

# ===================================
# LOAD MASTER COUNTRY DATASET
# ===================================

countries_df = pd.read_csv(
    "data/reference/countries.csv"
)

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
# GET COMTRADE CODE
# ===================================

def get_country_code(
    country_name
):

    country_name = (

        country_name

        .strip()

        .lower()
    )

    match = countries_df[

        countries_df["country_name"]

        .str.lower()

        == country_name
    ]

    if not match.empty:

        return str(
            match.iloc[0][
                "comtrade_code"
            ]
        )

    return None

# ===================================
# GET ISO3 CODE
# ===================================

def get_country_iso3(
    country_name
):

    country_name = (

        country_name

        .strip()

        .lower()
    )

    match = countries_df[

        countries_df["country_name"]

        .str.lower()

        == country_name
    ]

    if not match.empty:

        return str(
            match.iloc[0][
                "iso3"
            ]
        )

    return None

# ===================================
# GET ISO2 CODE
# ===================================

def get_country_iso2(
    country_name
):

    country_name = (

        country_name

        .strip()

        .lower()
    )

    match = countries_df[

        countries_df["country_name"]

        .str.lower()

        == country_name
    ]

    if not match.empty:

        return str(
            match.iloc[0][
                "iso2"
            ]
        )

    return None

# ===================================
# GET COUNTRY NAME
# ===================================

def get_country_name(
    comtrade_code
):

    comtrade_code = str(
        comtrade_code
    ).strip()

    match = countries_df[

        countries_df["comtrade_code"]
        == comtrade_code
    ]

    if not match.empty:

        return str(
            match.iloc[0][
                "country_name"
            ]
        )

    return None

# ===================================
# GET ALL COUNTRY OPTIONS
# ===================================

def get_all_country_options():

    return sorted(

        countries_df[
            "country_name"
        ].unique()
    )

# ===================================
# GET COUNTRY RECORD
# ===================================

def get_country_record(
    country_name
):

    country_name = (

        country_name

        .strip()

        .lower()
    )

    match = countries_df[

        countries_df["country_name"]

        .str.lower()

        == country_name
    ]

    if not match.empty:

        return (
            match.iloc[0]
            .to_dict()
        )

    return None