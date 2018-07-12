from django import forms
from django.forms import ModelForm
from django.utils import timezone
from .models import Monthly_Salary
from apps.ctc.models import CTC_breakdown
from django.utils import timezone

class BasicSalaryForm(ModelForm):

    #staff=forms.IntegerField(required=True)
    year = forms.CharField(
                           widget=forms.TextInput(
                               attrs={'readonly': True, 'class': 'form-control col-md-7 col-xs-12'}
                           ))

    month = forms.CharField(
        widget=forms.TextInput(
            attrs={'readonly': True,'class': 'form-control col-md-7 col-xs-12'}
        ))

    basic_monthly_salary= forms.FloatField(
                           widget=forms.TextInput(
                               attrs={'class': 'form-control col-md-7 col-xs-12'}))

    given_bonus=forms.IntegerField(widget=forms.TextInput(
                               attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model=Monthly_Salary
        fields=['basic_monthly_salary','given_bonus','year','month']

    def __init__(self, *args, **kwargs):
        super(BasicSalaryForm, self).__init__(*args, **kwargs)
        self.fields['year'].initial = timezone.now().year
        self.fields['month'].initial=timezone.now().month


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.year=self.cleaned_data.get('year')
            instance.month=self.cleaned_data.get('month')
            instance.save()
            local=CTC_breakdown.objects.get(staff_id=self.instance.staff_id,year=instance.year)
            local.year = instance.year
            local.save()
            my_list=[instance,local]
        return my_list

class SalaryGenerationForm(forms.Form):
    a=timezone.now().year
    year_choices = [tuple([str(x), x]) for x in range(2010, a+1)]

    year=forms.ChoiceField(choices=year_choices)

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






