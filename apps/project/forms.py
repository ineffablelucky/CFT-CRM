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
        label = 'PROJECT NAME',
        widget=forms.TextInput(

        )
    )

    project_description = forms.CharField(
        label= 'PROJECT DESCRIPTION',
        widget=forms.TextInput()
    )

    opportunity = forms.ModelChoiceField(
        label='OPPORTUNITY',
        queryset= Opportunity.objects.all(),
        widget= forms.Select()
    )

    project_manager = forms.ModelChoiceField(
        label='PROJECT MANAGER',
        queryset= MyUser.objects.all(),
        widget=forms.Select()
    )
    project_price = forms.CharField(
        label='PROJECT PRICE',
        widget=forms.TextInput()
    )
    project_start_date_time = forms.CharField(
        label='PROJECT START DATE',
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    project_end_date_time = forms.CharField(
        label='PROJECT END DATE',
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    project_total_working_hr = forms.CharField(
        label='TOTAL WORKING HOURS',
        widget=forms.TextInput()
    )
    client_id = forms.ModelChoiceField(
        label='CLIENT',
        queryset=CLIENT.objects.all(),
        widget=forms.Select()
    )
    employees_per_project = forms.ModelMultipleChoiceField(
        label='ALOT EMPLOYEES TO PROJECT',
        queryset=MyUser.objects.all(),
    )

    status = forms.ChoiceField(
        label='STATUS',
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

    def clean_project_name(self):
        value = self.cleaned_data.get('project_name')
        if len(value) < 3:
            raise forms.ValidationError('Name too small')
        return value

