from app import app, db
from app.models import User, Business, Review
import unittest

class FlaskTestCase(unittest.TestCase):
    # Ensure flask works
    def test_home(self):
        test_client = app.test_client(self)
        response = test_client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Check home page load
    def test_signup_load(self):
        test_client = app.test_client(self)
        response = test_client.get('/', content_type='html/text')
        self.assertTrue(b'Biashara is a web app' in response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        test_client = app.test_client()
        response = test_client.post('/login',
                    data=dict(username='Lmutu', password='Lmutu'),
                    follow_redirects=True)
        self.assertIn(b'Reviews', response.data)



    # Enssure login behaves correctly given wrong credentials    


if __name__ == '__main__':
    unittest.main()