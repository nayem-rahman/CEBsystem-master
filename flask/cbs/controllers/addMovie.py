from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
from cbs.models.Movie import Movie
from cbs.controllers.editMovie import checkEditMovieRequest
import functools
import sys


blueprint = Blueprint('addMovie',__name__, url_prefix='/')

@blueprint.route("/addMovie")
def view_addMovie():
    return(render_template('addMovie.html'))

@blueprint.route("/movieAdded", methods=['POST'])
def addMovie():
    db = open_db()
    movie = Movie()
    messages = checkEditMovieRequest(request)
    if len(messages) > 0:
        for message in messages:
            flash(message)
        return(render_template('addMovie.html'))
    movie.populate_movie_by_request(request)
    if movie.isUnique(db):
        movie.add_movie_to_db(db)
        flash("Movie Added Successfully")
        return(redirect(url_for('admin.view_admin')))
    else:
        flash("Movie with title already exists")
        return(render_template('addMovie.html'))
