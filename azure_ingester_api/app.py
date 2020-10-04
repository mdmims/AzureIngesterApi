from flask import Flask
import logging
from flask_marshmallow import Marshmallow
from .config import API_ENVIRONMENT

from .api.models import db as model_db

db = model_db

ma = Marshmallow()


def create_app(environment_config=None):
    app = Flask(__name__)
    configure_app(app, environment_config)
    configure_db(app)
    configure_blueprints(app)
    configure_logging(app)
    return app


def configure_db(app):
    db.init_app(app)


def configure_app(app, environment_config=API_ENVIRONMENT):
    app.config.from_object(environment_config)


def configure_blueprints(app):
    from .healthz import healthz_bp
    app.register_blueprint(healthz_bp)

    from .api.handlers import api_bp
    app.register_blueprint(api_bp)


def configure_logging(app):
    logging.getLogger('sqlalchemy')
