from flask_restful import Resource, request
from flask_jwt_extended import create_access_token

from models.users import User
from schemas.user_schema import UserSchema
from utilities.response import Response

response = Response()

class Login(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        user_schema = UserSchema(only=['email', 'password'])
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
            res, code = response.success('Login successful', active_user.data, 200)
            res.update({ 'token': create_access_token(identity=active_user.data['email']) })
            return res, code
        else:
            return response.error('Wrong credentials', 401)

class Signup(Resource):
    def post(self):
        data = request.get_json(force=True)

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
        res, code = response.success('User created', new_user.data, 201)
        res.update({ 'token': create_access_token(identity=new_user.data['email']) })
        return res, code