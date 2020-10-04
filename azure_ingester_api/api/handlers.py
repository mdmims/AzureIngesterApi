from flask import Blueprint
from flask_restful import Api
from azure_ingester_api.app import db

api_bp = Blueprint('api', __name__, url_prefix='/v1')
api_api = Api(api_bp)
