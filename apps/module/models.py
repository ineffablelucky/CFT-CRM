from django.db import models
from ..project.models import IT_Project
from ..users.models import MyUser

class Module(models.Model):
    module_name = models.CharField(max_length=250, blank=True,null=True,)
    module_description = models.CharField(max_length=1000, blank=True,null=True,)
    project = models.ForeignKey(IT_Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.module_name
