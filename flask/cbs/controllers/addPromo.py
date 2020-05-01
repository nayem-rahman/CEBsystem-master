from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from cbs.mysqldb import open_db
from cbs.models.Promo import Promo
from cbs.models.User import User, get_subscribed_emails
from cbs.controllers.editMovie import checkEditMovieRequest
import functools
import sys


blueprint = Blueprint('addPromo',__name__, url_prefix='/')

@blueprint.route("/addPromo")
def view_addPromo():
    if g.user is not None and g.user.status == 2:
        return(render_template('addPromo.html'))

@blueprint.route("/promoAdded", methods=['POST'])
def add_promo():
    
    messages = check_promo_request(request)
    if len(messages) > 0:
        for message in messages:
            flash(message)
            return(render_template('addPromo.html'))
    else:
        db = open_db()
        promo = Promo()
        promo.populate_from_request(request)
        added = promo.add_to_db(db)
        if added:
            email_subscribed_users(db, promo)
            flash("promo successfully added to DB")
        else:
            flash("promo could not be added to DB")

    return(render_template('addPromo.html'))


def check_promo_request(request):
    db = open_db()
    messages = []
    percentage = request.form['promo']
    code = request.form['code']
    start_date = request.form['start']
    end_date = request.form['end']

    promo = Promo()
    promo.code = code

    if not promo.is_code_uniq(db):
        messages.append("promo code already in use")

    if len(code) < 4:
        messages.append("promo code is too short")
    
    start_date = int(start_date.replace("-",""))
    end_date = int(end_date.replace("-",""))
    if end_date < start_date:
        messages.append("end date must be later than start date")
    
    return messages

def email_subscribed_users(db, promo):
    emails = get_subscribed_emails(db)
    email_list = []
    for email in emails:
        print(email[0])
        email_list.append(email[0])

    if len(email_list) > 0:
        mail = Mail(current_app)
        msg = Message( subject='CBS promotion notification',
                    sender = current_app.config['MAIL_USERNAME'],
                    recipients=email_list,
                    body="We would like to notify you of the promotion "+promo.start+" to "+promo.end+
                        ". please use the following code at checkout to receive "+str(promo.percentage)+"% off of ticket purchases. "+
                        "\r\n promo code: "+promo.code)
        mail.send(msg)




