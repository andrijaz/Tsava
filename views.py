from random import randint

from flask import render_template, request, redirect, session, flash
from models import User, db, Token
from utils.utils import send_email


def handle_login():
    """When user logs in. Create session and save username. Later we will use this in /profile."""
    message = None
    if request.method == "POST":
        session.permanent = True
        username, password = request.form["username"], request.form["password"]
        session['username'] = username

        user = User.query.filter_by(username=username).first_or_404()
        # Validate user during login
        if not user:
            return render_template("login_page.html", message="Wrong username")
        if user.password != password:
            return render_template("login_page.html", message="Wrong password")
        return redirect("/profile")

    return render_template("login_page.html", message=message)


def handle_register():
    if request.method == "POST":
        username, password, email = request.form["username"], request.form["password"], request.form["email"]
        new_user = User(username=username, password=password, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            return "There was error" + str(e)
    else:
        return render_template("register_page.html")


def handle_profile():
    name = session.get("username")
    if not name:
        return redirect("/")
    user = User.query.filter_by(username=name).first_or_404()
    return render_template("profile_page.html", user=user)


def handle_logout():
    session.clear()
    return redirect('/')


def handle_reset():
    message = reset_url = None
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first_or_404()
        if not user:
            message = "No user with this email"
        else:
            token = str(randint(1000, 10000))
            new_Token = Token(email=email, token=token)
            try:
                db.session.add(new_Token)
                db.session.commit()
            except:
                message = "something went wrong"
                return render_template("reset_page.html", message=message)
            reset_url = "/reset/new?token=" + token

            send_email(email, reset_url)
            message = f"Check email <b>{email}</b> with reset url"

    return render_template("reset_page.html", message=message, reset_url=reset_url)


def handle_new_pwd():
    """
        User recedes reset url in email in format "something.com/token=312".
        We take that token, find email that created it and perform password update.
        If token does not exist we should throw error.

    :return:
    """
    if request.method == "POST":
        token_string = str(request.query_string).split("=")[1].strip("\'")
        token_object = Token.query.filter_by(token=token_string)
        new_password = request.form.get("password")

        user = User.query.filter_by(email=token_object.email).first_or_404()
        user.password = new_password
        db.session.delete(token_object)
        db.session.commit()
        redirect("/login")
    return render_template("new_pwd_page.html")
