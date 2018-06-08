from django.db import models

class Salary_calculations(models.Model):
    cal_id = models.AutoField(primary_key=True)
    hra_percentage = models.IntegerField
    finanacial_year = models.IntegerField
    allowances =  models.CharField(max_length=45)
    ppf_percentage =  models.IntegerField