def calculate_co2(weight_kg: float, distance_km: float, mode: str) -> float:
    factors = {
        "truck": 0.062,
        "train": 0.022,
        "ship": 0.010,
        "plane": 0.600
    }
    if mode not in factors:
        raise ValueError("Invalid transport mode")

    # Calculation: (Weight in tons) * Distance * Factor
    return round((weight_kg / 1000) * distance_km * factors[mode], 2)