import unittest
from flask import Flask
from app import db
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

    # Check if loading own business gives delete option and viewing reviews
    def test_own_business_profile(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.get('/business/testName1', follow_redirects=True)
            self.assertIn(b'testDesc1', response.data)
            self.assertIn(b'Delete Business', response.data)
            self.assertIn(b'Update details', response.data)
            self.assertFalse(b'Review Business' in response.data)
            self.assertIn(b'testReview1', response.data)
            self.assertIn(b'Wick', response.data)

    # Test other's business profile with review options and no delete option
    def test_others_business_profile(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.get('/business/testName2', follow_redirects=True)
            self.assertIn(b'testDesc2', response.data)
            self.assertIn(b'Review Business', response.data)
            self.assertFalse(b'Delete Business' in response.data)

    # Test deleting functionality with proper confirmation
    def test_valid_deletion(self):
        with self.client:
            self.client.post('/login', data=dict(username='Wick', password='jwick'), follow_redirects=True) # log in John Wick
            response = self.client.post('/delete', data=dict(business_name='testName2'), follow_redirects=True)
            self.assert200
            self.assertIn(b'Successfully deleted business', response.data)
            business = Business.query.filter_by(name='testName2').all()
            self.assertNotEqual(None, business)
    
    # Test deleting functionality with bad confirmation
    def test_invalid_deletion(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.post('/delete', data=dict(business_name='testName5'), follow_redirects=True)
            self.assert200
            self.assertIn(b'Names do not match!', response.data)
        
    # Test deleting other's business
    def test_unauthorised_deletion(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.post('/delete', data=dict(business_name='testName2'), follow_redirects=True)
            self.assert200
            self.assertIn(b'Get your own business!', response.data)
            business = Business.query.filter_by(name='testName2').all()
            self.assertNotEqual([], business)
        
    # Test updating business profile
    def test_update_business(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.post('/update_business/testName1', 
                                data=dict(name='testName5', category='testCat5', description='testDesc5', location='testLoc5'), follow_redirects=True)
            self.assert200
            self.assertIn(b'Successfully updated details', response.data)
            business = Business.query.filter_by(name='testName5').all()
            self.assertNotEqual([], business)
            business = Business.query.filter_by(name='testName1').all()
            self.assertEqual([], business)
        
    # Test update business load
    def test_update_form_load(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.get('/update_business/testName1')
            self.assert200
            self.assertIn(b'testName1', response.data) 
        
    # Posting reviews functionality
    def test_post_review(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.post('/review/testName2', 
                            data=dict(post="teribble"))
            self.assert200
            self.assertIn(b'Review Posted', response.data)
            review = Review.query.filter_by(user_id=1).all()
            self.assertNotEqual([], review)
            self.assertEqual(2, review[0].business_id)

    # Test review page load
    def test_review_page_load(self):
        with self.client:
            self.client.post('/login', data=dict(username='Bloomy', password='bloomy'), follow_redirects=True) # log in bloomy
            response = self.client.get('/review/testName2')
            self.assert200
            self.assertIn(b'Review testName2', response.data) 
        
        


if __name__ == '__main__':
    unittest.main()