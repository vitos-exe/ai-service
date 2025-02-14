import secrets

from flask import Flask, jsonify

from ai_service import config, db, lyrics_reader, ml, model, prediction


def create_app(app_config=None):
    app = Flask(__name__)
    app.secret_key = secrets.token_hex()

    app.config.from_object(app_config if app_config else DevConfig)

    with app.app_context():
        ml.create_model()
        db.create_qdrant_client()
        db.setup_qdrant()

    @app.cli.command("populate_db")
    def populate_db():
        raw_lyrics = lyrics_reader.read_lyrics_from_csv()
        predictions = ml.predict_lyrics([l.lyrics for l in raw_lyrics])
        lyrics = [
            model.combine_raw_lyrics_and_prediction(rl, p)
            for rl, p in zip(raw_lyrics, predictions)
        ]
        db.add_lyrics(lyrics)

    @app.route("/health", methods=["GET"])
    def health_check():
        return (jsonify(status="healthy"),)

    app.register_blueprint(prediction.prediction_blueprint)

    return app
