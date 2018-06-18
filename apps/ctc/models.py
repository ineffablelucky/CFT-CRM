from django.db import models

# Create your models here.
class CTC_breakdown(models.Model):
    break_up = models.CharField(max_length=250)
    calculations = models.IntegerField()
    monthly_salary = models.IntegerField()
    yearly_salary = models.IntegerField()


