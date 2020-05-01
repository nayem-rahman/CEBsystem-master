import sys
from cbs.mysqldb import AccessDB

class Showroom:
    def __init__(self):
        self.id = -1
        self.num_seats = 0

    def get_by_id(self, db, showroom_id):
        query = "SELECT * FROM `showroom` WHERE showroom_id = %s"
        values = (showroom_id)

        result = AccessDB.select(db, query, values)
        
        if len(result) > 0:
            self.id = result[0][0]
            self.num_seats = result[0][2]


    @staticmethod
    def get_all_showrooms(db):
        showrooms = []
        query = "SELECT * FROM `showroom`"
        values = None
        result = AccessDB.select(db, query, values)
        for res in result:
            showroom = Showroom()
            showroom.id = res[0]
            showroom.num_seats = res[2]
            showrooms.append(showroom)
        
        return(showrooms)