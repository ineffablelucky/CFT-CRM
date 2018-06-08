from django.db import models
from ..project.models import IT_Project

class Task(models.Model):
    project = models.ForeignKey(IT_Project, on_delete=models.CASCADE, blank=True, null=True)
    task_name = models.CharField(max_length=30)
    task_description = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=30)
    task_start_date_time = models.DateTimeField()
    task_end_date_time = models.DateTimeField()
    status = models.CharField(max_length=30)



class Time_Entry(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    task_start_date_time = models.DateTimeField()
    task_end_date_time = models.DateTimeField()
    task_project_id = models.IntegerField()
