from django.forms import ModelForm
from .models import Module

class CreateProjectForm(ModelForm):
    class Meta:
        model = Module
        fields = '__all__'