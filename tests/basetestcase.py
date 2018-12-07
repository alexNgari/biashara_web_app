import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db
from app.models import User, Business, Review
from flask_login import current_user, login_user, logout_user


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config')
        return app

    def setUp(self):
        db.create_all()
        user = User(first_name='Mikael', middle_name='Bloomberg', last_name='Bloomy', username='Bloomy', email='bloomy@mail.com')
        user.set_password('bloomy')
        db.session.add(user)
        db.session.commit()
        business = Business(name='testName1', category='testCat1', desctiption='testDesc1', location='Area 51', user_id=1)
        db.session.add(business)
        db.session.commit()
        user2 = User(first_name='John', middle_name='Anderson', last_name='Wick', username='Wick', email='jwick@mail.com')
        user2.set_password('jwick')
        db.session.add(user2)
        db.session.commit()
        business2 = Business(name='testName2', category='testCat2', desctiption='testDesc2', location='Area 52', user_id=2)
        db.session.add(business2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
