import pandas as pd
from pathlib import Path

# Define the project location
project_location = Path(
    r"C:\Projects\Real_Estate"
)

# raw data location
raw_file = (
    project_location
    / "data"
    / "Residential Property Price Indices 2010 to 2026.xlsx"
)

# output folders
province_folder = (
    project_location
    / "data"
    / "province"
)

metro_folder = (
    project_location
    / "data"
    / "metro"
)

metro_overall_folder = (
    project_location
    / "data"
    / "metro_overall"
)


province_folder.mkdir(
    parents=True,
    exist_ok=True
)

metro_folder.mkdir(
    parents=True,
    exist_ok=True
)

metro_overall_folder.mkdir(
    parents=True,
    exist_ok=True
)

# output file locations
province_output = (
    province_folder
    / "Residential_Property_Price_Province.xlsx"
)

metro_output = (
    metro_folder
    / "Residential_Property_Price_Metro.xlsx"
)

metro_overall_output = (
    metro_overall_folder
    / "Residential_Property_Price_Metro_Overall.xlsx"
)

# Check whether the raw file exists
if not raw_file.exists():

    raise FileNotFoundError(
        f"Raw dataset was not found:\n{raw_file}"
    )

print("Raw file found:")
print(raw_file)

# Load the raw dataset
df = pd.read_excel(
    raw_file
)

print("\nRaw dataset loaded successfully.")

print(
    f"Rows: {df.shape[0]}"
)

print(
    f"Columns: {df.shape[1]}"
)

# Identify monthly columns
monthly_columns = [
    column
    for column in df.columns
    if str(column).startswith("m")
    and str(column)[1:].isdigit()
]

if not monthly_columns:

    raise ValueError(
        "No monthly columns were found."
    )

print(
    f"\nMonthly columns found: "
    f"{len(monthly_columns)}"
)

print(
    f"First month: {monthly_columns[0]}"
)

print(
    f"Last month: {monthly_columns[-1]}"
)

# Define metro property-type series
metro_series = [

    "RPPI for freehold properties",

    "RPPI for sectional title properties",

    "RPPI for resold properties",

    "RPPI for properties sold the first time"
]

# Define the provincial index series
province_series = (
    "Residential property price index: "
    "national and provincial indices"
)

# Define the overall metropolitan index series
metro_overall_series = (
    "Residential property price index: "
    "Metropolitan areas"
)

# Define the provinces to include
provinces = [

    "Western Cape",

    "Eastern Cape",

    "Northern Cape",

    "Free State",

    "KwaZulu-Natal",

    "North West",

    "Gauteng",

    "Mpumalanga",

    "Limpopo"
]

# Map metropolitan areas to their provinces
metro_to_province = {

    "Buffalo City":
        "Eastern Cape",

    "Nelson Mandela Bay":
        "Eastern Cape",

    "Mangaung":
        "Free State",

    "City of Johannesburg":
        "Gauteng",

    "City of Tshwane":
        "Gauteng",

    "Ekurhuleni":
        "Gauteng",

    "eThekwini":
        "KwaZulu-Natal",

    "City of Cape Town":
        "Western Cape"
}

# Convert monthly data from wide format to long format
def convert_to_long(
    dataframe,
    id_columns
):

    long_df = dataframe.melt(

        id_vars=id_columns,

        value_vars=monthly_columns,

        var_name="Month",

        value_name="Index_Value"
    )

    # Convert month identifiers into year-month dates
    long_df["Date"] = (

        pd.to_datetime(

            long_df["Month"].str[1:],

            format="%Y%m"

        )

        .dt.strftime("%Y-%m")
    )

    # Remove the original month identifier column
    long_df = long_df.drop(
        columns=["Month"]
    )

    return long_df

# Create the provincial overall dataset
print("\n" + "=" * 60)

print(
    "CREATING PROVINCE OVERALL DATASET"
)

print("=" * 60)

province_df = df[
    df["H04"] == province_series
].copy()

# Keep records for the nine provinces
province_df = province_df[
    province_df["H05"].isin(provinces)
].copy()

if province_df.empty:

    raise ValueError(
        "No provincial records were found."
    )

# Rename the provincial dataset columns
province_df = province_df.rename(

    columns={

        "H05":
            "Province",

        "H04":
            "Property_Index",

        "H03":
            "Series_Code"
    }
)

# Select the required provincial columns
province_df = province_df[

    [
        "Province",

        "Property_Index",

        "Series_Code"

    ]

    + monthly_columns
]

# Convert the provincial dataset to long format
province_df = convert_to_long(

    province_df,

    [
        "Province",

        "Property_Index",

        "Series_Code"
    ]
)

# Arrange the final provincial column order
province_df = province_df[

    [
        "Province",

        "Property_Index",

        "Series_Code",

        "Date",

        "Index_Value"
    ]
]

# Sort the provincial dataset by province and date
province_df = province_df.sort_values(

    by=[
        "Province",

        "Date"
    ]

).reset_index(drop=True)

# Save the provincial dataset
province_df.to_excel(

    province_output,

    index=False
)

