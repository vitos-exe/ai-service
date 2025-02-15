from ai_service.db import COLLECTION_NAME, add_lyrics, get_qdrant_client
from tests.base import TestBase


class TestDB(TestBase):
    def test_add_lyrics(self, app):
        client = get_qdrant_client()
        add_lyrics([TestBase.TEST_LYRICS])
        records = client.count(
            collection_name=COLLECTION_NAME,
        )[0]
        assert len(records) == 1
        assert records[0].payload["artist"] == TestBase.TEST_LYRICS.artist
