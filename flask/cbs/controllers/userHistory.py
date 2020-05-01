from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
import functools
import sys
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
from cbs.models.Booking import Booking, get_bookings_for_user

blueprint = Blueprint('userHistory',__name__, url_prefix='/')

@blueprint.route("/userHistory")
def view_history():
    if g.user is not None and g.user.status != 2:
        db = open_db()
        g.bookings = get_bookings_for_user(db, g.user.id)
        g.len_bookings = len(g.bookings)

        g.movies = []
        g.showings = []
        g.seats = []

        for booking in g.bookings:
            showing = Showing()
            showing.get_by_id(db, booking.sid)
            g.showings.append(showing)
            movie = Movie()
            movie.get_by_id(db, showing.movie_id)
            g.movies.append(movie.name)

            seats = booking.tickets.split("-")
            for x in range(0,len(seats)):
                seats[x] = seats[x][1:]
            
            g.seats.append(", ".join(seats))

        return(render_template('userHistory.html'))
    else:
        flash("you must be logged in to a user account to view this page")
        return(render_template('login.html'))