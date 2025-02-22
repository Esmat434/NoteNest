from rest_framework.test import APITestCase

class ScurityTest(APITestCase):
    def test_note_create_list_view(self):
        response = self.client.get('/api/note/')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.data['detail'],'No Token Provider.')
    
    def test_note_detail_update_delete_view(self):
        response = self.client.get('/api/note/1/')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.data['detail'],'No Token Provider.')
    
    def test_note_not_enable_view(self):
        response = self.client.get('/api/note/not_enable/')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.data['detail'],'No Token Provider.')