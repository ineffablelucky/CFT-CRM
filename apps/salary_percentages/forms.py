from django import forms
from django.forms import ModelForm
from .models import Salary_calculations,Employee_details
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

    def clean_financial_year(self):
        data=self.cleaned_data['financial_year']
        if Salary_calculations.objects.filter(financial_year=data).exists():
            raise forms.ValidationError('Salary Structure for this year has already been formed ')
        return data

    '''def clean_allowances(self):
        data=self.cleaned_data['allowances']
        if type(self.allowances) not in data:
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data

    def clean_hra_percentage(self):
        data=self.cleaned_data['hra_percentage']
        if type(self.hra_percentage) not in data:
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data


    def clean_ppf_percentage(self):
        data=self.cleaned_data['ppf_percentage']
        if type(self.ppf_percentage)>100:
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data'''

class CtcForm(ModelForm):

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            #tmp = Ctc_breakdown.objects.create(basic = instance.ctc*0.5)
        return instance

    class Meta:
        model=Employee_details
        fields=['ctc','given_bonus']





