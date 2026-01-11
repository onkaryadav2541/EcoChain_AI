import pytest
from logic.calculator import calculate_co2

def test_calculate_truck():
    # 1000kg, 500km, truck (factor 0.062) -> 31.0kg
    assert calculate_co2(1000, 500, "truck") == 31.0

def test_calculate_train():
    # Train is cleaner (factor 0.022) -> 11.0kg
    assert calculate_co2(1000, 500, "train") == 11.0