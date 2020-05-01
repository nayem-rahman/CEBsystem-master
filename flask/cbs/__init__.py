import os
from flask import Flask
from . import mysqldb
from cbs.controllers import login
from cbs.controllers import register
from cbs.controllers import profile
from cbs.controllers import index
from cbs.controllers import search
from cbs.controllers import admin
from cbs.controllers import forgot
from cbs.controllers import movieInfo
from cbs.controllers import addMovie
from cbs.controllers import manageShowtimes
from cbs.controllers import addShowtime
from cbs.controllers import editShowtime
from cbs.controllers import editMovie
from cbs.controllers import addPromo
from cbs.controllers import manageUsers
from cbs.controllers import seating
from cbs.controllers import userHistory
from cbs.controllers import halls
from cbs.controllers import report
from cbs.controllers import payment
from cbs.controllers import checkout
import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    mysqldb.init_db(app)
    app.register_blueprint(login.blueprint)
    app.register_blueprint(register.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(index.blueprint)
    app.register_blueprint(search.blueprint)
    app.register_blueprint(admin.blueprint)
    app.register_blueprint(forgot.blueprint)
    app.register_blueprint(movieInfo.blueprint)
    app.register_blueprint(addMovie.blueprint)
    app.register_blueprint(manageShowtimes.blueprint)
    app.register_blueprint(addShowtime.blueprint)
    app.register_blueprint(editShowtime.blueprint)
    app.register_blueprint(editMovie.blueprint)
    app.register_blueprint(addPromo.blueprint)
    app.register_blueprint(manageUsers.blueprint)
    app.register_blueprint(seating.blueprint)
    app.register_blueprint(userHistory.blueprint)
    app.register_blueprint(halls.blueprint)
    app.register_blueprint(report.blueprint)
    app.register_blueprint(checkout.blueprint)
    app.register_blueprint(payment.blueprint)
    d = datetime.datetime.today()
    year = str(d.year)
    month = str(d.month)
    day = str(d.day)

    if len(month) < 2:
        month = "0"+month
    if len(day) < 2:
        day = "0"+day
    
    date = year+month+day
    app.config['CURR_DATE'] = int(date)

    return app
