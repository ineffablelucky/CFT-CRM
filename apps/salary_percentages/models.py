from django.db import models
from datetime import datetime
class Salary_calculations(models.Model):

    financial_year = models.CharField(null=True, max_length=5)
    allowances = models.CharField(max_length=45)
    hra_percentage = models.IntegerField()
    ppf_percentage =  models.IntegerField()
