import os
from flask import Flask

from .database import db
from app.notes import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    with app.test_request_context():
        models.init_db()

    import app.notes.controllers as notes
    import app.general.controllers as general

    app.register_blueprint(general.module)
    app.register_blueprint(notes.module)

    return app
