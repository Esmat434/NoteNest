from django.test import TestCase
from accounts.models import CustomUser,Profile,Auth_Token

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username = "amin",
            email = "amin@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
        )
        self.assertEqual(user.username,"amin")
        self.assertEqual(user.email, "amin@gmail.com")
        self.assertEqual(user.phone_number,"0798459301")
    
    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            username = "amin",
            email = "amin@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

class ProfileModelTest(TestCase):
    def test_profile_create(self):
        user = CustomUser.objects.create_user(
            username = "amin",
            email = "amin@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
        )
        profile = Profile.objects.get(user = user)
        self.assertEqual(profile.user,user) 

class AuthTokenModelTest(TestCase):
    def test_token_create(self):
        user = CustomUser.objects.create_user(
            username = "amin",
            email = "amin@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
        )
        token = Auth_Token.objects.create(user = user)
        self.assertEqual(token.user,user)
