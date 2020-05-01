from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from cbs.mysqldb import open_db, AccessDB
import functools
from cbs.models.User import User
import sys
from cbs.controllers.login import login
import urllib.parse
from cbs.models.BillingInfo import BillingInfo


blueprint = Blueprint('register',__name__, url_prefix='/')

@blueprint.route("/register")
def view_login():
    return(render_template('register.html'))


def checkRegistration(request, billing=False):
    messages = []
    if billing == True:
        messages = BillingInfo.checkBillingInfo(request)

    if "@" not in request.form['email']:
        messages.append("Invalid Email")
    
    if request.form['password'] != request.form['repassword']:
        sys.stderr.write(request.form['password']+"\t"+request.form['repassword']+"\n")
        messages.append("Passwords don't match")
    
    if len(request.form['password']) < 4 or len(request.form['password']) > 20:
        messages.append("Password must be between 4-20 characters")
    
    if len(request.form['firstname']) < 2 or len(request.form['firstname']) > 30 or len(request.form['lastname']) < 2 or len(request.form['lastname']) > 30:
        messages.append("names must be between 2-30 characters")
    
    return messages


def sendEmail(email):
    encrpyted_email = AccessDB.encrypt(email, current_app.config['URL_CIPHER_KEY'])
    confirm_id = urllib.parse.quote(encrpyted_email, safe='')
    mail = Mail(current_app)
    msg = Message( subject='CBS email confirmation',
                   sender = current_app.config['MAIL_USERNAME'],
                   recipients=[email],
                   body="Thank you for creating an account with CBS,"+
                        " please follow the link provided to activate your account."+
                        "http://localhost:5000/confirmEmail?id="+confirm_id)
    mail.send(msg)


@blueprint.route('/registered', methods=['GET','POST'])
def register():
    if request.method == "POST":
        db = open_db()
        user = User()
        user.populate_user_from_registration(request)
        for key in request.form.keys():
            print(key, ":" ,request.form[key])
        
        billing = False
        if 'billing' in request.form.keys():
            billing = True
        if billing:
            billingInfo = BillingInfo()
            billingInfo.populate_billing_from_registration(request)

        messages = checkRegistration(request, billing=billing)
        if len(messages) > 0:
            for message in messages:
                flash(message)
            return(render_template("register.html"))

        if user.is_unique(db):
            added = user.add_user_to_db(db, current_app.config['CIPHER_KEY'])
        else:
            flash("Email Already Registered")
            return(render_template('register.html'))

        if added:
            if billing:
                # get user id to add as foreign key to billing
                user.load_user_data(db, current_app.config['CIPHER_KEY'])
                uid = user.get_id()
                billing_added = billingInfo.add_billing_to_db(uid, db, current_app.config['CIPHER_KEY'])
            sendEmail(request.form['email'])
            return(render_template('regConfirm.html'))
        else:
            flash("Failed to Register...")
            return(render_template('register.html'))


@blueprint.route("/confirmEmail", methods=["GET"])
def confirm_email_login():
    if request.method == "GET" and request.args.get('id') is not None:
        encrypted_email = request.args.get('id')
        email = AccessDB.decrypt(encrypted_email, current_app.config['URL_CIPHER_KEY'])
        g.email_input = email
        flash("Please login to confirm your email")
        return(render_template('confirmEmail.html'))
    else:
        return(render_template('index.html'))



@blueprint.route("/confirmedEmail", methods=["POST"])
def confirm_email():
    if request.method == "POST":
        db = open_db()
        email = request.form['email']
        pw = request.form['password']
        user = User()
        user.create_user(email, pw)

        if user.is_authentic(db, current_app.config['CIPHER_KEY']):
            session.clear()
            user.load_user_data(db, current_app.config['CIPHER_KEY'])
            session['user_id'] = user.get_id()
            session['user_status'] = user.get_status()
            g.user = user
            if session['user_status'] != 2:
                user.activate_user(db)
                flash("Email confirmed!")
                return(redirect(url_for('index.view_index')))
            else:
                flash("Email confirmed!")
                return(render_template('admin.html'))
        else:
            flash("Email/Password is Incorrect")
            encrpyted_email = AccessDB.encrypt(email, current_app.config['URL_CIPHER_KEY'])
            confirm_id = urllib.parse.quote(encrpyted_email, safe='')
            return(redirect(url_for('register.confirm_email_login')+"?id="+confirm_id))

