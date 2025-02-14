import pytest

from ai_service import create_app
from ai_service.config import TestConfig
from ai_service.db import get_qdrant_client, add_lyrics, COLLECTION_NAME

from ai_service.model.lyrics import Lyrics
from ai_service.model.prediction import Prediction

TEST_LYRICS = Lyrics('artist', 'title', Prediction(0.1, 0.25, 0.3, 0.15))

@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app

def test_get_qdrant_client(app):
    client = get_qdrant_client()
    assert client is not None


def test_add_lyrics(app):
    client = get_qdrant_client()
    add_lyrics([TEST_LYRICS])
    print(client.scroll(
        collection_name=COLLECTION_NAME,
    ))


def test_dict_without_prediction():
    lyrics_dict = TEST_LYRICS.dict_without_prediction
    assert 'artist' in lyrics_dict and 'title' in lyrics_dict and 'prediction' not in lyrics_dict
