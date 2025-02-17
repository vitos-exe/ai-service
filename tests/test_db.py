from dataclasses import astuple

from ai_service.db import COLLECTION_NAME, add_lyrics, get_qdrant_client
from tests.base import TestBase
from testfixtures import compare


class TestDB(TestBase):
    @staticmethod
    def round_to_five(f):
        return round(f, 5)

    def test_add_lyrics(self, app):
        client = get_qdrant_client()
        add_lyrics([TestBase.TEST_LYRICS])
        records = client.scroll(
            collection_name=COLLECTION_NAME,
            with_vectors=True
        )[0]
        assert len(records) == 1
        assert records[0].payload["artist"] == TestBase.TEST_LYRICS.artist
        vector = records[0].vector
        test_lyrics_vector = astuple(TestBase.TEST_LYRICS.prediction)
        compare(map(TestDB.round_to_five, vector), map(TestDB.round_to_five, test_lyrics_vector))
