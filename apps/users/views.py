from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/admin/login/')
    else:
        form = RegistrationForm()

    context = {'form' : form}
    return render(request,'registration/register.html',context)


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_or_username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return redirect('/admin/login/')
    else:
        return render(request, 'registration/login.html')


