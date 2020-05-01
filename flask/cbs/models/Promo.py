import sys
from cbs.mysqldb import AccessDB

class Promo:
    def __init__(self):
        self.id = -1
        self.percentage = 0
        self.code = ""
        self.start = ""
        self.end = ""

    def populate_from_request(self, request):
        self.percentage = int(request.form['promo'])
        self.code = request.form['code']
        self.start = request.form['start']
        self.end = request.form['end']

    def add_to_db(self, db):
        query = "INSERT INTO `promotion` (`promo_code`, `start_date`, `end_date`, `discount_pct`) VALUES (%s,%s,%s,%s)"
        values = (self.code, self.start, self.end, self.percentage)

        updateSuccess = AccessDB.update(db, query, values)

        if not updateSuccess:
            sys.stderr.write("FAILED TO ADD BILLING TO DB\n")
        
        return updateSuccess


    def is_code_uniq(self, db):
        query = "SELECT * FROM `promotion` WHERE promo_code = '%s'"
        values = (self.code,)

        result = AccessDB.select(db, query, values)

        if len(result) > 0:
            return False
        else:
            return True
    
def get_all_promos(db):
    promos = []
    query = "SELECT * FROM `promotion`"
    values = None
    result = AccessDB.select(db, query, values)
    for res in result:
        promo = Promo()
        promo.id = res[0]
        promo.code = res[1]
        promo.start = res[2]
        promo.end = res[3]
        promo.percentage = res[4]
        promos.append(promo)
    
    return(promos)
