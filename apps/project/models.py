from django.db import models
from ..users.models import MyUser
from ..client. models import CLIENT
from ..opportunity.models import Opportunity

class IT_Project(models.Model):
    Project_status = (
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('started', 'Started'),
    )
    opportunity = models.OneToOneField(Opportunity, on_delete=models.PROTECT, blank=True, default=None)
    project_name = models.CharField(max_length=30, blank=True,null=True,)
    project_description = models.CharField(max_length=30, blank=True,null=True,)
    project_manager = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True,null=True,)
    project_price = models.IntegerField(blank=True,null=True,)
    project_start_date_time = models.DateTimeField(blank=True,null=True,)
    project_end_date_time = models.DateTimeField(blank=True,null=True,)
    project_total_working_hr = models.IntegerField(blank=True,null=True,)
    project_total_time_taken = models.IntegerField(blank=True,null=True,)
    client_id = models.ForeignKey(CLIENT, on_delete=models.CASCADE, blank=True, null=True)
    employees_per_project = models.ManyToManyField(MyUser, blank=True, related_name='employees_per_project')
    status = models.CharField(max_length=30, choices=Project_status, default='In progress')




