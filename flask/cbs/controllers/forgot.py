from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
import functools
from cbs.models.User import User, email_exists
from cbs.mysqldb import open_db
from random import randint
from flask_mail import Mail, Message

blueprint = Blueprint('forgot',__name__, url_prefix='/')

@blueprint.route("/forgot")
def view_forgot():
    return(render_template('forgot.html'))

@blueprint.route("/passwordSent", methods=["POST"])
def send_forgot():
    if request.method == "POST":
        db = open_db()
        email = request.form['email']
        if email_exists(email, db):
            user = User()
            user.load_by_email(db, email)
            password = generate_password(12)
            user.update_profile_info(db, new_pass = password, key=current_app.config['CIPHER_KEY'])
            sendNewPassword(email, password)
            flash("Email Sent")
            return (render_template("login.html"))
        else:
            flash("Email does not exist in system, please register an account")
            return(render_template("forgot.html"))



def sendNewPassword(email, password):
    mail = Mail(current_app)
    msg = Message( subject='CBS password reset',
                   sender = current_app.config['MAIL_USERNAME'],
                   recipients=[email],
                   body="Your password for the CBS system has been reset to "+password+" Please login and change you password.")
    mail.send(msg)


def generate_password(length):
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    indices = []
    for x in range(length):
        rn = randint(0,len(chars)-1)
        indices.append(rn)
    
    password = ""
    for idx in indices:
        password+= chars[idx]
    
    return password
