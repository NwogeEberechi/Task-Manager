from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from models import User

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'todo-api-secret'
jwt = JWTManager(app)

api = Api(app)


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'Username field cannot be blank', required = True)
        parser.add_argument('password', help = 'Password field cannot be blank', required = True)
        data = parser.parse_args()
        
        current_user = None
        for user in User.users:
            current_user = user if user['username'] == data['username'] else current_user
        if not current_user:
            return {
                    'message': 'User not found, Login unsuccessful',
                    'status': 'unsuccessful',
                }, 404
        
        if data['password'] == current_user['password']:
            access_token = create_access_token(identity=current_user['username'])
            return {
                    'data': current_user,
                    'message': 'Login successful',
                    'status': 'success',
                    'token': access_token
                }, 200
        else:
            return {
                    'message': 'Wrong credentials',
                    'status': 'unsuccessful'
                }, 401

class Signup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'Username field cannot be blank', required = True)
        parser.add_argument('password', help = 'Password field cannot be blank', required = True)
        parser.add_argument('id', help = 'Id field cannot be blank', required = True)
        parser.add_argument('name', help = 'Name field cannot be blank', required = True)
        data = parser.parse_args()

        current_user = None
        for user in User.users:
            current_user = user if user['username'] == data['username'] else current_user
        if current_user:
            return {
                    'message': 'User {} already exist'.format(data['username']),
                    'status': 'unsuccessful',
                }, 404
    
        User.users.append(data)
        access_token = create_access_token(identity=data['username'])
        return {
                'data': data,
                'message': 'User Created',
                'status': 'success',
                'token': access_token
            }, 201 
        


api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')


if __name__ == '__main__':
    app.run()