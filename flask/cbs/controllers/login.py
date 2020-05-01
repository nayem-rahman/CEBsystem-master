from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
import functools
from cbs.models.User import User
from cbs.mysqldb import open_db


blueprint = Blueprint('login',__name__, url_prefix='/')

@blueprint.route("/login")
def view_login():
    return(render_template('login.html'))

@blueprint.route('/loggedin', methods=['GET','POST'])
def login():
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
            if session['user_status'] == 0:
                g.user = None
                session.clear()
                flash("Account Inactive, Check confirmation email")
                return(render_template('login.html'))
            if session['user_status'] == 1:
                return(redirect(url_for('index.view_index')))
            elif session['user_status'] == 2:
                return(redirect(url_for('admin.view_admin')))
            else:
                g.user = None
                session.clear()
                flash("Account Suspended")
                return(render_template('login.html'))
        else:
            session.clear()
            flash("Email/Password is Incorrect")
            g.email_input = email
            return(render_template('login.html'))


@blueprint.route('/logout')
def logout():
    g.user = None
    session.clear()
    return(redirect(url_for('index.view_index')))

@blueprint.before_app_request
def init_logged_in():
    user_id = session.get('user_id')
    if user_id is not None:
        db = open_db()
        user = User()
        user.load_by_id(db, user_id)
        g.user = user
    else:
        g.user = None



def require_login(view):
    @functools.wraps(view)
    def view_wrapper(**kwargs):
        if g.user is None:
            return(render_template('login.html'))
        else:
            return(view(**kwargs))
    
    return(view_wrapper)




