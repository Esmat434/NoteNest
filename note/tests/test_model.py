from django.test import TestCase
from django.contrib.auth import get_user_model
from note.models import Note

User = get_user_model()

class NoteModelTest(TestCase):
    def setUp(self):
        # register
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'testuser@gmail.com',
            phone_number = '0798349201',
            birth_date = '2000-01-02',
            password = 'Test123456%'
        )

        self.data = Note.objects.create(
            user  = self.user,
            title = 'test title',
            description = 'test description'
        )
    
    def test_note_model(self):
        self.assertEqual(self.data.title, 'test title')