import pandas as pd

# -----------------------------------
# LOAD COUNTRY FILES
# -----------------------------------

reporter_df = pd.read_csv(
    "data/reference/reporter_countries.csv"
)

partner_df = pd.read_csv(
    "data/reference/partner_countries.csv"
)

# -----------------------------------
# NORMALIZE NAMES
# -----------------------------------

reporter_df["text"] = (
    reporter_df["text"]
    .str.strip()
    .str.lower()
)

partner_df["text"] = (
    partner_df["text"]
    .str.strip()
    .str.lower()
)

# -----------------------------------
# COUNTRY LOOKUP
# -----------------------------------

def get_country_code(country_name):

    country_name = (
        country_name
        .strip()
        .lower()
    )

    # -----------------------------
    # SEARCH REPORTER FILE
    # -----------------------------

    reporter_match = reporter_df[

        reporter_df["text"]
        == country_name
    ]

    if not reporter_match.empty:

        return str(
            reporter_match.iloc[0]["id"]
        )

    # -----------------------------
    # SEARCH PARTNER FILE
    # -----------------------------

    partner_match = partner_df[

        partner_df["text"]
        == country_name
    ]

    if not partner_match.empty:

        return str(
            partner_match.iloc[0]["id"]
        )

    return None