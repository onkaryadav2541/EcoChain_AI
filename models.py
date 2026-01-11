from pydantic import BaseModel, Field

class CarbonRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Weight of the cargo in kg")
    distance_km: float = Field(..., gt=0, description="Distance in km")
    mode: str = Field(..., pattern="^(truck|train|ship|plane)$")

class CarbonResponse(BaseModel):
    co2_kg: float
    timestamp: str