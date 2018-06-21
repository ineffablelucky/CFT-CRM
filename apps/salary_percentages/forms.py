from django import forms
from django.forms import ModelForm
from .models import Salary_calculations
from django.utils import timezone

class SalaryForm(ModelForm):
    financial_year = forms.CharField(
        widget=forms.TextInput(
            attrs= {'readonly' : True}
        )
    )
    '''
    class SalaryForm(ModelForm):
        allowances = forms.CharField(
            widget=forms.TextInput(
                attrs={'type' : 'number'}
            ))
        '''

    class Meta:
        model= Salary_calculations
        fields=['financial_year','allowances','hra_percentage','ppf_percentage']

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        self.fields['financial_year'].initial = timezone.now().year
        print(type(timezone.now().year))
    #def clean_allowances(self  ):

    