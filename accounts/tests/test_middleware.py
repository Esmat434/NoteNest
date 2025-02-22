import json
from django.test import RequestFactory,TestCase
from django.utils import timezone
from django.http import JsonResponse
from accounts.middlewares import TokenExpirationMiddleware,LoginRateLimitationMiddleware
from accounts.models import Auth_Token,CustomUser

class TokenExpirationMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username = "testuser",
            email = "testuser@gmail.com",
            phone_number = "0771230009",
            birth_date = "2000-02-03",
            password = ""
        )
        self.token = Auth_Token.objects.create(user = self.user)
    
    def test_expired_token(self):
        self.token.created_at = timezone.now() - timezone.timedelta(days=31)
        self.token.save()
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.token.key}"
        middleware = TokenExpirationMiddleware(lambda request:None)
        response = middleware.process_request(request)
        request_data = json.loads(response.content)
        self.assertEqual(response.status_code,401)
        self.assertEqual(request_data['detail'], 'Token expired. Please log in again.')

class LoginRateLimitationMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LoginRateLimitationMiddleware(lambda req:JsonResponse({"message":"pk"}))
    
    def test_login_rate_limitation_middleware(self):
        request = self.factory.get('/api/login/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        
        for _ in range(3):
            response = self.middleware(request)
            self.assertEqual(response.status_code,200)
        
        response = self.middleware(request)
        self.assertEqual(response.status_code,429)
        
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data,{"error":"Login limit exceeded. Try again after 10 minutes."})