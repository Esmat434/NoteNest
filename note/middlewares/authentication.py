from django.shortcuts import redirect
from django.urls import reverse

# this middleware check if you do not login redirect to login page or if you login redirect note-list page
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not request.is_authenticated:
            return redirect(reverse('note-list'))
        else:
            return redirect(reverse('login'))