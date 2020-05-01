import sys
from cbs.mysqldb import AccessDB


class User:
    def __init__(self):
        self.id = -1
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.status = 0
        self.subscribed = False
        self.addess_ids = []
    
    ## setters
    def create_user(self, email, password):
        self.email = email
        self.password = password
    
    # getters
    def get_id(self):
        return self.id
    
    def get_status(self):
        return self.status

    # data access
    def load_by_id(self, db, uid):
        query = "SELECT * FROM user WHERE user_id = %s"
        values = (str(uid))
        result = AccessDB.select(db, query, values)
        if len(result) > 0:
            self._populate_user_from_query(result[0])
        else:
            self = User()

    def load_by_email(self, db, email):
        query = "SELECT * FROM user WHERE email = '%s'"
        values = (email)
        result = AccessDB.select(db, query, values)
        self._populate_user_from_query(result[0])

    def load_user_data(self, db, key):
        if self.email is not None:
            query = "SELECT * FROM user WHERE email = '%s'"
            values = (self.email)
            result = AccessDB.select(db, query, values)
            self._populate_user_from_query(result[0])
        else:
            sys.stderr.write("<CBS ERROR> Could not load user data..\n")
    
    def _populate_user_from_query(self, q_result):
        if q_result is not None:
            self.id = q_result[0]
            self.first_name = q_result[1]
            self.last_name = q_result[2]
            self.email = q_result[3]
            self.status = q_result[5]
            self.subscribed = bool(q_result[6])
        else:
            sys.stderr.write("<CBS ERROR> Could not load user data..\n")
    
    def populate_user_from_registration(self, request):
        self.email = request.form['email']
        self.password = request.form['password']
        self.first_name = request.form['firstname']
        self.last_name = request.form['lastname']
        self.status = 0
        if 'subscription' in request.form.keys():
            self.subscribed = True
        else:
            self.subscribed = False

    def add_user_to_db(self, db, key):
        values = (self.email, 
                  AccessDB.encrypt(self.password, key), 
                  self.first_name, 
                  self.last_name,
                  self.status,
                  self.subscribed)
        
        query = "INSERT INTO `user` (`email`, `password`, `first_name`, `last_name`, `status`, `sub_to_promo`) VALUES (%s, %s, %s, %s, %s, %s)"
        updated = AccessDB.update(db, query, values)
        return updated

    def is_authentic(self, db, key):
        query = "SELECT * FROM user WHERE email = '%s'"
        values = (self.email)
        result = AccessDB.select(db, query, values)

        if len(result) < 1:
            sys.stderr.write("<CBS ERROR> email doesn't exist in DB\n")
            return False
        
        if self.password == AccessDB.decrypt(result[0][4], key):
            return True

        else:
            sys.stderr.write("<CBS ERROR> Password is incorrect for "+self.email+"\n")
            return False
    
    def is_unique(self, db):
        query = "SELECT * FROM user WHERE email = '%s'"
        values = (self.email)
        result = AccessDB.select(db, query, values)

        if len(result) < 1:
            return True
        else:
            return False

    def update_profile_info(self, db, new_pass = None, key=None):
        if new_pass is None:
            query = "UPDATE user SET first_name = %s, last_name = %s, sub_to_promo = %s WHERE email = %s"
            values = (self.first_name, self.last_name, self.subscribed, self.email)
        else:
            query = "UPDATE user SET first_name = %s, last_name = %s, sub_to_promo = %s, password = %s WHERE email = %s"
            values = (self.first_name, self.last_name, self.subscribed, AccessDB.encrypt(new_pass, key), self.email)

        updated = AccessDB.update(db, query, values)  
        return updated

    def activate_user(self, db):
        query = "UPDATE user SET status = %s WHERE email = %s"
        values = (1, self.email)
        updated = AccessDB.update(db, query, values)  
        return updated
    
    def suspend_user(self, db):
        query = "UPDATE user SET status = %s WHERE email = %s"
        values = (self.status+3, self.email)
        updated = AccessDB.update(db, query, values)  
        return updated

    def unsuspend_user(self, db):
        query = "UPDATE user SET status = %s WHERE email = %s"
        values = (self.status-3, self.email)
        updated = AccessDB.update(db, query, values)  
        return updated

    

## general functions

def email_exists( email, db):
    query = "SELECT * FROM user WHERE email = '%s'"
    values = (email)
    result = AccessDB.select(db, query, values)
    if len(result) < 1:
        sys.stderr.write("<CBS ERROR> email doesn't exist in DB\n")
        return False
    else:
        return True

def get_subscribed_emails(db):
    query = "SELECT email FROM user WHERE sub_to_promo = '%s'"
    values = (1,)

    results = AccessDB.select(db, query, values)

    return results

def get_all_users(db):
    users = []
    query = "SELECT * FROM `user`"
    values = None
    result = AccessDB.select(db, query, values)
    for res in result:
        user = User()
        user.id = res[0]
        user.first_name = res[1]
        user.last_name = res[2]
        user.email = res[3]
        user.status = res[5]
        users.append(user)
    
    return(users)

        





