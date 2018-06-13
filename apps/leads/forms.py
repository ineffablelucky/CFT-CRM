from .models import LEADS
from django import forms
from django.forms import ModelForm


class CreateForm(forms.ModelForm):
    class Meta:
        model = LEADS
        fields = '__all__'


c=CreateForm()
print(c)
