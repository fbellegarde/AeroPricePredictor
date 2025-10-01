# D:\AeroPricePredictor\train_model.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Define file paths
PROCESSED_DATA_PATH = os.path.join('data', 'ne_flights_processed.csv')
MODEL_PATH = os.path.join('app', 'price_predictor_model.joblib')

def train_price_predictor():
    """
    Trains a simple Linear Regression model to predict scaled flight price.
    This simulates the core ML component.
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"ERROR: Processed data not found at {PROCESSED_DATA_PATH}. Run etl_script.py first.")
        return

    print("Starting ML Model Training...")
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # 1. Define Features (X) and Target (y)
    # The target is the 'price_scaled' to make the model robust
    features = ['origin', 'destination', 'month', 'day_of_week', 'airline', 'class']
    target = 'price_scaled'
    
    X = df[features]
    y = df[target]

    # 2. Define Preprocessing Steps (ColumnTransformer)
    # We need to one-hot encode categorical features like airport codes, airline, etc.
    categorical_features = ['origin', 'destination', 'airline', 'class']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough' # Keep other columns (none in this case, but good practice)
    )

    # 3. Create a Pipeline (Preprocessing + Estimator)
    # Pipeline ensures that preprocessing steps are consistently applied
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression()) # Simple regression model
    ])
    
    # 4. Split Data (Not strictly needed for a dummy model but essential for practice)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train the Model
    model_pipeline.fit(X_train, y_train)

    # 6. Evaluate (Practice)
    y_pred = model_pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model Training Complete. Mean Squared Error on test set: {mse:.4f}")

    # 7. Save the Model
    joblib.dump(model_pipeline, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")

if __name__ == '__main__':
    train_price_predictor()