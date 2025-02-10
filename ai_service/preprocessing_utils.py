import Stemmer
import re
import spacy

tokenizer = spacy.blank("en")
stemmer = Stemmer.Stemmer('english')


def clean(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(' +', ' ', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"^\d+ Contributors", "", text)
    text = re.sub(r"^(.*?)Lyrics", "", text, flags=re.MULTILINE)
    return text


def tokenize(text):
    tokens = tokenizer(text)
    tokens = [str(t).lower() for t in tokens if not t.is_stop]
    return [t for t in tokens if t.isalpha()]


def stem(tokens):
    return stemmer.stemWords(tokens)


def preprocess(text):
    text = clean(text)
    tokens = tokenize(text)
    return stem(tokens)
