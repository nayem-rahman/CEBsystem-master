from flask import Blueprint,current_app, flash, g, redirect, render_template, request, session, url_for
from cbs.mysqldb import open_db
import functools
import sys
from cbs.models.Movie import Movie, get_all_movies
from cbs.models.Showing import Showing


blueprint = Blueprint('search',__name__, url_prefix='/')

@blueprint.route("/search", methods=['POST'])
def view_search():
    title = ""
    rating = None
    genre = None
    showing = None
    date = current_app.config['CURR_DATE']

    if "searchValue" in request.form.keys():
        title = request.form["searchValue"]
        print("title:", title)
    if "Rating" in request.form.keys() and len(request.form['Rating']) > 0:
        rating = request.form['Rating']
        print("rating:", rating)
    if "Genre" in request.form.keys() and len(request.form['Genre']) > 0:
        genre = request.form["Genre"]
        print("genre:",genre)
    if "searchType" in request.form.keys():
        print("searchType:", request.form['searchType'])
        if request.form['searchType'] == "showing-now":
            showing = True
        else:
            showing = False
    if "date" in request.form.keys() and len(request.form['date']) > 0:
        print("date:",request.form['date'])
        date = request.form['date']
        split_date = date.split("/")
        date = split_date[2]+split_date[0]+split_date[1]
        date = int(date)

    g.date = date


    hits = search_movies(title, rating=rating, genre=genre, isShowing=showing, date=date)
    g.search_results = hits
    g.len_search_results = len(hits)

    if len(hits) > 0:
        for hit in hits:
            print(hit.name)
    else:
        print("no hits")
        flash("No results found")
    return(render_template('searchBS.html'))



def search_movies(title, rating=None, genre=None, isShowing=True, date=0):
    hits = []
    db = open_db()
    movies = get_all_movies(db)
    showing = Showing()
    for movie in movies:
        if title.lower() in movie.name.lower():
            if rating is None or rating == movie.rating:
                if genre is None or genre == movie.genre:
                    movie.showings = showing.get_movie_current_showings(db,movie.id, date)
                    if isShowing and len(movie.showings) > 0:
                        hits.append(movie)
                    elif not isShowing and len(movie.showings) < 1:
                        past_showings = showing.get_movie_past_showings(db,movie.id, date)
                        if len(past_showings) < 1:
                            hits.append(movie)
    
    return hits

