import datetime
import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from apps.client.models import CLIENT
from apps.opportunity.models import Opportunity
from apps.project.models import IT_Project
from apps.users.models import MyUser


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
        queryset=Opportunity.objects.filter(Q(status='Approved') & Q(client__isnull='True')),
        required=True,
        label='Opportunity',
        widget=forms.Select(
            attrs={'class': 'form-control col-md-7 col-xs-12 select2_group form-control'}
        )
    )

    email = forms.EmailField(
        label='Email ',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )

    company_name = forms.CharField(
        max_length=100,
        label='Company Name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    client_address = forms.CharField(
        max_length=10000,
        label='Client Address',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    project_name = forms.CharField(
        max_length=100,
        label='Project Name',
        required='True',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    project_description = forms.CharField(
        max_length=10000,
        widget=forms.Textarea(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        ),
        label='Project Description'
    )
    project_start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control col-md-7 col-xs-12'}),
        label='Project Start Date'
    )

    project_end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control col-md-7 col-xs-12'}),
        label='Project End Date'
    )

    project_total_working_hr = forms.IntegerField(
        label='Project Total Working Hours',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
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
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise forms.ValidationError("Amount should be greater than 0")
        else:
            return amount

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
        opportunity_modify.project_description = project_description
        opportunity_modify.project_start_date = project_start_date
        opportunity_modify.project_end_date = project_end_date
        opportunity_modify.project_total_working_hr = project_total_working_hr
        opportunity_modify.save()
        return instance


class AddExistingClientOpportunity(forms.ModelForm):

    client = forms.ModelChoiceField(
        queryset=CLIENT.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control col-md-7 col-xs-12 select2_group form-control'}
        )
    )
    project_start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control col-md-7 col-xs-12'}),
        label='Project Start Date'
    )

    project_end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control col-md-7 col-xs-12'}),
        label='Project End Date'
    )
    project_total_working_hr = forms.IntegerField(
        label='Project Total Working Hours',
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )

    project_name = forms.CharField(
        max_length=100,
        label='Project Name',
        required='True',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    project_description = forms.CharField(
        max_length=10000,
        label='Project Description',
        widget=forms.Textarea(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    opportunity = forms.ModelChoiceField(
        queryset=Opportunity.objects.filter(Q(status='Approved') & Q(client__isnull='True')),
        required='True',
        widget=forms.Select(
            attrs={'class': 'form-control col-md-7 col-xs-12 select2_group form-control'}
        )
    )

    amount = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}
        )
    )

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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise forms.ValidationError("Amount should be greater than 0")
        else:
            return amount

    class Meta:
        model = Opportunity
        fields = (
            'client',
            'project_start_date',
            'project_end_date',
            'project_name',
            'project_description',
            'project_total_working_hr'
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        client = instance.client
        project_start_date = instance.project_start_date
        project_end_date = instance.project_end_date
        project_name = instance.project_name
        project_description = instance.project_description
        project_total_working_hr = instance.project_total_working_hr
        opportunity = self.cleaned_data.get('opportunity')
        project_description = instance.project_description
        opportunity_modify = Opportunity.objects.get(id=opportunity.pk)
        opportunity_modify.client = client
        opportunity_modify.project_name = project_name
        opportunity_modify.project_description = project_description
        opportunity_modify.project_start_date = project_start_date
        opportunity_modify.project_end_date = project_end_date
        opportunity_modify.project_total_working_hr = project_total_working_hr
        opportunity_modify.amount = self.cleaned_data.get('amount')
        opportunity_modify.save()

        project = IT_Project.objects.create(
            project_name=project_name,
            project_description=project_description,
            project_start_date_time=project_start_date,
            project_end_date_time=project_end_date,
            project_total_working_hr=project_total_working_hr,
            opportunity=opportunity,
        )
        project.save()

        return instance
