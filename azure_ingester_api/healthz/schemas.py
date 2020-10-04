from marshmallow import Schema, fields


class HelloWorldSchema(Schema):
    id = fields.String(required=True)
    saying = fields.String(required=True)


helloworld_schema = HelloWorldSchema()
helloworlds_schema = HelloWorldSchema(many=True)
