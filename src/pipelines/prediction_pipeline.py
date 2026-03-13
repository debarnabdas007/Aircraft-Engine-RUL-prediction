import sys
import pandas as pd
import os
from src.exception import CustomException
from src.utils import load_object
from src.logger import logging

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features_df):
        try:
            logging.info("Prediction Pipeline Triggered.")
            
            # Load model.pkl
            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(file_path=model_path)
            
            # Prediction directly (No scaling needed for Random Forest/XGBoost!)
            logging.info("Making prediction on single web form input...")
            preds = model.predict(features_df)
            
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, s_2: float, s_3: float, s_4: float, 
                 s_7: float, s_11: float, s_12: float, 
                 s_15: float, s_17: float, s_20: float, s_21: float):
        
        # Capture the 10 sensors the user actually typed into the HTML form
        self.s_2 = s_2
        self.s_3 = s_3
        self.s_4 = s_4
        self.s_7 = s_7
        self.s_11 = s_11
        self.s_12 = s_12
        self.s_15 = s_15
        self.s_17 = s_17
        self.s_20 = s_20
        self.s_21 = s_21

    def get_data_as_dataframe(self):
        try:
            # These are the 14 sensors that survived our drop list
            active_sensors = ['s_2', 's_3', 's_4', 's_7', 's_8', 's_9', 's_11', 
                              's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21']
            
            # base dictionary.
            input_dict = {
                's_2': [self.s_2], 's_3': [self.s_3], 's_4': [self.s_4], 's_7': [self.s_7],
                's_8': [0], 's_9': [0], 's_11': [self.s_11], 's_12': [self.s_12],
                's_13': [0], 's_14': [0], 's_15': [self.s_15], 's_17': [self.s_17],
                's_20': [self.s_20], 's_21': [self.s_21]
            }

            df = pd.DataFrame(input_dict)

            # Create the ordered column list EXACTLY how the training loop did
            ordered_cols = active_sensors.copy() # Start with the base 14 sensors
            
            for sensor in active_sensors:
                # Add the mean and std to the dataframe
                df[f'{sensor}_mean'] = df[sensor]
                df[f'{sensor}_std'] = 0.0
                
                # Add them to our sorting list in pairs!
                ordered_cols.append(f'{sensor}_mean')
                ordered_cols.append(f'{sensor}_std')
            
            #Sort the dataframe using our perfectly matched list
            return df[ordered_cols]

        except Exception as e:
            raise CustomException(e, sys)