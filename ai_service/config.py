class Config:
    QDRANT_URL: str
    SETUP_QDRANT: bool = False
    LYRICS_PATH: str


class DevConfig(Config):
    QDRANT_URL = "localhost:6333"
    LYRICS_PATH = "lyrics.csv"


class TestConfig(Config):
    QDRANT_URL = ":memory:"
    SETUP_QDRANT: bool = True
