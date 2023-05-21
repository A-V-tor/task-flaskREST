from marshmallow import Schema, fields, validate


class UserShcema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=50)])
    token = fields.UUID()


class TokenShcema(Schema):
    id = fields.Integer(dump_only=True)
    token = fields.UUID()
