# from fastapi import FastAPI, HTTPException
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# import pickle
# import pandas as pd
# import numpy as np
# from typing import List
# import uvicorn


# app = FastAPI(
#     title = 'House Price Prediction API',
#     description= 'Api for Prediction house price using a trained linear regression model',
#     version = '1.0.0'
# )


# try:
#   with open('linear_regression_model.pkl', 'rb') as file:
#     model = pickle.load(file)

#   with open('scaler.pkl', 'rb') as file:
#     scaler = pickle.load(file)

#   print('Model & scaler load successfully')
# except FileNotFoundError as e:
#   print(f'Error loading model and scaler: {e}')
#   print('Please ensure you run the training notebook and saved the model file')


# # Define the input data model
# class HouseFeature(BaseModel):
#   """
#   Input Feature for house price prediction

#   Feature for the California Housing Dataset
#   - MedInc: Median Income in a block
#   - HouseAge: Median house age in the block
#   - AveRooms: Average number of rooms per house
#   - AveBedrms: Average number of bedrooms per house
#   - Population: Total population in the block
#   - AveOccup: Average number of households
#   - Latitude: Latitude of the block
#   - Longitude: Longitude of the block
#   """

#   Medinc: float
#   HouseAge: float
#   AveRooms: float
#   AveBedrms: float
#   Population: float
#   AveOccup: float
#   Latitude: float
#   Longitude: float


# # Define the output model
# class PredictionResponse(BaseModel):
#   'Response model for Prediction'
#   prediction_price: float
#   input_features: dict

# @app.get("/", response_class=HTMLResponse)
# async def root():
#   """Root endpoint with the User-Friendly Html page"""
#   return """
#   <!DOCTYPE html>
#   <html>
#   <head>
#     <title>House Price Prediction API</title>
#     <style>
#         body {
#           font-family: Arial, sans-serif;
#           background: #f4f4f4;
#           margin: 0;
#           padding: 0;
#         }

#         .container {
#           max-width: 500px;
#           margin: 60px auto;
#           padding: 32px 40px 32px 40px;
#           background: #fff;
#           border-radius: 10px;
#           box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
#           text-align: center;
#         }

#         h1 {
#           color: #2d6cdf;
#           margin-bottom: 10px;
#         }

#         p {
#           color: #444;
#           margin-bottom: 24px;
#         }

#         a.button {
#           display: inline-block;
#           padding: 12px 28px;
#           background-color: #2d6cdf;
#           color: #fff;
#           text-decoration: none;
#           border-radius: 6px;
#           font-size: 16px;
#           transition: background 0.2s;
#           }
#     </style>
#   </head>
#   <body>
#     <div class="container">
#       <h1>House Price Prediction API</h1>
#       <p>
#         Welcom! This API Prediction California house price using a machine learning
#         <b>Student:</b> Click blow to explore and test the API endpoints.
#       </p>
#       <a  class="button" href="/docs" target="blank">Open API Documentation</a>
#     </div>
#   </body>
#   </html>
#   """

# @app.post("/generate-listing")
# async def generate_listing():
#     ...


# @app.post("/predict", response_model=PredictionResponse)
# async def predict_house_price(features: HouseFeature):
#     """
#     Predict house price base of input feature

#     Args:
#         features: HouseFeature object containing all required features

#     Return:
#         PredictionResponse with predicted price and input features
#     """

#     try:
#       # convert input into numpy array
#       input_data = np.array([[
#           features.Medinc,
#           features.HouseAge,
#           features.AveRooms,
#           features.AveBedrms,
#           features.Population,
#           features.AveOccup,
#           features.Latitude,
#           features.Longitude
#       ]])

#       # Saved the input data using the saved scaler
#       input_scaler = scaler.transform(input_data)

#       # Make prediction
#       prediction = model.predict(input_scaler)[0]

#       # Convert Prediction into the more readable format
#       predicted_price = float(prediction * 100000)

#       return PredictionResponse(
#           prediction_price=predicted_price,
#           input_features=features.dict()
#       )
#     except Exception as e:
#       raise HTTPException(status_code=500, detail=f'Predictive error: {str(e)}')

# # Example using and testing
# if __name__ == '__main__':
#   import uvicorn
#   uvicorn.run(app, host='127.0.0.1', port=8000)


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.conversation_service import check_missing_fields
from services.listing_service import generate_listing

app = FastAPI(
    title="Voice-Based Property Listing Generator (HF)",
    version="2.0.0"
)

@app.post("/generate-listing")
async def generate_property_listing(property_data: dict):
    missing_fields = check_missing_fields(property_data)

    if missing_fields:
        return JSONResponse(
            content={
                "status": "missing_fields",
                "ask_for": missing_fields
            }
        )

    try:
        listing = generate_listing(property_data)
        return JSONResponse(content=listing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
