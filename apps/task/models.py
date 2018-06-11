from django.db import models
from ..project.models import IT_Project
from ..users.models import MyUser

class Task(models.Model):
    project = models.ForeignKey(IT_Project, on_delete=models.CASCADE, blank=True, null=True)
    task_name = models.CharField(max_length=30, blank=True,null=True,)
    task_description = models.CharField(max_length=30, blank=True,null=True,)
    employee_id = models.CharField(max_length=30, blank=True,null=True,)
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)
    status = models.CharField(max_length=30, blank=True,null=True,)



class Time_Entry(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)
    task_project_id = models.IntegerField(blank=True,null=True,)
