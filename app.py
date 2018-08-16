import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from views.users import Login, Signup

load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
api = Api(app)

        
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')


if __name__ == '__main__':
    app.run()