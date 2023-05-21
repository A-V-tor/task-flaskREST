from marshmallow import Schema, fields, validate


class QuestionSchema(Schema):
    questions_num = fields.Int(required=True, validate=validate.Range(min=1))


class QuizSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_question = fields.Integer()
    question_created_at = fields.DateTime()
    question = fields.String(validate=[validate.Length(max=255)])
    answer = fields.String(validate=[validate.Length(max=255)])
