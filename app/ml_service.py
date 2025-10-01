# D:\AeroPricePredictor\app\ml_service.py
import joblib
import markovify
import os
import pandas as pd
import random
from datetime import date, timedelta

# Define file paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'price_predictor_model.joblib')
SLOGAN_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'slogan_model.json')

# Load the models globally on startup to prevent slow requests
try:
    PRICE_MODEL = joblib.load(MODEL_PATH)
    print("Price Prediction Model loaded successfully.")
except Exception as e:
    print(f"Warning: Price Model not loaded. Run train_model.py. Error: {e}")
    PRICE_MODEL = None

try:
    with open(SLOGAN_MODEL_PATH, 'r') as f:
        SLOGAN_MODEL = markovify.Text.from_json(f.read())
    print("Slogan Markov Model loaded successfully.")
except Exception as e:
    print(f"Warning: Slogan Model not loaded. Run generate_slogans.py. Error: {e}")
    SLOGAN_MODEL = None


def generate_flight_slogan():
    """Generates a dynamic slogan using the Markov Chain model."""
    if SLOGAN_MODEL:
        # Try to generate a short, non-null sentence
        slogan = SLOGAN_MODEL.make_short_sentence(140, tries=10)
        return slogan if slogan else "Plan your flight, predict your price."
    return "AeroPricePredictor: Your smart travel assistant."


def get_flight_predictions(origin_code, destination_code):
    """
    Generates a 30-day price forecast using the loaded ML model.
    In a real app, we would also load the original scaler from ETL.
    """
    if not PRICE_MODEL:
        # Return fallback data if the model failed to load
        return {
            "next_30_days": [
                {"date": date.today().strftime('%Y-%m-%d'), "price": "Model Error", "recommendation": "N/A"}
            ],
            "historical_avg": "N/A",
            "inflation_adjusted": "N/A"
        }

    forecast_data = []
    historical_prices = []
    
    # 1. Simulate 30-day forecast
    today = date.today()
    
    # SIMULATED CONSTANTS (Must be replaced with real data/analysis in later phases)
    SAMPLE_AIRLINE = 'Delta'
    SAMPLE_CLASS = 'Economy'
    BASE_AVG_PRICE = 250.0 # Dummy historical average for the route

    for i in range(1, 31):
        forecast_date = today + timedelta(days=i)
        
        # Create a new row of features for the prediction
        # The model expects categorical values like 'BOS', 'LAX', etc.
        input_data = pd.DataFrame([{
            'origin': origin_code, 
            'destination': destination_code, 
            'month': forecast_date.month, 
            'day_of_week': forecast_date.weekday(),
            'airline': SAMPLE_AIRLINE,
            'class': SAMPLE_CLASS
        }])
        
        # Predict the scaled price
        scaled_prediction = PRICE_MODEL.predict(input_data)[0]

        # REVERSE SCALING (We don't have the original scaler, so we SIMULATE it)
        # Assuming our StandardScaler on price_scaled yields values roughly between -2 and 2
        # We'll map the scaled prediction back to a plausible price range for the route
        price_offset = scaled_prediction * 50 # 50 is an arbitrary factor for simulation
        
        # Final price: Base + Offset + Random Noise
        predicted_price = BASE_AVG_PRICE + price_offset + random.uniform(-10, 10)
        predicted_price = max(100.0, predicted_price) # Ensure no negative prices

        # Add to historical for calculating final summary
        historical_prices.append(predicted_price)
        
        # Determine recommendation (simple rule)
        recommendation = ""
        if predicted_price < (BASE_AVG_PRICE * 0.9):
            recommendation = "BEST BUY"
        elif predicted_price > (BASE_AVG_PRICE * 1.15):
            recommendation = "AVOID"

        forecast_data.append({
            "date": forecast_date.strftime('%Y-%m-%d'), 
            "price": f"${predicted_price:.2f}", 
            "recommendation": recommendation,
        })

    # 2. Calculate Averages
    overall_historical_avg = sum(historical_prices) / len(historical_prices) if historical_prices else 0
    # Simulate a 15% inflation adjustment (DUMMY VALUE)
    inflation_adjusted = overall_historical_avg * 1.15

    return {
        "next_30_days": forecast_data,
        "historical_avg": f"${overall_historical_avg:.2f}",
        "inflation_adjusted": f"${inflation_adjusted:.2f}"
    }

# This is the entry point if you wanted to test this module in isolation
if __name__ == '__main__':
    print(generate_flight_slogan())
    # Test a route from Boston (BOS) to Los Angeles (LAX)
    predictions = get_flight_predictions('BOS', 'LAX') 
    print(predictions)