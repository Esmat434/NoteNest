import json
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from accounts.models import Auth_Token

User = get_user_model()

class RegistrationViewTest(APITestCase):
    def test_successfull_registration(self):
        data = {
            'username':'testuser',
            'email': 'testuser@gmail.com',
            'phone_number': '0791244505',
            'birth_date': '2000-01-04',
            'password': 'As12345678%',
            'password2': 'As12345678%'
        }
        response = self.client.post('/api/signup/',data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['Message'],'User registered successfully.')
    
    def test_invalid_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'phone_number': '0791240009',
            'birth_date': '2000-03-04',
            'password': 'As1234567%',
            'password2': 'As1234567%ksdjklsdklsdj'
        }
        response = self.client.post('/api/signup/',data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.data['Message'],'Enter valid data.')

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349105',
            birth_date = '2000-02-03',
            password = 'As1234567@'
        ) 
    def test_successfull_login(self):
        data = {
            'username': 'testuser',
            'password': 'As1234567@'
        }
        response = self.client.post('/api/login/',data)
        self.assertEqual(response.status_code,200)
        self.assertIn('token',response.data)
    
    def test_invalid_login(self):
        data = {
            'username': 'testuser',
            'password': 'Askjkdl0903@$%'
        }
        response = self.client.post('/api/login/',data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.data['error'],'Invalid credentials.')

class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'email@gmail.com',
            phone_number = '0771250009',
            birth_date = '2000-03-02',
            password = 'As1234567&'
        )
        self.token = Auth_Token.objects.create(user = self.user)
    
    def test_successfull_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        response = self.client.delete('/api/log-out/')
        self.assertEqual(response.status_code,204)
    
    def test_invalid_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        response = self.client.delete('/api/log-out/')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,401)
        self.assertEqual(response_data['detail'],'Invalid token.')
