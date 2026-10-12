import pandas as pd
import numpy as np
from pathlib import Path

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Define the project location
project_location = Path(r"C:\Projects\Real_Estate")

data_folder = project_location / "data"

# Define the input file locations
province_input = (
    data_folder
    / "province"
    / "Residential_Property_Price_Province_Features.xlsx"
)

metro_input = (
    data_folder
    / "metro"
    / "Residential_Property_Price_Metro_Features.xlsx"
)

metro_overall_input = (
    data_folder
    / "metro_overall"
    / "Residential_Property_Price_Metro_Overall_Features.xlsx"
)

# Define the output folders
province_output_folder = (
    data_folder / "analysis" / "province"
)

metro_output_folder = (
    data_folder / "analysis" / "metro"
)

metro_overall_output_folder = (
    data_folder / "analysis" / "metro_overall"
)

# Create output folders if they do not exist
for folder in [
    province_output_folder,
    metro_output_folder,
    metro_overall_output_folder
]:
    folder.mkdir(parents=True, exist_ok=True)

# Define the forecast settings
FORECAST_MONTHS = 12
TEST_MONTHS = 12
MIN_TRAIN_MONTHS = 24

# Create forecasts and evaluate model performance
def create_forecast(
    data,
    forecast_months=FORECAST_MONTHS,
    test_months=TEST_MONTHS
):
    """
    Prepare a monthly time series, evaluate the model on a
    holdout period, and forecast future property price indices.
    """

    data = data[["Date", "Index_Value"]].copy()

    # Convert dates and index values to the correct data types
    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    data["Index_Value"] = pd.to_numeric(
        data["Index_Value"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Date", "Index_Value"]
    )

    if data.empty:
        return None, None, None

    # Combine duplicate monthly observations
    data = (
        data.groupby("Date", as_index=False)["Index_Value"]
        .mean()
        .sort_values("Date")
    )

    # Convert the data into a continuous monthly time series
    data = data.set_index("Date").asfreq("MS")

    # Fill missing monthly observations
    data["Index_Value"] = (
        data["Index_Value"]
        .interpolate(method="linear")
        .ffill()
        .bfill()
    )

    data = data.dropna(
        subset=["Index_Value"]
    )

    # Check whether enough observations are available
    minimum_observations = MIN_TRAIN_MONTHS + test_months

    if len(data) < minimum_observations:
        return None, None, None

    # Split the data into training and testing periods
    train = data.iloc[:-test_months]
    test = data.iloc[-test_months:]

    # Fit the validation model using the training data
    validation_model = ExponentialSmoothing(
        train["Index_Value"],
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated"
    )

    validation_fitted = validation_model.fit(
        optimized=True
    )

    # Forecast the held-out months
    test_forecast = validation_fitted.forecast(
        test_months
    )

    # Compare actual and predicted index values
    test_results = pd.DataFrame({
        "Date": test.index,
        "Actual": test["Index_Value"].to_numpy(),
        "Forecast": test_forecast.to_numpy()
    })

    test_results["Error"] = (
        test_results["Actual"] - test_results["Forecast"]
    )

    test_results["Absolute_Error"] = (
        test_results["Error"].abs()
    )

    # Calculate percentage errors while avoiding division by zero
    test_results["Percentage_Error"] = np.where(
        test_results["Actual"] != 0,
        (
            test_results["Absolute_Error"]
            / test_results["Actual"].abs()
        ) * 100,
        np.nan
    )

    # Calculate model evaluation metrics
    mae = test_results["Absolute_Error"].mean()
    mape = test_results["Percentage_Error"].mean()

    # Fit the final model using all available observations
    final_model = ExponentialSmoothing(
        data["Index_Value"],
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated"
    )

    final_fitted_model = final_model.fit(
        optimized=True
    )

    # Forecast future property price index values
    future_forecast = final_fitted_model.forecast(
        forecast_months
    )

    forecast_results = pd.DataFrame({
        "Date": future_forecast.index,
        "Forecast_Index": future_forecast.to_numpy()
    })

    # Store model performance metrics
    model_metrics = {
        "MAE": mae,
        "MAPE": mape,
        "Training_Observations": len(train),
        "Testing_Observations": len(test),
        "Total_Observations": len(data),
        "Last_Observed_Date": data.index.max()
    }

    return forecast_results, model_metrics, test_results

# Process each dataset and save the forecasting results
def run_forecasting(
    input_file,
    output_file,
    dataset_name
):
    print("\n" + "=" * 75)
    print(f"FORECASTING: {dataset_name.upper()}")
    print("=" * 75)

    # Check whether the input file exists
    if not input_file.exists():
        print("\nERROR: Input file was not found.")
        print(f"Expected location: {input_file}")
        return

    # Load the input dataset
    df = pd.read_excel(input_file)

    print(f"\nInput file: {input_file}")
    print(f"Rows loaded: {len(df):,}")

    # Validate the required columns
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
        print(
            "\nERROR: Missing required columns: "
            + ", ".join(missing_columns)
        )
        return

    # Identify whether the dataset contains metropolitan areas
    has_metro = "Metro" in df.columns

    # Convert dates and index values to the correct data types
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Index_Value"] = pd.to_numeric(
        df["Index_Value"],
        errors="coerce"
    )

    # Remove records with invalid required values
    df = df.dropna(
        subset=[
            "Province",
            "Property_Index",
            "Series_Code",
            "Date",
            "Index_Value"
        ]
    ).copy()

    if has_metro:
        df = df.dropna(
            subset=["Metro"]
        ).copy()

    if df.empty:
        print("\nERROR: No valid data remains after cleaning.")
        return

    # Define the fields used to separate individual time series
    group_columns = [
        "Province",
        "Property_Index",
        "Series_Code"
    ]

    if has_metro:
        group_columns.insert(1, "Metro")

    forecast_results = []
    model_results = []
    test_predictions = []

    # Run forecasts for each individual series
    grouped_data = df.groupby(
        group_columns,
        dropna=False
    )

    for group_key, group in grouped_data:
        if not isinstance(group_key, tuple):
            group_key = (group_key,)

        series_info = dict(
            zip(group_columns, group_key)
        )

        series_label = " | ".join(
            f"{column}: {value}"
            for column, value in series_info.items()
        )

        print(f"\nForecasting: {series_label}")

        try:
            forecast, metrics, test_results = create_forecast(
                group,
                forecast_months=FORECAST_MONTHS,
                test_months=TEST_MONTHS
            )

            if forecast is None:
                print(
                    "Skipped: insufficient valid monthly "
                    "observations for the model."
                )
                continue

            # Add identifying fields to the future forecasts
            for column, value in series_info.items():
                forecast[column] = value

            forecast_results.append(forecast)

            # Add identifying fields to model performance results
            performance_row = dict(series_info)
            performance_row.update(metrics)
            model_results.append(performance_row)

            # Add identifying fields to test predictions
            for column, value in series_info.items():
                test_results[column] = value

            test_predictions.append(test_results)

            print(f"MAE: {metrics['MAE']:.4f}")

            if pd.notna(metrics["MAPE"]):
                print(f"MAPE: {metrics['MAPE']:.2f}%")
            else:
                print("MAPE: Not available")

        except Exception as error:
            print(f"Forecast failed for this series: {error}")
            continue

    # Check whether any forecasts were generated
    if not forecast_results:
        print(
            "\nNo forecasts were generated for "
            f"{dataset_name}."
        )
        return

    forecast_output = pd.concat(
        forecast_results,
        ignore_index=True
    )

    model_performance = pd.DataFrame(
        model_results
    )

    test_output = pd.concat(
        test_predictions,
        ignore_index=True
    )

    # Arrange forecast columns for Excel and Power BI
    identifier_columns = [
        column
        for column in [
            "Province",
            "Metro",
            "Property_Index",
            "Series_Code"
        ]
        if column in forecast_output.columns
    ]

    forecast_output = forecast_output[
        identifier_columns + ["Date", "Forecast_Index"]
    ].sort_values(
        identifier_columns + ["Date"]
    )

    test_identifier_columns = [
        column
        for column in [
            "Province",
            "Metro",
            "Property_Index",
            "Series_Code"
        ]
        if column in test_output.columns
    ]

    test_output = test_output[
        test_identifier_columns
        + [
            "Date",
            "Actual",
            "Forecast",
            "Error",
            "Absolute_Error",
            "Percentage_Error"
        ]
    ].sort_values(
        test_identifier_columns + ["Date"]
    )

    # Save the forecast results and evaluation metrics
    print("\nSaving forecast results...")

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:
        forecast_output.to_excel(
            writer,
            sheet_name="Forecast",
            index=False
        )

        model_performance.to_excel(
            writer,
            sheet_name="Model_Performance",
            index=False
        )

        test_output.to_excel(
            writer,
            sheet_name="Test_Predictions",
            index=False
        )

    # Display the forecasting summary
    print("\nForecasting completed.")
    print(f"Forecast rows: {len(forecast_output):,}")
    print(f"Series forecasted: {len(model_performance):,}")
    print(f"Test prediction rows: {len(test_output):,}")
    print(f"Saved to: {output_file}")

# Forecast provincial property price indices
run_forecasting(
    input_file=province_input,
    output_file=(
        province_output_folder
        / "Province_Property_Price_Forecast.xlsx"
    ),
    dataset_name="Province Overall"
)

# Forecast metro property-type indices
run_forecasting(
    input_file=metro_input,
    output_file=(
        metro_output_folder
        / "Metro_Property_Type_Forecast.xlsx"
    ),
    dataset_name="Metro Property-Type"
)

# Forecast overall metropolitan property price indices
run_forecasting(
    input_file=metro_overall_input,
    output_file=(
        metro_overall_output_folder
        / "Metro_Overall_Forecast.xlsx"
    ),
    dataset_name="Metro Overall"
)

# Display the completion message
print("\n" + "=" * 75)
print("ALL FORECASTING TASKS FINISHED")
print("=" * 75)