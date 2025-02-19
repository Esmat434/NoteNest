from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from .models import Auth_Token


class TokenExpirationMiddleware(MiddlewareMixin):
    def process_request(self,request):
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