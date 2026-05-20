import requests
import json

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# CODELIST ENDPOINT
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
# JSON
# ===================================

data = response.json()

# ===================================
# SAVE
# ===================================

with open(

    "data/api_specs/"
    "er_codelists.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(
        data,
        f,
        indent=4
    )

print(
    "\nSaved codelists."
)