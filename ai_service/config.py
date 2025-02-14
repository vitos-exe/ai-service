class Config:
    QDRANT_URL: str
    SETUP_QDRANT: bool = False


class DevConfig(Config):
    QDRANT_URL = 'localhost:6333'


class TestConfig(Config):
    QDRANT_URL = ':memory:'
    SETUP_QDRANT: bool = True
