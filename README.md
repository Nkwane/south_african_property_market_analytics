# South African Property Market Analytics
Provincial and metropolitan residential property market analysis in South Africa using Python, statistical analysis, forecasting and Power BI.

## Project Overview
This project analyses South Africa's residential property market across provinces and metropolitan areas using historical Residential Property Price Index (RPPI) data.

The objective is to identify regional property market trends, compare long-term price index growth, examine differences in property market behaviour, assess market volatility and stability and explore potential future trends through forecasting.

Python is used for data processing, statistical analysis, feature engineering and forecasting and Power BI is used to develop the dashboards that communicate key findings.

The analysis covers provincial and metropolitan markets using monthly observations from 2010 to April 2026. Data source STATS SA

## Objectives

- Analyse long-term residential property price index trends across South African provinces and metropolitan areas.
- Compare index growth across residential property types.
- Measure month-on-month and year-on-year index growth.
- Examine historical growth variability and compare market stability.
- Identify differences in regional and property-type performance.
- Develop and evaluate time-series forecasts.
- Report findings through Power BI dashboard.

## Data Scope

The project uses historical residential property price index data covering South African provinces and metropolitan areas.

The analysis focuses on:

Provincial markets: Comparing residential property price index movements across South Africa's nine provinces.

Metropolitan markets: Examining differences in property market performance across metropolitan areas.

Property types: Analysing freehold properties, sectional title properties, resold properties, and properties sold for the first time where data is available.

Historical trends: Evaluating changes in property price indices over time.

The data is organised into separate provincial, metropolitan and individual metropolitan-area datasets to support the relevant analyses.

## Analytical Approach

1.Data Ingestion and Validation

Load the source residential property price index data.

Validate the source file and inspect the data structure.

Identify duplicate records and assess data consistency.

2.Data Transformation

Restructure the historical monthly data into an analysis-ready format.

Standardise date fields and relevant attributes.

Separate provincial indices, overall metropolitan indices, and individual metropolitan-area indices.

Prepare datasets for subsequent analysis.

3.Feature Engineering and Statistical Analysis

Calculate relevant market growth measures.

Examine historical price index movements.

Assess market volatility using the project's calculated measures.

Prepare analytical features for comparisons and forecasting.

4.Power BI Dashboard Development

The dashboard is structured around five analytical pages:

Executive Market Overview — Provincial market performance, key indicators and long-term growth.

Provincial Market Analysis — Detailed comparisons of residential property price index trends and provincial performance.

Metropolitan Market Analysis — Comparisons of metropolitan property market trends and property-type behaviour.

Market Risk & Stability — Analysis of growth, volatility and differences in market stability across provinces and metropolitan areas.

Market Forecasting — Forecasted index movements and model evaluation using appropriate error metrics, including MAE and MAPE where applicable.

5.Forecasting and Model Evaluation

Forecasting methods are used to investigate potential future price index movements based on historical patterns. Forecast accuracy is assessed using appropriate evaluation metrics.

Forecasts are exploratory and should not be interpreted as guaranteed future property market outcomes.

## Tools and Technologies
- Python: Data processing, feature engineering, statistical analysis, and forecasting.
- Pandas and NumPy: Data manipulation and numerical calculations.
- Matplotlib: Data visualisation and exploratory analysis.
- Power BI: Interactive dashboards and analytical reporting.
- Microsoft Excel: Source data and processed dataset storage.
- Git and GitHub: Version control and project documentation.


Visual Studio: Python development environment.

Author
DR Nkwane

#License
This project is intended for educational, analytical and portfolio demonstration purposes. Residential property price indices measure changes in index values and do not directly represent individual property valuations or guaranteed investment returns. Historical performance and model forecasts should be interpreted in the context of the available data and the limitations of the analytical methods.

