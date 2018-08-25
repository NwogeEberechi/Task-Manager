from flask import Flask
from flask_script import Manager, Command

app = Flask(__name__)
# configure your app

manager = Manager(app)

class Hello(Command):
    "prints hello world"

    def run(self):
        print ("hello world")

manager.add_command('test', Hello())

if __name__ == "__main__":
    manager.run()