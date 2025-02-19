from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class UserFlowTest(APITestCase):
    def test_user_registration_login_profile(self):
        # Register
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '0798458301',
            'birth_date': '2000-01-01',
            'password': 'Password123!',
            'password2': 'Password123!'
        }
        registration_response = self.client.post('/api/signup/', registration_data)
        self.assertEqual(registration_response.status_code, 201)

        # Login
        login_data = {
            'username': 'testuser',
            'password': 'Password123!'
        }
        login_response = self.client.post('/api/login/', login_data)
        self.assertEqual(login_response.status_code, 200)
