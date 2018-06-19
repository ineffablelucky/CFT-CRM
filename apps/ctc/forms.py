from django import forms
from django.forms import ModelForm
from .models import Dropdown

class DropForm(ModelForm):
    class Meta:
        model = Dropdown
        fields = ['select_year','select_month']


