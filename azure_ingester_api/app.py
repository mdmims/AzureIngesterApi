from flask import Flask
import logging
from flask_marshmallow import Marshmallow
from secure import SecureHeaders
from flask_httpauth import HTTPTokenAuth
from .config import DATA_HUB_MODEL_ENVIRONMENT

from .api.models import db as model_db

db = model_db

ma = Marshmallow()
secure_headers = SecureHeaders()
auth_token = HTTPTokenAuth('Bearer')


def create_app(environment_config=None):
    app = Flask(__name__)
    configure_app(app, environment_config)
    if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        app.config['SQLALCHEMY_POOL_SIZE'] = 20
        app.config['SQLALCHEMY_POOL_RECYCLE'] = 600
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'fast_executemany': True}
    configure_db(app)
    configure_blueprints(app)
    configure_logging(app)
    return app


def configure_db(app):
    db.init_app(app)


def configure_app(app, environment_config=DATA_HUB_MODEL_ENVIRONMENT):
    app.config.from_object(environment_config)


def configure_blueprints(app):
    from .healthz import healthz_bp
    app.register_blueprint(healthz_bp)

    from .api.resources import api_bp
    app.register_blueprint(api_bp)


def configure_logging(app):
    logging.getLogger('sqlalchemy')
