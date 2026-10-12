# south_african_property_market_analytics
Provincial and metropolitan residential property market analysis in South Africa using Python, statistical analysis, forecasting and Power BI.

## Project Overview
This project demonstrates the development of a modern Data Warehouse solution using SQL Server, Medallion Architecture, and Power BI.

The solution integrates CRM and ERP source systems, transforms raw data into analytical datasets, and delivers interactive business intelligence dashboards.



Project Architecture

CRM & ERP Sources
↓
Bronze Layer
↓
Silver Layer
↓
Gold Layer
↓
Power BI Dashboard

Objectives
- Build an end-to-end Data Warehouse solution
- Implement Bronze, Silver, and Gold layers
- Perform data cleansing and transformation
- Design a Star Schema model
- Create interactive Power BI dashboards
- Demonstrate ETL and BI development skills

Technologies Used

SQL Server 
Power BI
GitHub 
Draw.io

Data Warehouse Layers

Bronze Layer
Stores raw data from source systems without transformations.

 Tables
- crm_sales_details
- crm_cust_info
- crm_prd_info
- erp_cust_az12
- erp_loc_a101
- erp_px_cat_g1v2

Silver Layer
Cleansed and standardized data layer.
- Remove duplicates
- Handle null values
- Standardize formats
- Apply business rules

Gold Layer
Business-ready analytical layer designed using a Star Schema.

Fact Table
- fact_sales

Dimension Tables
- dim_customers
- dim_product


ETL Process

 Bronze Layer
- Extract raw data
- Load source files into SQL Server

Silver Layer
- Clean and transform data
- Standardize business entities

Gold Layer
- Create dimensions and fact tables
- Prepare data for reporting

Power BI Dashboard

The Power BI dashboard includes:
- Sales 
- Monthly Sales Summary
- Customer Analysis
- Product Performance
- Interactive Filters & Slicers
- Total Sales KPI
- Total Quantity KPI
- Total Orders KPI
- Sales Trend Analysis
- Monthly Sales Matrix
- Dynamic Filtering

Skills Demonstrated
- Data Warehousing
- ETL Development
- SQL Development
- Data Modelling
- Business Intelligence
- Power BI Reporting
- Git Version Control

Author
DR Nkwane

#License
This project is for educational and portfolio purposes.

