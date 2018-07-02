from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from .forms import RegistrationForm, ResetPasswordForm
from .models import MyUser, user_token
from django.core.mail import  send_mail
from django.contrib.auth.hashers import make_password
from configs.settings import BASE_URL
from django.utils.crypto import get_random_string
from django.urls.exceptions import Http404
from django.http import HttpResponse
import re


def index(request):
    return render(request, 'users/index.html')

# @login_required
# @permission_required('users.add_myuser', raise_exception=True)
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()

    context = {'form' : form}
    return render(request,'users/registration/register.html',context)


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_or_username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return redirect('welcome/')
    else:
        return render(request, 'users/registration/Login/login.html')

def lout(request):
    logout(request)
    return redirect('/')


def profile(request, id):
    user = MyUser.objects.get(pk = id)
    print(user)
    return render(request, 'users/profile.html', {'user':user})

def welcome(request):
    return render(request, 'users/welcome.html')


def sendEmail(request, subject, message, sender, to):
    send_mail(
        subject,
        message,
        sender,
        [to],
        fail_silently=True
    )

def forgot_password(request):
    if request.method == 'POST':
        subject = 'Change Password for CFT-CRM Account!'
        key = get_random_string(length=30)
        email = request.POST.get('email')
        sender = 'kapilarj1997@gmail.com'
        try:
            MyUser.objects.get(email=email)
            user = MyUser.objects.get(email=email)
            user_id = user.id
            try:
                user_token.objects.get(user_id=user_id).delete()
            except:
                pass
            username = user.username
            key = BASE_URL + 'reset-link/' + username + '!!!' + key + '/'
            sendEmail(request, subject, key, sender, email)
            token = user_token.objects.create(token=key, user=user)
            token.save()
            return render(request, 'users/registration/password_reset_done.html')

        except MyUser.DoesNotExist:
            return  render(request, 'users/registration/wrong_reset_email.html')

    else:
        form = PasswordResetForm
        return render(request, 'users/registration/Login/reset-password.html', {'form':form,})

def reset_password(request, token):
    username = re.split('!!!', token)[0]
    user = MyUser.objects.get(username=username)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.password = make_password(request.POST.get('password2'))
            user.save()
            user_token.objects.get(user_id=user.id).delete()
            return render(request, 'users/registration/password_reset_complete.html')

    else:
        form = ResetPasswordForm()
    return render(request, 'users/registration/Login/change-password.html', {'token':token,'form':form,})



def verify(request, key):
    token = key
    key = BASE_URL + 'reset-link/' + str(key) +'/'
    print(key)
    try:
        user_token.objects.get(token=key)
        return reset_password(request, token)

    except user_token.DoesNotExist:
        return render(request, 'users/registration/wrong_token.html')




