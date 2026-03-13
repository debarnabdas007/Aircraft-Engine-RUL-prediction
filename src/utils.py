import os
import sys
import joblib
from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    """
    Takes any Python object (like trained model or preprocessor)
    and saves it securely as a file in the artifacts folder.
    """
    try:
        # Figure out exactly which folder to put it in
        dir_path = os.path.dirname(file_path)
        
        # Create the folder if it doesn't exist yet
        os.makedirs(dir_path, exist_ok=True)

        # Freeze the object and save it
        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)
            
    except Exception as e:
        # we are going to use this try catch block in many places, for the custom exception class to handle it and log it
        raise CustomException(e, sys)


def load_object(file_path):
    """
    Wakes up a frozen object (like the .pkl model) from the artifacts folder so Flask app can use it to make predictions
    """
    try:
        with open(file_path, "rb") as file_obj:
            return joblib.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    


    