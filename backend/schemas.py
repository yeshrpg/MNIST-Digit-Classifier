from pydantic import BaseModel
from typing import List

class PredictionResponse(BaseModel):
    digit: int
    confidence: float
    probabilities: List[float]