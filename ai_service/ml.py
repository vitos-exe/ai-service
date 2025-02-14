import gensim.downloader
import numpy as np
import torch
from gensim.models import KeyedVectors

from ai_service.model import Prediction
from ai_service.nn_definition import SentimentDNN
from ai_service.preprocessing_utils import clean, tokenize

MODEL_PATH_TEMPLATE = "models/{name}.pt"
WORD2VEC_NAME = "word2vec-google-news-300"

MODEL: SentimentDNN = None
WORD2VEC_MODEL: KeyedVectors = None


def create_model() -> None:
    global MODEL, WORD2VEC_MODEL

    MODEL = SentimentDNN()
    MODEL.load_state_dict(
        torch.load(MODEL_PATH_TEMPLATE.format(name=MODEL.name), weights_only=True)
    )
    WORD2VEC_MODEL = gensim.downloader.load(WORD2VEC_NAME)


def predict_lyrics(lyrics: list[str]) -> list[Prediction]:
    X = torch.tensor(np.array([get_sentence_embedding(l) for l in lyrics])).float()
    preds = MODEL(X).detach().numpy()
    return [Prediction(*[p.item() for p in pred]) for pred in preds]


def get_sentence_embedding(sentence: str, vector_size: int = 300) -> np.ndarray:
    tokens = tokenize(clean(sentence))
    vectors = [WORD2VEC_MODEL[word] for word in tokens if word in WORD2VEC_MODEL]
    if len(vectors) == 0:
        return np.zeros(vector_size)
    return np.mean(vectors, axis=0)
