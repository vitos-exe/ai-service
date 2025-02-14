from tests.base import TestBase


class TestModel(TestBase):
    def test_dict_without_prediction(self):
        lyrics_dict = TestBase.TEST_LYRICS.dict_without_prediction
        assert (
            "artist" in lyrics_dict
            and "title" in lyrics_dict
            and "prediction" not in lyrics_dict
        )
