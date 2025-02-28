class Config:
    QDRANT_URL: str
    LYRICS_PATH: str


class DevConfig(Config):
    QDRANT_URL = "http://localhost:6333"
    LYRICS_PATH = "lyrics.csv"


class TestConfig(Config):
    QDRANT_URL = ":memory:"
    LYRICS_PATH = "lyrics_test.csv"
    TESTING = True


class DockerComposeConfig(Config):
    QDRANT_URL = "http://qdrant:6333"
    LYRICS_PATH = "lyrics.csv"
