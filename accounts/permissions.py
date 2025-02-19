from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import responses
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .models import Auth_Token
User = get_user_model()

class TokenAuthenticationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = get_authorization_header(request).decode('utf-8')
        token_key = auth_header.split(' ')[1] if ' ' in auth_header else None

        if token_key is None:
            raise AuthenticationFailed({"detail":"No Token Provider."})
        
        try:
            token = Auth_Token.objects.get(key = token_key)
            request.user = token.user
            return True
        except Auth_Token.DoesNotExist:
            raise AuthenticationFailed({"detial":"Invalid Token"})