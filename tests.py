import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db
from app.models import User, Business, Review
from flask_login import current_user


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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCase(BaseTestCase):
    # Ensure flask works
    def test_home(self):
        response = self.client.get('/', content_type='html/text')
        self.assert200

    # Check home page load
    def test_signup_load(self):
        response = self.client.get('/', content_type='html/text')
        self.assertTrue(b'Biashara is a web app' in response.data)

        # Ensure logout requires login
    def test_logout_require_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assert401

        
class UsersViewsTests(BaseTestCase):
    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post('/login',
                        data=dict(username='Bloomy', password='bloomy'),
                        follow_redirects=True)
            self.assertIn(b'Reviews', response.data)
            self.assertTrue(current_user.username == 'Bloomy')
            self.assertTrue(current_user.is_active)

    # Ensure login behaves correctly given wrong credentials    
    def test_incorrect_login(self):
        response = self.client.post('/login',
                    data=dict(username='Lmutu', password='Lmutu'),
                    follow_redirects=True)
        self.assertIn(b'Wrong username or password', response.data)

    # Ensure landing page requires login
    def test_landing_require_login(self):
        response = self.client.get('/landing/Bloomy')
        self.assert401




if __name__ == '__main__':
    unittest.main()