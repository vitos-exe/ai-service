from ai_service.model import LyricsDataFormat


class Config:
    QDRANT_URL: str
    LYRICS_DATA_FORMAT: LyricsDataFormat = "structured-folders"
    LYRICS_CSV_PATH: str
    LYRICS_FOLDER_STRUCTURE_PATH: str


class DevConfig(Config):
    QDRANT_URL = "http://localhost:6333"
    LYRICS_CSV_PATH = "lyrics.csv"
    LYRICS_FOLDER_STRUCTURE_PATH = "lyrics"


class TestConfig(Config):
    QDRANT_URL = ":memory:"
    LYRICS_CSV_PATH = "tests/data/lyrics_test.csv"
    LYRICS_FOLDER_STRUCTURE_PATH = "tests/data/lyrics_test"
    TESTING = True


class DockerComposeConfig(Config):
    QDRANT_URL = "http://qdrant:6333"
    LYRICS_CSV_PATH = "lyrics.csv"
