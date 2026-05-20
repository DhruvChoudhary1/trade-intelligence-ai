import json

# ===================================
# LOAD OPENAPI SPEC
# ===================================

with open(

    "data/api_specs/imf_openapi.json",

    "r",

    encoding="utf-8"

) as f:

    api_spec = json.load(f)

# ===================================
# PRINT BASIC INFO
# ===================================

print("\nAPI TITLE:\n")

print(
    api_spec.get("info", {})
)

# ===================================
# LIST ENDPOINTS
# ===================================

print("\nAVAILABLE ENDPOINTS:\n")

paths = api_spec.get(
    "paths",
    {}
)

for endpoint in paths:

    print(endpoint)