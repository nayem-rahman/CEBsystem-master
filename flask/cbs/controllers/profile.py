from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
import functools
from cbs.models.User import User
from cbs.models.BillingInfo import BillingInfo
from cbs.controllers.login import require_login
from flask_mail import Mail, Message

blueprint = Blueprint('profile',__name__, url_prefix='/')

@blueprint.route("/profile")
@require_login
def view_profile():
    return(render_template('profile.html'))

@blueprint.route("/profileBilling")
@require_login
def view_billing():
    if g.user.id == 2:
        flash("must be a general user to edit billing")
        return(render_template('login.html'))
    db = open_db()
    billing = BillingInfo()
    billing.get_billing(session['user_id'], db)
    g.billing = billing
    return(render_template('billing.html'))


@blueprint.route("/edit", methods=['POST'])
def edit_profile():
    if request.method == "POST":
        db = open_db()
        user = User()

        user.populate_user_from_registration(request)
        is_authentic = user.is_authentic(db, current_app.config['CIPHER_KEY'])

        if is_authentic:
            if 'newpassword' in request.form.keys() and request.form['newpassword'] != "":
                if request.form['newpassword'] == request.form['newrepassword']:
                    updated = user.update_profile_info(db, new_pass=request.form['newpassword'], key=current_app.config['CIPHER_KEY'])
                else:
                    flash("new passwords do not match")
                    return(render_template('profile.html'))
            else:
                updated = user.update_profile_info(db)

            if updated:
                g.user = user
                flash("Account Updated")
                sendUpdateEmail(g.user.email)
                return(render_template('profile.html'))
            else:
                flash("Update failed...")
                return(render_template('profile.html'))
        
        else:
            flash("Password incorrect")
            return(render_template('profile.html'))



@blueprint.route("/editBilling", methods=['POST'])
def edit_billing():
    if request.method == "POST":
        db = open_db()
        billing = BillingInfo()

        messages = billing.checkBillingInfo(request)
        if len(messages) > 0:
            for message in messages:
                flash(message)
            return(redirect(url_for('profile.view_billing')))
        else:
            billing.populate_billing_from_registration(request)
            stored_billing = BillingInfo()
            stored_billing.get_billing(session['user_id'], db)
            if stored_billing.id > -1:
                updated = billing.update_billing_info(session['user_id'], db, current_app.config['CIPHER_KEY'])
            else:
                updated = billing.add_billing_to_db(session['user_id'], db, current_app.config['CIPHER_KEY'])

            if updated:
                g.billing = billing
                flash("Billing Info Updated")
                sendUpdateEmail(g.user.email, billing=True)
                return(redirect(url_for('profile.view_billing')))
            else:
                flash('Billing Info Failed to Update')
                return(redirect(url_for('profile.view_billing')))



def sendUpdateEmail(email, billing=False):
    if not billing:
        body = "Your account information on CBS has been updated."
    else:
        body = "Your account billing information has been updated."
    mail = Mail(current_app)
    msg = Message( subject='CBS Account Info Updated',
                   sender = current_app.config['MAIL_USERNAME'],
                   recipients=[email],
                   body=body)
    mail.send(msg)