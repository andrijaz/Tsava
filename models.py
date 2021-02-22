from flask import  Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = "Tsava"
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username

    def __int__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

class Token(db.Model):
    """This table is used when resetting password.

    1. Create new entry when user requests to reset.
    2. Later when user recieves reset url with token, find token in DB.
    3. Use token and delete it from DB.
    """
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(10))
    # Set when token will expire/ not be valid
    # duration = db.Column(db.Integer)