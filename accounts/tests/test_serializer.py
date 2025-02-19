from django.contrib.auth import get_user_model
from accounts.models import Profile
from rest_framework.test import APITestCase
from accounts.serializer import RegistrationSerializer,UserSerializer,ProfileSerializer,LoginSerializer

User = get_user_model()

class RegistrationSerializerTest(APITestCase):
    def test_valid_registrations(self):
        data = {
            "username":"testuser",
            "email": "test@gmail.com",
            "phone_number": "0798456354",
            "birth_date": "2000-01-02",
            "password": "Pa1234567%",
            "password2": "Pa1234567%"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_registrations(self):
        data = {
            "username": "tetsuser",
            "email": "testusergmail.com",
            "phone_number": "078376387376",
            "birth_date": "2000-03-04",
            "password": "Pa1234567%",
            "password2": "sajdsjlkjsdlkjlkjsdlkj"
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class LoginSerializerTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "testuser",
            "password": "password123"
        }
    
    def test_valid_login(self):
        serializer = LoginSerializer(data = self.data)
        self.assertTrue(serializer.is_valid())

class UserSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username = "testuser",
            email = "testuser@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
            )
        
    def test_user_list(self):
        serializer = UserSerializer(self.user)
        excepted_keys = {"username","email","first_name","last_name","phone_number","picture","country","city","birth_date","password"}
        self.assertEqual(set(serializer.data.keys()),excepted_keys)

class ProfileSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username = "testuser",
            email = "testuser@gmail.com",
            phone_number = "0798459301",
            birth_date = "2000-02-03",
            password = "Bb12345678%"
            )
        self.profile = Profile.objects.get(user = self.user)
    
    def test_profile(self):
        serializer = ProfileSerializer(self.profile)
        excepted_keys = {"user","is_enable","created_time","updated_time"}
        self.assertEqual(set(serializer.data.keys()),excepted_keys)