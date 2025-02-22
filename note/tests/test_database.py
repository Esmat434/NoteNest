from django.test import TestCase
from django.contrib.auth import get_user_model
from note.models import Note

User = get_user_model()

class DatabaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            email = "testuser@gmail.com",
            phone_number = "0771230009",
            birth_date = "2000-01-02",
            password= "As1234567@%"
        )
        self.note = Note.objects.create(
            user = self.user,
            title = "test title",
            description = "test description",
        )
    def test_note_model_data(self):
        self.assertEqual(Note.objects.count(),1)
        self.assertEqual(self.note.title , "test title")