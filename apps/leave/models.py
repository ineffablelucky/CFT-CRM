from django.db import models
#from Crmproject.project.apps.users import User


class Leave(models.Model):
    pl = models.IntegerField(null = True)
    cl = models.IntegerField(null = True)
    half_day = models.IntegerField(null= True)
    comp_off = models.IntegerField(null= True)
#user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
