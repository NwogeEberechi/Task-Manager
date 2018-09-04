from app import db

class User(db.Model):
    """This class represents the user table."""
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True) 
    name = db.Column('name', db.String())
    email = db.Column('email', db.String(), unique=True)
    password = db.Column(db.Text)

    def __init__(self, name, email, password):
        """initialize with name, email and password"""
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        """saves a new user to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()
