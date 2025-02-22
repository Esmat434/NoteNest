from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.authentication import get_authorization_header
from .models import Auth_Token


class TokenExpirationMiddleware(MiddlewareMixin):
    def process_request(self,request):

        exempt_paths = ['/api/login/','/api/signup/']

        if request.path in exempt_paths:
            return 

        auth_header = get_authorization_header(request).decode('utf-8')
        if auth_header:
            try:
                token_key = auth_header.split(' ')[1]
                token = Auth_Token.objects.get(key = token_key)
                if token.created_at + timezone.timedelta(days=30) < timezone.now():
                    token.delete()
                    request.user = AnonymousUser()
                    return JsonResponse({"detail":"Token expired. Please log in again."},status=401)
            except Auth_Token.DoesNotExist:
                return JsonResponse({"detail":"Invalid token."},status=401)

class LoginRateLimitationMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response
        self.exempt = ['/api/login/']
    
    def __call__(self,request):
        if request.path not in self.exempt:
            return self.get_response(request)
        
        ip = request.META.get('REMOTE_ADDR','')
        failed_attempts = cache.get(f"failed_login_{ip}",0)

        lock_time = cache.get(f'lock_{ip}')
        if lock_time:
            return JsonResponse({"error": "Login limit exceeded. Try again after 10 minutes."}, status=429)

        failed_attempts +=1
        cache.set(f"failed_login_{ip}",failed_attempts,timeout=600)

        if failed_attempts > 3:
            cache.set(f"lock_{ip}",True,timeout=600)
            return JsonResponse({"error": "Login limit exceeded. Try again after 10 minutes."}, status=429)

        return self.get_response(request)