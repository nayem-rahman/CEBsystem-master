from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from cbs.mysqldb import open_db
from cbs.models.Promo import Promo
from cbs.models.User import User, get_subscribed_emails, get_all_users
from cbs.controllers.editMovie import checkEditMovieRequest
from cbs.models.Movie import Movie, get_all_movies
import functools
import sys


blueprint = Blueprint('manageUsers',__name__, url_prefix='/')

@blueprint.route("/manageUsers")
def view_manageUsers():
    if g.user is not None and g.user.status == 2:
        db = open_db()
        g.all_users = get_all_users(db)
        g.user_len = len(g.all_users)
        g.user_status = []
        for user in g.all_users:
            if user.status == 0:
                g.user_status.append("Inactive User")
            elif user.status == 1:
                g.user_status.append("Active User")
            elif user.status == 2:
                g.user_status.append("Admin")
            elif user.status >= 3:
                g.user_status.append("Suspended User")
        return(render_template('manageUsers.html'))

@blueprint.route("/suspendUser", methods=["GET"])
def suspend_user():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        user_id = int(request.args.get('id'))
        db = open_db()
        user = User()
        user.load_by_id(db, user_id)
        user.suspend_user(db)
        return(redirect(url_for('manageUsers.view_manageUsers')))

@blueprint.route("/unsuspendUser", methods=["GET"])
def unsuspend_user():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        user_id = int(request.args.get('id'))
        db = open_db()
        user = User()
        user.load_by_id(db, user_id)
        user.unsuspend_user(db)
        return(redirect(url_for('manageUsers.view_manageUsers')))
