from marshmallow import Schema, fields

class URLSchema(Schema):
    url = fields.URL(required=True)