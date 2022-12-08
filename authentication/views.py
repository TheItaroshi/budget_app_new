import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email


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
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email is already taken choose another one!'}, status=409)
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # messages.success(request, "Success registration")
        # messages.warning(request, "Warning in registration")
        # messages.info(request, "Info in registration")
        # messages.error(request, "Error registration")

        # Get data from form and keep them in fields
        username, email, password = request.POST['username'], request.POST['email'], request.POST['password']
        context = {
            'fieldValues': request.POST
        }

        # Validate user data
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password should be at least 7 characters")
                    return render(request, 'authentication/register.html', context=context)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account successfully created")
        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')