from flask import Flask

from ai_service.ai_service import populate_model
from ai_service.index import index_blueprint
from ai_service.prediction import prediction_blueprint

app = Flask(__name__)

with app.app_context():
    populate_model()

app.register_blueprint(index_blueprint)
app.register_blueprint(prediction_blueprint)
