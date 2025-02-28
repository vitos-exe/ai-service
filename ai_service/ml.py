from abc import ABC, abstractmethod
from functools import cached_property

import gensim.downloader
import numpy as np
import torch
from flask import current_app

from ai_service.model import Prediction, RawLyrics
from ai_service.nn_definition import SentimentDNNCore
from ai_service.preprocessing_utils import clean, tokenize


class SentimentModel(ABC):
    @abstractmethod
    def predict_lyrics(self, lyrics: list[RawLyrics]) -> list[Prediction]:
        pass


SENTIMENT_MODEL: SentimentModel = None


def create_model():
    global SENTIMENT_MODEL
    SENTIMENT_MODEL = SentimentDNN()


class SentimentDNN(SentimentModel):
    MODEL_PATH_TEMPLATE = "models/{name}.pt"
    WORD2VEC_NAME = "word2vec-google-news-300"

    def __init__(self):
        self.model = SentimentDNNCore()
        self.model.load_state_dict(
            torch.load(
                SentimentDNN.MODEL_PATH_TEMPLATE.format(name=SentimentDNNCore.name),
                weights_only=True,
            )
        )

        # If we are not testing, we should load word2vec immediately
        if not current_app.testing:
            self._word2vec()

    @cached_property
    def _word2vec(self):
        return gensim.downloader.load(SentimentDNN.WORD2VEC_NAME)

    def get_sentence_embedding(
        self, sentence: str, vector_size: int = 300
    ) -> np.ndarray:
        tokens = tokenize(clean(sentence))
        vectors = [self._word2vec[word] for word in tokens if word in self._word2vec]
        if len(vectors) == 0:
            return np.zeros(vector_size)
        return np.mean(vectors, axis=0)

    def predict_lyrics(self, lyrics: list[RawLyrics]) -> list[Prediction]:
        embeddings = np.array([self.get_sentence_embedding(lr.lyrics) for lr in lyrics])
        X = torch.from_numpy(embeddings).float()
        preds = self.model(X).detach().numpy()
        return [Prediction(*[p.item() for p in pred]) for pred in preds]
