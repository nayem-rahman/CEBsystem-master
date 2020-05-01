import sys
from cbs.mysqldb import AccessDB

class Movie:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.genre = ""
        self.rating = ""
        self.description = ""
        self.image = ""
        self.trailer = ""
        self.runtime = ""
        self.cast = ""
        self.director = ""
        self.producer = ""
        self.showings = []

    def get_by_id(self, db, movie_id):
        query = "SELECT * FROM `movie` WHERE movie_id = %s"
        values = (movie_id)

        result = AccessDB.select(db, query, values)
        
        if len(result) > 0:
            self.id = result[0][0]
            self.name = result[0][1]
            self.genre = result[0][2]
            self.rating = result[0][3]
            self.description = result[0][4]
            self.image = result[0][5]
            self.trailer = result[0][6]
            self.runtime = result[0][7]
            self.cast = result[0][8]
            self.director = result[0][9]
            self.producer = result[0][10]
    
    
    def populate_movie_by_request(self, request):
        self.name = request.form["title"]
        self.description = request.form['description']
        self.cast = request.form['cast']
        self.director = request.form['director']
        self.producer = request.form['producer']
        self.image = request.form['pic']
        self.trailer = request.form['trailer']
        self.runtime = request.form['runtime']
        self.rating = request.form['Rating']
        self.genre = request.form['Genre']

    def isUnique(self, db):
        query = "SELECT * FROM `movie` WHERE movie_name = '%s'"
        values = (self.name)

        result = AccessDB.select(db, query, values)
        if len(result) > 0:
            return False
        else:
            return True

    def add_movie_to_db(self, db):
        query = "INSERT into `movie` (`movie_name`, `genre`, `rating`, `description`, `image_url`, `trailer_link`, `run_time`, `stars`, `director`, `producer`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.name,
                  self.genre,
                  self.rating,
                  self.description,
                  self.image,
                  self.trailer,
                  self.runtime,
                  self.cast,
                  self.director,
                  self.producer)
        
        movie_added = AccessDB.update(db, query, values)

        return movie_added

    def get_id_by_name(self, db):
        query = "SELECT * FROM `movie` WHERE movie_name = '%s'"
        values = (self.name)

        result = AccessDB.select(db, query, values)

        if len(result) > 0:
            return result[0][0]
        else:
            return -1

    def update_in_db(self, db, idx):
        query = "UPDATE movie SET movie_name = %s, genre = %s, rating = %s, description = %s, image_url = %s, trailer_link = %s, run_time = %s, stars = %s, director = %s, producer = %s WHERE movie_id = %s"
        values = (self.name, self.genre, self.rating, self.description, self.image, self.trailer, self.runtime, self.cast, self.director, self.producer, idx)

        updated = AccessDB.update(db, query, values) 
        return updated

    def remove_from_db(self, db):
        query = "DELETE FROM movie WHERE movie_name = %s"
        values = (self.name,)

        updated = AccessDB.update(db, query, values)
        return updated

def get_all_movies(db):
    movies = []
    query = "SELECT * FROM `movie`"
    values = None
    result = AccessDB.select(db, query, values)
    for res in result:
        movie = Movie()
        movie.id = res[0]
        movie.name = res[1]
        movie.genre = res[2]
        movie.rating = res[3]
        movie.description = res[4]
        movie.image = res[5]
        movie.trailer = res[6]
        movie.runtime = res[7]
        movie.cast = res[8]
        movie.director = res[9]
        movie.producer = res[10]

        movies.append(movie)
    
    return movies

def get_end_time(start_time, duration):
    split_dur = duration.split(" ")
    duration_hours = int(split_dur[0].replace("h",""))
    duration_minutes = int(split_dur[1].replace("m",""))

    start = str(start_time)

    if len(start) < 4:
        start_hours = int(start[0])
        start_minutes = int(start[1]+start[2])
    else:
        print(start)
        start_hours = int(start[0]+start[1])
        start_minutes = int(start[2]+start[3])

    end_hours = start_hours + duration_hours

    end_minutes = start_minutes + duration_minutes

    if end_minutes >= 60:
        end_hours += 1
        end_minutes -= 60
    
    end_hours = end_hours*100

    end_time = end_hours+end_minutes

    return(end_time)
