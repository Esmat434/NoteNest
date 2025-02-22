from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from note.serializer import NoteSerializer
User = get_user_model()

class SerializerTest(APITestCase):
    def setUp(self):
        # register
        self.user = User.objects.create_user(
            username = 'test title',
            email = 'testuser@gmail.com',
            phone_number = '0798349103',
            birth_date = '2000-02-03',
            password= 'Test123456@'
        )
        # create note data api
        self.data = {
            'user': 1,
            'title': 'test title',
            'description': 'test description',
            'is_enable': True,
            "is_deleted": False,
            "deleted_at": None,
            "created_at": "2025-02-20T14:59:58.444954Z",
            "updated_at": "2025-02-20T14:59:58.444954Z"
        }
    
    # this function for check the note serializer
    def test_note_serializer(self):
        serializer = NoteSerializer(data = self.data)
        self.assertTrue(serializer.is_valid())