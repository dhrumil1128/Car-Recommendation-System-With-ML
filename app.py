from flask_cors import CORS
from flask import Flask, request, jsonify
import pandas as pd


# Load the dataset
data = pd.read_csv(r'C:\Users\Dhrumil\Desktop\New folder\Car Recommandation System\CARS_1.csv')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Parse input data
        user_input = request.json
        
        seating_capacity = float(user_input.get('seatingCapacity', 0))
        fuel_type = user_input.get('fuelType', '').capitalize()
        starting_price = int(user_input.get('startingPrice', 0))
        ending_price = int(user_input.get('endingPrice', 0))
        transmission_type = user_input.get('transmissionType', '').capitalize()
        body_type = user_input.get('bodyType', '').capitalize()

        # Filter data based on user input
        filtered_data = data[
            (data['seating_capacity'] >= seating_capacity) &
            (data['fuel_type'] == fuel_type) &
            (data['starting_price'] >= starting_price) &
            (data['ending_price'] <= ending_price) &
            (data['transmission_type'] == transmission_type) &
            (data['body_type'] == body_type)
        ]

        # Convert to JSON-friendly format
        recommendations = filtered_data.to_dict(orient='records')

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
