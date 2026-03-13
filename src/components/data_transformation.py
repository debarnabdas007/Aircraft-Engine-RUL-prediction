import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    #Configuration: we tell where to save our .pkl 
    preprocessor_obj_file_path: str = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function creates the actual 'rules' for cleaning the data.
        In advanced Scikit-Learn, this would be a Pipeline object. 
        For our custom time-series math, we will save the configuration itself.
        """
        try:
            # The exact rules from Jupyter Notebook
            cols_to_drop = ['setting_1', 'setting_2', 'setting_3', 's_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19']
            window_size = 5
            
            # We bundle these rules into a dictionary to act as our "preprocessor" !!
            preprocessor_rules = {
                'cols_to_drop': cols_to_drop,
                'window_size': window_size
            }
            
            return preprocessor_rules

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        This function does: reading the raw CSVs, 
        applying the rolling math, calculating RUL and saving the clean data.
        """
        try:
            logging.info("Starting Data Transformation")
            
            # Read the raw data that Data Ingestion just gave us
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            # Grab the preprocessor rules
            preprocessor_rules = self.get_data_transformer_object()
            cols_to_drop = preprocessor_rules['cols_to_drop']
            window_size = preprocessor_rules['window_size']

            logging.info("Applying drops and time-series feature engineering...")

            ## APPLY NOTEBOOK LOGIC TO TRAIN DATA 
            # Drop useless columns
            train_df = train_df.drop(columns=cols_to_drop, errors='ignore')
            
            # Rolling Means and Stds
            sensor_cols = [col for col in train_df.columns if 's_' in col]
            for sensor in sensor_cols:
                train_df[f'{sensor}_mean'] = train_df.groupby('unit_nr')[sensor].transform(lambda x: x.rolling(window_size).mean())
                train_df[f'{sensor}_std'] = train_df.groupby('unit_nr')[sensor].transform(lambda x: x.rolling(window_size).std())
            
            # Drop the NaN rows created by the rolling window
            train_df = train_df.dropna().reset_index(drop=True)

            # Calculate the RUL for Training Data (Max cycles - current cycle)
            train_max_cycles = train_df.groupby('unit_nr')['time_cycles'].max().reset_index()
            train_max_cycles.rename(columns={'time_cycles': 'max_cycle'}, inplace=True)
            train_df = pd.merge(train_df, train_max_cycles, on='unit_nr', how='left')
            train_df['RUL'] = train_df['max_cycle'] - train_df['time_cycles']
            train_df.drop(['max_cycle'], axis=1, inplace=True)

            # Saving Preprocessor
            logging.info("Saving preprocessing object.")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_rules
            )

            logging.info("Data Transformation completed successfully.")

            # We return the fully engineered training dataframe and the path to the preprocessor
            return (
                train_df, 
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)