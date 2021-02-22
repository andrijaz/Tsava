from functools import wraps

from flask import session, flash, redirect
from rq.decorators import job
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from job import r as redis_conn


def login_required(f):
    """Decorator to create protected routes."""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect('/')
    return wrap


@job('low', connection=redis_conn, timeout=5)
def send_email(email, reset_url):
    """Should be async/using redis Q for example."""

    message = Mail(
        from_email='myemail@example.com',
        to_emails=email,
        subject='Reset passwrod',
        html_content=f'Click this link<strong>{reset_url}</strong>')
    try:
        sg = SendGridAPIClient('SENDGRID_API_KEY')
        response = sg.send(message)

    except Exception as e:
        return "Error:" + str(e)
