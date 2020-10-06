from flask import Blueprint, current_app
from flask_restful import Api, Resource
from .models import HelloWorld
from .schemas import helloworlds_schema


healthz_bp = Blueprint('healthz', __name__, url_prefix='/healthz')
api = Api(healthz_bp)


class PingResource(Resource):
    def get(self):
        current_app.logger.info('Running Ping Resource')
        return {'status': 'OK', 'data': 'PONG!'}, 200


class HelloWorldResource(Resource):
    def get(self):
        helloworld_phrases = HelloWorld.retrieve_all()
        helloworld_phrases = helloworlds_schema.dump(helloworld_phrases)
        return {'status': 'OK', 'data': helloworld_phrases}, 200


# Configure resources
api.add_resource(PingResource, '/ping')
api.add_resource(HelloWorldResource, '/helloworld')
