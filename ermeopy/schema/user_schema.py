from marshmallow import Schema, fields, validate
from ermeopy.schema.common_schema import IdSchema

type_enum = ['document', 'asset', 'intervention', 'user', 'report']


class UserSchema(Schema):
    username = fields.Str()
    code = fields.Str()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str()
    timezone = fields.Str(required=True)
    is_enabled = fields.Bool()
    teams = fields.List(fields.Nested(IdSchema))
    attributes = fields.List(fields.Nested(IdSchema))
    role = fields.Nested(IdSchema)
    workspaces_available = fields.List(fields.Nested(IdSchema))
    locale = fields.Str()


class UserSchemaUpdate(Schema):
    code = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    timezone = fields.Str()
    is_enabled = fields.Bool()
    teams = fields.List(fields.Nested(IdSchema))
    attributes = fields.List(fields.Nested(IdSchema))
    role = fields.Nested(IdSchema)
    workspaces_available = fields.List(fields.Nested(IdSchema))
    locale = fields.Str()


class RoleSchema(Schema):
    code = fields.Str()
    name = fields.Str(required=True)
    enabled = fields.Bool(default=True)
    platform_permission = fields.List(fields.Int())
    app_permission = fields.List(fields.Int())


class RoleSchemaUpdate(Schema):
    code = fields.Str()
    name = fields.Str()
    enabled = fields.Bool()
    platform_permission = fields.List(fields.Int())
    app_permission = fields.List(fields.Int())


class AccessRightSchema(Schema):
    code = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str()
    type = fields.Str(validate=[validate.OneOf(type_enum)])
    full_access = fields.Bool()
    full_write = fields.Bool()
    hidden = fields.Bool()


class AccessRightSchemaUpdate(Schema):
    code = fields.Str()
    name = fields.Str()
    description = fields.Str()
    type = fields.Str(validate=[validate.OneOf(type_enum)])
    full_access = fields.Bool()
    full_write = fields.Bool()
    hidden = fields.Bool()


class TeamSchema(Schema):
    code = fields.Str()
    name = fields.Str(required=True)
    users = fields.List(fields.Nested(IdSchema))
    leaders = fields.List(fields.Nested(IdSchema))
    access_rights = fields.List(fields.Nested(IdSchema))


class TeamSchemaUpdate(Schema):
    code = fields.Str()
    name = fields.Str(required=True)
    users = fields.List(fields.Nested(IdSchema))
    leaders = fields.List(fields.Nested(IdSchema))
    access_rights = fields.List(fields.Nested(IdSchema))
