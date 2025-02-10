from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    angry: float
    happy: float
    relaxed: float
    sad: float
