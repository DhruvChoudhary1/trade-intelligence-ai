import pandas as pd

# ===================================
# LOAD HS DATA
# ===================================

hs_df = pd.read_csv(
    "data/reference/hs_codes.csv"
)

# ===================================
# CLEAN DATA
# ===================================

hs_df["id"] = (

    hs_df["id"]

    .astype(str)

    .str.strip()
)

hs_df["text"] = (

    hs_df["text"]

    .astype(str)

    .str.strip()
)

# ===================================
# KEEP ONLY 4-DIGIT HS CODES
# ===================================

hs_df = hs_df[
    hs_df["aggrLevel"] == 4
]

# ===================================
# GET HS CODE
# ===================================

def get_hs_code(description):

    description = (
        description
        .strip()
        .lower()
    )

    match = hs_df[

        hs_df["text"]

        .str.lower()

        == description
    ]

    if not match.empty:

        return str(
            match.iloc[0]["id"]
        )

    return None

# ===================================
# GET DESCRIPTION
# ===================================

def get_hs_description(hs_code):

    hs_code = str(hs_code)

    match = hs_df[

        hs_df["id"]
        == hs_code
    ]

    if not match.empty:

        return str(
            match.iloc[0]["text"]
        )

    return None

# ===================================
# GET ALL OPTIONS
# ===================================

def get_all_hs_options():

    options = []

    for _, row in hs_df.iterrows():

        option = (

            f"{row['id']} - "
            f"{row['text']}"
        )

        options.append(option)

    return sorted(options)

# ===================================
# EXTRACT CODE
# ===================================

def extract_hs_code(
    dropdown_value
):

    return (
        dropdown_value
        .split("-")[0]
        .strip()
    )