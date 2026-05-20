import requests
import pandas as pd
import json

# ===================================
# IMF SDMX 3.0 API
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# FETCH EXCHANGE RATE DATA
# ===================================

def fetch_exchange_rates(

    country_iso3,

    start_year,

    end_year,

    frequency="M"
):

    """
    Fetch IMF Exchange Rate Data

    Parameters
    ----------
    country_iso3 : str
        Example:
        IND, JPN, CHN

    start_year : int

    end_year : int

    frequency : str
        M = Monthly
        A = Annual
    """

    # ===================================
    # DATAFLOW CONFIG
    # ===================================

    context = "dataflow"

    agency_id = "IMF.STA"

    resource_id = "ER"

    version = "4.0.1"

    # ===================================
    # INDICATOR
    # ===================================

    # USD per domestic currency

    indicator = "USD_XDC"

    # ===================================
    # TRANSFORMATION
    # ===================================

    # Period Average Rate

    transformation = "PA_RT"

    # ===================================
    # DIMENSION ORDER
    # ===================================

    # COUNTRY
    # INDICATOR
    # TYPE_OF_TRANSFORMATION
    # FREQUENCY

    key = (

        f"{country_iso3}."

        f"{indicator}."

        f"{transformation}."

        f"{frequency}"
    )

    # ===================================
    # FINAL URL
    # ===================================

    url = (

        f"{BASE_URL}"

        f"/data/"

        f"{context}/"

        f"{agency_id}/"

        f"{resource_id}/"

        f"{version}/"

        f"{key}"
    )

    # ===================================
    # PARAMETERS
    # ===================================

    params = {

        "startPeriod":
            str(start_year),

        "endPeriod":
            str(end_year)
    }

    # ===================================
    # DEBUG INFO
    # ===================================

    print(
        "\nFINAL IMF URL:\n"
    )

    print(url)

    print(
        "\nSDMX KEY:\n"
    )

    print(key)

    print(
        "\nPARAMETERS:\n"
    )

    print(params)

    # ===================================
    # REQUEST
    # ===================================

    try:

        response = requests.get(

            url,

            params=params,

            timeout=120
        )

        # ===================================
        # STATUS
        # ===================================

        print(
            f"\nStatus Code: "
            f"{response.status_code}"
        )

        # ===================================
        # API ERROR
        # ===================================

        if response.status_code != 200:

            print(
                "\nAPI Error:\n"
            )

            print(response.text)

            return pd.DataFrame()

        # ===================================
        # JSON RESPONSE
        # ===================================

        data = response.json()

        # ===================================
        # SAVE RAW RESPONSE
        # ===================================

        with open(

            "data/api_specs/"
            "imf_exchange_response.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4
            )

        print(
            "\nSaved raw IMF response."
        )

        # ===================================
        # DATASETS
        # ===================================

        datasets = (

            data["data"]
            ["dataSets"]
        )

        # ===================================
        # CHECK SERIES
        # ===================================

        if (
            "series"
            not in datasets[0]
        ):

            print(
                "\nNo series data found."
            )

            return pd.DataFrame()

        # ===================================
        # STRUCTURES
        # ===================================

        structures = (

            data["data"]
            ["structures"]
        )

        # ===================================
        # TIME VALUES
        # ===================================

        time_values = (

            structures[0]

            ["dimensions"]

            ["observation"][0]

            ["values"]
        )

        # ===================================
        # SERIES
        # ===================================

        series = datasets[0]["series"]

        observations = []

        # ===================================
        # LOOP THROUGH SERIES
        # ===================================

        for (

            series_key,

            series_data

        ) in series.items():

            # -----------------------------------
            # OBSERVATIONS
            # -----------------------------------

            obs = series_data[
                "observations"
            ]

            # -----------------------------------
            # LOOP OBS
            # -----------------------------------

            for (

                time_index,

                value

            ) in obs.items():

                # -----------------------------------
                # SAFE TIME EXTRACTION
                # -----------------------------------

                raw_time = (

                    time_values[
                        int(time_index)
                    ]
                )

                # IMF may return:
                # {"id": "..."}
                # OR plain strings

                if isinstance(
                    raw_time,
                    dict
                ):

                    # IMF sometimes stores:
                    # {"value": "1957-M01"}

                    period = (

                        raw_time.get("id")

                        or raw_time.get("value")

                        or str(raw_time)
                    )

                else:

                    period = str(raw_time)

                # -----------------------------------
                # EXCHANGE RATE
                # -----------------------------------

                exchange_rate = float(
                    value[0]
                )

                observations.append({

                    "period":
                        period,

                    "exchange_rate":
                        exchange_rate
                })

        # ===================================
        # DATAFRAME
        # ===================================

        df = pd.DataFrame(
            observations
        )

        # ===================================
        # SORT
        # ===================================

        if not df.empty:

            df = df.sort_values(
                by="period"
            )
        
        # ===================================
        # FILTER YEARS
        # ===================================

        df = df[
            df["period"] >= f"{start_year}-M01"
        ]

        return df

    # ===================================
    # REQUEST ERROR
    # ===================================

    except Exception as e:

        print(
            f"\nRequest Error: {e}"
        )

        return pd.DataFrame()

# ===================================
# TEST
# ===================================

if __name__ == "__main__":

    df = fetch_exchange_rates(

        country_iso3="IND",

        start_year=2020,

        end_year=2024,

        frequency="M"
    )

    print(
        "\nExchange Rate Data:\n"
    )

    print(df.head())

    print(
        f"\nTotal Rows: {len(df)}"
    )