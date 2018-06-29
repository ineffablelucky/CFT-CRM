from django.db import models
from ..users.models import MyUser
from django.conf import settings
from django.db.models.signals import post_save


class Leave(models.Model):
    pl = models.IntegerField(default=8)
    cl = models.IntegerField(default=8)
    half_day = models.IntegerField(default=0)
    comp_off = models.IntegerField(default=8)
    user = models.OneToOneField(MyUser, on_delete=models.PROTECT, blank=True, default=None)

    class Meta:
        permissions = (
            ('view_Leave', 'Can view Leave'),
        )


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Leave.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
