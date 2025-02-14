import secrets
from dataclasses import astuple

from flask import Flask

from ai_service.config import DevConfig
from ai_service.db import add_lyrics, create_qdrant_client, setup_qdrant
from ai_service.lyrics_reader import read_lyrics_from_csv
from ai_service.ml import create_model, predict_lyrics
from ai_service.model import combine_raw_lyrics_and_prediction
from ai_service.prediction import prediction_blueprint


def create_app(app_config=None):
    app = Flask(__name__)
    app.secret_key = secrets.token_hex()

    app.config.from_object(app_config if app_config else DevConfig)

    with app.app_context():
        create_model()
        create_qdrant_client()
        setup_qdrant()

    @app.cli.command("populate_db")
    def populate_db():
        raw_lyrics = read_lyrics_from_csv()
        breakpoint()
        predictions = predict_lyrics([l.lyrics for l in raw_lyrics])
        breakpoint()
        lyrics = [
            combine_raw_lyrics_and_prediction(rl, p)
            for rl, p in zip(raw_lyrics, predictions)
        ]
        add_lyrics(lyrics)

    @app.route("/")
    def index():
        return "Hello world", 200

    app.register_blueprint(prediction_blueprint)

    return app
