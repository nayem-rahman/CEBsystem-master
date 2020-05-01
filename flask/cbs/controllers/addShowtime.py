from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies, get_end_time
from cbs.models.Showing import Showing, str_to_int_time, date_to_int
from cbs.models.Showroom import Showroom
import functools
import sys


blueprint = Blueprint('addShowtime',__name__, url_prefix='/')

@blueprint.route("/addShowtime", methods=["GET"])
def view_showtimes():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        movie = Movie()
        movie.get_by_id(db, int(request.args.get('id')))
        g.movie = movie
        showroom = Showroom()
        g.showrooms = showroom.get_all_showrooms(db)
        return(render_template('addShowtime.html'))


@blueprint.route("/showtimeAdded", methods=["GET","POST"])
def add_showtime():
    if g.user is not None and g.user.status == 2 and request.args.get('id') is not None:
        db = open_db()
        movie = Movie()
        movie.get_by_id(db, int(request.args.get('id')))

        showroom_id = int(request.form['hall'])
        messages = check_showtime_request(request)
        if len(messages) == 0:
            available = showingIsAvailable(db, movie.runtime, request.form['time'], request.form['start'], request.form['end'], showroom_id)
            if available:
                showing = Showing()
                showing.populate_by_request(request, int(request.args.get('id')))
                added = showing.add_to_db(db)
                if added:
                    flash("showing added successfully")
                    return(redirect(url_for('admin.view_admin')))
                else:
                    flash("failed to add showing to db")
                    return(redirect("http://localhost:5000/addShowtime?id="+request.args.get('id')))

            else:
                flash("timeslot already taken")
                return(redirect("http://localhost:5000/addShowtime?id="+request.args.get('id')))
        else:
            for message in messages:
                flash(message)
                return(redirect("http://localhost:5000/addShowtime?id="+request.args.get('id')))

        


def check_showtime_request(request):
    messages = []
    time = request.form['time']
    if ":" not in time or ("a" not in time and "p" not in time) or "m" in time:
        messages.append("time is not formatted correctly (9:30p)")
    
    start_date = request.form['start']

    if "/" not in start_date or len(start_date) != 10:
        messages.append("start date formatted incorrectly (MM/DD/YYYY)")

    end_date = request.form['end']

    if "/" not in end_date or len(end_date) != 10:
        messages.append("start date formatted incorrectly (MM/DD/YYYY)")

    return messages


def showingIsAvailable(db, movie_duration, showtime, startdate, enddate, showroom_id, show_id=None):
    showing = Showing()
    showings_in_showroom = showing.get_showroom_showings(db, showroom_id)
    start_time = str_to_int_time(showtime)
    end_time = get_end_time(start_time, movie_duration)
    startdate = date_to_int(startdate, flipped=True)
    enddate = date_to_int(enddate, flipped=True)

    for show in showings_in_showroom:
        show_movie = Movie()
        show_movie.get_by_id(db, show.movie_id)
        show_start = str_to_int_time(show.show_time)
        show_end = get_end_time(show_start, show_movie.runtime)

        print("addedShow",start_time, end_time)
        print("existingShow", show_start, show_end)
        if (show_start <= start_time and start_time <= show_end) or (show_start <= end_time and end_time <= show_end):
            print("addedShow", startdate, enddate)
            print("existingShow", show.start_date, show.end_date)
            if(show.start_date <= startdate and startdate <= show.end_date) or (show.start_date <= enddate and enddate <= show.end_date):
                if show_id == None:
                    return False
                else:
                    if show_id != show.id:
                        return False
    
    return True





        
        

