
import pandas as pd

file_path = "data/processed/population_2024_clean.csv"
df = pd.read_csv(file_path)

print("\nPROVINCE RECORDS")
print(
    df.loc[df["geography_level"] == "Province",
           ["geography_name_clean", "population"]]
    .to_string(index=False)
)

print("\nCITY/MUNICIPALITY RECORDS")
print(
    df.loc[df["geography_level"] == "City/Municipality",
           ["geography_name_clean", "province", "population"]]
    .head(20)
    .to_string(index=False)
)

print("\nMISSING PROVINCE ASSIGNMENTS")
print(
    df.loc[
        (df["geography_level"] == "City/Municipality")
        & df["province"].isna(),
        ["geography_name_clean", "population"]
    ].to_string(index=False)
)


print("\nINDEPENDENT CITY CHECK")
print(
    df.loc[
        df["geography_name_clean"].str.contains(
            "Zamboanga|Isabela", case=False, na=False
        ),
        [
            "geography_name_clean",
            "geography_level",
            "region",
            "province",
            "city_municipality",
            "population",
        ],
    ].to_string(index=False)
)
