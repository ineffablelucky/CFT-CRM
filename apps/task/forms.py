import re
from django.forms import ModelForm
from .models import Task
from django import forms
from django.utils import timezone
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from apps.client.models import CLIENT
from apps.project.models import IT_Project
from django.db.models import Q


class CreateTaskForm(ModelForm):

    task_status = (
        ('start later', 'start later'),
        ('started', 'started'),
        ('completed', 'completed'),
        ('in progress', 'in progress'),
    )

    # project = forms.ModelChoiceField(
    #     label='PROJECT NAME',
    #     # required=False,
    #     queryset=IT_Project.objects.all(),
    #     widget=forms.Select(),
    # )

    project = forms.CharField(
        widget=forms.TextInput(attrs={'type':'readonly'}), label='PROJECT NAME'

    )

    task_name = forms.CharField(
        label = 'TASK NAME',

        widget=forms.TextInput(

        )
    )

    task_description = forms.CharField(
        label= 'TASK DESCRIPTION',
        required=False,
        widget=forms.Textarea()
    )

    employee_id = forms.ModelChoiceField(
        label='ASSIGN TO',
        # required=False,
        queryset=MyUser.objects.filter(Q(department='IT') & Q(designation='Employee')),
        widget=forms.Select(),
    )

    task_start_date_time = forms.CharField(
        label='TASK START DATE',
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    task_end_date_time = forms.CharField(
        label='TASK END DATE',
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    expected_time = forms.IntegerField(
        label='EXPECTED WORKING HOURS',
        widget=forms.TextInput()
    )

    status = forms.ChoiceField(
        label='STATUS',
        choices=task_status,
        widget=forms.Select()
    )

    class Meta:
        model = Task
        fields = (
            # 'project',
            'task_name',
            'task_description',
            'employee_id',
            'task_start_date_time',
            'task_end_date_time',
            'status',
            'expected_time',
        )
    def __init__(self,  *args, **kwargs):
        self.project_id = kwargs.pop('project_id')
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        x = IT_Project.objects.get(id=self.project_id)
        print('$$$$$$$$$$$$$$$$$$$$$$')
        print(x.project_name)
        self.fields['project'].initial = x.project_name
        print('In form')
        print(self.fields['project'].initial)
        self.fields['task_start_date_time'].initial = timezone.now().date
        self.fields['task_end_date_time'].initial = timezone.now().date
        self.fields['task_description'].widget.attrs['placeholder']= 'write task description here'
        self.fields['task_name'].widget.attrs['placeholder']= 'write task name here'
        # self.fields['project_description'].widget.attrs['placeholder']= 'write project description here'



    # def __init__(self, *args, **kwargs):
    #     self.oppo = kwargs.pop('oppo_id')
    #     super().__init__(*args, **kwargs)
    #     self.fields['Opportunity'].initial = self.oppo
    #
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     print(self.oppo)
    #     instance.Opportunity_id = self.oppo
    #     instance.save()
    #     return instance


    # def __init__(self,  *args, **kwargs):
    #     super(CreateProjectForm, self).__init__(*args, **kwargs)
    #     self.fields['project_name'].initial = timezone.now().date
    #     self.fields['project_description'].widget.attrs['placeholder']= 'asfsadf'

    # def clean_task_name(self):
    #     value = self.cleaned_data.get('task_name')
    #     if len(value) < 3:
    #         raise forms.ValidationError('Name too small')
    #     return value

    # def clean_opportunity(self):
    #     value = self.cleaned_data['opportunity']
    #     print(" ##############################  ",value.id)
    #     if self.instance.pk is not None:
    #         return value
    #     else:
    #         pass

    # def clean_project_name(self):
    #     data = self.cleaned_data.get('project_name')
    #     if re.match('^\w*$', data):
    #     #if re.match(r'^[-a-zA-Z0-9_]+$',data):
    #         return data
    #     else:
    #         raise forms.ValidationError("Only alphabets and numbers are allowed")
    #
    # def clean_project_description(self):
    #     data = self.cleaned_data.get('project_description')
    #     if re.match('^\w*$', data):
    #     #if re.match(r'^[-a-zA-Z0-9_]+$',data):
    #         return data
    #     else:
    #         raise forms.ValidationError("Only alphabets and numbers are allowed")
    #


    # def clean_expected_time(self):
    #      data = self.cleaned_data.get('expected_time')
    #      data = str(data)
    #      if re.match(r'^[0-9_]+$', data):
    #          return data
    #      else:
    #          raise forms.ValidationError("Only Numbers are alllowed")

    # def clean_project_total_working_hr(self):
    #      data = self.cleaned_data.get('project_total_working_hr')
    #      data = str(data)
    #      if re.match(r'^[0-9_]+$', data):
    #          return data
    #      else:
    #          raise forms.ValidationError("Only Numbers are alllowed")

    # def clean_task_end_date_time(self):
    #     data = self.cleaned_data.get('project_end_date_time')
    #     value = self.cleaned_data.get('project_start_date_time')
    #
    #     if(data > value):
    #         return data
    #     else:
    #         raise forms.ValidationError("Project end date should be either same or more than start date!")