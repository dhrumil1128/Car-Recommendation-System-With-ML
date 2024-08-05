from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load the dataset globally
user_data = pd.read_csv(r"C:\Users\Dhrumil\Downloads\CARS_1.csv")

@app.route('/')
def index():
    return render_template('index.html')

def recommend_cars(user_input, num_recommendations=5):
    try:
        # Create a copy of the dataset to filter
        filtered_data = user_data.copy()
        
        # For Fuel:
        if 'fuel_type' in user_input and user_input['fuel_type']:
            filtered_data = filtered_data[filtered_data['fuel_type'] == user_input['fuel_type']]
        print("Filtered by fuel_type:", filtered_data)
        
        # For Transmission Type:
        if 'transmission_type' in user_input and user_input['transmission_type']:
            filtered_data = filtered_data[filtered_data['transmission_type'] == user_input['transmission_type']]
        print("Filtered by transmission_type:", filtered_data)
        
        # For Body Type:
        if 'body_type' in user_input and user_input['body_type']:
            filtered_data = filtered_data[filtered_data['body_type'] == user_input['body_type']]
        print("Filtered by body_type:", filtered_data)
        
        # For Seating Capacity:
        if 'seating_capacity' in user_input and user_input['seating_capacity']:
            filtered_data = filtered_data[filtered_data['seating_capacity'] == user_input['seating_capacity']]
        print("Filtered by seating_capacity:", filtered_data)
        
        # For Starting Price-Ending Price:
        if 'starting_price' in user_input and 'ending_price' in user_input and user_input['starting_price'] and user_input['ending_price']:
            starting_price = int(user_input['starting_price'])
            ending_price = int(user_input['ending_price'])
            filtered_data = filtered_data[
                (filtered_data['starting_price'] >= starting_price) & 
                (filtered_data['ending_price'] <= ending_price)
            ]
        print("Filtered by price range:", filtered_data)

        # If no cars match the filters, return an empty DataFrame
        if filtered_data.empty:
            print("No cars match the filters")
            return pd.DataFrame(columns=user_data.columns)
        
        # Select features to calculate similarities
        features = filtered_data[['starting_price', 'ending_price', 'rating', 'max_torque_nm', 'max_power_bhp']]
        
        # Compute cosine similarity between cars based on the selected features
        similarities = cosine_similarity(features)
        
        # Use the first entry in the filtered data to find similar cars
        car_index = filtered_data.index[0]
        similar_indices = similarities[car_index].argsort()[-num_recommendations-1:-1][::-1]
        
        # Get the recommended cars based on similarity indices
        recommended_cars = filtered_data.iloc[similar_indices]
        print("Recommended cars:", recommended_cars)
        return recommended_cars
    except Exception as e:
        print(f"Error in recommend_cars function: {e}")
        return pd.DataFrame(columns=user_data.columns)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json
    recommendations = recommend_cars(user_input)
    
    if not recommendations.empty:
        return jsonify(recommendations.to_dict(orient='records'))
    else:
        return jsonify({'recommendations': []})

if __name__ == '__main__':
    app.run(debug=True)
