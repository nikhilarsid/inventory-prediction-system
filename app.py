import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

try:
    models = joblib.load('prediction_models.pkl')
    print("✅ Prediction models loaded successfully.")
except FileNotFoundError:
    print("❌ Error: prediction_models.pkl not found. Please run train_model.py first.")
    models = None

@app.route('/predict', methods=['POST'])
def predict():
    if models is None:
        return jsonify({"error": "Models not loaded. Please check server logs."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input: No JSON data received."}), 400

    product_id = data.get('product_id')
    day_of_year = data.get('day_of_year')

    if product_id is None or day_of_year is None:
        return jsonify({"error": "Missing 'product_id' or 'day_of_year' in request."}), 400

    try:
        product_id = int(product_id)
    except ValueError:
        return jsonify({"error": f"Invalid product_id: '{product_id}'. Must be an integer."}), 400

    if product_id not in models:
        return jsonify({"error": f"No model found for product_id {product_id}."}), 404

    try:
        input_features = np.array([[day_of_year]])
        model = models[product_id]
        prediction = model.predict(input_features)
        predicted_quantity = int(prediction[0])

        return jsonify({
            "product_id": product_id,
            "day_of_year": day_of_year,
            "predicted_quantity_sold": predicted_quantity
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
