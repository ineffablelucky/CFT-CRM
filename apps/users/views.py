from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm

def index(request):
    return render(request, 'employee_leads.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()


    form.password1 = request.POST.get('password1')
    form.password2 = request.POST.get('password2')

    print(form.password1, form.password2)
    context = {'form' : form}
    return render(request,'registration/register.html',context)


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_or_username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return render(request, 'welcome.html')
    else:
        return render(request, 'registration/login.html')

def lout(request):
    logout(request)
    return redirect('/')



