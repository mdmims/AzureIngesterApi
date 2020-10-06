from flask import Blueprint, Request, abort
from flask_restful import Api, Resource
from azure_ingester_api.app import db
from . import models
from . import schemas


api_bp = Blueprint('api', __name__, url_prefix='/v1')
api_api = Api(api_bp)


def handle_success_response(schema, response, status=200):
    return schema.dump(response), status


class AssetTypesHandler(Resource):
    @staticmethod
    def get():
        asset_type = models.AssetType.retrieve_all_data_asset_types()
        if asset_type:
            response = models.DataAssetTypeResponse(asset_type)
            db.session.commit()
            return handle_success_response(schemas.AssetTypesResponseSchema(), response)
        else:
            db.session.rollback()
            abort(404)


api_api.add_resource(AssetTypesHandler, '/AssetTypes')
