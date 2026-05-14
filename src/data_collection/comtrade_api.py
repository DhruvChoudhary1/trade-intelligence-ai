import requests
import pandas as pd

# -----------------------------------
# BASE URL
# -----------------------------------

BASE_URL = (
    "https://comtradeapi.un.org/public/v1/preview"
)

# -----------------------------------
# FETCH TRADE DATA
# -----------------------------------

def get_trade_data(
    reporter_code,
    partner_code,
    flow_code,
    cmd_code,
    period,
    partner2_code="0",
    type_code="C",
    freq_code="A",
    cl_code="HS"
):

    # Build endpoint URL
    url = (
        f"{BASE_URL}/"
        f"{type_code}/"
        f"{freq_code}/"
        f"{cl_code}"
    )

    # Query parameters
    params = {
        "reporterCode": reporter_code,
        "partnerCode": partner_code,
        "partner2Code": partner2_code,
        "flowCode": flow_code,
        "cmdCode": cmd_code,
        "period": period
    }

    # API request
    response = requests.get(
        url,
        params=params
    )

    # -----------------------------------
    # ERROR HANDLING
    # -----------------------------------

    if response.status_code != 200:

        print(
            f"\nAPI Error: {response.status_code}"
        )

        print(response.text)

        return None

    # Convert response to JSON
    data = response.json()

    return data

# -----------------------------------
# JSON TO DATAFRAME
# -----------------------------------

def json_to_dataframe(data):

    if data is None:
        return None

    # Check if data exists
    if "data" not in data:

        print("\nNo trade data returned.")

        print("\nFull Response:\n")

        print(data)

        return None

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data["data"])

    return df

# -----------------------------------
# SAVE DATAFRAME
# -----------------------------------

def save_dataframe(df, filename):

    if df is None:
        return

    path = f"data/raw/{filename}"

    df.to_csv(
        path,
        index=False
    )

    print(f"\nSaved dataset to: {path}")

# -----------------------------------
# MAIN TEST
# -----------------------------------

if __name__ == "__main__":

    print("\nFetching India Imports From China...\n")

    # India imports from China
    india_imports_json = get_trade_data(
        reporter_code="356",   # India
        partner_code="156",    # China
        flow_code="M",         # Imports
        cmd_code="8517",
        period="2024"
    )

    india_imports_df = json_to_dataframe(
        india_imports_json
    )

    if india_imports_df is not None:

        print("\nIndia Imports Data Retrieved:\n")

        print(india_imports_df.head())

        print("\nColumns:\n")

        print(india_imports_df.columns)

        # Save CSV
        save_dataframe(
            india_imports_df,
            "india_imports_api.csv"
        )

    print("\nFetching China Exports To India...\n")

    # China exports to India
    china_exports_json = get_trade_data(
        reporter_code="156",   # China
        partner_code="356",    # India
        flow_code="X",         # Exports
        cmd_code="8517",
        period="2024"
    )

    china_exports_df = json_to_dataframe(
        china_exports_json
    )

    if china_exports_df is not None:

        print("\nChina Exports Data Retrieved:\n")

        print(china_exports_df.head())

        print("\nColumns:\n")

        print(china_exports_df.columns)

        # Save CSV
        save_dataframe(
            china_exports_df,
            "china_exports_api.csv"
        )

    print("\nAPI Trade Data Collection Complete.")