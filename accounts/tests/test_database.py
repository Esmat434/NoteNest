from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class DatabaseTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0787456354',
            birth_date = '2000-04-05',
            password= 'As1234567%'
        )
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(user.email , 'testuser@gmail.com')