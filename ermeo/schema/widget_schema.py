from marshmallow import Schema, fields, validate

type_enum = ['action', 'multiple_choice', 'picture_choice', 'ab_choice', 'array', 'yes_no', 'opinion_scale',
             'location', 'phone_information', 'photo', 'signature', 'text', 'date', 'number', 'barcode', 'duration',
             'rating', 'send_emails', 'phone', 'image', 'asset', 'section', 'repeat_section', 'transfer', 'end_send', 'text_information', 'duration_information'
             'number_information', 'pdf', 'web_page', 'template', 'document', 'tools', 'hour']
category_enum = ['task', 'organization', 'information']


class SettingSchema(Schema):
    min = fields.Float()
    max = fields.Float()
    duplicate_answer = fields.Bool()
    wording_repeat = fields.Str()
    wording_delete = fields.Str()
    wording_end = fields.Str()


class WidgetSchema(Schema):
    code = fields.Str()
    name = fields.Str(required=True)
    icon = fields.Str(required=True)
    category = fields.Str(validate=[validate.OneOf(category_enum)])
    type = fields.Str(required=True, validate=[validate.OneOf(type_enum), ])
        
    settings = fields.Nested(SettingSchema)
