from django.db import models
from apps.client.models import CLIENT
from apps.leads.models import LEADS
from apps.users.models import MyUser


class Opportunity(models.Model):

    CHOICES = (
        ('Approved', 'Approved'),
        ('RQ_stage', 'Requirement Stage'),
        ('Negotiation', 'Negotiation Stage'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')

    )
    price = models.BigIntegerField(default=0, blank=True, null=True)
    description = models.TextField(max_length=1000)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.PROTECT, blank=True, related_name='assigned_to')
    lead = models.OneToOneField(LEADS, on_delete=models.PROTECT, blank=True)
    client = models.ForeignKey(CLIENT, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES, default='Pending')
    proj_manager = models.ForeignKey(
        MyUser, on_delete=models.PROTECT, related_name='proj_manager', blank=True, null=True
    )

    def __str__(self):
        return self.description