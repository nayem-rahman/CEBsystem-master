from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
import functools
import sys
from cbs.mysqldb import open_db, close_db
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing
from cbs.models.BillingInfo import BillingInfo
from cbs.controllers.payment import get_total
from cbs.models.Promo import Promo, get_all_promos
from cbs.models.User import User
from cbs.models.Seat import Seat
from cbs.models.Booking import Booking
from flask_mail import Mail, Message

blueprint = Blueprint('checkout',__name__, url_prefix='/')

@blueprint.route("/checkout", methods=["POST", "GET"])
def view_checkout():
    if g.user is not None and g.user.status != 2:
        db = open_db()

        show_id = request.args.get('show_id')
        seats = request.args.get('seats')
        seats = seats.split("-")
        seat_types = []
        for x in range(0,len(seats)):
            seat_types.append(int(seats[x][0]))
            seats[x] = seats[x][1:]

        g.show_id = show_id
        g.seat_url = request.args.get('seats')
        g.date = request.args.get('date')
        g.num_seats = len(seats)
        g.seats = seats
        g.seat_types = seat_types

        g.adult_price = 12
        g.child_price = 8
        g.senior_price = 8

        g.discount = 0
        g.promo_code = ""
        
        billing = BillingInfo()
        
        if 'promo' in request.form.keys() and request.form['promo'] is not None:
            billing.get_billing(g.user.id, db, newest=True)
            g.billing = billing
            print(request.form['promo'])
            promos = get_all_promos(db)
            for promo in promos:
                if request.form['promo'] == promo.code:
                    g.discount = promo.percentage
                    g.promo_code = promo.code
            

            if g.promo_code == "":
                flash("Incorrect Promo code")
                return(redirect("http://localhost:5000/checkout?seats="+g.seat_url+"&show_id="+g.show_id+"&date="+str(g.date)))
            
            g.total = get_total(seat_types, g.adult_price, g.child_price, g.senior_price, promo=g.discount)
            return(render_template('checkout.html'))
        
        else:
            
            messages = billing.checkBillingInfo(request)
            if len(messages) > 0:
                flash(messages[0])
                g.seat_type = g.seat_types
                return(redirect("http://localhost:5000/payment?show_id="+g.show_id+"&seats="+g.seat_url+"&date="+str(g.date)))

            billing.populate_billing_from_registration(request)
            billing.add_billing_to_db(g.user.id, db, current_app.config["CIPHER_KEY"])

            billing.get_billing(g.user.id, db, newest=True)
            g.billing = billing

            g.total = get_total(seat_types, g.adult_price, g.child_price, g.senior_price, promo=g.discount)

            for vals in request.form.keys():
                print(vals, request.form[vals])
            return(render_template('checkout.html'))
    else:
        flash("must be logged in to a user account to checkout")
        return(render_template('login.html'))

@blueprint.route("/orderConfirm", methods=["POST", "GET"])
def confirm_checkout():
    db = open_db()
    show_id = request.args.get('show_id')
    date = request.args.get('date')
    bill_id = request.args.get('bill_id')
    seats = request.args.get('seats')
    total = request.args.get('total')
    seats = seats.split("-")
    adult_tickets = 0
    child_tickets = 0
    senior_tickets = 0

    seat_list = []
    for seat in seats:
        if seat[0] == "0":
            adult_tickets +=1
        elif seat[0] == "1":
            child_tickets += 1
        else:
            senior_tickets += 1
        
        seatObj = Seat()
        seatObj.populate(show_id, seat[1:])
        reserved = seatObj.is_reserved(db)
        if reserved == True:
            flash("Unable to purchase tickets, seats were already reserved")
            return(render_template("index.html"))
        
        seat_list.append(seatObj)
    
    for seatObj in seat_list:
        seatObj.add_to_db(db)


    send_confirmation(db, show_id, date, bill_id, seats, adult_tickets, child_tickets, senior_tickets, total)

    billing = BillingInfo()
    billing.get_billing_by_id(bill_id, db)
    user = User()
    user.load_by_id(db, billing.uid)

    showing = Showing()
    showing.get_by_id(db, show_id)

    booking = Booking()
    booking.populate(user.id, bill_id, showing.id, "-".join(seats), float(total), date)
    booking.add_to_db(db)



    return(render_template("orderConfirm.html"))


def send_confirmation(db, show_id, date, bill_id, seats, adult_tickets, child_tickets, senior_tickets, total):
    billing = BillingInfo()
    billing.get_billing_by_id(bill_id, db)
    user = User()
    user.load_by_id(db, billing.uid)

    showing = Showing()
    showing.get_by_id(db, show_id)

    movie = Movie()
    movie.get_by_id(db, showing.movie_id)

    date = str(date)
    year = date[0]+date[1]+date[2]+date[3]
    month = date[4]+date[5]
    day = date[6]+date[7]
    str_date = month+"/"+day+"/"+year

    tickets = "\r\n"
    if adult_tickets > 0:
        tickets += "adult tickets: "+str(adult_tickets)+"\r\n"
    if child_tickets > 0:
        tickets += "child tickets: "+str(child_tickets)+"\r\n"
    if senior_tickets > 0:
        tickets += "senior tickets: "+str(senior_tickets)+"\r\n"

    mail = Mail(current_app)
    msg = Message( subject='CBS purchase confirmation',
                sender = current_app.config['MAIL_USERNAME'],
                recipients=[user.email],
                body="This email is to confirm your purchase of "+str(len(seats))+" seats for "+movie.name+" at "+showing.show_time+" on "+str_date+tickets+"\r\n Total Cost: $"+total)
    mail.send(msg)