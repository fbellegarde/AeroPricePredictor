# D:\AeroPricePredictor\tests\test_app.py
import pytest
import os

# We need to import the create_app factory from the main application
# This assumes the project structure: tests/test_app.py and app/__init__.py
import sys
# Add the project root to the path to import the 'app' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

# 1. Pytest Fixture: Setup the Test Client
# This fixture creates a Flask application context for testing
@pytest.fixture
def client():
    # Set a dummy secret key for testing purposes
    os.environ['SECRET_KEY'] = 'test-secret-key'
    app = create_app()
    # Use Flask's built-in test client for making requests
    with app.test_client() as client:
        yield client # This is where the testing happens

# 2. Test the Home Page
def test_home_page(client):
    """Test that the home page loads successfully (status code 200)."""
    response = client.get('/')
    # Check for a successful HTTP status
    assert response.status_code == 200
    # Check for a key string on the page
    assert b"Welcome to AeroPricePredictor" in response.data

# 3. Test the Search Route (Success)
def test_search_success(client):
    """Test the search route with valid query parameters."""
    # Simulate a search from BOS to PVD
    response = client.get('/search?origin=BOS+to+Boston+Logan&destination=PVD+to+T.F.+Green+%28Providence%29')
    assert response.status_code == 200
    # Check for expected text on the results page
    assert b"Flight Price Prediction for BOS to Boston Logan to PVD to T.F. Green (Providence)" in response.data

# 4. Test the Search Route (Failure/Redirect)
def test_search_no_params(client):
    """Test the search route without parameters (should redirect to home)."""
    response = client.get('/search')
    # Check for a redirect status code (302)
    assert response.status_code == 302
    # Check that the redirect location is the home page
    assert '/historical' not in response.location