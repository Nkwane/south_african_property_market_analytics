import pandas as pd
from pathlib import Path

# Define the project location
project_location = Path(
    r"C:\Projects\Real_Estate"
)

# Define the input file locations
province_input = (
    project_location
    / "data"
    / "province"
    / "Residential_Property_Price_Province.xlsx"
)

metro_input = (
    project_location
    / "data"
    / "metro"
    / "Residential_Property_Price_Metro.xlsx"
)

metro_overall_input = (
    project_location
    / "data"
    / "metro_overall"
    / "Residential_Property_Price_Metro_Overall.xlsx"
)

# Define the output file locations
province_output = (
    project_location
    / "data"
    / "province"
    / "Residential_Property_Price_Province_Features.xlsx"
)

metro_output = (
    project_location
    / "data"
    / "metro"
    / "Residential_Property_Price_Metro_Features.xlsx"
)

metro_overall_output = (
    project_location
    / "data"
    / "metro_overall"
    / "Residential_Property_Price_Metro_Overall_Features.xlsx"
)

# Define the function to calculate features
def calculate_features(
    input_file,
    output_file,
    dataset_name
):
    print("\n" + "=" * 70)
    print(f"PROCESSING: {dataset_name}")
    print("=" * 70)

    # Check whether the input file exists
    if not input_file.exists():
        print("\nERROR: Input dataset was not found.")
        print(f"Expected location:\n{input_file}")
        raise FileNotFoundError(input_file)

    # Load the dataset
    try:
        df = pd.read_excel(input_file)

        print("\nDataset loaded successfully.")
        print(f"Rows:    {df.shape[0]:,}")
        print(f"Columns: {df.shape[1]:,}")

    except Exception as error:
        print("\nERROR: Could not load dataset.")
        print(error)
        raise

    # Check the required columns
    required_columns = [
        "Province",
        "Property_Index",
        "Series_Code",
        "Date",
        "Index_Value"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Identify whether the dataset contains a Metro column
    has_metro = "Metro" in df.columns

    if has_metro:
        print("\nMetro column detected.")
        print("Growth calculations will be performed separately for each Metro.")
    else:
        print("\nNo Metro column detected.")
        print("Growth calculations will be performed separately for each Province / Index series.")

    # Convert dates to datetime format
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%Y-%m",
        errors="coerce"
    )

    # Convert index values to numeric
    df["Index_Value"] = pd.to_numeric(
        df["Index_Value"],
        errors="coerce"
    )

    # Identify invalid dates
    invalid_dates = df["Date"].isna().sum()

    if invalid_dates > 0:
        print(f"\nWARNING: {invalid_dates:,} invalid dates found.")

    # Identify duplicate observations
    if has_metro:
        duplicate_columns = [
            "Province",
            "Metro",
            "Property_Index",
            "Series_Code",
            "Date"
        ]
    else:
        duplicate_columns = [
            "Province",
            "Property_Index",
            "Series_Code",
            "Date"
        ]

    duplicate_count = df.duplicated(
        subset=duplicate_columns
    ).sum()

    print(f"\nDuplicate observations: {duplicate_count:,}")

    if duplicate_count > 0:
        print("WARNING: Duplicate observations detected.")
        print("Duplicates will NOT be silently removed.")

    # Sort the dataset
    if has_metro:
        sort_columns = [
            "Province",
            "Metro",
            "Property_Index",
            "Date"
        ]
    else:
        sort_columns = [
            "Province",
            "Property_Index",
            "Date"
        ]

    df = df.sort_values(
        by=sort_columns
    ).reset_index(drop=True)

    # Calculate month-over-month growth
    print("\n" + "-" * 70)
    print("CALCULATING MONTH-OVER-MONTH GROWTH")
    print("-" * 70)

    if has_metro:
        growth_group = [
            "Province",
            "Metro",
            "Property_Index",
            "Series_Code"
        ]
    else:
        growth_group = [
            "Province",
            "Property_Index",
            "Series_Code"
        ]

    df["MoM_Growth"] = (
        df.groupby(growth_group)["Index_Value"].pct_change() * 100
    )

    # Calculate year-over-year growth
    print("\n" + "-" * 70)
    print("CALCULATING YEAR-OVER-YEAR GROWTH")
    print("-" * 70)

    df["YoY_Growth"] = (
        df.groupby(growth_group)["Index_Value"].pct_change(periods=12) * 100
    )

    # Calculate long-term growth
    print("\n" + "-" * 70)
    print("CALCULATING LONG-TERM GROWTH")
    print("-" * 70)

    # Compare each index with its first available observation within its own series
    first_index_value = (
        df.groupby(growth_group)["Index_Value"].transform("first")
    )

    df["Long_Term_Growth"] = (
        (df["Index_Value"] - first_index_value)
        / first_index_value
        * 100
    )

    # Calculate volatility using the standard deviation of monthly growth
    print("\n" + "-" * 70)
    print("CALCULATING VOLATILITY")
    print("-" * 70)

    df["Volatility"] = (
        df.groupby(growth_group)["MoM_Growth"].transform("std")
    )

    # Arrange the final column order
    if has_metro:
        final_columns = [
            "Province",
            "Metro",
            "Property_Index",
            "Series_Code",
            "Date",
            "Index_Value",
            "MoM_Growth",
            "YoY_Growth",
            "Long_Term_Growth",
            "Volatility"
        ]
    else:
        final_columns = [
            "Province",
            "Property_Index",
            "Series_Code",
            "Date",
            "Index_Value",
            "MoM_Growth",
            "YoY_Growth",
            "Long_Term_Growth",
            "Volatility"
        ]

    df = df[final_columns]

    # Save the feature dataset
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        output_file,
        index=False
    )

    # Display the dataset summary
    print("\nFeature dataset created successfully.")
    print(f"\nRows:    {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")
    print("\nColumns:")

    for number, column in enumerate(df.columns, start=1):
        print(f"{number:>3}. {column}")

    print("\nSaved to:")
    print(output_file)

    return df

# Calculate province features
province_features = calculate_features(
    province_input,
    province_output,
    "PROVINCE OVERALL"
)

# Calculate metro property-type features
metro_features = calculate_features(
    metro_input,
    metro_output,
    "METRO PROPERTY-TYPE"
)

# Calculate overall metro features
metro_overall_features = calculate_features(
    metro_overall_input,
    metro_overall_output,
    "METRO OVERALL"
)

# Display the final summary
print("\n" + "=" * 70)
print("ALL FEATURE DATASETS CREATED SUCCESSFULLY")
print("=" * 70)

print("\nProvince Features:")
print(province_output)

print("\nMetro Property-Type Features:")
print(metro_output)

print("\nMetro Overall Features:")
print(metro_overall_output)

print("\n" + "=" * 70)
print("CALCULATIONS COMPLETE")
print("=" * 70)