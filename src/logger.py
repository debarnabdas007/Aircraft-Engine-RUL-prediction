import logging
import os
from datetime import datetime

# 1. Create a unique log file name based on the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the path where the logs will be saved (the 'logs/' folder in the root directory)
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

# 3. Combine the path and the file name
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# 4. Set up the basic configuration for the logging system
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Testing:-

logging.info("Logging has started perfectly.")