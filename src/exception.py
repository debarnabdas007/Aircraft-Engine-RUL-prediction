import sys
import logging
from src.logger import logging  # We import our custom logger so we can log the errors!

def error_message_detail(error, error_detail: sys):
    """
    This function digs into the Python system (sys) to pull out the exact 
    file name and line number where the code crashed.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = str(error)
    
    # Format the error nicely
    detailed_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{error_message}]"
    
    return detailed_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # Inherit from Python's standard Exception class
        super().__init__(error_message)
        
        # Use our custom function to get the detailed error message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        # When we print the error, it will show our detailed, clean message
        return self.error_message


#Testing:-

# if __name__ == "__main__":
#     try:
#         a = 1 / 0  # This will purposely cause a divide-by-zero crash
#     except Exception as e:
#         logging.info("We triggered a deliberate division by zero error.")
#         raise CustomException(e, sys)




'''
When standard Python crashes, it throws a massive, confusing wall of red text. This custom handler acts as a translator. It catches the error, finds exactly which file and which line of code caused it, and formats it into a clean, readable message.
'''