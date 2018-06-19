from django.db import models
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone
from apps.users.models import MyUser


class CTC_breakdown(models.Model):

    break_up = models.CharField(max_length=250)
    calculations = models.IntegerField(default=0)
    monthly_salary = models.IntegerField(default=0)
    yearly_salary = models.IntegerField(default=0)
    employee = models.ForeignKey(MyUser,on_delete=models.CASCADE)

    #def basic_sal(self):
       # self.calculations =

class Dropdown(models.Model):

    a=timezone.now().year
    year_choices = [tuple([str(x),x]) for x in range(2010,a)]
    select_year=models.CharField(max_length=4,choices=year_choices,default=2018)

    month_choices = (
        ('january','January'),
        ('february', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('august', 'August'),
        ('september', 'September'),
        ('october', 'October'),
        ('november', 'November'),
        ('december', 'December')
    )
    select_month = models.CharField(max_length=50,choices=month_choices,default = 'January')


