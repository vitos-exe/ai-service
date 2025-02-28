import os

from ai_service.lyrics_reader import load_lyrics_to_df
from tests.base import TestBase


class TestLyricsReader(TestBase):
    def test_load_lyrics_to_df(self, app):
        path = app.config["LYRICS_FOLDER_STRUCTURE_PATH"]
        count = 0
        for root, _, files in os.walk(path):
            count += sum(int(file.endswith(".txt")) for file in files)
        df = load_lyrics_to_df(path)
        assert len(df) == count
        assert not df.isna().any().any()
