import sys
from cbs.mysqldb import AccessDB

class Booking:
    def __init__(self):
        self.id = -1
        self.uid = -1
        self.bid = -1
        self.sid = -1
        self.tickets = ""
        self.total = 0
        self.date = ""

    def populate(self, uid, bid, sid, tickets, total, date):
        self.uid = uid
        self.bid = bid
        self.sid = sid
        self.tickets = tickets
        self.total = total
        self.date = date

    def add_to_db(self, db):
        query = "INSERT into `booking` (`user_id`, `card_id`, `show_id`, `tickets`, `total_price`, `purchase_date`) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.uid,
                  self.bid,
                  self.sid,
                  self.tickets,
                  self.total,
                  self.date)
        
        booking_added = AccessDB.update(db, query, values)

        return booking_added

def remove_bookings_for_showing(db, show_id):
    query = "DELETE FROM booking WHERE show_id = %s"
    values = (show_id,)

    updated = AccessDB.update(db, query, values)
    return updated

def get_bookings_for_user(db, uid):
    bookings = []
    
    query = "SELECT * FROM `booking` WHERE user_id = %s"
    values = (uid,)
    result = AccessDB.select(db, query, values)
    for res in result:
        booking = Booking()
        booking.id = res[0]
        booking.uid = res[1]
        booking.bid = res[2]
        booking.sid = res[3]
        booking.tickets = res[4]
        booking.total = res[5]
        booking.date = res[6]

        bookings.append(booking)
    
    return bookings