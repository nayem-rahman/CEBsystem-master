import mysql.connector as conn
from flask import current_app, g
from flask.cli import with_appcontext
import sys
from cryptography.fernet import Fernet

def open_db():
    if 'db' not in g:
        g.db = conn.connect(user=current_app.config['DB_USER'],
                            password=current_app.config['DB_PASSWORD'],
                            host=current_app.config['DB_HOST'],
                            database=current_app.config['DB_NAME'])
    
    return g.db


def close_db(e=None):
    db = g.pop('db',None) # removes db from g, returns db
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db) # calls close_db() when response is returned


class AccessDB:
    @staticmethod
    def select(db, query, values):
        result = []
        try:
            cursor = db.cursor()
            if values is not None:
                print(query % values)
                cursor.execute(query % values)
            else:
                print(query)
                cursor.execute(query)
            result = cursor.fetchall()
        except:
            sys.stderr.write("<CBS ERROR> DB QUERY FAILED...")
        return result

    @staticmethod
    def update(db, query, values):
        try:
            cursor = db.cursor()
            
            if values is not None:
                print(query % values)
                cursor.execute(query,values)
            else:
                print(query)
                cursor.execute(query)
            db.commit()

        except Exception as e:
            print(e)
            sys.stderr.write("<CBS ERROR> DB QUERY FAILED...")
            return False
        
        return True

    @staticmethod
    def decrypt(password, key):
        pw_bytes = password.encode()
        cipher = Fernet(key)
        decrypted_bytes = cipher.decrypt(pw_bytes)
        decrypted = decrypted_bytes.decode()
        sys.stderr.write(decrypted+"\n")
        return decrypted

    @staticmethod
    def encrypt(password, key):
        pw_bytes = password.encode()
        cipher = Fernet(key)
        encrypted_bytes = cipher.encrypt(pw_bytes)
        encrypted = encrypted_bytes.decode()
        return encrypted