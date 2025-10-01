# D:\AeroPricePredictor\generate_slogans.py
import markovify
import os

# 1. Define the input text (corpus) for the Markov Chain
# In a real-world scenario, this would be scraped/collected marketing slogans.
CORPUS_TEXT = """
New England flights are your key to freedom.
Find the best price for your next journey from Boston.
Travel safely and securely with AeroPricePredictor.
Fly from Providence to any destination with confidence.
The lowest prices are always a prediction away.
Historical data guides your future travel booking.
Your journey starts here and now.
Predict, plan, and fly smart.
"""

MODEL_PATH = os.path.join('app', 'slogan_model.json')

def generate_and_save_markov_model():
    """Builds and saves the Markov Chain model for slogan generation."""
    print("Building Markov Chain Model...")
    
    # markovify.Text processes the text and creates the model
    text_model = markovify.Text(CORPUS_TEXT, state_size=2)
    
    # Save the model as a JSON file
    with open(MODEL_PATH, 'w') as f:
        f.write(text_model.to_json())
        
    print(f"Markov Model saved to {MODEL_PATH}")

def load_and_generate_slogan():
    """Loads the model and generates a new slogan."""
    if not os.path.exists(MODEL_PATH):
        generate_and_save_markov_model()

    with open(MODEL_PATH, 'r') as f:
        model_json = f.read()
        
    reconstituted_model = markovify.Text.from_json(model_json)
    
    # Try to generate a sentence with max 140 chars and 3 retries
    slogan = reconstituted_model.make_short_sentence(140, tries=3)
    
    return slogan if slogan else "Plan your flight, predict your price."

if __name__ == '__main__':
    generate_and_save_markov_model()
    print("--- Test Slogan Generation ---")
    print(load_and_generate_slogan())