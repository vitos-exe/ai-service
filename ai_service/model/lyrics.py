from dataclasses import dataclass, asdict

from ai_service.model.prediction import Prediction


@dataclass(frozen=True)
class Lyrics:
    artist: str
    title: str
    prediction: Prediction

    @property
    def dict_without_prediction(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k != 'prediction'}