print(
    "\nProvince Excel saved to:"
)

print(
    province_output
)

print(
    f"Rows: {len(province_df):,}"
)

# Create the metro property-type dataset
print("\n" + "=" * 60)

print(
    "CREATING METRO PROPERTY-TYPE DATASET"
)

print("=" * 60)

metro_df = df[
    df["H04"].isin(metro_series)
].copy()

# Remove the aggregate metropolitan area records
metro_df = metro_df[
    metro_df["H05"]
    != "All metropolitan areas"
].copy()

if metro_df.empty:

    raise ValueError(
        "No metro property-type records were found."
    )

# Identify metropolitan areas without a province mapping
unmapped_metros = (

    metro_df["H05"]

    .dropna()

    .unique()
)

unmapped_metros = [

    metro

    for metro in unmapped_metros

    if metro not in metro_to_province
]

if unmapped_metros:

    raise ValueError(

        "Unmapped Metro values found:\n"

        + "\n".join(

            str(metro)

            for metro in unmapped_metros
        )
    )

# Add the province associated with each metropolitan area
metro_df["Province"] = (

    metro_df["H05"]

    .map(metro_to_province)
)

# Rename the metro dataset columns
metro_df = metro_df.rename(

    columns={

        "H05":
            "Metro",

        "H04":
            "Property_Index",

        "H03":
            "Series_Code"
    }
)

# Select the required metro columns
metro_df = metro_df[

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code"

    ]

    + monthly_columns
]

# Convert the metro dataset to long format
metro_df = convert_to_long(

    metro_df,

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code"
    ]
)

# Arrange the final metro column order
metro_df = metro_df[

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code",

        "Date",

        "Index_Value"
    ]
]

# Sort the metro dataset by province, metro, property type and date
metro_df = metro_df.sort_values(

    by=[

        "Province",

        "Metro",

        "Property_Index",

        "Date"
    ]

).reset_index(drop=True)

# Save the metro property-type dataset
metro_df.to_excel(

    metro_output,

    index=False
)

print(
    "\nMetro Excel saved to:"
)

print(
    metro_output
)

print(
    f"Rows: {len(metro_df):,}"
)

# Create the overall metropolitan dataset
print("\n" + "=" * 60)

print(
    "CREATING METRO OVERALL DATASET"
)

print("=" * 60)

metro_overall_df = df[

    df["H04"] == metro_overall_series

].copy()

# Remove the aggregate metropolitan area records
metro_overall_df = metro_overall_df[

    metro_overall_df["H05"]
    != "All metropolitan areas"

].copy()

if metro_overall_df.empty:

    raise ValueError(
        "No overall metro records were found."
    )

# Identify metropolitan areas without a province mapping
unmapped_overall_metros = (

    metro_overall_df["H05"]

    .dropna()

    .unique()
)

unmapped_overall_metros = [

    metro

    for metro in unmapped_overall_metros

    if metro not in metro_to_province
]

if unmapped_overall_metros:

    raise ValueError(

        "Unmapped Metro values found "
        "in Metro Overall dataset:\n"

        + "\n".join(

            str(metro)

            for metro in unmapped_overall_metros
        )
    )

# Add the province associated with each metropolitan area
metro_overall_df["Province"] = (

    metro_overall_df["H05"]

    .map(metro_to_province)
)

# Rename the overall metro dataset columns
metro_overall_df = metro_overall_df.rename(

    columns={

        "H05":
            "Metro",

        "H04":
            "Property_Index",

        "H03":
            "Series_Code"
    }
)

# Select the required overall metro columns
metro_overall_df = metro_overall_df[

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code"

    ]

    + monthly_columns
]

# Convert the overall metro dataset to long format
metro_overall_df = convert_to_long(

    metro_overall_df,

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code"
    ]
)

# Arrange the final overall metro column order
metro_overall_df = metro_overall_df[

    [

        "Province",

        "Metro",

        "Property_Index",

        "Series_Code",

        "Date",

        "Index_Value"
    ]
]

# Sort the overall metro dataset by province, metro and date
metro_overall_df = metro_overall_df.sort_values(

    by=[

        "Province",

        "Metro",

        "Date"
    ]

).reset_index(drop=True)

# Save the overall metro dataset
metro_overall_df.to_excel(

    metro_overall_output,

    index=False
)

print(
    "\nMetro Overall Excel saved to:"
)

print(
    metro_overall_output
)

print(
    f"Rows: {len(metro_overall_df):,}"
)

# Display the final transformation summary
print("\n" + "=" * 60)
print("TRANSFORMATION COMPLETE")
print("=" * 60)
print("\nFiles created:")
print("\n1. Province:")
print(province_output)
print("\n2. Metro:")
print( metro_output)
print("\n3. Metro Overall:")
print(metro_overall_output)
print("\nRow counts:")
print(f"Province: "
    f"{len(province_df):,}")
print(
    f"Metro: "
    f"{len(metro_df):,}")
print(
    f"Metro Overall: "
    f"{len(metro_overall_df):,}")
print(
    "\nAll three datasets were created successfully.")