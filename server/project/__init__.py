import json

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pathlib import Path


QUESTIONS = []

# setup extensions
socketio = SocketIO()


def create_app(script_info=None):

    app = Flask(__name__)
    CORS(app)
    setup_blueprints(app)

    # setup extensions
    socketio.init_app(app)

    setup_questions()

    return app


def setup_blueprints(app):
    from project.routes.api import api_bp
    from project.routes import main as socket_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(socket_bp)


def setup_questions():
    global QUESTIONS

    file = Path(__file__, "../../project/externals/questions.json").resolve()
    with open(file) as f:
        data = json.load(f)
    for q in data["question"]:
        QUESTIONS.append(q['text'])
