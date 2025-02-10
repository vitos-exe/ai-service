import gensim.downloader
import numpy as np
import torch

from ai_service.model.prediction import Prediction
from ai_service.model_definitions.dnn import SentimentDNN
from ai_service.preprocessing_utils import tokenize, clean

MODEL_PATH_TEMPLATE = 'models/{name}.pt'
WORD2VEC_NAME = 'word2vec-google-news-300'

MODEL: SentimentDNN = None
WORD2VEC_MODEL: gensim.models.KeyedVectors = None


def populate_model() -> None:
    global MODEL, WORD2VEC_MODEL

    MODEL = SentimentDNN()
    MODEL.load_state_dict(torch.load(MODEL_PATH_TEMPLATE.format(name=MODEL.name), weights_only=True))
    WORD2VEC_MODEL = gensim.downloader.load(WORD2VEC_NAME)


def predict_lyrics(lyrics: str) -> Prediction:
    X = torch.tensor([get_sentence_embedding(lyrics)])
    preds = MODEL(X).detach().numpy()[0]
    return Prediction(*[p.item() for p in preds])


def get_sentence_embedding(sentence, vector_size=300):
    tokens = tokenize(clean(sentence))
    vectors = [WORD2VEC_MODEL[word] for word in tokens if word in WORD2VEC_MODEL]
    if len(vectors) == 0:
        return np.zeros(vector_size)
    return np.mean(vectors, axis=0)
