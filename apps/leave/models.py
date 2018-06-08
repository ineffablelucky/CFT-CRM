from django.db import models
from ..users.models import MyUser


class Leave(models.Model):
    pl = models.IntegerField(default=None)
    cl = models.IntegerField(default=None)
    half_day = models.IntegerField(default=None)
    comp_off = models.IntegerField(default=None)
    user = models.OneToOneField(MyUser, on_delete=models.PROTECT, blank=True, default=None)
