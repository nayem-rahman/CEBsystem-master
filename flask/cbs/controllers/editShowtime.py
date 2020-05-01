from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing, int_to_str_date
from cbs.controllers.addShowtime import showingIsAvailable, check_showtime_request
from cbs.models.Showroom import Showroom
import functools
import sys


blueprint = Blueprint('editShowtime',__name__, url_prefix='/')

@blueprint.route("/editShowtime", methods=["GET"])
def view_showtimes():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        showing = Showing()
        showing.get_by_id(db, int(request.args.get('id')))
        showing.start_date = int_to_str_date(showing.start_date)
        showing.end_date = int_to_str_date(showing.end_date)
        g.showing = showing

        showroom = Showroom()
        g.showrooms = showroom.get_all_showrooms(db)

        movie = Movie()
        movie.get_by_id(db, showing.movie_id)
        g.movie = movie
        return(render_template('editShowtime.html'))

@blueprint.route("/showtimeEdited", methods=["GET","POST"])
def edit_showtime():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        original_showing = Showing()
        original_showing.get_by_id(db, int(request.args.get('id')))

        movie = Movie()
        movie.get_by_id(db, original_showing.movie_id)
        messages = check_showtime_request(request)
        if len(messages) > 0:
            flash(messages[0])
            return(redirect("http://localhost:5000/editShowtime?id="+request.args.get('id')))
        else:
            available = showingIsAvailable(db, movie.runtime, request.form['time'], request.form['start'], request.form['end'], int(request.form['hall']), show_id=int(request.args.get('id')))
            if available:
                new_showing = Showing()
                new_showing.populate_by_request(request, original_showing.movie_id)
                added = new_showing.update_in_db(db, int(request.args.get('id')))
                if added:
                    flash("showtime updated successfully")
                    return(redirect("http://localhost:5000/manageShowtimes?id="+str(original_showing.movie_id)))
                else:
                    flash("failed to add to db")
                    return(redirect("http://localhost:5000/editShowtime?id="+request.args.get('id')))

            else:
                flash("this showtime is already taken")
                return(redirect("http://localhost:5000/editShowtime?id="+request.args.get('id')))



# def showingIsAvailable(db, movie_duration, showtime, startdate, enddate, showroom_id, show_id=None):
