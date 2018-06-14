from django.db import models
from ..users.models import MyUser


class Leave(models.Model):
    pl = models.IntegerField(default=8)
    cl = models.IntegerField(default=8)
    half_day = models.IntegerField(default=8)
    comp_off = models.IntegerField(default=8)
    user = models.OneToOneField(MyUser, on_delete=models.PROTECT, blank=True, default=None)
