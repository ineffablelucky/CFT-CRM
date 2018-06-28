from django.db import models
from ..project.models import IT_Project
from ..users.models import MyUser
task_status = (
        ('start later', 'start later'),
        ('started', 'started'),
        ('completed', 'completed'),
        ('in progress', 'in progress'),
    )
task_current_state = (

    ('stopped', 'stopped'),
    ('running', 'running'),
)

class Task(models.Model):
    project = models.ForeignKey(IT_Project, on_delete=models.PROTECT, blank=True, null=True)
    task_name = models.CharField(max_length=30, blank=True,null=True,)
    task_description = models.CharField(max_length=1000, blank=True,null=True,)
    employee_id = models.ForeignKey(MyUser, on_delete=models.PROTECT, blank=True, null=True)
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)
    status = models.CharField(max_length=30, blank=True,null=True, choices=task_status)
    expected_time = models.CharField(max_length=30, blank=True,null=True, default=4)
    task_current_state = models.CharField(max_length=10, blank=True, null=True, default='stopped', choices=task_current_state)

    def __str__(self):
        return self.task_name


    class Meta:
        permissions = (
            ('view_task', 'Can view tasks'),
        )

class Time_Entry(models.Model):

    task = models.ForeignKey(Task, on_delete=models.PROTECT, blank=True, null=True, related_name="taskname")
    task_start_date_time = models.DateTimeField(blank=True,null=True,)
    task_end_date_time = models.DateTimeField(blank=True,null=True,)
    time_per_session = models.DateTimeField(max_length=30, blank=True, null=True,)
    time_spent = models.DateTimeField(max_length=30, blank=True, null=True,)
