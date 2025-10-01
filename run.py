# D:\AeroPricePredictor\run.py

from app import create_app

# This script is used for local development only.
# In production (Docker/ECS), we will use Gunicorn.

app = create_app()

if __name__ == '__main__':
    # Setting debug=True is safe for local development but MUST be False in production!
    app.run(debug=True, host='0.0.0.0', port=5000)