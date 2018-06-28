from django.db import models
from ..users.models import MyUser
from ..client. models import CLIENT
from ..opportunity.models import Opportunity
from datetime import datetime

class IT_Project(models.Model):
    Project_status = (
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    )
    opportunity = models.OneToOneField(Opportunity, on_delete=models.PROTECT, blank=True, null=True, default=None)
    project_name = models.CharField(max_length=30, blank=True,null=True,)
    project_description = models.CharField(max_length=10000, blank=True,null=True,)
    project_price = models.IntegerField(blank=True,null=True,)
    project_start_date_time = models.DateField(blank=True,null=True, default=datetime.now())
    project_end_date_time = models.DateField(blank=True,null=True, default=None)
    project_total_working_hr = models.IntegerField(blank=True,null=True,)
    project_total_time_taken = models.IntegerField(blank=True,null=True,)
    client_id = models.ForeignKey(CLIENT, on_delete=models.CASCADE, blank=True, null=True)
    employees_per_project = models.ManyToManyField(MyUser, blank=True, related_name='employees_per_project')
    status = models.CharField(max_length=30, choices=Project_status, default='active')

    def __str__(self):
        return self.project_name


    class Meta:
        permissions = (
            ('view_it_project', 'Can view projects'),
        )