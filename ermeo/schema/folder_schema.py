from marshmallow import Schema, fields
from ermeo.schema.common_schema import IdSchema


class ResourceSchema(Schema):
    type = fields.Str(default="document")


class FolderSchema(Schema):
    name = fields.Str(required=True)
    resource = fields.Nested(ResourceSchema, required=True)
    parent = fields.Nested(IdSchema)
