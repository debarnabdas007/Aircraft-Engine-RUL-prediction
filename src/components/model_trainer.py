import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# Configuration: where to put model.pkl
@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_df):
        """
        Takes the fully cleaned data, dynamically trains multiple algorithms,
        scores them, and automatically saves the absolute best one.
        """
        try:
            logging.info("Starting the Model Training phase")

            # Split data into Features (X) and Target (y)
            logging.info("Splitting dependent and independent variables")
            y = train_df['RUL']
            X = train_df.drop(columns=['RUL', 'unit_nr', 'time_cycles'], errors='ignore')

            # Created an internal Train/Validation split to grade the models
            # We hold back 20% of the data for evaluation of the algorithms
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

            # 3. Define the dictionary of models we want to test
            models = {
                "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42),
                "XGBoost": XGBRegressor(n_estimators=50, max_depth=5, learning_rate=0.1, random_state=42)
            }

            model_report = {}
            logging.info("Evaluating models to find the best model...")

            # The Evaluation Loop
            for model_name, model in models.items():
                
                # Train
                model.fit(X_train, y_train)
                
                # Make predictions on the unseen validation data
                y_val_pred = model.predict(X_val)
                
                # Grade the model (R2 Score - Closer to 1.0 is better)
                model_score = r2_score(y_val, y_val_pred)
                
                # Save the score in logger
                model_report[model_name] = model_score
                logging.info(f"{model_name} achieved an R2 Score of: {model_score:.4f}")

            # here we automatically find the highest score and the best model's name
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            # Safety Net: Don't save a garbage model
            # If the best model is still terrible (e.g., less than 60% accuracy), stop the pipeline !!
            if best_model_score < 0.6:
                raise CustomException("No acceptable model found. All scores were below 0.6", sys)

            logging.info(f" CHAMPION FOUND: {best_model_name} (Score: {best_model_score:.4f})")

            # Save the winning model to the artifacts folder
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            logging.info("Model Training completed successfully.")

            return self.model_trainer_config.trained_model_file_path

        except Exception as e:
            raise CustomException(e, sys)