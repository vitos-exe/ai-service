import pytest

from ai_service.db import get_qdrant_client
from tests.base import TestBase


class TestDBBase(TestBase):
    @pytest.fixture
    def db_client(self, app):
        return get_qdrant_client()
