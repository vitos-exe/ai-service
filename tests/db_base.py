import pytest

from ai_service.db import create_qdrant_client, get_qdrant_client
from tests.base import TestBase


class TestDBBase(TestBase):
    @pytest.fixture(scope="function")
    def db_client(self, app):
        with app.app_context():
            create_qdrant_client()
        return get_qdrant_client()
