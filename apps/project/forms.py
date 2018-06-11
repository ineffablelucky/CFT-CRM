from django.forms import ModelForm
from .models import IT_Project

class CreateProjectForm(ModelForm):
    class Meta:
        model = IT_Project
        fields = '__all__'