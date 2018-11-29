import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "mytestuser"
        password = "@Alex.ngari03"
        db = "andelaApp"
 
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cursor = self.connection.cursor()

    def sign_up(self, first_name, middle_name, last_name, email, username, password):
        hashed_pass = generate_password_hash(password)
        query = f"""INSERT INTO users (first_name, middle_name, last_name, email, username, password) 
                    VALUES ('{first_name}', '{middle_name}', '{last_name}', '{email}', '{username}', '{hashed_pass}')"""
        self.cursor.execute(query)
        self.connection.commit()

    
    def check_username(self, username):
        query = f'''SELECT * FROM users WHERE username="{username}"'''
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        return rows

    def log_in(self, username, password):
        rows = self.check_username(username)
        if len(rows) == 1:
            return check_password_hash(rows[0]['password'], password)
        else:
            return False
 

    def register_business(self, name, description, location, created_by, logo_path=''):
        query = f'''INSERT INTO businesses (business_name, description, location, created_by, logo_path) 
                    VALUES ('{name}', '{description}', '{location}', '{created_by}', '{logo_path}')'''
        self.cursor.execute(query)
        self.connection.commit()


    def test(self):
        self.cursor.execute('SELECT user_name, password FROM users')
        row = self.cursor.fetchone()
        username = row['user_name']
        password = row['password']
        return username, password
