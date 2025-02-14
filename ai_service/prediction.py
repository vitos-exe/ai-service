from dataclasses import asdict

from flask import Blueprint, request

from ai_service.ai_service import predict_lyrics

prediction_blueprint = Blueprint("prediction", __name__, url_prefix="/prediction")


@prediction_blueprint.route("", methods=["POST"])
def get_prediction():
    lyrics = request.get_json()["lyrics"]
    prediction = predict_lyrics([lyrics])[0]
    return asdict(prediction), 200


@prediction_blueprint.route("/batch", methods=["POST"])
def get_predictions():
    lyrics = [obj["lyrics"] for obj in request.get_json()]
    preds = predict_lyrics(lyrics)
    return [asdict(p) for p in preds], 200
