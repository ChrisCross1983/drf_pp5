from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_redirect_url(self, request):
        return "/api/auth/login/"
