from rest_framework.test import APITestCase,APIClient
from django.contrib.auth import get_user_model
from accounts.models import Auth_Token
from note.models import Note

User = get_user_model()

class NoteFunctionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349102',
            birth_date = '2000-02-03',
            password= 'test123456%'
        )

        self.token = Auth_Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+self.token.key)

        self.data = {
            'user': 1,
            'title': 'Af',
            'description': 'This is Afghanistan',
            'is_enable':True
        }
    
    def test_note_model_functional(self):
        response =  self.client.post('/api/note/',self.data)
        self.assertEqual(response.status_code,201)

        response = self.client.get('/api/note/')
        self.assertEqual(response.status_code,200)