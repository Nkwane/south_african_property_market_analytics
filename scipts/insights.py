import pandas as pd
from pathlib import Path

# Define the project location
project_location = Path(r"C:\Projects\Real_Estate")

# Define the input file locations
province_input = (
    project_location
    / "data"
    / "province"
    / "Residential_Property_Price_Province_Features.xlsx"
)

metro_input = (
    project_location
    / "data"
    / "metro"
    / "Residential_Property_Price_Metro_Features.xlsx"
)

metro_overall_input = (
    project_location
    / "data"
    / "metro_overall"
    / "Residential_Property_Price_Metro_Overall_Features.xlsx"
)

# Define the output folders
analysis_folder = (
    project_location
    / "data"
    / "analysis"
)

province_analysis_folder = analysis_folder / "province"
metro_analysis_folder = analysis_folder / "metro"
metro_overall_analysis_folder = analysis_folder / "metro_overall"

# Create output folders if they do not exist
for folder in [
    province_analysis_folder,
    metro_analysis_folder,
    metro_overall_analysis_folder
]:
    folder.mkdir(parents=True, exist_ok=True)

# Define the analysis function
def analyse_dataset(input_file, output_file, dataset_name):
    print("\n" + "=" * 70)
    print(f"ANALYSING: {dataset_name}")
    print("=" * 70)

    # Check whether the input file exists
    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{input_file}"
        )

    # Load the dataset
    df = pd.read_excel(input_file)

    required_columns = [
        "Province",
        "Property_Index",
        "Series_Code",
        "Date",
        "Index_Value",
        "MoM_Growth",
        "YoY_Growth"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name}: Missing columns {missing_columns}"
        )

    # Convert dates and numerical columns to the correct data types
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    for column in [
        "Index_Value",
        "MoM_Growth",
        "YoY_Growth"
    ]:
        df[column