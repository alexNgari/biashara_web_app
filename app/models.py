from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


@login.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None


# @login.user_loader
# def load_user(id):
#     return User.query.get(id)

# @login_manager.user_loader
# def load_user(user_id):
#     db = Database()
#     if len(db.check_username(user_id)) == 1:
#         return User(user_id)
#     else:
#         return None

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    middle_name = db.Column(db.String(64), index=True, unique=False, nullable=True)
    last_name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    category = db.Column(db.String(64), index=True, unique=False, nullable=False)
    desctiption = db.Column(db.String(512), index=True, unique=False, nullable=False)
    location = db.Column(db.String(64), index=True, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    post = db.Column(db.String(512), index=True, unique=False, nullable=False)
    pub_date= db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Review {}>'.format(self.post)