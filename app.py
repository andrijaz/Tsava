from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from views import handle_login, handle_register, handle_profile, handle_new_pwd, handle_logout, handle_reset
from utils.utils import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# problems with postgres
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgresSava"
app.config['SECRET_KEY'] = "teamsava"
db = SQLAlchemy(app)




@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    return handle_login()


@app.route('/register', methods=["GET", "POST"])
def register():
    return handle_register()

@login_required
@app.route("/logout",  methods=["GET"])
def logout():
    return handle_logout()


@app.route("/reset",  methods=["GET", "POST"])
def reset():
    return handle_reset()

@app.route("/reset/new",  methods=["GET", "POST"])
def reset_new():
    return handle_new_pwd()

@login_required
@app.route('/profile',  methods=["GET"])
def profile():
    return handle_profile()


if __name__ == '__main__':
    db.create_all()
    app.run()
