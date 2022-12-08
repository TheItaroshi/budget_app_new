import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric (letters and numbers) '
                                                   'characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username is already taken choose another one!'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')