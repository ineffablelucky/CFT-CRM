from django.db import models
from ..users.models import MyUser


class Leave(models.Model):
    pl = models.IntegerField(null=True)
    cl = models.IntegerField(null=True)
    half_day = models.IntegerField(null= True)
    comp_off = models.IntegerField(null= True)
    user = models.OneToOneField(MyUser, on_delete=models.PROTECT, blank=True)
