from rest_framework.test import APITestCase,APIClient
from django.contrib.auth import get_user_model
from accounts.models import Auth_Token

User = get_user_model()

class NoteErrorHandlingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349205',
            birth_date = '2000-03-04',
            password= 'test123456%'
        )
        self.token = Auth_Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+self.token.key)

    def test_invalid_note_data(self):
        data = {
            'user':"",
            "title":"afj"
        }
        response = self.client.post("/api/note/",data)
        self.assertEqual(response.status_code,400)