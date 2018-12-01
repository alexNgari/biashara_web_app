import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
 

    def register_business(self, name, category, description, location, created_by, logo_path=''):
        query = f'''INSERT INTO businesses (business_name, category, description, location, created_by, logo_path) 
                    VALUES ('{name}', '{category}', '{description}', '{location}', '{created_by}', '{logo_path}')'''
        self.cursor.execute(query)
        self.connection.commit()


    def test(self):
        self.cursor.execute('SELECT user_name, password FROM users')
        row = self.cursor.fetchone()
        username = row['user_name']
        password = row['password']
        return username, password

    
    def search_business(self, keyword_type, keyword):
        query = f'''SELECT * FROM businesses WHERE {keyword_type}="{keyword}"'''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def search_business_names(self, keyword_type, keyword):
        rows = self.search_business(keyword_type, keyword)
        names = []
        for item in rows:
            names.append(item['business_name'])
        return names


    def all_business_names(self):
        query = "SELECT (business_name) FROM businesses"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    
    def delete_business(self, business_name):
        query = f'''DELETE FROM businesses WHERE business_name="{business_name}"'''
        self.cursor.execute(query)
        self.connection.commit()


    def my_businesses(self, username):
        query = f'''SELECT (business_name) FROM businesses WHERE created_by="{username}"'''
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        return rows


    def update_business(self, old_name, name, category, description, location, logo_path=''):
        query = f'''UPDATE businesses SET business_name='{name}', category='{category}', description='{description}', 
                    location='{location}', created_by, logo_path='{logo_path}' WHERE business_name="{old_name}"'''
        self.cursor.execute(query)
        self.connection.commit()

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

