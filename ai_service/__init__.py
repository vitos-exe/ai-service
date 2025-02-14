import secrets

from flask import Flask

from ai_service.ai_service import create_model
from ai_service.config import DevConfig
from ai_service.db import create_qdrant_client, setup_qdrant
from ai_service.index import index_blueprint
from ai_service.prediction import prediction_blueprint


def create_app(app_config=None):
    app = Flask(__name__)
    app.secret_key = secrets.token_hex()

    app.config.from_object(app_config if app_config else DevConfig)

    with app.app_context():
        # create_model()
        create_qdrant_client()
        if app.config['SETUP_QDRANT']:
            setup_qdrant()

    app.register_blueprint(index_blueprint)
    app.register_blueprint(prediction_blueprint)

    return app
