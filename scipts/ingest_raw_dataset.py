import pandas as pd
from pathlib import Path

# project location and raw dataset path
project_location = Path(r"C:\Projects\Real_Estate")

raw_dataset = (
    project_location
    / "data"
    / "Residential Property Price Indices 2010 to 2026.xlsx"
)

# Check if raw dataset exists
print("\nChecking dataset...")

if not raw_dataset.exists():

    print("ERROR: Dataset was not found.")
    print(f"Expected location: {raw_dataset}")

    raise SystemExit(1)

else:

    print("Dataset found successfully.")

# Load the Excel workbook
print("\nLoading Excel workbook...")

try:

    excel_file = pd.ExcelFile(raw_dataset)

    print("Excel workbook loaded successfully.")

except Exception as error:

    print("ERROR: Could not load Excel workbook.")
    print(error)

    raise SystemExit(1)

# Identify and load the first worksheet
sheet_name = excel_file.sheet_names[0]

print("\n" + "=" * 70)
print("READING FIRST WORKSHEET")
print("=" * 70)

print(f"\nWorksheet: {sheet_name}")

df = pd.read_excel(
    raw_dataset,
    sheet_name=sheet_name
)

print("Worksheet loaded successfully.")

# Displays the dataset dimensions
print("\n" + "=" * 70)
print("DATASET SIZE")
print("=" * 70)

print(f"\nRows:    {df.shape[0]:,}")
print(f"Columns: {df.shape[1]:,}")

# Display all column names
print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)

for number, column in enumerate(df.columns, start=1):

    print(f"{number:>3}. {column}")

# Check for missing values in each column
print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

missing_values = df.isnull().sum()

print()

print(missing_values.to_string())

# Check for duplicate 
print("\n" + "=" * 70)
print("DUPLICATE ROWS")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicate_rows:,}")

# Generate a statistical summary of numeric columns
print("\n" + "=" * 70)
print("NUMERIC DATA SUMMARY")
print("=" * 70)

print()

print(
    df.describe(include="number").to_string()
)

# Display the raw data ingestion completion message
print("\n" + "=" * 70)
print("RAW DATA INGESTION COMPLETE")
print("=" * 70)