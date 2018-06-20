from django.db import models
from ..project.models import IT_Project
from ..users.models import MyUser
task_status = (
        ('started', 'started'),
        ('completed', 'completed'),
        ('in progress', 'in progress'),
    )
class Task(models.Model):
    project = models.ForeignKey(IT_Project, on_delete=models.PROTECT, blank=True, null=True)
    task_name = models.CharField(max_length=30, blank=True,null=True,)
    task_description = models.CharField(max_length=30, blank=True,null=True,)
    employee_id = models.ForeignKey(MyUser, on_delete=models.PROTECT, blank=True, null=True)
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)
    status = models.CharField(max_length=30, blank=True,null=True, choices=task_status)
    expected_time = models.CharField(max_length=30, blank=True,null=True, default=4)

    def __str__(self):
        return self.task_name



class Time_Entry(models.Model):

    task = models.ForeignKey(Task, on_delete=models.PROTECT, blank=True, null=True)
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)

