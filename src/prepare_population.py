
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = list(DATA_DIR.glob("*.xlsx"))
if not files:
    raise FileNotFoundError("No Excel workbook found in data/raw.")

source_file = files[0]
raw = pd.read_excel(
    source_file,
    sheet_name="2024 POPULATION",
    header=None
)

# Extract the two columns containing geographic labels and population.
df = raw.iloc[:, :2].copy()
df.columns = ["geography_raw", "population"]

df = df.dropna(subset=["geography_raw", "population"]).copy()
df["geography_raw"] = df["geography_raw"].astype(str).str.strip()
df["population"] = pd.to_numeric(df["population"], errors="coerce")
df = df.dropna(subset=["population"]).copy()
df["population"] = df["population"].astype("int64")

# Count leading dots to identify hierarchy levels.
df["dot_count"] = df["geography_raw"].str.extract(r"^(\.*)")[0].str.len()
df["geography_name_raw"] = df["geography_raw"].str.replace(
    r"^\.+", "", regex=True
).str.strip()

# Preserve and flag trailing numeric footnote markers such as "1/" or "3/".
df["has_footnote_marker"] = df["geography_name_raw"].str.contains(
    r"\s+\d+/$", regex=True
)

df["geography_name"] = df["geography_name_raw"].str.replace(
    r"\s+\d+/$", "", regex=True
).str.strip()

# Assign levels using the hierarchy confirmed from the worksheet.
level_map = {
    2: "Region",
    4: "Province",
    6: "City/Municipality",
    8: "Barangay",
}
df["geography_level"] = df["dot_count"].map(level_map)

# Preserve unknown levels for review rather than discarding them.
df["geography_level"] = df["geography_level"].fillna("Review")

# Keep the province/city/municipality hierarchy using forward fill.
# This makes each row's parent province and city/municipality explicit.
df["region"] = pd.NA
df["province"] = pd.NA
df["city_municipality"] = pd.NA

current_region = None
current_province = None
current_city = None

for idx, row in df.iterrows():
    level = row["geography_level"]
    name = row["geography_name"]

    if level == "Region":
        current_region = name
        current_province = None
        current_city = None
    elif level == "Province":
        current_province = name
        current_city = None
    elif level == "City/Municipality":
        current_city = name

    df.at[idx, "region"] = current_region
    df.at[idx, "province"] = current_province
    df.at[idx, "city_municipality"] = current_city

# Barangay records inherit the current region, province, and city/municipality.
# Non-barangay records retain their parent fields as appropriate.
output_columns = [
    "region",
    "province",
    "city_municipality",
    "geography_name",
    "geography_level",
    "population",
    "has_footnote_marker",
    "geography_raw",
]

output = df[output_columns].copy()
output = output.rename(columns={"geography_name": "geography_name_clean"})

output_file = OUTPUT_DIR / "population_2024_clean.csv"
output.to_csv(output_file, index=False, encoding="utf-8-sig")

print("Population dataset created.")
print(f"Output: {output_file}")
print("\nRecords by geographic level:")
print(output["geography_level"].value_counts(dropna=False))
print("\nFootnote-marked records:", int(output["has_footnote_marker"].sum()))
print("\nFirst 10 records:")
print(output.head(10).to_string(index=False))
print("\nReview required: validate parent assignments and footnote meanings.")
