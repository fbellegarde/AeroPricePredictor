# D:\AeroPricePredictor\app\main.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json # Used to load mock data for now

# Create a Blueprint named 'main_bp'
main_bp = Blueprint('main_bp', __name__)

# --- Mock Data and Functions (To be replaced in Phase 2) ---
# We will simulate the ML/GenAI components here for now
def get_flight_predictions(origin, destination):
    # DUMMY: Simulate ML prediction results
    return {
        "next_30_days": [
            {"date": "2025-10-01", "price": "$150"},
            {"date": "2025-10-15", "price": "$125", "recommendation": "BEST BUY"}
        ],
        "historical_avg": "$180",
        "inflation_adjusted": "$200"
    }

def generate_flight_slogan():
    # DUMMY: Simulate Generative AI output (Markov Chain in Phase 3)
    return "Your next New England adventure is just a click away! Book now."
# -----------------------------------------------------------


# --- Route for the Home Page ---
@main_bp.route('/')
def index():
    """Renders the main landing page with interactive elements."""
    
    # Simulate loading airport data for the dropdowns
    airports = ["Boston (BOS)", "Providence (PVD)", "Manchester (MHT)", "Portland (PWM)"]
    
    slogan = generate_flight_slogan() # Get a dynamic slogan
    
    # Render the template and pass the data
    return render_template('index.html', 
                           airports=airports, 
                           slogan=slogan,
                           title="AeroPricePredictor: NE Flight Analysis")


# --- Route for the Search Results/Prediction Page ---
@main_bp.route('/search', methods=['GET'])
def search_flights():
    """Handles the flight search and displays prediction results."""
    
    # Safely get the query parameters from the URL
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    # Basic validation (to be improved later)
    if not origin or not destination:
        # Redirect back to home with an error, or just show the index
        return redirect(url_for('main_bp.index'))
    
    # Get the simulated ML predictions
    predictions = get_flight_predictions(origin, destination)
    
    return render_template('search.html', 
                           origin=origin, 
                           destination=destination, 
                           predictions=predictions)
                           
# --- Route for the Historical Data Page (Placeholder) ---
@main_bp.route('/historical')
def historical_data():
    """Placeholder for the page showing raw historical flight data."""
    return render_template('historical.html', title="Historical Data Explorer")


# --- Route for the About/ML Explanation Page (Placeholder) ---
@main_bp.route('/about')
def about():
    """Placeholder for the page explaining the ML model and data sources."""
    return render_template('about.html', title="About Our Predictions")