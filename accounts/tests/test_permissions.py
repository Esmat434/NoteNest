from django.test import TestCase
from rest_framework.test import APIClient,APIRequestFactory
from rest_framework.exceptions import AuthenticationFailed
from accounts.permissions import TokenAuthenticationPermission
from accounts.models import Auth_Token,CustomUser

class TokenAuthenticationPermissionTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349203',
            birth_date = '2000-02-02',
            password = 'As123456&%'
        )
        self.token = Auth_Token.objects.create(user = self.user)
        self.permission = TokenAuthenticationPermission()
        self.factory = APIRequestFactory()
    
    def test_valid_token(self):
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token.key}'
        self.assertTrue(self.permission.has_permission(request,None))
    
    def test_invalid_token(self):
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Token Invalid.'
        with self.assertRaises(AuthenticationFailed):
            self.permission.has_permission(request,None)