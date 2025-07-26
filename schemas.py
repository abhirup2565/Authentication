from marshmallow import fields,Schema

class userSchema(Schema):
    id=fields.String()
    username=fields.String()
    email=fields.String()