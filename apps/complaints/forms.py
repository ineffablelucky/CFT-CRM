from django import forms
from django.conf import settings
from django.forms import ModelForm
from apps.users.models import MyUser



from .models import Complaints


class createcomplaintsform(ModelForm):
    date = forms.CharField(
        label='date',
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': '',}
        )
    )
    # againstEmp = forms.ModelChoiceField(
    #     label='againstEmp',
    #     to_field_name='department',
    #     queryset=MyUser.objects.only('department').all(),
    #
    # )

    department_choice = (
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
        ('Accounts', 'Accounts'),
        ('IT', 'IT'),

    )
    againstEmp = forms.ChoiceField(
        label='againstEmp',
        choices=department_choice,
        widget=forms.Select(


        )
    )



    class Meta:
        model=Complaints
        fields=('fromEmp','againstEmp','description','date')