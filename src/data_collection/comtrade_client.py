import requests
import pandas as pd
import os
from dotenv import load_dotenv

# ===================================
# LOAD ENV VARIABLES
# ===================================

load_dotenv()

SUBSCRIPTION_KEY = os.getenv(
    "COMTRADE_API_KEY"
)

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://comtradeapi.un.org"
)

# ===================================
# FETCH TRADE DATA
# ===================================

def fetch_trade_data(

    reporter_code,

    partner_code,

    period,

    flow_code,

    cmd_code,

    freq_code="M",

    cl_code="HS"
):

    # -----------------------------------
    # API ENDPOINT
    # -----------------------------------

    endpoint = (

        f"{BASE_URL}"
        f"/data/v1/get/"
        f"C/"
        f"{freq_code}/"
        f"{cl_code}"
    )

    # -----------------------------------
    # PARAMETERS
    # -----------------------------------

    params = {

        "reporterCode":
            reporter_code,

        "partnerCode":
            partner_code,

        "period":
            period,

        "cmdCode":
            cmd_code,

        "flowCode":
            flow_code,

        "includeDesc":
            True
    }

    # -----------------------------------
    # HEADERS
    # -----------------------------------

    headers = {

        "Ocp-Apim-Subscription-Key":
            SUBSCRIPTION_KEY
    }

    # -----------------------------------
    # DEBUG LOGGING
    # -----------------------------------

    print(
        f"\nReporter Code: "
        f"{reporter_code}"
    )

    print(
        f"Partner Code: "
        f"{partner_code}"
    )

    print(
        f"Period: "
        f"{period}"
    )

    print(
        f"Flow Code: "
        f"{flow_code}"
    )

    print(
        f"Commodity Code: "
        f"{cmd_code}"
    )

    # -----------------------------------
    # REQUEST
    # -----------------------------------

    try:

        response = requests.get(

            endpoint,

            params=params,

            headers=headers,

            timeout=120
        )

        # -----------------------------------
        # STATUS
        # -----------------------------------

        print(
            f"\nStatus Code: "
            f"{response.status_code}"
        )

        # -----------------------------------
        # ERROR HANDLING
        # -----------------------------------

        if response.status_code != 200:

            print(
                "\nAPI Error:"
            )

            print(
                response.text
            )

            return pd.DataFrame()

        # -----------------------------------
        # JSON RESPONSE
        # -----------------------------------

        data = response.json()

        # -----------------------------------
        # RAW DEBUG
        # -----------------------------------

        if "data" not in data:

            print(
                "\nInvalid API response."
            )

            print(data)

            return pd.DataFrame()

        # -----------------------------------
        # EMPTY RESPONSE
        # -----------------------------------

        if len(data["data"]) == 0:

            print(
                "\nNo trade data returned."
            )

            return pd.DataFrame()

        # -----------------------------------
        # DATAFRAME
        # -----------------------------------

        df = pd.DataFrame(
            data["data"]
        )

        return df

    # -----------------------------------
    # EXCEPTION
    # -----------------------------------

    except Exception as e:

        print(
            f"\nRequest Error: {e}"
        )

        return pd.DataFrame()