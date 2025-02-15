from tests.base import TestBase
from ai_service.db import get_qdrant_client, COLLECTION_NAME
import pytest

class TestCLI(TestBase):
    @pytest.fixture
    def runner(self, app):
        return app.test_cli_runner()

    def test_populate_db(self, runner):
        runner.invoke(args='populate_db')
        client = get_qdrant_client()
        count = client.count(
            collection_name=COLLECTION_NAME,
        ).count
        assert count == 2595
        search_result = client.scroll(collection_name=COLLECTION_NAME, limit=100)[0]
        for record in search_result:
            # Ensure each record has a valid vector (not empty)
            assert record.vector is not None, f"Record {record.id} has an empty vector"
            assert len(record.vector) > 0, f"Record {record.id} has an empty vector"

            # Ensure each record has a valid payload (not empty)
            assert record.payload is not None, f"Record {record.id} has an empty payload"
            assert len(record.payload) > 0, f"Record {record.id} has an empty payload"

