from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from models import User

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'todo-api-secret'
jwt = JWTManager(app)

api = Api(app)



parser = reqparse.RequestParser()
parser.add_argument('username', help = 'Username field cannot be blank', required = True)
parser.add_argument('password', help = 'Password field cannot be blank', required = True)

class UserLogin(Resource):
    def post(self):
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


api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    app.run()