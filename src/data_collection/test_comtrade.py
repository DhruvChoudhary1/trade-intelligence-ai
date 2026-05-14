import comtradeapicall
import pandas as pd

# -----------------------------------
# FETCH SIMPLE TEST DATA
# -----------------------------------

df = comtradeapicall.previewFinalData(
    typeCode='C',
    freqCode='A',
    clCode='HS',

    period='2024',

    reporterCode='356',

    flowCode='M',

    partnerCode='156',

    cmdCode='TOTAL',

    partner2Code=None,
    customsCode=None,
    motCode=None,

    maxRecords=50,

    format_output='JSON',

    aggregateBy=None,

    breakdownMode='classic',

    countOnly=None,

    includeDesc=False
)

# -----------------------------------
# CHECK RESULT
# -----------------------------------

if df is None:

    print("\nNo data returned.")

else:

    print("\nTrade Data Retrieved:\n")

    print(df.head())

    print("\nColumns:\n")

    print(df.columns)