from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.users import User
from schemas.user_schema import UserSchema
from utilities.response import Response

response = Response()
parser = reqparse.RequestParser()
parser.add_argument('email', help = 'email field cannot be blank', required = True)
parser.add_argument('password', help = 'Password field cannot be blank', required = True)

class Login(Resource):
    def post(self):
        data = parser.parse_args()
        
        user_schema = UserSchema()
        result = user_schema.load(data)
        if result.errors:
            return response.error(result.errors, 400)
        
        current_user = None
        for user in User.users:
            if user['email'] == data['email']:
                current_user = user
                break
        
        if not current_user:
            return response.error('User not found, Login unsuccessful', 403)
        
        if data['password'] == current_user['password']:
            user_schema = UserSchema(exclude=['password'])
            active_user = user_schema.dump(current_user)
            token = create_access_token(identity=active_user.data['email'])
            return response.success('Login successful', active_user.data, token, 200)
        else:
            return response.error('Wrong credentials', 401)

class Signup(Resource):
    def post(self):
        signup_parser = parser.copy()
        signup_parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        data = signup_parser.parse_args()

        user_schema = UserSchema()
        result = user_schema.load(data)
        if result.errors:
            return response.error(result.errors, 400)
        
        current_user = None
        for user in User.users:
            if user['email'] == data['email']:
                current_user = user
                break
        if current_user:
            return response.error('User already exist', 409)

        data['id'] = len(User.users) + 1
        User.users.append(data)
        user_schema = UserSchema(exclude=['password'])
        new_user = user_schema.dump(data)
        token = create_access_token(identity=new_user.data['email'])
        return response.success('User created', new_user.data, token, 201)