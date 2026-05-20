import requests
import json

# ===================================
# BASE URL
# ===================================

BASE_URL = (
    "https://api.imf.org/external/sdmx/3.0"
)

# ===================================
# ER DATASET STRUCTURE
# ===================================

url = (

    f"{BASE_URL}"

    f"/structure/datastructure/"

    f"IMF.STA/"

    f"DSD_ER_PUB/"
    
    f"4.0.0"
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
# JSON RESPONSE
# ===================================

data = response.json()

# ===================================
# SAVE STRUCTURE
# ===================================

with open(

    "data/api_specs/"
    "er_structure.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(
        data,
        f,
        indent=4
    )

print(
    "\nSaved ER structure."
)