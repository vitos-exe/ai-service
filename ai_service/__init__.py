import secrets
from dataclasses import asdict

from flask import Flask, jsonify, request

from ai_service import db, lyrics_reader, ml, model


def create_app(app_config="ai_service.config.DevConfig"):
    app = Flask(__name__)
    app.secret_key = secrets.token_hex()
    app.config.from_object(app_config)

    @app.cli.command("populate_db")
    def populate_db():
        raw_lyrics = lyrics_reader.read_lyrics(app.config["LYRICS_DATA_FORMAT"])
        predictions = ml.SENTIMENT_MODEL.predict_lyrics(raw_lyrics)
        lyrics = [
            model.combine_raw_lyrics_and_prediction(rl, p)
            for rl, p in zip(raw_lyrics, predictions)
        ]
        db.add_lyrics(lyrics)

    @app.get("/health")
    def health_check():
        return jsonify(status="healthy"), 200

    @app.post("/")
    def get_prediction():
        save = request.args.get("save")
        raw_lyrics = model.RawLyrics(**request.get_json())
        prediction = ml.SENTIMENT_MODEL.predict_lyrics([raw_lyrics])[0]
        if save:
            db.add_lyrics(
                [model.combine_raw_lyrics_and_prediction(raw_lyrics, prediction)]
            )
        return asdict(prediction), 200

    @app.post("/batch")
    def get_predictions():
        save = request.args.get("save")
        lyrics = [model.RawLyrics(**obj) for obj in request.get_json()]
        preds = ml.SENTIMENT_MODEL.predict_lyrics(lyrics)
        if save:
            db.add_lyrics(
                [
                    model.combine_raw_lyrics_and_prediction(lyr, pred)
                    for lyr, pred in zip(lyrics, preds)
                ]
            )
        return [asdict(p) for p in preds], 200

    @app.post("/closest")
    def get_closest():
        pred = model.Prediction(**request.get_json())
        closest = db.search_n_closest(pred, n=1)
        return jsonify(closest)

    with app.app_context():
        ml.create_model()
        db.create_qdrant_client()

    return app
