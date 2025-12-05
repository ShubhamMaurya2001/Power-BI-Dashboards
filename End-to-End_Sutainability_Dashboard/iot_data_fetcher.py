import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- CONFIGURATION ---
# Target Location: New York (Example for fetching public weather data)
LATITUDE = 40.7128
LONGITUDE = -74.0060
DAYS_OF_DATA = 30  # How many days of history to fetch/generate
FILENAME = "Company_Sustainability_Data.xlsx"

class SustainabilityDataPipeline:
    def __init__(self, lat, lon, days):
        self.lat = lat
        self.lon = lon
        self.days = days
        # Standard Grid Emission Factor (kg CO2e per kWh) - approx US avg
        self.EMISSION_FACTOR_ELECTRICITY = 0.385

    def fetch_public_weather_data(self):
        """
        Fetches hourly historical weather data from Open-Meteo (Public API).
        We use this as the 'External Environment' dataset.
        """
        print(f"Fetching public weather data for coordinates: {self.lat}, {self.lon}...")

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=self.days)).strftime("%Y-%m-%d")

        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,shortwave_radiation,relative_humidity_2m",
            "timezone": "auto"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Create DataFrame
            df = pd.DataFrame({
                'Timestamp': data['hourly']['time'],
                'Outside_Temp_C': data['hourly']['temperature_2m'],
                'Solar_Irradiance_W_m2': data['hourly']['shortwave_radiation'],
                'Humidity_Pct': data['hourly']['relative_humidity_2m']
            })
            return df
        except Exception as e:
            print(f"Error fetching API data: {e}")
            return pd.DataFrame()

    def simulate_iot_sensors(self, weather_df):
        """
        Simulates internal IoT sensors based on external weather.
        Logic: Higher temp = Higher HVAC usage.
        """
        print("Simulating internal IoT sensor network...")

        records = []

        for index, row in weather_df.iterrows():
            # Parse time
            current_time = pd.to_datetime(row['Timestamp'])
            hour = current_time.hour
            is_weekend = current_time.weekday() >= 5

            # 1. OCCUPANCY SENSOR (Simulated)
            # Normal business hours: 8am - 6pm, low on weekends
            if 8 <= hour <= 18 and not is_weekend:
                occupancy = random.randint(150, 300) # Active office
            else:
                occupancy = random.randint(0, 10)    # Security/Cleaning only

            # 2. HVAC & ENERGY SENSORS (Correlated to Weather)
            base_load = 50.0 # Base server/lighting load in kWh

            # HVAC works harder if temp is far from 21C (70F)
            temp_diff = abs(row['Outside_Temp_C'] - 21)
            hvac_load = temp_diff * 3.5

            # Add occupancy impact (people generate heat + lights)
            occupancy_load = occupancy * 0.1

            total_kwh = base_load + hvac_load + occupancy_load

            # 3. RENEWABLE GENERATION (Solar Panels)
            # Efficiency * Panel Area * Solar Irradiance
            solar_generation = (row['Solar_Irradiance_W_m2'] * 0.001) * 200 * 0.18

            # NET METERING
            net_energy = total_kwh - solar_generation

            records.append({
                'Timestamp': row['Timestamp'],
                'Department': random.choice(['HQ', 'R&D', 'Logistics']),
                'Sensor_ID': f"METER-{random.randint(100,105)}",
                'Energy_Consumption_kWh': round(total_kwh, 2),
                'Solar_Generation_kWh': round(solar_generation, 2),
                'Net_Energy_Usage_kWh': round(net_energy, 2),
                'Occupancy_Count': occupancy,
                'Outside_Temp_C': row['Outside_Temp_C']
            })

        return pd.DataFrame(records)

    def calculate_esg_metrics(self, df):
        """
        Calculates Scope 2 Emissions based on energy usage.
        """
        print("Calculating ESG Sustainability Metrics...")

        # Scope 2 Emissions (Market-based)
        # Formula: kWh * Grid Emission Factor
        df['Scope2_Emissions_kgCO2'] = df['Net_Energy_Usage_kWh'] * self.EMISSION_FACTOR_ELECTRICITY

        # Avoided Emissions (Thanks to Solar)
        df['Avoided_Emissions_kgCO2'] = df['Solar_Generation_kWh'] * self.EMISSION_FACTOR_ELECTRICITY

        return df

    def run(self):
        # 1. Fetch
        weather_data = self.fetch_public_weather_data()

        if not weather_data.empty:
            # 2. Simulate & Merge
            sensor_data = self.simulate_iot_sensors(weather_data)

            # 3. Calculate Insights
            final_df = self.calculate_esg_metrics(sensor_data)

            # 4. Export
            print(f"Saving {len(final_df)} rows to {FILENAME}...")
            final_df.to_excel(FILENAME, index=False)
            print("Success! Data is ready for Power BI.")
        else:
            print("Failed to generate data pipeline.")

if __name__ == "__main__":
    # Run pipeline for New York coordinates, last 30 days
    pipeline = SustainabilityDataPipeline(LATITUDE, LONGITUDE, DAYS_OF_DATA)
    pipeline.run()