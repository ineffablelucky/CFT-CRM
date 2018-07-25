from django.db import models

# Create your models here.


class Complaints(models.Model):
    fromEmp=models.CharField(max_length=45,blank=True)
    againstEmp = models.CharField(max_length=45,blank=True)
    description=models.CharField(max_length=70,blank=True)
    date=models.DateField(blank=True)