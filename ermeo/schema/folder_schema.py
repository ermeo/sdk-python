from marshmallow import Schema, fields


class ResourceSchema(Schema):
    type = fields.Str(default="document")


class ParentSchema(Schema):
    id = fields.Str(required=True)


class FolderSchema(Schema):
    name = fields.Str(required=True)
    resource = fields.Nested(ResourceSchema, required=True)
    parent = fields.Nested(ParentSchema)
