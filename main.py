from fastapi import FastAPI, HTTPException
from logic.calculator import calculate_co2
from models import CarbonRequest, CarbonResponse
from datetime import datetime

# 1. Initialize the App
app = FastAPI(
    title="EcoChain AI API",
    description="Agile Carbon Footprint Calculator for LkSG Compliance",
    version="1.0.0"
)

# 2. The "Health Check" Endpoint
# DevOps teams use this to check if the server is alive.
@app.get("/")
def read_root():
    return {"status": "active", "message": "EcoChain AI is running"}

# 3. The Calculation Endpoint
# This connects your Logic (Day 3) to the Web (Day 4)
@app.post("/calculate", response_model=CarbonResponse)
def calculate_footprint(request: CarbonRequest):
    try:
        # Call the logic function we wrote yesterday
        co2_result = calculate_co2(
            weight_kg=request.weight_kg,
            distance_km=request.distance_km,
            mode=request.mode
        )
        
        return CarbonResponse(
            co2_kg=co2_result,
            timestamp=datetime.now().isoformat()
        )
    except ValueError as e:
        # Return a polite error message (400 Bad Request)
        raise HTTPException(status_code=400, detail=str(e))