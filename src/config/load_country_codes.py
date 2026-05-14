import pandas as pd

# -----------------------------------
# LOAD COUNTRY TABLES
# -----------------------------------

reporters_df = pd.read_csv(
    "data/reference/reporter_countries.csv"
)

partners_df = pd.read_csv(
    "data/reference/partner_countries.csv"
)

# -----------------------------------
# COUNTRY LOOKUP FUNCTIONS
# -----------------------------------

def get_reporter_code(country_name):

    result = reporters_df[
        reporters_df["text"]
        .str.lower()
        == country_name.lower()
    ]

    if result.empty:

        return None

    return str(
        result.iloc[0]["id"]
    )

# -----------------------------------

def get_partner_code(country_name):

    result = partners_df[
        partners_df["text"]
        .str.lower()
        == country_name.lower()
    ]

    if result.empty:

        return None

    return str(
        result.iloc[0]["id"]
    )

# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    india_reporter = get_reporter_code(
        "India"
    )

    china_partner = get_partner_code(
        "China"
    )

    print(
        f"\nIndia Reporter Code: "
        f"{india_reporter}"
    )

    print(
        f"China Partner Code: "
        f"{china_partner}"
    )