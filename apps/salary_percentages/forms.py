from django import forms
from django.forms import ModelForm
from .models import Salary_calculations
from django.utils import timezone

class SalaryForm(ModelForm):
    financial_year = forms.CharField(required=False,
        widget=forms.TextInput(
            attrs= {'readonly' : True}
        )
    )
    allowances=forms.IntegerField(required=False)
    hra_percentage=forms.IntegerField(required=False)
    ppf_percentage=forms.IntegerField(required=False)
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

    def clean_allowances(self):
        data=self.cleaned_data['allowances']
        if not (0<data<100):
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data

    def clean_hra_percentage(self):
        data=self.cleaned_data['hra_percentage']
        if not (0<data<100):
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data


    def clean_ppf_percentage(self):
        data=self.cleaned_data['ppf_percentage']
        if not (0<data<100):
            raise forms.ValidationError('Enter an integral value between 0-100')
        return data

    def clean(self):
        cleaned_data=super().clean()
        allowances=cleaned_data.get('allowances')
        hra_percentage = cleaned_data.get('hra_percentage')
        ppf_percentage = cleaned_data.get('ppf_percentage')
        if not (0<allowances+hra_percentage+ppf_percentage<100):
            raise forms.ValidationError('You have entered an incorrect data')
        return cleaned_data

class CtcForm(forms.Form):

    ctc = forms.IntegerField(required=False)
    given_bonus=forms.IntegerField(required=False)

    # class Meta:
    #     model=CTC_breakdown
    #     fields=['ctc','given_bonus']
    #
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if commit:
    #         instance.save()
    #         #tmp = Ctc_breakdown.objects.create(basic = instance.ctc*0.5)
    #     return instance
class SalaryGenerationForm(forms.Form):
    a=timezone.now().year
    year_choices = [tuple([str(x), x]) for x in range(2010, a+1)]

    year=forms.ChoiceField(choices=year_choices)

    # year = forms.ChoiceField(choices=year_choices,
    #     widget = forms.Select(
    #         attrs={"onChange":'formSubmit()'}
    #     )
    # )

    month_choices = (
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    )
    month = forms.ChoiceField(choices=month_choices)

    # month = forms.ChoiceField(choices = month_choices,
    #     widget=forms.Select(
    #         attrs={"onChange":'formSubmit()'}
    #     )
    # )






