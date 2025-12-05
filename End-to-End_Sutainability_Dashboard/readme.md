# Sustainability Impact Dashboard Data Pipeline

## 🚀 Project Overview

This repository contains the Python script necessary to generate a foundational dataset for a Sustainability Impact Dashboard. It simulates the ingestion of real-time IoT sensor data (Energy, Occupancy) and blends it with publicly available environmental data (Weather, Solar Irradiance) to calculate core ESG metrics (Scope 2 Emissions).

The resulting Excel file is optimized for direct consumption by Power BI, enabling the creation of advanced visualizations for corporate net-zero goal tracking and scenario analysis.

## 🛠️ Data Sources & Technology Stack

| Component | Source/Role | Technology |
|-----------|-------------|------------|
| Public Data Source | External weather/solar radiation data | Open-Meteo API (via `requests`) |
| Simulated IoT Data | Internal Smart Meter & Occupancy simulation | Python (`numpy`, `random`) |
| Data Processing | ETL, ESG metric calculation (Scope 2) | Python (`pandas`) |
| Output | Power BI Source Data | Excel (`.xlsx`) |

## 1. Prerequisites

To run the Python pipeline, you need a stable Python environment (Python 3.8+).

### Installation

Install the necessary libraries using `pip`. Note that `openpyxl` is required by pandas to handle Excel file writing.

```bash
pip install pandas requests openpyxl numpy
```

## 2. Running the Data Pipeline

The core script, `iot_data_fetcher.py` (which you have), fetches real-time data and simulates your company's sensor network, outputting the result to a spreadsheet.

### Execution

Run the script directly from your terminal:

```bash
python iot_data_fetcher.py
```

### Output File

A file named `Company_Sustainability_Data.xlsx` will be generated in the current directory. This file contains hourly data points and calculated metrics:

- **Timestamp**: Hourly data points
- **Outside_Temp_C**: Real historical weather data from the web
- **Energy_Consumption_kWh**: Simulated building energy usage
- **Scope2_Emissions_kgCO2**: Automatically calculated carbon footprint
- **Occupancy_Count**: Simulated people count (useful for "Energy per Employee" metrics)

## 3. Power BI Dashboard Setup

Use the generated Excel file to create your interactive sustainability dashboard.

### 3.1 Load Data

1. Open Power BI Desktop
2. Click **Get Data** → **Excel Workbook**
3. Select `Company_Sustainability_Data.xlsx`
4. Click **Load**

### 3.2 Key Measures (DAX)

Foundational DAX measures to calculate key performance indicators (KPIs) in Power BI:

| Measure Name | DAX Formula | Purpose |
|--------------|-------------|---------|
| Total Emissions | `Total Emissions = SUM(Sheet1[Scope2_Emissions_kgCO2])` | Total calculated Scope 2 Carbon Footprint |
| Renewable % | `Renewable % = DIVIDE(SUM(Sheet1[Solar_Generation_kWh]), SUM(Sheet1[Energy_Consumption_kWh]), 0)` | Percentage of total energy offset by simulated solar generation |
| Intensity | `Intensity = DIVIDE(SUM(Sheet1[Energy_Consumption_kWh]), SUM(Sheet1[Occupancy_Count]), 0)` | Energy Consumption per Person, a key efficiency metric |

### 3.3 Recommended Visualizations

There are the following visuals to bring the data to life:

1. **KPI Cards**: Display `Total Emissions` and `Renewable %` for an executive summary header
2. **Trend Lines (Line Chart)**: Compare the `Energy_Consumption_kWh` against `Outside_Temp_C` over time to visualize the relationship between external environment and internal usage (HVAC correlation)
3. **Departmental Heatmap (Matrix)**: Use a Matrix visual with `Department` on the Rows and `Scope2_Emissions_kgCO2` as the Value. Apply Conditional Formatting to the background color to create a visual intensity map
4. **AI Narrative**: Use Power BI's built-in Smart Narrative visual for automatically generated text summaries of trends and outliers

## 4. Automation and Deployment

For a "Live" dashboard experience, automate the data refresh process:

1. Schedule the Python script to run daily using Windows Task Scheduler or a Cron job on Linux/macOS
2. Save the updated `Company_Sustainability_Data.xlsx` file to a cloud location like OneDrive or SharePoint
3. In Power BI, update the data source settings to point directly to the cloud file path. Power BI Service can then refresh the dashboard automatically, ensuring the data is always up-to-date
