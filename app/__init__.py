# D:\AeroPricePredictor\app\__init__.py

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# --- Application Factory Function ---
def create_app():
    # 1. Create the Flask app instance
    app = Flask(__name__)
    
    # 2. Load configuration from environment variables (e.g., SECRET_KEY)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Ensure a secret key is set for security
    if not app.config['SECRET_KEY']:
        raise RuntimeError("SECRET_KEY not set. Check your .env file.")

    # 3. Import and Register Blueprints (routes)
    # Blueprints organize app routes into modular parts.
    from .main import main_bp
    app.register_blueprint(main_bp)

    # 4. Optional: Global Error Handlers (Good practice for production)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

# If you wanted to run the app directly (for local development)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)