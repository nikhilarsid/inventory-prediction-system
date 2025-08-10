# app.py

import joblib
from flask import Flask, request, jsonify
import numpy as np

# --- 1. Initialize Flask App ---
app = Flask(__name__)

# --- 2. Load the Prediction Models ---
# Load the dictionary of models we saved in the previous step.
try:
    models = joblib.load('prediction_models.pkl')
    print("✅ Prediction models loaded successfully.")
except FileNotFoundError:
    print("❌ Error: prediction_models.pkl not found. Please run train_model.py first.")
    models = None # Set models to None if file doesn't exist

# --- 3. Create the Prediction API Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to predict sales for a given product and day.
    Expects a JSON payload with 'product_id' and 'day_of_year'.
    Example: {"product_id": 101, "day_of_year": 15}
    """
    # First, check if models were loaded correctly
    if models is None:
        return jsonify({"error": "Models not loaded. Please check server logs."}), 500

    # Get the JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input: No JSON data received."}), 400

    # --- 4. Validate Input ---
    product_id = data.get('product_id')
    day_of_year = data.get('day_of_year')

    if product_id is None or day_of_year is None:
        return jsonify({"error": "Missing 'product_id' or 'day_of_year' in request."}), 400

    # Ensure product_id is an integer, as our model keys are integers
    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": f"Invalid product_id: '{product_id}'. Must be an integer."}), 400

    # Check if we have a model for this product
    if product_id not in models:
        return jsonify({"error": f"No model found for product_id {product_id}."}), 404

    # --- 5. Make Prediction ---
    try:
        # The model expects a 2D array as input, so we reshape it.
        # np.array([[day_of_year]]) creates a shape of (1, 1)
        input_features = np.array([[day_of_year]])
        
        # Get the specific model for the product
        model = models[product_id]
        
        # Use the model to predict
        prediction = model.predict(input_features)
        
        # The prediction is an array, so we get the first element.
        # We also convert it to an integer as we can't sell fractions of items.
        predicted_quantity = int(prediction[0])

        # --- 6. Return the Result ---
        return jsonify({
            "product_id": product_id,
            "day_of_year": day_of_year,
            "predicted_quantity_sold": predicted_quantity
        })

    except Exception as e:
        # Catch any other potential errors during prediction
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

# --- 7. Run the App ---
if __name__ == '__main__':
    # Runs the Flask app on a local development server.
    # Host '0.0.0.0' makes it accessible on your local network.
    # Port 5000 is the default for Flask.
    app.run(host='0.0.0.0', port=5000, debug=True)