import requests
import json

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# DATAFLOW URL
# ===================================

url = (

    f"{BASE_URL}"

    f"/structure/dataflow/"

    f"IMF.STA/"

    f"ER"
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
# RAW RESPONSE
# ===================================

print(
    "\nResponse Preview:\n"
)

print(
    response.text[:5000]
)

# ===================================
# SAVE JSON
# ===================================

try:

    data = response.json()

    with open(

        "data/api_specs/"
        "er_dataflow.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    print(
        "\nSaved er_dataflow.json"
    )

except Exception as e:

    print(
        f"\nJSON Parse Error: {e}"
    )