import unittest
from flask import Flask
from app.models import User, Business, Review
from flask_login import current_user, login_user, logout_user
from tests.basetestcase import BaseTestCase

class FlaskTestCase(BaseTestCase):
    # Ensure flask works
    def test_home(self):
        response = self.client.get('/', content_type='html/text')
        self.assert200

    # Check home page load
    def test_home_load(self):
        response = self.client.get('/', content_type='html/text')
        self.assertTrue(b'Biashara is a web app' in response.data)

    # Ensure logout requires login
    def test_logout_require_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assert401

    # Ensure landing page requires login
    def test_landing_require_login(self):
        response = self.client.get('/landing/Bloomy')
        self.assert401

    # Test signup method
    def test_signup(self):
        response = self.client.get('/sign_up')
        self.assert200
    
    # Test signup page loads correctly
    def test_signup_load(self):
        response = self.client.get('/sign_up')
        self.assertIn(b'Sign up', response.data)

    # Test register business require login
    def test_register_business_require_login(self):
        response = self.client.get('/register_business/Bloomy', follow_redirects=True)
        self.assert401


if __name__ == '__main__':
    unittest.main()