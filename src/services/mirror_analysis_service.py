import pandas as pd

from src.data_collection.comtrade_client import (
    fetch_trade_data
)

# -----------------------------------
# DISPLAY SETTINGS
# -----------------------------------

pd.set_option(
    'display.float_format',
    '{:,.2f}'.format
)

# -----------------------------------
# MAIN SERVICE
# -----------------------------------

def run_mirror_analysis(

    reporter_country,

    partner_country,

    hs_code,

    start_year,

    end_year,

    frequency="M"
):

    results = []

    # -----------------------------------
    # GENERATE PERIODS
    # -----------------------------------

    periods = []

    if frequency == "A":

        for year in range(
            start_year,
            end_year + 1
        ):

            periods.append(
                str(year)
            )

    else:

        for year in range(
            start_year,
            end_year + 1
        ):

            for month in range(1, 13):

                period = (
                    f"{year}"
                    f"{month:02d}"
                )

                periods.append(
                    period
                )

    # -----------------------------------
    # PROCESS EACH PERIOD
    # -----------------------------------

    for period in periods:

        try:

            print(
                f"Processing: {period}"
            )

            # -----------------------------
            # IMPORTS
            # -----------------------------

            imports_df = fetch_trade_data(

                reporter_country=
                    reporter_country,

                partner_country=
                    partner_country,

                period=period,

                flow_code="M",

                cmd_code=hs_code,

                freq_code=frequency
            )

            # -----------------------------
            # EXPORTS
            # -----------------------------

            exports_df = fetch_trade_data(

                reporter_country=
                    partner_country,

                partner_country=
                    reporter_country,

                period=period,

                flow_code="X",

                cmd_code=hs_code,

                freq_code=frequency
            )

            # -----------------------------
            # VALIDATION
            # -----------------------------

            if (
                imports_df is None
                or imports_df.empty
                or exports_df is None
                or exports_df.empty
            ):

                continue

            # -----------------------------
            # VALUES
            # -----------------------------

            import_value = float(

                imports_df.iloc[0][
                    "primaryValue"
                ]
            )

            export_value = float(

                exports_df.iloc[0][
                    "primaryValue"
                ]
            )

            # -----------------------------
            # GAP
            # -----------------------------

            trade_gap = (
                import_value
                -
                export_value
            )

            # -----------------------------
            # SYMMETRIC MISMATCH
            # -----------------------------

            mismatch_percent = (

                abs(trade_gap)

                /

                (
                    (
                        import_value
                        +
                        export_value
                    ) / 2
                )

            ) * 100

            # -----------------------------
            # STORE
            # -----------------------------

            results.append({

                "period": period,

                "hs_code": hs_code,

                "reporter_country":
                    reporter_country,

                "partner_country":
                    partner_country,

                "import_value":
                    import_value,

                "export_value":
                    export_value,

                "trade_gap":
                    trade_gap,

                "mismatch_percent":
                    mismatch_percent
            })

        except Exception as e:

            print(
                f"Error on {period}: {e}"
            )

    # -----------------------------------
    # FINAL DATAFRAME
    # -----------------------------------

    df = pd.DataFrame(
        results
    )

    return df