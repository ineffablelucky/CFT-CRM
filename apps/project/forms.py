from django.forms import ModelForm
from .models import IT_Project
from django import forms
from django.utils import timezone
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from apps.client.models import CLIENT

class CreateProjectForm(ModelForm):
    Project_status = (
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    )

    project_name = forms.CharField(
        widget=forms.TextInput()
    )

    project_description = forms.CharField(
        widget=forms.TextInput()
    )

    opportunity = forms.ModelChoiceField(
        queryset= Opportunity.objects.all(),
        widget= forms.Select()
    )

    project_manager = forms.ModelChoiceField(
        queryset= MyUser.objects.all(),
        widget=forms.Select()
    )
    project_price = forms.CharField(
        widget=forms.TextInput()
    )
    project_start_date_time = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    project_end_date_time = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    project_total_working_hr = forms.CharField(
        widget=forms.TextInput()
    )
    client_id = forms.ModelChoiceField(
        queryset=CLIENT.objects.all(),
        widget=forms.Select()
    )
    employees_per_project = forms.ModelChoiceField(
        queryset=MyUser.objects.all(),
        widget=forms.CheckboxSelectMultiple(),

    )
    status = forms.ChoiceField(
        choices=Project_status,
        widget=forms.Select()
    )

    class Meta:
        model = IT_Project
        fields = (
            'opportunity',
            'project_name',
            'project_description',
            'project_manager',
            'project_price',
            'project_start_date_time',
            'project_end_date_time',
            'project_total_working_hr',
            'client_id',
            'employees_per_project',
            'status',
        )

    def __init__(self,  *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        #self.fields['project_name'].initial = timezone.now().date
        self.fields['project_description'].widget.attrs['placeholder']= 'asfsadf'

