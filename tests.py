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

        
class UsersViewsTests(BaseTestCase):
    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post('/login',
                        data=dict(username='Bloomy', password='bloomy'),
                        follow_redirects=True)
            self.assertTrue(current_user.username == 'Bloomy')
            self.assertTrue(current_user.is_active)

    # Ensure login behaves correctly given wrong credentials    
    def test_incorrect_login(self):
        response = self.client.post('/login',
                    data=dict(username='Lmutu', password='Lmutu'),
                    follow_redirects=True)
        self.assertIn(b'Wrong username or password', response.data)

    # Test logout user
    def test_logout(self):
        with self.client:
            self.client.post('/login',
                        data=dict(username='Bloomy', password='bloomy'))
            response = self.client.get('logout', follow_redirects=True)
            self.assertIn(b'Biashara is a web app', response.data)

    # Test landing loads correctly for logged in user
    def test_landing(self):
        with self.client:
            response = self.client.post('/login',
                        data=dict(username='Bloomy', password='bloomy'),
                        follow_redirects=True)
            self.assertIn(b'Reviews', response.data)

    # Test valid signup
    def test_signup_functionality(self):
        with self.client:
            response = self.client.post('/sign_up', data=dict(first_name='Michael', middle_name='Bay', last_name='Musonda', username='mbay', email='mbay@mail.com', password='mbay', password2='mbay'),
            follow_redirects=True)
            self.assertIn(b'Sign-up Successful. Click login above to log in', response.data)

    # Test reused username signup
    def test_used_username_signup(self):
        with self.client:
            response = self.client.post('/sign_up', data=dict(first_name='Michael', middle_name='Bay', last_name='Musonda', username='Bloomy', email='mbay@mail.com', password='mbay', password2='mbay'),
                follow_redirects=True)
            self.assertIn(b'Username has already been taken', response.data)

    # Test register_business_page loads correctly
    def test_register_business_page(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy')) # log in user
            response = self.client.get('/register_business/Bloomy')
            self.assert200
            self.assertIn(b'Business Name', response.data) 
        

    # Test register business functionality
    def test_register_business_functionality(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy')) # log in user
            response = self.client.post('/register_business/Bloomy', 
                        data=dict(name='testName', category='testCat', description='testDesc', location='Area 51'))
            self.assertIn(b'The business has been successfully registered', response.data)

    # Test search functionality
    def test_search_functionality(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy')) # log in user
            response = self.client.get('/search_business', 
                        data=dict(keyword_type='business_name', keyword='Tala'))
            self.assert200
            self.assertIn(b'No results found', response.data)


class BusinessesReviewsTests(BaseTestCase):

    # Test landing page list existing businesses
    def test_landing_list_existing_business(self):
        with self.client:
            response = self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            # response = self.client.get('/search_business', 
            #                             data=dict(keyword_type='business_name', keyword='testName1'))
            self.assert200
            self.assertIn(b'testName1', response.data)
            self.assertTrue(b'testName2' in response.data)


            
        


if __name__ == '__main__':
    unittest.main()