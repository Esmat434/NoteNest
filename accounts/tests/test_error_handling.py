from rest_framework.test import APITestCase

class ErrorHandlingTests(APITestCase):
    def test_invalid_registration_data(self):
        data = {
            'username':'testuser',
            'email': 'invalid_email',
            'phone_number': '0785463213',
            'birth_date': '2000-03-04',
            'password': 'As1234567%',
            'password2': 'As1234567%'
        }
        response = self.client.post('/api/signup/',data)
        self.assertEqual(response.status_code,400)