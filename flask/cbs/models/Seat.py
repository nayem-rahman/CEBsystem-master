import sys
from cbs.mysqldb import AccessDB

class Seat:
    def __init__(self):
        self.id = -1
        self.showing = -1
        self.seat_num = -1

    
    def populate(self, show_id, seat_num):
        self.showing = show_id
        self.seat_num = seat_num

    def is_reserved(self, db):
        query = "SELECT * FROM `seat` WHERE show_id = '%s' and seat_num = %s"
        values = (self.showing, self.seat_num)

        result = AccessDB.select(db, query, values)

        if len(result) > 0:
            return True
        else:
            return False

    def add_to_db(self, db):
        query = "INSERT into `seat` (`show_id`, `seat_num`) VALUES (%s, %s)"
        values = (self.showing, self.seat_num)
        
        seat_added = AccessDB.update(db, query, values)

        return seat_added
    

def remove_showing_seats_from_db(db, showing_id):
    query = "DELETE FROM seat WHERE show_id = %s"
    values = (showing_id,)

    updated = AccessDB.update(db, query, values)
    return updated

    

def get_reserved_seats(db, showing_id):
    query = "SELECT * FROM `seat` WHERE show_id = '%s'"
    values = (showing_id)

    result = AccessDB.select(db, query, values)

    seats = []

    for res in result:
        seats.append(res[1])
    
    return seats

def get_all_seats(reserved, num_seats):
    avail_seats = []
    is_reserved = []
    row = ["A","B","C","D","E","F","G","H","I","J"]
    row_idx = 0
    print("NUM SEATS",num_seats)
    for x in range(0,num_seats,10):
        seat_row = []
        reserved_row = []
        for x in range(0,10):
            seat_name = row[row_idx]+str(x+1)
            seat_row.append(seat_name)
            if seat_name not in reserved:
                reserved_row.append(False)
            else:
                reserved_row.append(True)
        
        print(seat_row)
        avail_seats.append(seat_row)
        is_reserved.append(reserved_row)
        
        row_idx +=1
    
    return avail_seats, is_reserved
