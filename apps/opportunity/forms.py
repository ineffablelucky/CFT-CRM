from django import forms
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from django.db.models import Q
from apps.client.models import CLIENT
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from apps.project.models import IT_Project


class ChangeStatus(forms.ModelForm):
    Opportunity_status = (
        ('Approved', 'Approved'),
        ('RQ_stage', 'Requirement Stage'),
        ('Negotiation', 'Negotiation Stage'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )

    status = forms.ChoiceField(choices=Opportunity_status, widget=forms.Select(), label='Change Status')

    class Meta:
        model = Opportunity
        fields = ('status',)


class AddProjManager(forms.ModelForm):
    proj_manager = forms.ModelChoiceField(
        label='Select Project Manager',
        queryset=MyUser.objects.filter(Q(department='IT') & Q(designation='Manager'))
    )

    class Meta:
        model = Opportunity
        fields = ('proj_manager',)


class CreateClientForm(forms.ModelForm):
    opportunity = forms.ModelChoiceField(
        queryset=Opportunity.objects.filter(status='Approved'),
        required=True
    )

    email = forms.EmailField(
        label='Email ',
        widget=forms.TextInput(),
        required=True
    )

    company_name = forms.CharField(
        max_length=100,
        label='Company Name',
        required=True
    )
    client_address = forms.CharField(
        max_length=10000,
        widget=forms.Textarea(),
        label='Client Address',
        required=True
    )
    project_name = forms.CharField(
        max_length=100,
        label='Project Name'
    )
    project_description = forms.CharField(
        max_length=10000,
        widget=forms.Textarea(),
        label='Project Description'
    )
    project_start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': ''}),
        label='Project Start Date'
    )

    project_end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': ''}),
        label='Project End Date'
    )

    project_total_working_hr = forms.IntegerField(
        label='Project Total Working Hours'
    )
    # password = forms.CharField(
    #     widget=forms.HiddenInput(),
    #     required=False,
    # )
    username = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    amount = forms.IntegerField(
        required=True
    )
    # middle_name = forms.CharField(
    #     widget=forms.HiddenInput(),
    #     initial=None,
    #     required=False
    # )

    class Meta:
        model = MyUser
        fields = (
            'email',
            'username',
        )

    def clean_email(self):
        data = self.cleaned_data.get('email').lower()
        try:
            MyUser.objects.get(email=data)
            raise forms.ValidationError("Email already exists")
        except MyUser.DoesNotExist:
            return data

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name').strip()
        company_name = re.findall(r'\S+', company_name)
        # print('Print Company_name')
        # print(company_name)
        company_name = ' '.join(company_name)
        return company_name

    def clean_project_name(self):
        project_name = self.cleaned_data.get('project_name').strip()
        project_name = re.findall(r'\S+', project_name)
        # print('Print project_name')
        # print(project_name)
        project_name = ' '.join(project_name)
        return project_name

    def clean_project_start_date(self):
        project_start_date = self.cleaned_data.get('project_start_date')
        if project_start_date < datetime.date.today():
            raise forms.ValidationError("Please select a future date or current date")
        else:
            return project_start_date

    def clean_project_end_date(self):
        project_end_date = self.cleaned_data.get('project_end_date')
        if project_end_date < datetime.date.today():
            raise forms.ValidationError("Please select a future date or current date")
        else:
            return project_end_date

    def save(self, commit=True):
        instance = super().save(commit=False)
        # creating username
        instance.username = '_'.join(re.findall(r'\S+', self.cleaned_data.get('company_name')))
        # creating password
        password = instance.username + '1234'
        instance.first_name = 'client'
        instance.designation = 'Client'
        instance.password = make_password(password)
        project_name = self.cleaned_data.get('project_name')
        project_description = self.cleaned_data.get('project_description')
        project_start_date = self.cleaned_data.get('project_start_date')
        project_end_date = self.cleaned_data.get('project_end_date')
        client_address = self.cleaned_data.get('client_address')
        opportunity = self.cleaned_data.get('opportunity')
        amount = self.cleaned_data.get('amount')
        company_name = self.cleaned_data.get('company_name')
        project_end_date = self.cleaned_data.get('project_end_date')
        project_total_working_hr = self.cleaned_data.get('project_total_working_hr')
        if commit:
            instance.save()
        project = IT_Project.objects.create(
            project_name=project_name,
            project_description=project_description,
            project_start_date_time=project_start_date,
            project_end_date_time=project_end_date,
            project_total_working_hr=project_total_working_hr,
            opportunity=opportunity,
        )
        print('printing project')
        project.save()
        print(project)
        client = CLIENT.objects.create(
            company_name=company_name,
            address=client_address,
            client_user=instance
        )
        client.save()
        project = IT_Project.objects.get(opportunity=opportunity)
        project.client_id = client
        project.save()
        opportunity_modify = Opportunity.objects.get(pk=opportunity.pk)
        opportunity_modify.price = amount
        opportunity_modify.client = client
        opportunity_modify.save()
        return instance
