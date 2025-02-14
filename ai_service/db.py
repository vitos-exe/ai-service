import uuid
from dataclasses import astuple

from flask import current_app
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from ai_service.lyrics_reader import read_lyrics_from_csv
from ai_service.model import Lyrics

QDRANT_CLIENT: QdrantClient = None
COLLECTION_NAME: str = "lyrics"


def create_qdrant_client() -> None:
    global QDRANT_CLIENT

    location = current_app.config.get("QDRANT_URL", None)
    QDRANT_CLIENT = QdrantClient(location)


def setup_qdrant() -> None:
    client = get_qdrant_client()
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=4, distance=Distance.COSINE),
        )


def get_qdrant_client() -> QdrantClient:
    if QDRANT_CLIENT is None:
        raise Exception("QdrantClient was accessed but it is None")
    return QDRANT_CLIENT


def add_lyrics(lyrics: list[Lyrics]) -> None:
    client = get_qdrant_client()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[lyrics_to_point_struct(l) for l in lyrics],
    )


def lyrics_to_point_struct(lyrics: Lyrics) -> PointStruct:
    return PointStruct(
        id=str(uuid.uuid4()),
        vector=astuple(lyrics.prediction),
        payload=lyrics.dict_without_prediction,
    )
