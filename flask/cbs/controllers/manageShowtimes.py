from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing, int_to_str_date
import functools
import sys


blueprint = Blueprint('manageShowtimes',__name__, url_prefix='/')

@blueprint.route("/manageShowtimes",methods=["GET"])
def view_showtimes():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        movie = Movie()
        movie.get_by_id(db, int(request.args.get('id')))

        showing = Showing()
        movie_showings = showing.get_movie_showings(db, movie.id)
        for show in movie_showings:
            show.start_date = int_to_str_date(show.start_date)
            show.end_date = int_to_str_date(show.end_date)
        g.movie = movie
        g.showings = movie_showings
        g.len_showings = len(movie_showings)
        return(render_template('manageShowtimes.html'))

@blueprint.route("/removeShowtime",methods=["GET"])
def remove_showing():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        showing = Showing()
        showing.get_by_id(db, int(request.args.get('id')))
        removed = showing.remove_from_db(db)

        if removed:
            flash("showing removed successfully")
            return(redirect("http://localhost:5000/manageShowtimes?id="+str(showing.movie_id)))
        else:
            flash("failed to remove showing")
            return(redirect("http://localhost:5000/manageShowtimes?id="+str(showing.movie_id)))
