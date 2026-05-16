import pandas as pd

from src.data_collection.comtrade_client import (
    fetch_trade_data
)

from src.services.country_service import (
    get_country_code
)

# ===================================
# DISPLAY SETTINGS
# ===================================

pd.set_option(
    'display.float_format',
    '{:,.2f}'.format
)

# ===================================
# MAIN MIRROR ANALYSIS SERVICE
# ===================================

def run_mirror_analysis(

    reporter_country,

    partner_country,

    hs_code,

    start_year,

    end_year,

    frequency="M"
):

    # ===================================
    # COUNTRY CODE LOOKUP
    # ===================================

    reporter_code = get_country_code(
        reporter_country
    )

    partner_code = get_country_code(
        partner_country
    )

    # ===================================
    # VALIDATION
    # ===================================

    if reporter_code is None:

        raise ValueError(

            f"Reporter country not found: "
            f"{reporter_country}"
        )

    if partner_code is None:

        raise ValueError(

            f"Partner country not found: "
            f"{partner_country}"
        )

    # ===================================
    # DEBUG INFO
    # ===================================

    print(
        f"\nReporter: "
        f"{reporter_country}"
        f" ({reporter_code})"
    )

    print(
        f"Partner: "
        f"{partner_country}"
        f" ({partner_code})"
    )

    # ===================================
    # GENERATE PERIODS
    # ===================================

    periods = []

    # -----------------------------------
    # ANNUAL
    # -----------------------------------

    if frequency == "A":

        for year in range(
            start_year,
            end_year + 1
        ):

            periods.append(
                str(year)
            )

    # -----------------------------------
    # MONTHLY
    # -----------------------------------

    else:

        for year in range(
            start_year,
            end_year + 1
        ):

            for month in range(1, 13):

                periods.append(
                    f"{year}{month:02d}"
                )

    # ===================================
    # STORAGE
    # ===================================

    results = []

    # ===================================
    # MAIN LOOP
    # ===================================

    for period in periods:

        try:

            print(
                f"\nProcessing Period: "
                f"{period}"
            )

            # ===================================
            # IMPORT DATA
            # Reporter imports from partner
            # ===================================

            imports_df = fetch_trade_data(

                reporter_code=
                    reporter_code,

                partner_code=
                    partner_code,

                period=
                    period,

                flow_code=
                    "M",

                cmd_code=
                    hs_code,

                freq_code=
                    frequency
            )

            # ===================================
            # EXPORT DATA
            # Partner exports to reporter
            # ===================================

            exports_df = fetch_trade_data(

                reporter_code=
                    partner_code,

                partner_code=
                    reporter_code,

                period=
                    period,

                flow_code=
                    "X",

                cmd_code=
                    hs_code,

                freq_code=
                    frequency
            )

            # ===================================
            # VALIDATION
            # ===================================

            if imports_df.empty:

                print(
                    "No import data."
                )

                continue

            if exports_df.empty:

                print(
                    "No export data."
                )

                continue

            # ===================================
            # EXTRACT VALUES
            # ===================================

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

            # ===================================
            # TRADE GAP
            # ===================================

            trade_gap = (

                import_value
                -
                export_value
            )

            # ===================================
            # MISMATCH %
            # Symmetric Formula
            # ===================================

            denominator = (

                (
                    import_value
                    +
                    export_value
                ) / 2
            )

            if denominator == 0:

                mismatch_percent = 0

            else:

                mismatch_percent = (

                    abs(trade_gap)

                    /

                    denominator

                ) * 100

            # ===================================
            # STORE RESULTS
            # ===================================

            results.append({

                "period":
                    period,

                "frequency":
                    frequency,

                "hs_code":
                    hs_code,

                "reporter_country":
                    reporter_country,

                "partner_country":
                    partner_country,

                "reporter_code":
                    reporter_code,

                "partner_code":
                    partner_code,

                "import_value":
                    import_value,

                "export_value":
                    export_value,

                "trade_gap":
                    trade_gap,

                "mismatch_percent":
                    mismatch_percent
            })

            # ===================================
            # DEBUG OUTPUT
            # ===================================

            print(
                f"Imports: "
                f"${import_value:,.2f}"
            )

            print(
                f"Exports: "
                f"${export_value:,.2f}"
            )

            print(
                f"Mismatch: "
                f"{mismatch_percent:.2f}%"
            )

        # ===================================
        # ERROR HANDLING
        # ===================================

        except Exception as e:

            print(
                f"Error on "
                f"{period}: {e}"
            )

    # ===================================
    # FINAL DATAFRAME
    # ===================================

    final_df = pd.DataFrame(
        results
    )

    # ===================================
    # RETURN
    # ===================================

    return final_df