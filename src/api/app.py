from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()
rf_model = joblib.load('models/rf_autumn_2020.joblib')

class WeatherFeatures(BaseModel):
    bulk_shear_10m_850: float
    bulk_shear_850_500: float
    bulk_shear_10m_500: float
    dir_shear_10m_850: float
    dir_shear_850_500: float
    dir_shear_10m_500: float
    cape: float
    brn: float

@app.post("/predict")
def rfPredict(data: WeatherFeatures) -> dict:
    sentdf = pd.DataFrame({
        'bulk_shear_10m_850': [data.bulk_shear_10m_850],
        'bulk_shear_850_500': [data.bulk_shear_850_500],
        'bulk_shear_10m_500': [data.bulk_shear_10m_500],
        'dir_shear_10m_850': [data.dir_shear_10m_850],
        'dir_shear_850_500': [data.dir_shear_850_500],
        'dir_shear_10m_500': [data.dir_shear_10m_500],
        'cape': [data.cape],
        'brn': [data.brn]
    })

    rf_probs = rf_model.predict_proba(sentdf)[:, 1]
    classification = (rf_probs >= 0.35).astype(int)

    return {
        "probability": float(rf_probs[0]),
        "heavy_rain": int(classification[0])
    }
