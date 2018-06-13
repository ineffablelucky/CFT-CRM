from django.forms import ModelForm
from .models import IT_Project

class CreateProjectForm(ModelForm):
    class Meta:
        model = IT_Project
        fields = (
            'opportunity',
            'project_name',
            'project_description',
            'project_manager',
            'project_price',
            'project_start_date_time',
            'project_end_date_time',
            'project_total_working_hr',
            'client_id',
            'employees_per_project',
            'status',
        )

