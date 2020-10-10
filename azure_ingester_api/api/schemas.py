from marshmallow import Schema, fields, validate


# validation regex for integers
RE_INT_CHARS = "[-+]?[0-9]"
RE_INT_PATTERN = f'^{RE_INT_CHARS}+$'
RE_INT_PATTERN_ERROR = "Invalid input. Only integer values are allowed."
RE_INT_VALIDATOR = validate.Regexp(RE_INT_PATTERN, flags=0, error=RE_INT_PATTERN_ERROR)


class StatusSchema(Schema):
    status = fields.String(required=True)
    code = fields.Integer(required=True)
    messages = fields.List(fields.String(), required=True)


class AssetTypeSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


class AssetTypesResultSchema(Schema):
    assetTypes = fields.Nested(AssetTypeSchema, many=True, attribute='asset_type')


class AssetTypesResponseSchema(StatusSchema):
    result = fields.Nested(AssetTypesResultSchema)


class AssetTypeResultSchema(Schema):
    assetType = fields.Nested(AssetTypeSchema, attribute='asset_type')


class AssetTypeResponseSchema(StatusSchema):
    result = fields.Nested(AssetTypeResultSchema)