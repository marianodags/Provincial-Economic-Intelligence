
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = (
    PROJECT_DIR / "data" / "processed" / "population_2024_clean.csv"
)

df = pd.read_csv(INPUT_FILE)

# Find barangays without an assigned city/municipality.
missing = df[
    (df["geography_level"] == "Barangay")
    & (df["city_municipality"].isna())
]

print(f"Barangays missing city/municipality: {len(missing)}")
print("\nFirst 30 affected records:")

columns = [
    "region",
    "province",
    "geography_name_clean",
    "geography_raw",
    "population",
]

print(missing[columns].head(30).to_string(index=True))

# Show the records immediately before and after the first affected row.
if not missing.empty:
    first_index = missing.index[0]
    start = max(0, first_index - 5)
    end = min(len(df), first_index + 6)

    print("\nContext around the first affected record:")
    print(
        df.loc[start:end-1, [
            "province",
            "city_municipality",
            "geography_name_clean",
            "geography_level",
            "geography_raw",
        ]].to_string(index=True)
    )

print("\nDiagnosis complete. No files were modified.")
