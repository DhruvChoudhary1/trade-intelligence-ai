import requests
import json

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# GET ALL IMF.STA CODELISTS
# ===================================

url = (

    f"{BASE_URL}"

    f"/structure/codelist/"

    f"IMF.STA"
)

# ===================================
# REQUEST
# ===================================

response = requests.get(url)

print(
    f"\nStatus Code: "
    f"{response.status_code}"
)

# ===================================
# CHECK RESPONSE
# ===================================

if response.status_code != 200:

    print(
        "\nRequest Failed"
    )

    print(response.text)

    exit()

# ===================================
# PARSE JSON
# ===================================

data = response.json()

# ===================================
# SAVE JSON FILE
# ===================================

output_path = (

    "data/api_specs/"
    "all_imf_codelists.json"
)

with open(

    output_path,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        data,

        f,

        indent=4,

        ensure_ascii=False
    )

# ===================================
# SUCCESS
# ===================================

print(
    "\nSaved JSON file:"
)

print(output_path)

# ===================================
# OPTIONAL:
# PRINT NUMBER OF CODELISTS
# ===================================

try:

    codelists = (

        data["data"]
        ["codelists"]
    )

    print(
        f"\nTotal Codelists: "
        f"{len(codelists)}"
    )

except Exception as e:

    print(
        f"\nCould not count "
        f"codelists: {e}"
    )