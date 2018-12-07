import unittest
from flask import Flask
from app.models import User, Business, Review
from flask_login import current_user, login_user, logout_user
from tests.basetestcase import BaseTestCase

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



if __name__ == '__main__':
    unittest.main()