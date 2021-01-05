from flask import Blueprint, abort, request
from flask_restful import Api, Resource, reqparse

from azure_ingester_api.app import db
from . import models
from . import schemas

api_bp = Blueprint('api', __name__, url_prefix='/v1')
api_api = Api(api_bp)


def handle_success_response(schema, response, status=200):
    return schema.dump(response), status


asset_types_parser = reqparse.RequestParser()
asset_types_parser.add_argument("page", required=False, type=int, location="args", help="Page number to retrieve")
asset_types_parser.add_argument("perPage", required=False, type=int, location="args", help="Items per page to retrieve")


class AssetTypesHandler(Resource):
    def get(self):
        args = asset_types_parser.parse_args()
        page = args["page"]
        per_page = args["perPage"]

        asset_type = models.AssetType.retrieve_all_asset_types(page, per_page)
        if asset_type:
            response = models.DataAssetTypesPagedResponse(asset_types=asset_type, request=request)
            db.session.commit()
            return handle_success_response(schemas.AssetTypesResponseSchema(), response)
        else:
            db.session.rollback()
            abort(404)


class AssetTypeHandler(Resource):
    def get(self, typeId):
        type_id = typeId
        try:
            type_id = int(type_id)
        except ValueError:
            abort(404)
        asset_type = models.AssetType.retrieve_data_asset_type_by_id(type_id)
        if asset_type:
            response = models.DataAssetTypeResponse(asset_type)
            db.session.commit()
            return handle_success_response(schemas.AssetTypeResponseSchema(), response)
        else:
            db.session.rollback()
            abort(404)


api_api.add_resource(AssetTypesHandler, '/assetTypes')
api_api.add_resource(AssetTypeHandler, '/assetTypes/<typeId>')
