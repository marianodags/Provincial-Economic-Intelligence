
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Find Excel workbooks
excel_files = list(DATA_DIR.glob("*.xlsx"))

if not excel_files:
    raise FileNotFoundError(
        f"No .xlsx files found in: {DATA_DIR}\n"
        "Place your original PSA workbook in data/raw/."
    )

for file_path in excel_files:
    print("\n" + "=" * 70)
    print(f"WORKBOOK: {file_path.name}")
    print("=" * 70)

    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        print(f"\nWORKSHEET: {sheet_name}")

        # Read a small preview without changing the source file
        preview = pd.read_excel(
            excel_file,
            sheet_name=sheet_name,
            header=None,
            nrows=10
        )

        print(f"Preview dimensions: {preview.shape}")
        print(preview.to_string(index=False, header=False))

print("\nInspection completed. No source files were modified.")
