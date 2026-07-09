# ERA5 Heavy Precipitation Prediction Pipeline

An end-to-end machine learning pipeline for detecting heavy precipitation events from ERA5 atmospheric reanalysis data

The project processes multi-dimensional meteorological data, engineers physics-informed atmospheric predictors, trains machine learning classifiers, and deploys the final model through a FastAPI REST API using Docker

## Overview

Heavy precipitation prediction is a challenging imbalanced classification problem because extreme rainfall events are rare compared to normal atmospheric conditions

This pipeline uses ERA5 reanalysis data to generate meteorological predictors including:

- Convective Available Potential Energy (CAPE)
- Bulk wind shear
- Directional wind shear
- Bulk Richardson Number (BRN)

These physics-informed features are used to train and evaluate machine learning models for heavy precipitation detection

## Features

- Processing of large-scale ERA5 atmospheric datasets using xarray
- Parallel CAPE calculation using Dask process-based scheduling
- Meteorological feature engineering using MetPy
- Wind shear and Bulk Richardson Number calculations
- Handling of imbalanced precipitation events using class weighting
- Probability threshold optimisation for event detection
- Benchmarking Logistic Regression, Random Forest, and XGBoost classifiers
- Dockerised FastAPI inference service

## Model Performance

Models were evaluated using ROC-AUC and PR-AUC due to the highly imbalanced nature of heavy precipitation events

Dataset:
- 1.17 million atmospheric samples
- Heavy precipitation treated as the minority class

| Model | ROC-AUC | PR-AUC |
|---|---:|---:|
| Logistic Regression | 0.738 | 0.125 |
| Random Forest | 0.842 | 0.307 |
| XGBoost | 0.798 | 0.217 |

The Random Forest classifier was selected for deployment

## Running the API with Docker

### Build 

docker build -t weather-api .

### Run the API

docker run -p 8000:8000 weather-api

Interactive API documentation:
http://localhost:8000/docs

## Making Predictions

The /predict endpoint accepts atmospheric feature values and returns the predicted probability of heavy precipitation

Example request:

curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
"bulk_shear_10m_850": 5.0,
"bulk_shear_850_500": 10.0,
"bulk_shear_10m_500": 15.0,
"dir_shear_10m_850": 20.0,
"dir_shear_850_500": 30.0,
"dir_shear_10m_500": 40.0,
"cape": 1000,
"brn": 20
}'

Example response:

{
    "probability": 0.02,
    "heavy_rain": 0
}

## Local Development

Create a virtual environment:

python -m venv venv

Activate:

Linux/macOS:
source venv/bin/activate

Windows:
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run FastAPI:
uvicorn src.api.app:app --reload

## Data

ERA5 data can be downloaded using the scripts in the scripts directory

Raw and processed datasets are excluded from version control due to their size. The pipeline expects ERA5 input data to be available locally when running the feature generation workflow

## Technologies

- Python
- xarray
- Dask
- MetPy
- NumPy
- Pandas
- scikit-learn
- XGBoost
- FastAPI
- Docker
