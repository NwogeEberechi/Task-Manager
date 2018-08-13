import re

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from models.users import User

EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

class Signup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'email field cannot be blank', required = True)
        parser.add_argument('password', help = 'Password field cannot be blank', required = True)
        parser.add_argument('id', help = 'Id field cannot be blank', required = True)
        parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        data = parser.parse_args()

        if not EMAIL_REGEX.match(data['email']):
            return {
                    'message': 'invalid email',
                    'status': 'error',
                }, 400

        if len(data['password']) < 6:
            return {
                    'message': 'Password Should not be less than 6 characters',
                    'status': 'error',
                }, 400
        
        current_user = None
        for user in User.users:
            if user['email'] == data['email']:
                current_user = user
                break
        if current_user:
            return {
                    'message': 'User {} already exist'.format(data['email']),
                    'status': 'error',
                }, 404
    
        User.users.append(data)
        access_token = create_access_token(identity=data['email'])
        return {
                'data': {
                    'id': data['id'],
                    'name': data['name'],
                    'email': data['email']
                },
                'message': 'User Created',
                'status': 'success',
                'token': access_token
            }, 201 