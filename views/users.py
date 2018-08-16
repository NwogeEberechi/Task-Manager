import re

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.users import User

EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

parser = reqparse.RequestParser()
parser.add_argument('email', help = 'email field cannot be blank', required = True)
parser.add_argument('password', help = 'Password field cannot be blank', required = True)

class Login(Resource):
    def post(self):
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
        
        if not current_user:
            return {
                    'message': 'User not found, Login unsuccessful',
                    'status': 'error',
                }, 403
        
        if data['password'] == current_user['password']:
            access_token = create_access_token(identity=current_user['email'])
            return {
                    'data': {
                        'id': current_user['id'],
                        'name': current_user['name'],
                        'email': current_user['email']
                    },
                    'message': 'Login successful',
                    'status': 'success',
                    'token': access_token
                }, 200
        else:
            return {
                    'message': 'Wrong credentials',
                    'status': 'error'
                }, 401

class Signup(Resource):
    def post(self):
        #parser = reqparse.RequestParser()
        #parser.add_argument('email', help = 'email field cannot be blank', required = True)
        #parser.add_argument('password', help = 'Password field cannot be blank', required = True)
        #parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        signup_parser = parser.copy()
        signup_parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        data = signup_parser.parse_args()

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
                }, 409

        data['id'] = len(User.users) + 1
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