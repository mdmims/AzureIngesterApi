import re
from urllib.parse import unquote

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


class PageSchema(Schema):
    page = fields.Integer(required=True, attribute="pagination_obj.page")
    totalPages = fields.Integer(required=True, attribute="pagination_obj.pages")
    totalItems = fields.Integer(required=True, attribute="pagination_obj.total")
    perPage = fields.Integer(required=True, attribute="pagination_obj.per_page")
    hasNext = fields.Boolean(required=True, attribute="pagination_obj.has_next")
    nextPageNum = fields.Integer(required=True, attribute="pagination_obj.next_num")
    prevPageNum = fields.Integer(required=True, attribute="pagination_obj.prev_num")
    hasPrev = fields.Boolean(required=True, attribute="pagination_obj.has_prev")
    nextPage = fields.Method("get_next_page")
    prevPage = fields.Method("get_prev_page")

    def get_next_page(self, obj):
        return self.get_pages(obj, "next")

    def get_prev_page(self, obj):
        return self.get_pages(obj, "previous")

    def get_pages(self, obj, target_field):
        if all(key in obj for key in ("pagination_obj", "request")):
            p = obj["pagination_obj"]
            r = obj["request"]

            _full_path = str(unquote(r.full_path))
            output = {}

            if "page" in r.values:
                page = r.values["page"]
            else:
                sep = "&" if "?" in _full_path else "?"
                _full_path += sep + "page=1"
                _full_path = _full_path.replace("?&", "?")
                page = 1

            if p.has_prev:
                output["previous"] = re.sub(f"page={page}", f"page={p.prev_num}", _full_path)
            if p.has_next:
                output["next"] = re.sub(f"page={page}", f"page={p.next_num}", _full_path)

        return output.get(target_field)


class AssetTypeSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


class AssetTypesResultSchema(Schema):
    assetTypes = fields.Nested(AssetTypeSchema, many=True, attribute='asset_type')
    page = fields.Nested(PageSchema, attribute="page")


class AssetTypesResponseSchema(StatusSchema):
    result = fields.Nested(AssetTypesResultSchema)


class AssetTypeResultSchema(Schema):
    assetType = fields.Nested(AssetTypeSchema, attribute='asset_type')


class AssetTypeResponseSchema(StatusSchema):
    result = fields.Nested(AssetTypeResultSchema)
