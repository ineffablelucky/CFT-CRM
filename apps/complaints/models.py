from django.db import models

# Create your models here.


class Complaints(models.Model):
    fromEmp=models.CharField(max_length=45)
    againstEmp = models.CharField(max_length=45)
    description=models.CharField(max_length=70)
    date=models.DateField()