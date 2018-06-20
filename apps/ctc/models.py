from django.db import models
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone
from apps.users.models import MyUser


class CTC_breakdown(models.Model):

    break_up = models.CharField(max_length=250)
    calculations = models.IntegerField(default=0)
    monthly_salary = models.IntegerField(default=0)
    yearly_salary = models.IntegerField(default=0)
    employee = models.ForeignKey(MyUser,on_delete=models.PROTECT,default=None)

    def basic_sal(self):
        self.calculations =

