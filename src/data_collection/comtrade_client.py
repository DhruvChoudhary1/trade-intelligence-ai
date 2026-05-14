import comtradeapicall
import pandas as pd
import os

from dotenv import load_dotenv

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

SUBSCRIPTION_KEY = os.getenv(
    "COMTRADE_API_KEY"
)

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
# FETCH TRADE DATA
# -----------------------------------

def fetch_trade_data(
    reporter_country,
    partner_country,
    period,
    flow_code,
    cmd_code,
    freq_code="A"
):

    reporter_code = get_reporter_code(
        reporter_country
    )

    partner_code = get_partner_code(
        partner_country
    )

    print(
        f"\nReporter Code: "
        f"{reporter_code}"
    )

    print(
        f"Partner Code: "
        f"{partner_code}"
    )

    # -----------------------------------
    # API CALL
    # -----------------------------------

    df = comtradeapicall.getFinalData(

        SUBSCRIPTION_KEY,

        typeCode='C',

        freqCode=freq_code,

        clCode='HS',

        period=period,

        reporterCode=reporter_code,

        cmdCode=cmd_code,

        flowCode=flow_code,

        partnerCode=partner_code,

        partner2Code=None,

        customsCode=None,

        motCode=None,

        maxRecords=2500,

        format_output='JSON',

        aggregateBy=None,

        breakdownMode='classic',

        countOnly=None,

        includeDesc=True
    )

    return df

# -----------------------------------
# MAIN TEST
# -----------------------------------

if __name__ == "__main__":

    print(
        "\nFetching Trade Data...\n"
    )

    # China exports to India
    df = fetch_trade_data(

        reporter_country="China",

        partner_country="India",

        period="2024",

        flow_code="X",

        cmd_code="8517",

        freq_code="A"
    )

    # -----------------------------------
    # CHECK RESULT
    # -----------------------------------

    if df is None or df.empty:

        print(
            "\nNo trade data retrieved."
        )

    else:

        print(
            "\nTrade Data Retrieved:\n"
        )

        print(df.head())

        print(
            f"\nDataset Shape: "
            f"{df.shape}"
        )

        print(
            "\nColumns:\n"
        )

        print(df.columns)

        # -----------------------------------
        # SAVE CSV
        # -----------------------------------

        os.makedirs(
            "data/raw",
            exist_ok=True
        )

        output_path = (
            "data/raw/"
            "china_exports_2024.csv"
        )

        df.to_csv(
            output_path,
            index=False
        )

        print(
            f"\nSaved dataset to:\n"
            f"{output_path}"
        )

        