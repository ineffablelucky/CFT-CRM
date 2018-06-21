from django.db import models
from datetime import datetime

class Salary_calculations(models.Model):

    financial_year = models.IntegerField(default=2018, null=False)
    allowances = models.IntegerField(default=6, null=False)
    hra_percentage = models.IntegerField(default=12, null=False)
    ppf_percentage =  models.IntegerField(default=20, null=False)

