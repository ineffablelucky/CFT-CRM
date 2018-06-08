from django.forms import ModelForm
from .models import  MyUser
from django import forms
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'password1',
            'password2',
            'contact',
            'is_superuser',
            'is_staff',
            'department',
            'designation',
            'salary',
        )

    def save(self, commit=True):
        myuser = super(RegistrationForm, self).save(commit=True)
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        myuser.email = self.cleaned_data['email']

        if commit:
            myuser.save()

        return myuser






