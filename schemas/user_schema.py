from marshmallow import Schema, fields, validates, ValidationError

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @validates('password')
    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password Should not be less than 6 characters')

    @validates('name')
    def validate_name(self, name):
        if len(name) < 2:
            raise ValidationError('Name is too short')
        if not name.replace(' ', '').isalpha():
            raise ValidationError('Name should only contain alphabets')
