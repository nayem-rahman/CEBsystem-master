from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
import functools
import sys


blueprint = Blueprint('editMovie',__name__, url_prefix='/')

@blueprint.route("/editMovie", methods=["GET"])
def view_editMovie():
    if request.args.get('id') is not None:
        movie = Movie()
        db = open_db()
        movie.get_by_id(db, int(request.args.get('id')))
        g.movie = movie
        print(movie.runtime)
        print(g.movie.runtime)
        return(render_template('editMovie.html'))

@blueprint.route("/movieEdited", methods=["GET","POST"])
def editMovie():
    if request.args.get('id') is not None:
        movie = Movie()
        db = open_db()
        previous_movie = Movie()
        previous_movie.get_by_id(db, int(request.args.get('id')))
        
        messages = checkEditMovieRequest(request)
        if len(messages) > 0:
            for message in messages:
                flash(message)
            g.movie = previous_movie
            return(render_template('editMovie.html'))

        movie.populate_movie_by_request(request)

        if movie.get_id_by_name(db) == int(request.args.get('id')) or movie.get_id_by_name(db) == -1:
            updated = movie.update_in_db(db, int(request.args.get('id')))
            if updated:
                flash("movie updated successfully")
                return(redirect(url_for('admin.view_admin')))
            else:
                flash("failed to update movie")
                g.movie = previous_movie
                return(render_template('editMovie.html'))

        
        else:
            flash("new movie title already exists in db")
            g.movie = previous_movie
            return(render_template('editMovie.html'))


def checkEditMovieRequest(request):
    messages = []
    runtime = request.form['runtime']
    split_runtime = runtime.split(" ")
    
    if len(runtime) < 5 or "h" not in runtime or "m" not in runtime or len(split_runtime) < 2:
        messages.append("Duration is not formatted correctly (2h 10m)")
    else:
        hours = split_runtime[0].replace("h","")
        minutes = hours = split_runtime[1].replace("m","")
        try:
            int(hours)
            int(minutes)
        except Exception:
            messages.append("Duration is not formatted correctly (2h 10m)")
    
    return messages
