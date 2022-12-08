import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from validate_email import validate_email
from .utils import AppTokenGenerator


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
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token_generator = AppTokenGenerator()
                token = token_generator.make_token(user)
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                activate_url = f'http://{domain}{link}'

                email_subject = 'Budget app activation mail'
                email_body = f'Hi {user.username}!\n\n' \
                             f'To activate your account please click the link below:\n' \
                             f'{activate_url}'

                email_handler = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@budgetter.com',
                    [email],
                )
                email_handler.send(fail_silently=False)
                messages.success(request, "Account successfully created")
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

