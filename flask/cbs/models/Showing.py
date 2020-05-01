import sys
from cbs.mysqldb import AccessDB

class Showing:
    def __init__(self):
        self.id = -1
        self.show_time = ""
        self.movie_id = ""
        self.showroom_id = ""
        self.start_date = 0
        self.end_date = 0

    def get_by_id(self, db, show_id):
        query = "SELECT * FROM `showing` WHERE show_id = %s"
        values = (show_id)

        result = AccessDB.select(db, query, values)
        
        if len(result) > 0:
            self.id = result[0][0]
            self.show_time = time_to_string(result[0][1])
            self.movie_id = result[0][2]
            self.showroom_id = result[0][3]
            self.start_date = date_to_int(result[0][4])
            self.end_date = date_to_int(result[0][5])
    
    def populate_by_request(self, request, movie_id):
        time = request.form['time']
        hour = time.split(":")[0]
        minute = time.split(":")[1].replace("p","").replace("a","")
        if time[-1] == "p" and int(hour) < 12:
            hour = str(int(hour)+12)
        if len(hour) == 1:
            hour = "0"+hour
        time = hour+":"+minute+":00"
        print("trying to add time:",time)

        self.show_time = time
        self.movie_id = movie_id
        self.showroom_id = request.form['hall']
        start_date = request.form['start']
        str_date = str(start_date).replace("-","")
        str_date = str_date.replace("/","")
        month = str_date[0]+str_date[1]
        day = str_date[2]+str_date[3]
        year = str_date[4]+str_date[5]+str_date[6]+str_date[7]
        str_date = year+"-"+month+"-"+day
        
        self.start_date = str_date

        end_date = request.form['end']
        str_date = str(end_date).replace("-","")
        str_date = str_date.replace("/","")
        month = str_date[0]+str_date[1]
        day = str_date[2]+str_date[3]
        year = str_date[4]+str_date[5]+str_date[6]+str_date[7]
        str_date = year+"-"+month+"-"+day
        
        self.end_date = str_date

        print(self.start_date, self.end_date, self.show_time)


    def add_to_db(self, db):
        query = "INSERT into `showing` (`show_time`, `movie_id`, `showroom_id`, `start_date`, `end_date`) VALUES (%s, %s, %s, %s, %s)"
        values = (self.show_time, self.movie_id, self.showroom_id, self.start_date, self.end_date)

        updated = AccessDB.update(db, query, values)

        return updated

    def update_in_db(self, db, show_id):
        query = "UPDATE showing SET show_time = %s, movie_id = %s, showroom_id = %s, start_date = %s, end_date = %s WHERE show_id = %s"
        values = (self.show_time, self.movie_id, self.showroom_id, self.start_date, self.end_date, show_id)
        
        updated = AccessDB.update(db, query, values) 
        return updated

    def remove_from_db(self,db):
        query = "DELETE FROM `showing` WHERE show_id = %s"
        values = (self.id,)
        updated = AccessDB.update(db, query, values)
        return updated
    
    @staticmethod
    def get_showroom_showings(db, showroom_id):
        query = "SELECT * FROM `showing` WHERE showroom_id = %s"
        values = (showroom_id)

        results = AccessDB.select(db, query, values)
        
        showings = []
        for res in results:
            showing = Showing()
            showing.id = res[0]
            showing.show_time = time_to_string(res[1])
            showing.movie_id = res[2]
            showing.showroom_id = res[3]
            showing.start_date = date_to_int(res[4])
            showing.end_date = date_to_int(res[5])
            showings.append(showing)
        
        return showings

    @staticmethod
    def get_movie_showings(db, movie_id):
        query = "SELECT * FROM `showing` WHERE movie_id = %s"
        values = (movie_id)

        results = AccessDB.select(db, query, values)
        
        showings = []
        for res in results:
            showing = Showing()
            showing.id = res[0]
            showing.show_time = time_to_string(res[1])
            showing.movie_id = res[2]
            showing.showroom_id = res[3]
            showing.start_date = date_to_int(res[4])
            showing.end_date = date_to_int(res[5])
            showings.append(showing)
        
        return showings

    @staticmethod
    def get_movie_current_showings(db,movie_id,date):
        query = "SELECT * FROM `showing` WHERE movie_id = %s"
        values = (movie_id)

        results = AccessDB.select(db, query, values)
        
        showings = []
        for res in results:
            showing = Showing()
            showing.id = res[0]
            showing.show_time = time_to_string(res[1])
            showing.movie_id = res[2]
            showing.showroom_id = res[3]
            showing.start_date = date_to_int(res[4])
            showing.end_date = date_to_int(res[5])
            print(showing.start_date, date, showing.end_date)
            if showing.start_date <= date and date <= showing.end_date: 
                showings.append(showing)
        
        return showings
    
    @staticmethod
    def get_movie_future_showings(db,movie_id,date):
        query = "SELECT * FROM `showing` WHERE movie_id = %s"
        values = (movie_id)

        results = AccessDB.select(db, query, values)
        
        showings = []
        for res in results:
            showing = Showing()
            showing.id = res[0]
            showing.show_time = time_to_string(res[1])
            showing.movie_id = res[2]
            showing.showroom_id = res[3]
            showing.start_date = date_to_int(res[4])
            showing.end_date = date_to_int(res[5])
            if date < showing.start_date: 
                showings.append(showing)
        
        return showings
    
    @staticmethod
    def get_movie_past_showings(db,movie_id,date):
        query = "SELECT * FROM `showing` WHERE movie_id = %s"
        values = (movie_id)

        results = AccessDB.select(db, query, values)
        
        showings = []
        for res in results:
            showing = Showing()
            showing.id = res[0]
            showing.show_time = time_to_string(res[1])
            showing.movie_id = res[2]
            showing.showroom_id = res[3]
            showing.start_date = date_to_int(res[4])
            showing.end_date = date_to_int(res[5])
            if showing.end_date < date: 
                showings.append(showing)
        
        return showings

def time_to_string(datetime):
    string = str(datetime)
    split_string = string.split(":")
    hour = int(split_string[0])
    minute = split_string[1]
    ampm = "a"
    if hour >= 12:
        ampm = "p"
        if hour > 12:
            hour = hour-12
    
    time_string = str(hour)+":"+minute+ampm

    return(time_string)


def str_to_int_time(str_time):
    ampm = str_time[-1]
    split_str = str_time.split(":")
    hour = int(split_str[0])
    minutes = split_str[1].replace("a","").replace("p","")

    if ampm == "p" and hour < 12:
        hour += 12
    
    hour = str(hour)
    
    int_time = int(hour+minutes)

    return(int_time)

def date_to_int(date, flipped=False):
    str_date = str(date).replace("-","")
    str_date = str_date.replace("/","")
    if flipped == True:
        month = str_date[0]+str_date[1]
        day = str_date[2]+str_date[3]
        year = str_date[4]+str_date[5]+str_date[6]+str_date[7]
        str_date = year+month+day
    int_date = int(str_date)
    return(int_date)

def int_to_str_date(int_date):
    str_date = str(int_date)
    year = str_date[0:4]
    month = str_date[4:6]
    day = str_date[6:8]
    str_date = month+"/"+day+"/"+year

    return str_date



    
    