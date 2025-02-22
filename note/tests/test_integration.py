from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase,APIClient
from accounts.models import Auth_Token
from note.models import Note

User = get_user_model()

class NoteIntegrationTest(APITestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349102',
            birth_date = '2000-02-03',
            password= 'test123456%'
        )

        # login
        self.token = Auth_Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+self.token.key)
    
        # cerate note
        self.note = Note.objects.create(
            user = self.user,
            title = 'test',
            description = 'test description',
            is_enable = True
        )

        # cerate not enable note
        self.note1 = Note.objects.create(
            user = self.user,
            title = 'test title',
            description = 'test description',
        )

        # create data for api
        self.data = {
            'user':1,
            'title':'test title.',
            'description':'this is test.'
        }

        # create update data
        self.update = {
            'title': 'test update'
        }

    def test_note_view_integration(self):
        # set get method to list of data
        response = self.client.get('/api/note/')
        self.assertEqual(response.status_code,200)

        # post method
        response = self.client.post('/api/note/',self.data)
        self.assertEqual(response.status_code,201)

        # set get method to detail of data
        response = self.client.get(f'/api/note/{self.note.id}/')
        self.assertEqual(response.status_code,200)

        # set put method 
        response = self.client.put(f'/api/note/{self.note.id}/',self.update)
        self.assertEqual(response.status_code,200)

        # set delete method
        response = self.client.delete(f'/api/note/{self.note.id}/')
        self.assertEqual(response.status_code,204)

        # set get method to show the not enable data
        response = self.client.get('/api/note/not_enable/')
        self.assertEqual(response.status_code,200)