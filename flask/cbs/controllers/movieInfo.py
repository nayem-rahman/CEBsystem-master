from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
from cbs.models.Movie import Movie
from cbs.models.Showing import Showing
import functools
import sys


blueprint = Blueprint('movieInfo',__name__, url_prefix='/')

@blueprint.route("/movieInfo", methods=['GET','POST'])
def view_movieInfo():
    if request.args.get('id') is not None:
        movie = Movie()
        db = open_db()
        movie.get_by_id(db, int(request.args.get('id')))
        movie.trailer = getEmbededYoutubeUrl(movie.trailer)
        g.detailed_movie = movie
        if 'date' in request.form.keys():
            date = request.form['date']
            split_date = date.split("/")
            date = int(split_date[2]+split_date[0]+split_date[1])
        else:
            date = current_app.config["CURR_DATE"]
        
        showing = Showing()
        showings = showing.get_movie_current_showings(db, movie.id, date)

        g.detailed_showings = showings

        g.date = date

        return(render_template('movieInfo.html'))


def getEmbededYoutubeUrl(url):
    split_url = url.split("=")
    vid_id = split_url[1]
    embeded_url = "https://www.youtube.com/embed/"+vid_id
    return embeded_url