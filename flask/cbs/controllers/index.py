from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
import functools
import sys


blueprint = Blueprint('index',__name__, url_prefix='/')

@blueprint.route("/")
def view_index():
    if g.user and g.user.get_status() == 2:
        return(redirect(url_for('admin.view_admin')))
    db = open_db()
    movies = get_all_movies(db)
    movies_showing = []
    coming_soon = []
    for movie in movies:
        showing = Showing()
        movie_current_showings = showing.get_movie_current_showings(db,movie.id, current_app.config['CURR_DATE'])

        if len(movie_current_showings) > 0:
            movies_showing.append(movie)
            print(movie.name,"SHOWING")
        else:
            coming_soon.append(movie)
            print(movie.name,"NOT SHOWING")
    g.movies_showing = movies_showing
    g.coming_soon = coming_soon
    close_db()
    return(render_template('index.html'))




    


