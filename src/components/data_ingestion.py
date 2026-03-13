import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass

# Configuration: Tell pipeline exactly where to save the incoming data
@dataclass
class DataIngestionConfig:
    
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")


# The Main Ingestion Component
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered Data Ingestion Component ")
        try:
            # The 26 column names we used in the Jupyter Notebook
            columns = ['unit_nr', 'time_cycles', 'setting_1', 'setting_2', 'setting_3'] + \
                      [f's_{i}' for i in range(1, 22)]

            # Read the raw text files from your data folder 
            # (Make sure your NASA files are actually inside a 'data' folder at your project root!)
            logging.info("Reading raw NASA text files as pandas dataframes")
            
            # Update these paths if your raw files are located somewhere else
            train_df = pd.read_csv('data/raw/train_FD001.txt', sep=r'\s+', names=columns)
            test_df = pd.read_csv('data/raw/test_FD001.txt', sep=r'\s+', names=columns)

            # Create the artifacts folder if it doesn't exist yet
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            #Save the DataFrames securely into the artifacts folder as CSVs
            logging.info("Saving Train and Test data into artifacts folder")
            train_df.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion is completely successful - Train and Test CSVs are ready in the artifacts folder")

            #Return the paths (Data Transformation)
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # suppose is missing or misspelled, complimentary step
            raise CustomException(e, sys)





# # Testing
# if __name__ == "__main__":
#     ingestion_component = DataIngestion()
#     train_path, test_path = ingestion_component.initiate_data_ingestion()
#     print(f"Data saved at: {train_path} and {test_path}")