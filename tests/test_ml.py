from ai_service import lyrics_reader, ml, model
from tests.base import TestBase
from dataclasses import astuple
from testfixtures import compare


class TestML(TestBase):
    def test_predict_lyrics(self, raw_lyrics):
        predictions = ml.predict_lyrics([l.lyrics for l in raw_lyrics])
        prediction_sums = [round(sum(astuple(p)), 5) for p in predictions]
        compare([1] * len(predictions), prediction_sums)
