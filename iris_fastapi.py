from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Iris Classifier API")

# Load the model from the local file
model = joblib.load("model.joblib")

# Input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Classifier API!"} 

@app.post("/predict/")
def predict_species(data: IrisInput):
    # Convert input data to a DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # Make prediction
    prediction = model.predict(input_df)[0] 
    
    return {
        "predicted_class": str(prediction)
    }
