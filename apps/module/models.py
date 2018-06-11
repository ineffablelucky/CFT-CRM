from django.db import models
from ..project.models import IT_Project


class Module(models.Model):

    project = models.ForeignKey(IT_Project, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)