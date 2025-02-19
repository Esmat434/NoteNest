from rest_framework.test import APITestCase

class SecurityTests(APITestCase):
    def test_access_without_token(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code,403)
        self.assertEqual(response.data['detail'], 'No Token Provider.')