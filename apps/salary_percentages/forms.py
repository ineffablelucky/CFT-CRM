from django import forms
from django.forms import ModelForm
from .models import Salary_Structure
from django.utils import timezone

class SalaryStructureForm(ModelForm):
    financial_year = forms.CharField(required=False,
        widget=forms.TextInput(
            attrs= {'readonly' : True}
        )
    )
    hra_percentage=forms.FloatField()
    dearness_percentage=forms.FloatField()
    pf_percentage=forms.FloatField()
    medical_allowance = forms.FloatField()
    conveyance_allowance = forms.FloatField()
    washing_allowance = forms.FloatField()
    other_allowance_percentage=forms.FloatField()
    max_bonus_percentage=forms.FloatField()

    class Meta:
        model= Salary_Structure
        fields=['financial_year','hra_percentage','dearness_percentage','pf_percentage','medical_allowance','conveyance_allowance','washing_allowance','other_allowance_percentage','max_bonus_percentage']

    def __init__(self, *args, **kwargs):
        super(SalaryStructureForm, self).__init__(*args, **kwargs)
        self.fields['financial_year'].initial = timezone.now().year

    def clean_financial_year(self):
        data=self.cleaned_data['financial_year']
        if Salary_Structure.objects.filter(financial_year=data).exists():
            raise forms.ValidationError('Salary Structure for this year has already been formed ')
        return data

    # def clean(self):
    #     cleaned_data=super().clean()
    #     year=cleaned_data.get('year')
    #     if self.hra_percentage<0:
    #         raise forms.ValidationError('Enter a positive value ')
    #     return cleaned_data







