
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

excel_files = list(DATA_DIR.glob("*.xlsx"))

if not excel_files:
    raise FileNotFoundError(f"No Excel workbooks found in {DATA_DIR}")

inventory = []

for file_path in excel_files:
    workbook = pd.ExcelFile(file_path)

    for sheet_name in workbook.sheet_names:
        # Read worksheet without assuming the first row is a header
        df = pd.read_excel(
            workbook,
            sheet_name=sheet_name,
            header=None
        )

        # Find rows that contain at least one non-empty value
        nonempty_rows = df.notna().any(axis=1).sum()

        # Show first 8 rows to help identify title/header placement
        print("\n" + "=" * 70)
        print(f"Workbook: {file_path.name}")
        print(f"Worksheet: {sheet_name}")
        print(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"Non-empty rows: {nonempty_rows}")
        print("\nFirst 8 rows:")
        print(df.head(8).to_string(index=False, header=False))

        inventory.append({
            "workbook": file_path.name,
            "worksheet": sheet_name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "nonempty_rows": int(nonempty_rows),
            "fully_empty_rows": int(df.isna().all(axis=1).sum()),
            "fully_empty_columns": int(df.isna().all(axis=0).sum()),
            "duplicate_rows": int(df.duplicated().sum()),
        })

inventory_df = pd.DataFrame(inventory)

output_path = OUTPUT_DIR / "source_data_inventory.csv"
inventory_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n" + "=" * 70)
print("DATA INVENTORY COMPLETED")
print(f"Inventory saved to: {output_path}")
print(inventory_df.to_string(index=False))
