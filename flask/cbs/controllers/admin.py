from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
import functools
import sys
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
from cbs.models.Seat import Seat, remove_showing_seats_from_db
from cbs.models.Booking import Booking, remove_bookings_for_showing

blueprint = Blueprint('admin',__name__, url_prefix='/')

@blueprint.route("/admin", methods=["GET","POST"])
def view_admin():
    if g.user is not None and g.user.status == 2:
        db = open_db()
        movies = get_all_movies(db)
        g.movies = movies
        g.len_movies = len(movies)
        return(render_template('admin.html'))
    else:
        flash("only admins can access this page, please log into an admin account")
        return(render_template('login.html'))


@blueprint.route("/removeMovie",methods=["GET"])
def remove_movie():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        movie = Movie()
        movie.get_by_id(db,int(request.args.get('id')))

        ## TODO REMOVE SEATS ASSOCIATED WITH SHOWING ##
        showing = Showing()
        movie_showings = showing.get_movie_showings(db, movie.id)
        for show in movie_showings:
            removed = remove_showing_seats_from_db(db, show.id)
            removed = remove_bookings_for_showing(db, show.id)
            removed = show.remove_from_db(db)

        removed = movie.remove_from_db(db)
        if removed:
            flash(movie.name+" removed successfully")
        else:
            flash("Unable to remove "+movie.name)

        return(redirect(url_for('admin.view_admin')))
