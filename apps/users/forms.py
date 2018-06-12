from django.forms import ModelForm
from .models import  MyUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
import re


class RegistrationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = (
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
        myuser = super(RegistrationForm, self).save(commit=False)
        myuser.email = self.cleaned_data['email']
        myuser.username = self.cleaned_data['email'].lower().split('@')[0]

        if commit:
            myuser.save()

        return myuser

    def clean_email(self):
        data = self.cleaned_data.get('email').lower()
        try:
            MyUser.objects.get(email=data)
            raise forms.ValidationError("Email already exists")
        except MyUser.DoesNotExist:
            return data


    def clean_first_name(self):
        data = self.cleaned_data.get('first_name').title()
        try:
            re.match(r'^[A-Za-z]+$',data)
            return data
        except:
            raise forms.ValidationError("enter correct name pattern")

