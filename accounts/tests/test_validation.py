from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class ValidationTest(TestCase):
    def test_invalid_email(self):
        user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349203',
            birth_date = '2000-03-04',
            password= 'As123456@'
        )

        with self.assertRaises(ValidationError):
            user.full_clean()