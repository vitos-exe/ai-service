from dataclasses import astuple

from testfixtures import compare

from ai_service import ml
from tests.base import TestBase


class TestML(TestBase):
    def test_predict_lyrics(self, raw_lyrics):
        predictions = ml.SENTIMENT_MODEL.predict_lyrics(raw_lyrics)
        prediction_sums = [round(sum(astuple(p)), 5) for p in predictions]
        compare([1] * len(predictions), prediction_sums)
