from django.db import models
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser


class MEETING(models.Model):

    description = models.TextField(max_length=10000, blank=True)
    Opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, blank=True, null=True, related_query_name='meeting'
    )
    date = models.DateField()
    extras = models.ManyToManyField(MyUser, related_name='meetings_extra', blank=True, null=True)


    def __unicode__(self):
        return self.date

    class Meta:
        permissions = (
            ('view_meeting', 'Can view Meetings'),
        )
