from django.db import models
from apps.salary_percentages.models import Salary_calculations


class CTC_breakdown(models.Model):
    break_up = models.CharField(max_length=250)
    calculations = models.IntegerField()
    monthly_salary = models.IntegerField()
    yearly_salary = models.IntegerField()

    def basic_sal(self):
        self.calculations = 0.5*gross

