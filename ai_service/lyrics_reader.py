import os
from typing import Literal

import pandas as pd
from flask import current_app

from ai_service.model import RawLyrics


def load_lyrics_to_df(root_folder) -> pd.DataFrame:
    data = []

    for label in os.listdir(root_folder):
        label_dir = os.path.join(root_folder, label)
        if not os.path.isdir(label_dir):
            continue

        for filename in os.listdir(label_dir):
            if filename.endswith(".txt"):
                artist, title = filename[:-4].split(" - ")
                filepath = os.path.join(label_dir, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    lyrics = f.read()

                data.append(
                    {"label": label, "artist": artist, "title": title, "lyrics": lyrics}
                )

    return pd.DataFrame(data)


def read_lyrics(data_type: Literal["csv", "folder-structure"] = "csv") -> list[RawLyrics]:
    path_config_key, extract_fn = (
        ("LYRICS_CSV_PATH", pd.read_csv)
        if data_type == "csv"
        else ("LYRICS_FOLDER_STRUCTURE_PATH", load_lyrics_to_df)
    )
    df = extract_fn(current_app.config[path_config_key])
    return [get_raw_lyrics_from_row(row) for row in df.iterrows()]


def get_raw_lyrics_from_row(row) -> RawLyrics:
    data = row[1]
    return RawLyrics(data["artist"], data["title"], data["lyrics"])


def lyrics_by_artist(artist: str) -> str:
    lyrics = read_lyrics()
    return next(filter(lambda rl: rl.artist == artist, lyrics))
