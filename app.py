from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

car_dataset = pd.read_csv("CARS_1.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    rating = float(request.form.get('rating'))
    fuel = request.form.get('fuel')
    starting_price = float(request.form.get('starting_price'))
    ending_price = float(request.form.get('ending_price'))
    transmission = request.form.get('transmission')

    filtered_cars = car_dataset[
        (car_dataset['rating'] == rating) &
        (car_dataset['fuel_type'] == fuel) &
        (car_dataset['starting_price'] >= starting_price) &
        (car_dataset['ending_price'] <= ending_price) &
        (car_dataset['transmission_type'] == transmission)
    ]

    recommendations = filtered_cars.to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
