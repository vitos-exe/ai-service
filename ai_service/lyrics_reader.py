import pandas as pd
from flask import current_app

from ai_service.model import RawLyrics


def read_lyrics_from_csv() -> list[RawLyrics]:
    path = current_app.config["LYRICS_PATH"]
    df = pd.read_csv(path)
    return [get_raw_lyrics_from_row(row) for row in df.iterrows()]


def get_raw_lyrics_from_row(row):
    data = row[1]
    return RawLyrics(data["artist"], data["title"], data["lyrics"])

def lyrics_by_artist(artist: str) -> str:
    lyrics = read_lyrics_from_csv()
    return next(filter(lambda l: l.artist == artist , lyrics))
