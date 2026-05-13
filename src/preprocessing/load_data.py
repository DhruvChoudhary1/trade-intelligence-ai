import pandas as pd


# Load datasets
india_imports = pd.read_csv("data/raw/india_imports_8517.csv")
china_exports = pd.read_csv("data/raw/china_exports_8517_clean.csv")

print("India Imports Shape:", india_imports.shape)
print("China Exports Shape:", china_exports.shape)

print("\nIndia Imports Columns:")
print(india_imports.columns)

print("\nChina Exports Columns:")
print(china_exports.columns)

print("\nSample Data:")
print(india_imports.head())
print(china_exports.head())
print(india_imports[["refYear", "cmdCode"]])
print(china_exports[["refYear", "cmdCode"]])