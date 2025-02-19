from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class PerformanceTest(TestCase):
    def test_multiple_request(self):
        client = APIClient()
        for _ in range(100):
            response = client.get(reverse('profile'))
            self.assertEqual(response.status_code,403)