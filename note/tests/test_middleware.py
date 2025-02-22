import json
from django.test import TestCase,RequestFactory
from django.http import JsonResponse
from django.core.cache import cache
# middlewares
from note.middlewares.rate_limiting import RateLimitingMiddleware
from note.middlewares.security import SecurityMiddleware
from note.middlewares.error_handling import ErrorHandlingMiddleware
from note.middlewares.cross_origin_resource_sharing import CrosMiddleware
from note.middlewares.cache import CacheMiddleware

class RateLimitingMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()  # clear the cache before every test

    def test_rate_limitting_middleware(self):
        middleware = RateLimitingMiddleware(lambda req: JsonResponse({"message": "OK"}))
        request = self.factory.get('/api/note/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'

        # sending 100 request
        for _ in range(100):
            response = middleware(request)
            self.assertEqual(response.status_code, 200)

        # sending 101 request
        response = middleware(request)
        self.assertEqual(response.status_code, 429)

        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, {"error": "Rate limit exceeded"})
    
    def test_scurity_middleware(self):
        middleware = SecurityMiddleware(lambda req: JsonResponse({"message": "OK"}))
        request = self.factory.get('/api/note/')
        response = middleware(request)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.get('X-Content-Type-Options'),'nosniff')
        self.assertEqual(response['X-Frame-Options'],'DENY')
        self.assertEqual(response['X-XSS-Protection'],'1; mode=block')
        self.assertEqual(response['Cache-Control'],'no-store, no-cache, must-revalidate, max-age=0')
        self.assertEqual(response['Referrer-Policy'],'strict-origin-when-cross-origin')
        self.assertEqual(response['Permissions-Policy'],'geolocation=(), microphone=(), camera=()')
    
    # this is for test error handling middleware
    def test_error_handling_middleware(self):
        middleware = ErrorHandlingMiddleware(lambda req:JsonResponse({"message":"ok"}))
        request = self.factory.get('/api/note/')
        response = middleware(request)
        self.assertEqual(response.status_code,200)
    
    def test_cross_oroigin_middleware(self):
        middleware = CrosMiddleware(lambda req:JsonResponse({"message":"ok"}))
        request = self.factory.get('/api/note/')
        response = middleware(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response['Access-Control-Allow-Origin'],'*')
        self.assertEqual(response['Access-Control-Allow-Methods'],'GET, POST, PUT, DELETE, OPTIONS')
        self.assertEqual(response['Access-Control-Allow-Headers'],'Content-Type, Authorization')
    
    def test_cache_middleware(self):
        request = self.factory.get('/api/note/')
        middleware = CacheMiddleware(lambda req:JsonResponse({"message":"ok"}))
        response1 = middleware(request)
        
        self.assertEqual(response1.status_code,200)

        cached_response = cache.get(request.path)
        self.assertIsNotNone(cached_response)
        self.assertEqual(cached_response.status_code,200)

        response2 = middleware(request)
        self.assertEqual(response2.status_code,200)

        self.assertEqual(response1.content,response2.content)