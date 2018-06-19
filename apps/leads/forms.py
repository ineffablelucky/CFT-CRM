from .models import LEADS
from django import forms
from django.forms import ModelForm
from ..users.models import MyUser


class CreateForm(forms.ModelForm):

    class Meta:
        model = LEADS
        fields = '__all__'



class DetailForm(forms.Form):
    assign = forms.ModelChoiceField(
        label='select employee',
        queryset=MyUser.objects.filter(department='Marketing'),
        widget=forms.Select()
    )
    # checkbox=forms.CheckboxInput()
    # class Meta:
    #     model=LEADS
    #     fields='__all__'






