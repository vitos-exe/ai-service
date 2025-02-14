import pytest

from ai_service import create_app
from ai_service.config import TestConfig
from ai_service.model import Lyrics, Prediction


class TestBase:
    TEST_LYRICS = Lyrics("artist", "title", Prediction(0.1, 0.25, 0.3, 0.15))

    @pytest.fixture
    def app(self):
        app = create_app(TestConfig)
        yield app
