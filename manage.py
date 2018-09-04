
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from app import db, app
from models.users import User


migrate = Migrate(app, db)


manager = Manager(app)

class Hello(Command):
    "prints hello world"

    def run(self):
        print ("hello world")

manager.add_command('test', Hello())
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()