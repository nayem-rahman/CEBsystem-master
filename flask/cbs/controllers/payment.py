from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
import functools
import sys
from cbs.mysqldb import open_db, close_db, AccessDB
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
from cbs.models.BillingInfo import BillingInfo

blueprint = Blueprint('payment',__name__, url_prefix='/')

@blueprint.route("/payment", methods=["POST","GET"])
def view_payment():
    if g.user is not None and g.user.status != 2:
        seats = []
        seat_type = []
        seat_url = []
        for vals in request.form.keys():
            if "Seat" in vals:
                seat = vals.split(" ")[1]
                seats.append(seat)
                if "Adult" in request.form[vals]:
                    seat = "0"+seat
                    seat_type.append(0)
                elif "Child" in request.form[vals]:
                    seat = "1"+seat
                    seat_type.append(1)
                else:
                    seat = "2"+seat
                    seat_type.append(2)
                seat_url.append(seat)
            print(vals, request.form[vals])

        if len(seat_url) < 1 and request.args.get('seats') is not None:
            seat_url = request.args.get('seats').split("-")
            seat_type = []
            seats = seat_url
            for x in range(0,len(seats)):
                seat_type.append(int(seats[x][0]))
        elif len(seat_url) < 1:
            flash("Please select at least one seat")
            return(redirect("http://localhost:5000/seating?id="+request.args.get('show_id')+"&date="+request.args.get('date')))
        

        g.show_id = request.args.get('show_id')
        g.date = request.args.get('date')
        seat_url = "-".join(seat_url)
        g.seat_url = seat_url
        g.seats = seats
        g.seat_type = seat_type
        g.num_seats = len(seats)

        g.adult_price = 12
        g.child_price = 8
        g.senior_price = 8

        g.total = get_total(g.seat_type, g.adult_price, g.child_price, g.senior_price)


        db = open_db()
        accessDB = AccessDB()
        billing = BillingInfo()
        billing.get_billing(g.user.id, db)
        if billing.card_num != "":
            billing.card_num = accessDB.decrypt(billing.card_num, current_app.config["CIPHER_KEY"])
            # billing.card_num = "XXXX-XXXX-XXXX-"+str(billing.card_num[-4])+str(billing.card_num[-3])+str(billing.card_num[-2])+str(billing.card_num[-1])
        g.billing = billing
        return(render_template('payment.html'))
    else:
        flash("must be logged in to a user account to checkout")
        return(render_template('login.html'))


    
def get_total(seat_types, adult_price, child_price, senior_price, promo=0.0):
    total = 0
    for seat in seat_types:
        if seat == 0:
            total += adult_price
        elif seat == 1:
            total += child_price
        else:
            total += senior_price
    
    discount = total * (promo/100)

    total = total - discount

    return round(total,2)