# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 22:04:38 2025

@author: aagam
"""

# app.py
from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model_car.pkl', 'rb'))

# Define a function to process the input data
def process_input(data):
    features = [
        'year', 'km_driven', 'fuel', 'seller_type', 'transmission',
        'owner', 'seats', 'max_power', 'mileage', 'engine_cc'
    ]
    
    # Create a list of values in the correct order
    processed_data = [float(data[feature]) for feature in features]
    
    # Convert the list to a numpy array and reshape it
    processed_data = np.array(processed_data).reshape(1, -1)
    
    return processed_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    # Get the form data
    data = request.form.to_dict()
    
    # Process the input data
    processed_data = process_input(data)
    
    # Make a prediction
    prediction = model.predict(processed_data)
    
    # Convert the prediction to a standard Python float
    prediction = float(prediction[0])
    
    return render_template('prediction.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)