import sys
from cbs.mysqldb import AccessDB

class BillingInfo:
    def __init__(self):
        self.id = -1
        self.uid = -1
        self.full_name = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.name_on_card = ""
        self.card_num = ""
        self.card_exp_month = ""
        self.card_exp_year = ""
        self.card_cvv = ""

    # setters
    def populate_billing_from_registration(self, request):
        self.full_name = request.form['fullname']
        self.address = request.form['address']
        self.city = request.form['city']
        self.state = request.form['state']
        self.zip = request.form['zip']
        self.name_on_card = request.form['cardname']
        self.card_num = request.form['cardnumber'].replace("-","")
        self.card_exp_month = request.form['expmonth']
        self.card_exp_year = request.form['expyear']
        self.card_cvv = request.form['cvv']

    # data access
    def add_billing_to_db(self, uid, db, key):
        query = "INSERT INTO `card_info` (`user_id`, `card_num`, `cvv`, `exp_month`, `exp_year`, `full_name`, `address`, `city`, `state`, `zip`, `name_card`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"

        values = (uid, 
                  AccessDB.encrypt(self.card_num.replace("-",""), key), 
                  self.card_cvv, 
                  self.card_exp_month, 
                  self.card_exp_year, 
                  self.full_name, 
                  self.address,
                  self.city, 
                  self.state, 
                  self.zip,
                  self.name_on_card)
        
        updateSuccess = AccessDB.update(db, query, values)

        if not updateSuccess:
            sys.stderr.write("FAILED TO ADD BILLING TO DB\n")
        
        return updateSuccess

    def get_billing(self, uid, db, newest=False):
        query = "SELECT * FROM card_info WHERE user_id = '%s'"
        values = (uid)
        result = AccessDB.select(db, query, values)
        
        if len(result) > 0:
            if not newest:
                self.id = result[0][0]
                self.uid = result[0][1]
                self.card_num = result[0][2]
                self.card_cvv = result[0][3]
                self.card_exp_month = result[0][4]
                self.card_exp_year = result[0][5]
                self.full_name = result[0][6]
                self.name_on_card = result[0][7]
                self.address = result[0][8]
                self.city = result[0][9]
                self.state = result[0][10]
                self.zip = result[0][11]
            else:
                self.id = result[-1][0]
                self.uid = result[-1][1]
                self.card_num = result[-1][2]
                self.card_cvv = result[-1][3]
                self.card_exp_month = result[-1][4]
                self.card_exp_year = result[-1][5]
                self.full_name = result[-1][6]
                self.name_on_card = result[-1][7]
                self.address = result[-1][8]
                self.city = result[-1][9]
                self.state = result[-1][10]
                self.zip = result[-1][11]

    def get_billing_by_id(self, bid, db, newest=False):
        query = "SELECT * FROM card_info WHERE payment_id = '%s'"
        values = (bid)
        result = AccessDB.select(db, query, values)
        
        if len(result) > 0:
            if not newest:
                self.id = result[0][0]
                self.uid = result[0][1]
                self.card_num = result[0][2]
                self.card_cvv = result[0][3]
                self.card_exp_month = result[0][4]
                self.card_exp_year = result[0][5]
                self.full_name = result[0][6]
                self.name_on_card = result[0][7]
                self.address = result[0][8]
                self.city = result[0][9]
                self.state = result[0][10]
                self.zip = result[0][11]
            else:
                self.id = result[-1][0]
                self.uid = result[-1][1]
                self.card_num = result[-1][2]
                self.card_cvv = result[-1][3]
                self.card_exp_month = result[-1][4]
                self.card_exp_year = result[-1][5]
                self.full_name = result[-1][6]
                self.name_on_card = result[-1][7]
                self.address = result[-1][8]
                self.city = result[-1][9]
                self.state = result[-1][10]
                self.zip = result[-1][11]


    def update_billing_info(self, uid, db, key):
        query = "UPDATE card_info SET card_num = %s, cvv = %s, exp_month = %s, exp_year = %s, full_name = %s, name_card = %s, address = %s, city = %s, state = %s, zip = %s WHERE user_id = %s"   
        values = (  AccessDB.encrypt(self.card_num.replace("-",""), key),
                    self.card_cvv,
                    self.card_exp_month,
                    self.card_exp_year,
                    self.full_name,
                    self.name_on_card,
                    self.address,
                    self.city,
                    self.state,
                    self.zip,
                    uid )

        updateSuccess = AccessDB.update(db, query, values)
        if not updateSuccess:
            sys.stderr.write("FAILED TO ADD BILLING TO DB\n")
        return updateSuccess

    @staticmethod
    def checkBillingInfo(request):
        messages = []
        billing_fields = ["fullname",'address','city','state','zip','cardname','expmonth','expyear','cvv']
        valid_months = ["january","february","march","april","may","june","july","august","september","october","november","december"]

        if len(request.form['fullname']) < 2:
            messages.append("Invalid Billing Name")
        if len(request.form['address']) < 5:
            messages.append("Invalid Address")
        if len(request.form['city']) < 2:
            messages.append("Invalid City")
        if len(request.form['state']) != 2:
            messages.append("Invalid State, use two character abbreviation")
        if len(request.form['zip']) != 5 or not request.form['zip'].isdigit():
            messages.append("Invalid Zip Code")
        if len(request.form['cardname']) < 2:
            messages.append("Invalid Name on Card")
        if len(request.form['cardnumber'].replace("-","")) != 16 or not (request.form['cardnumber'].replace("-","").isdigit()):
            messages.append("Invalid Card Number")
        # if len(request.form['expmonth']) < 3 or request.form['expmonth'].lower() not in valid_months:
        #     messages.append("Invalid Expiration Month, spell out whole month")
        if len(request.form['expyear']) < 4 or int(request.form['expyear']) < 2019:
            messages.append("Invalid Expiration Year")
        if len(request.form['cvv']) > 4 or len(request.form['cvv']) < 3 or not request.form['cvv'].isdigit():
            messages.append("Invalid CVV")
        
        return messages
        
        
        
        


