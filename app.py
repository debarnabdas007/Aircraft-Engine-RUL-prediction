from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from src.pipelines.prediction_pipeline import CustomData, PredictPipeline
from src.logger import logging



application = Flask(__name__)
app = application


# Home
@app.route('/')
def index():
    return render_template('index.html') 

# Prediction
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        
        try:
            # we wrap in float() because HTML forms always send text and our model needs decimals
            data = CustomData(
                s_2=float(request.form.get('s_2')),
                s_3=float(request.form.get('s_3')),
                s_4=float(request.form.get('s_4')),
                s_7=float(request.form.get('s_7')),
                s_11=float(request.form.get('s_11')),
                s_12=float(request.form.get('s_12')),
                s_15=float(request.form.get('s_15')),
                s_17=float(request.form.get('s_17')),
                s_20=float(request.form.get('s_20')),
                s_21=float(request.form.get('s_21'))
            )
            
            logging.info("User data successfully captured from HTML form.")

            
            pred_df = data.get_data_as_dataframe()
            
            
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            
            logging.info(f"AI predicted RUL: {results[0]}")

            # rounding off
            final_result = round(results[0])
            
            return render_template('home.html', results=final_result)
            
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return "An error occurred. Please check the terminal logs."


# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)