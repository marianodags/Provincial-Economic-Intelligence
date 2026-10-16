
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "population_2024_clean.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Cleaned dataset not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("POPULATION DATA VALIDATION")
print("=" * 60)

# 1. Basic checks
print("\n1. Dataset size")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# 2. Missing values
print("\n2. Missing values")
print(df.isna().sum().to_string())

# 3. Geographic levels
print("\n3. Records by geographic level")
print(df["geography_level"].value_counts(dropna=False).to_string())

# 4. Duplicate records
print("\n4. Duplicate checks")
print("Exact duplicate rows:", int(df.duplicated().sum()))

key_columns = ["geography_level", "geography_name_clean"]
print(
    "Duplicate level/name combinations:",
    int(df.duplicated(subset=key_columns).sum())
)

# 5. Population values
print("\n5. Population checks")
print("Zero or negative population:", int((df["population"] <= 0).sum()))
print("Minimum population:", int(df["population"].min()))
print("Maximum population:", int(df["population"].max()))

# 6. Check expected region total against the source figure
region_rows = df[df["geography_level"] == "Region"]
print("\n6. Region total")
print(region_rows[["geography_name_clean", "population"]].to_string(index=False))

expected_region_population = 5_089_934
if len(region_rows) == 1:
    actual = int(region_rows.iloc[0]["population"])
    print("Expected:", expected_region_population)
    print("Actual:", actual)
    print("Match:", actual == expected_region_population)
else:
    print("Review required: expected one region row.")

# 7. Check records missing a parent assignment
print("\n7. Parent assignment checks")
for level in ["Province", "City/Municipality", "Barangay"]:
    subset = df[df["geography_level"] == level]
    parent_col = {
        "Province": "region",
        "City/Municipality": "province",
        "Barangay": "city_municipality",
    }[level]

    missing_parent = subset[parent_col].isna().sum()
    print(f"{level} records missing {parent_col}: {missing_parent}")

# 8. Footnote markers
print("\n8. Records with footnote markers")
marked = df[df["has_footnote_marker"].astype(str).str.lower() == "true"]
print(f"Count: {len(marked)}")
if not marked.empty:
    print(marked[["geography_raw", "geography_name_clean"]].head(20).to_string(index=False))

print("\nValidation report completed.")
print("Investigate any unexpected findings before using the data in Power BI.")
