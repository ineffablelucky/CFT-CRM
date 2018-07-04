from django.forms import ModelForm
from .models import  MyUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import Group

import re
from django.contrib.auth.hashers import make_password

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
            'department',
            'designation',
            'gender',
        )

    def save(self, commit=True):
        myuser = super(RegistrationForm, self).save(commit=False)
        myuser.username = self.cleaned_data['email'].split('@')[0]

        if commit:

            myuser.save()

            designation = self.cleaned_data['designation']
            department = self.cleaned_data['department']

            if designation == 'Admin':
                group_user = Group.objects.get_by_natural_key('Admin Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'Marketing':
                group_user = Group.objects.get_by_natural_key('Marketing Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'HR':
                group_user = Group.objects.get_by_natural_key('HR Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('HR Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'IT':
                group_user = Group.objects.get_by_natural_key('IT Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('IT Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif department == 'Accounts' and designation == 'Manager':
                group_user = Group.objects.get_by_natural_key('Account Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Account Employee Group')
                group_user .user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Employee':
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)
                if department == 'HR':
                    group_user = Group.objects.get_by_natural_key('HR Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'IT':
                    group_user = Group.objects.get_by_natural_key('IT Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'Marketing':
                    group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'Accounts':
                    group_user = Group.objects.get_by_natural_key('Account Employee Group')
                    group_user.user_set.add(myuser)

            elif designation == 'Client':
                group_user = Group.objects.get_by_natural_key('Client Group')
                group_user.user_set.add(myuser)

            else:
                raise Exception("Not correct designation or department")


        return myuser


    def clean_email(self):
        if self.instance.email:
            return self.instance.email
        else:
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


    def clean_contact_number(self):
        data = self.cleaned_data.get('contact_Number')
        if data == None:
            pass
        else:
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            elif re.search('^[0-9]+$') & len(data) == 10:
                return data
            else:
                raise forms.ValidationError("Please enter a 10 digit number")


    def clean_salary(self):
        data = self.cleaned_data.get('salary')
        if data == None:
            pass
        else:
            data = str(data)
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            else:
                return data


    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        department = self.cleaned_data.get('department')
        if designation == department:
            raise forms.ValidationError("designation and department both can not be NA")
        elif designation == 'Client' and department != 'NA':
            raise forms.ValidationError('not correct match of designation and department')
        else:
            return designation

    designation_choices = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('NA', 'NA'),
    )

    department_choices = (
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
        ('Accounts', 'Accounts'),
        ('IT', 'IT'),
    )

    department = forms.ChoiceField(
        label='Department',
        choices=department_choices,
        widget=forms.Select()
    )

    designation = forms.ChoiceField(
        label='Designation',
        choices=designation_choices,
        widget=forms.Select()
    )

    email = forms.EmailField(
        label='Email ',
        widget = forms.TextInput(),
    )

    first_name = forms.CharField(
        label='First name ',
        widget=forms.TextInput(),
    )

    middle_name = forms.CharField(
        label='Middle Name ',
        widget=forms.TextInput(),
        required = False,
    )

    last_name = forms.CharField(
        label='Last Name ',
        widget=forms.TextInput(),
        required = False,
    )

    contact = forms.CharField(
        label='Contact ',
        widget=forms.NumberInput(),
        required = False,
    )

    salary = forms.IntegerField(
        label='Salary ',
        widget=forms.NumberInput(),
        required=False,
    )



class ResetPasswordForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            'password1',
            'password2',
        )


class EditProfile(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'first_name',
            'last_name',
            'contact',
            'middle_name',
            'designation',
            'gender',
            'salary',
            'department'
        )

    def save(self, commit=True):
        myuser = super(EditProfile, self).save(commit=False)

        if commit:

            myuser.save()
            myuser.groups.clear()
            designation = self.cleaned_data['designation']
            department = self.cleaned_data['department']

            if designation == 'Admin':
                group_user = Group.objects.get_by_natural_key('Admin Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'Marketing':
                group_user = Group.objects.get_by_natural_key('Marketing Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'HR':
                group_user = Group.objects.get_by_natural_key('HR Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('HR Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Manager' and department == 'IT':
                group_user = Group.objects.get_by_natural_key('IT Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('IT Employee Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif department == 'Accounts' and designation == 'Manager':
                group_user = Group.objects.get_by_natural_key('Account Manager Group')
                group_user.user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Account Employee Group')
                group_user .user_set.add(myuser)
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)

            elif designation == 'Employee':
                group_user = Group.objects.get_by_natural_key('Employee Group')
                group_user.user_set.add(myuser)
                if department == 'HR':
                    group_user = Group.objects.get_by_natural_key('HR Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'IT':
                    group_user = Group.objects.get_by_natural_key('IT Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'Marketing':
                    group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
                    group_user.user_set.add(myuser)
                elif department == 'Accounts':
                    group_user = Group.objects.get_by_natural_key('Account Employee Group')
                    group_user.user_set.add(myuser)

            elif designation == 'Client':
                group_user = Group.objects.get_by_natural_key('Client Group')
                group_user.user_set.add(myuser)

            else:
                raise Exception("Not correct designation or department")


        return myuser

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


    def clean_contact_number(self):
        data = self.cleaned_data.get('contact_Number')
        if data == None:
            pass
        else:
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            elif re.search('^[0-9]+$') & len(data) == 10:
                return data
            else:
                raise forms.ValidationError("Please enter a 10 digit number")


    def clean_salary(self):
        data = self.cleaned_data.get('salary')
        if data == None:
            pass
        else:
            data = str(data)
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            else:
                return data


    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        department = self.cleaned_data.get('department')
        if designation == department:
            raise forms.ValidationError("designation and department both can not be NA")
        elif designation == 'Client' and department != 'NA':
            raise forms.ValidationError('not correct match of designation and department')
        else:
            return designation

    designation_choices = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('NA', 'NA'),
    )

    department_choices = (
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
        ('Accounts', 'Accounts'),
        ('IT', 'IT'),
    )

    department = forms.ChoiceField(
        label='Department',
        choices=department_choices,
        widget=forms.Select()
    )

    designation = forms.ChoiceField(
        label='Designation',
        choices=designation_choices,
        widget=forms.Select()
    )

    first_name = forms.CharField(
        label='First name ',
        widget=forms.TextInput(),
    )

    middle_name = forms.CharField(
        label='Middle Name ',
        widget=forms.TextInput(),
        required = False,
    )

    last_name = forms.CharField(
        label='Last Name ',
        widget=forms.TextInput(),
        required = False,
    )

    contact = forms.CharField(
        label='Contact ',
        widget=forms.NumberInput(),
        required = False,
    )

    salary = forms.IntegerField(
        label='Salary ',
        widget=forms.NumberInput(),
        required=False,
    )



    # def save(self, commit=True):
    #     user = self.instance
    #     if commit:
    #         user.save()
    #     return user

    # def __init__(self, *args, **kwargs):
    #     super(EditProfile, self).__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         self.fields['email'].value = self.instance.email


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     # user.password = self.cleaned_data['password2']
    #     user.email = self.instance.email
    #     print(user.password)
    #     if commit:
    #         user.save()
    #     return user

    # def clean_email(self):
    #     print(self.instance)
    #     return self.instance.email
    # def clean_username(self):
    #     return self.instance.username
    #
    # def clean_email(self):
    #     return self.instance.email

    # def clean_password2(self):
    #     return self.instance.password
    #
    # password1 = forms.CharField(
    #     required=False,
    #     label=("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput,
    #     help_text=password_validation.password_validators_help_text_html(),
    # )
    #
    # password2 = forms.CharField(
    #     required=False,
    #     label=("Password confirmation"),
    #     widget=forms.PasswordInput,
    #     strip=False,
    #     help_text=("Enter the same password as before, for verification."),
    #  )

    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'readonly': True}
    #     )
    # )
    #
    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'readonly': True}
    #     )
    # )
    #
    # date_joined = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'readonly': True, 'type' : 'date'}
    #     )
    # )