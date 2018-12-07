import unittest
from flask import Flask
from app.models import User, Business, Review
from flask_login import current_user, login_user, logout_user
from tests.basetestcase import BaseTestCase

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