# AEGIS AERO

## Project Overview
AEGIS AERO is a predictive maintenance web application for aircraft engines. It predicts remaining useful life (RUL) using machine learning to help schedule maintenance and prevent failures.

## Data
The project uses the NASA Turbofan Engine Degradation Simulation Data Set from Kaggle, specifically the FD001 subset. FD001 contains time-series data from 100 training engines and 100 test engines, all operating under one condition (sea level) with one fault mode (HPC degradation). Each engine's data includes operational cycles, settings, and 21 sensor measurements. We chose FD001 for its simplicity and focus on a single degradation scenario. The training data shows engines from start to failure, while test data ends before failure, requiring RUL prediction.

## Tech Stack
- Python 3.12
- Flask (web framework)
- Scikit-Learn (Random Forest model)
- Pandas, NumPy (data processing)
- Matplotlib, Seaborn (visualization)
- Jupyter Notebook (EDA and prototyping)

## Project Architecture
The project follows a modular MLOps pipeline structure under the `src/` directory:
- `components/`: Handles data ingestion, transformation, and model training
- `pipelines/`: Contains training and prediction pipelines
- `utils/`: Utility functions for logging and exceptions
- `templates/`: HTML templates for the web interface

## How to Run Locally
1. Clone the repository and navigate to the project directory.
2. Create a virtual environment: `python -m venv aircraft22_venv`
3. Activate the environment: `aircraft22_venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your browser to `http://localhost:5000`