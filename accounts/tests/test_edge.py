from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from accounts.models import Auth_Token

User = get_user_model()

class EdgeCaseTest(APITestCase):
    def test_login_with_expired_token(self):
        user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798457354',
            birth_date = '2000-04-06',
            password= 'As1234567&%'
        )
        token = Auth_Token.objects.create(user = user)
        token.created_at = timezone.now() - timezone.timedelta(days=31)
        token.save()
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {token.key}')
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code,401)