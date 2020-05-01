from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
import functools
import sys
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing

blueprint = Blueprint('report',__name__, url_prefix='/')

@blueprint.route("/report")
def view_admin():
    if g.user is not None and g.user.status == 2:
        return(render_template('report.html'))
    else:
        flash("only admins can access this page, please log into an admin account")
        return(render_template('login.html'))