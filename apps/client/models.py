from django.db import models
from apps.users.models import MyUser


class CLIENT(models.Model):

    company_name = models.CharField(max_length=100)
    client_user = models.OneToOneField(MyUser, on_delete=models.PROTECT)
