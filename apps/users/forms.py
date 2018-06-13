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
        myuser.username = self.cleaned_data['email'].split('@')[0]

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
        data = self.cleaned_data.get('first_name')
        data = data.strip().title()
        if re.match(r'^[A-Za-z]+$',data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")


    def clean_middle_name(self):
        data = self.cleaned_data.get('middle_name')
        if re.match('^[a-zA-Z ]*$',data):
            data = re.split(' +',data)
            data = ' '.join(data).title()
            return data
        else:
            raise forms.ValidationError("Only alphabetes and spaces are allowed")


    def clean_last_name(self):
        data = self.cleaned_data.get('last_name').strip().title()
        if re.match('^[a-zA-Z]*$',data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")


    def clean_contact(self):
        data = self.cleaned_data.get('contact')
        if data == None:
            pass
        else:
            data = str(data)
            print(data)
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            elif len(data) == 10:
                return data
            else:
                raise forms.ValidationError("Please enter a 10 digit number")


    def clean_salary(self):
        data = self.cleaned_data.get('salary')
        data = str(data)
        if data == None:
            pass
        elif re.search('[+-]', data):
            raise forms.ValidationError("'+', '-' are not allowed")
        else:
            return data

