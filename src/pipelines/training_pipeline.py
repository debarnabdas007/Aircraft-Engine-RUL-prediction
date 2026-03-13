import sys
from src.exception import CustomException
from src.logger import logging


from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        """
        This is the pipeline that connect ingestion, transformation and model trainer. It triggers Ingestion, passes the result to Transformation and passes that result to the Trainer.
        """
        try:
            logging.info(" ....... TRAINING PIPELINE STARTED .........")

            # Data Ingestion
            ingestion = DataIngestion()
            train_data_path, test_data_path = ingestion.initiate_data_ingestion()
            logging.info("Step 1 Complete: Data Ingested.")

            # Data Transformation
            transformation = DataTransformation()
            train_df, preprocessor_path = transformation.initiate_data_transformation(
                train_path=train_data_path, 
                test_path=test_data_path
            )
            logging.info("Step 2 Complete: Data Transformed and Preprocessor Saved.")

            # Model Training
            trainer = ModelTrainer()
            model_path = trainer.initiate_model_trainer(train_df=train_df)
            logging.info(f"Step 3 Complete: Model Trained and saved at {model_path}.")

            logging.info(" ........... TRAINING PIPELINE FINISHED SUCCESSFULLY ......... ")

        except Exception as e:
            logging.error("Pipeline Failed!")
            raise CustomException(e, sys)









# # Testing
# if __name__ == "__main__":
#     pipeline = TrainingPipeline()
#     pipeline.run_pipeline()
#     print("Pipeline ran successfully! Check artifacts folder and logs")