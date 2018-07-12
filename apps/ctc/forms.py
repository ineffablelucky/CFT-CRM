from django import forms
from django.utils import timezone

class SalaryGenerationForm(forms.Form):
    a=timezone.now().year
    year_choices = [tuple([str(x), x]) for x in range(2010, a+1)]

    year = forms.ChoiceField(choices=year_choices)
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

