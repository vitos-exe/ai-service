from dataclasses import asdict

from flask import Blueprint, request

from ai_service.ai_service import predict_lyrics

prediction_blueprint = Blueprint('prediction', __name__, url_prefix='/prediction')


@prediction_blueprint.route('', methods=['POST'])
def get_prediction():
    lyrics = request.json['lyrics']
    return asdict(predict_lyrics(lyrics)), 200
