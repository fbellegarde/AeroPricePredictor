# D:\AeroPricePredictor\etl_script.py
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

# Define file paths
RAW_DATA_PATH = os.path.join('data', 'ne_flights_raw.csv')
PROCESSED_DATA_PATH = os.path.join('data', 'ne_flights_processed.csv')

def perform_etl():
    """
    Performs Extract, Transform, and Load operations on the flight data.
    This simulates the data preparation step before ML model training.
    """
    print(f"Starting ETL process on: {RAW_DATA_PATH}")

    try:
        # E - Extract
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"Extracted {len(df)} rows.")
        
        # T - Transform
        # 1. Data Cleaning: Drop rows with missing values (simple cleaning)
        df.dropna(inplace=True)
        
        # 2. Feature Engineering: Extract Month and Day of Week
        df['departure_date'] = pd.to_datetime(df['departure_date'])
        df['month'] = df['departure_date'].dt.month
        df['day_of_week'] = df['departure_date'].dt.dayofweek # Monday=0, Sunday=6
        
        # 3. Standardization (for ML): Normalize numerical features (e.g., price)
        # In a real scenario, this scaler would be saved and reused for predictions
        scaler = StandardScaler()
        df['price_scaled'] = scaler.fit_transform(df[['price']])

        # 4. Feature Selection: Keep only the necessary columns for the ML model
        # We also keep the original price for display
        df_processed = df[['origin', 'destination', 'month', 'day_of_week', 'airline', 'class', 'price', 'price_scaled']]
        
        # L - Load (save to a new file)
        df_processed.to_csv(PROCESSED_DATA_PATH, index=False)
        print(f"Successfully processed and saved data to: {PROCESSED_DATA_PATH}")

    except FileNotFoundError:
        print(f"ERROR: Raw data file not found at {RAW_DATA_PATH}. Check your data folder.")
    except Exception as e:
        print(f"An unexpected error occurred during ETL: {e}")

if __name__ == '__main__':
    perform_etl()