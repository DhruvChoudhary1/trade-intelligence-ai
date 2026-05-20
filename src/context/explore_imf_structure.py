import requests
import json

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# STRUCTURE ENDPOINT
# ===================================

url = (

    f"{BASE_URL}"
    f"/structure/dataflow"
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
# RESPONSE
# ===================================

data = response.json()

# ===================================
# SAVE RAW RESPONSE
# ===================================

with open(

    "data/api_specs/"
    "imf_dataflows.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(
        data,
        f,
        indent=4
    )

print(
    "\nSaved IMF dataflows."
)