from django.test import TestCase
from rest_framework.test import APIRequestFactory,APIClient
from django.contrib.auth import get_user_model
from accounts.models import Auth_Token
from note.models import Note
from note.permission import IsOwner

User = get_user_model()

class PermissionTest(TestCase):
    def setUp(self):
        # register
        self.user = User.objects.create_user(
            username= 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349205',
            birth_date = '2000-02-03',
            password= 'Testuser12345$'
        )

        self.permission = IsOwner()
        self.factory = APIRequestFactory()
        # login
        self.token = Auth_Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+self.token.key)
    
        # create note
        self.data = Note.objects.create(
            user = self.user,
            title = 'test title',
            description = 'test description'
        )
    
    def test_isowner_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        self.assertTrue(self.permission.has_object_permission(request,None,self.data))