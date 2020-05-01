from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from cbs.mysqldb import open_db
from cbs.models.Promo import Promo
from cbs.models.User import User, get_subscribed_emails
from cbs.controllers.editMovie import checkEditMovieRequest
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
from cbs.models.Showroom import Showroom
from cbs.models.Seat import Seat, get_reserved_seats, get_all_seats
import functools
import sys


blueprint = Blueprint('seating',__name__, url_prefix='/')

@blueprint.route("/seating", methods=["GET"])
def view_seating():
    if g.user is None:
        return(render_template("login.html"))
    elif request.args.get('id') is not None and request.args.get('date') is not None:
        db = open_db()
        showing_id = request.args.get('id')
        showing = Showing()
        showing.get_by_id(db, showing_id)

        showroom = Showroom()
        showroom.get_by_id(db, int(showing.showroom_id))
        print("SHOWROOM", int(showing.showroom_id))

        movie = Movie()
        movie.get_by_id(db, int(showing.movie_id))

        reserved = get_reserved_seats(db, showing_id)
        all_seats, is_reserved = get_all_seats(reserved, showroom.num_seats)

        print(all_seats)
        g.num_rows = len(all_seats)
        g.num_seats = len(all_seats[0])
        g.all_seats = all_seats
        g.is_reserved = is_reserved
        g.showing = showing
        g.showroom = showroom
        g.movie = movie
        g.date = request.args.get('date')

        


        return(render_template('seating.html'))
