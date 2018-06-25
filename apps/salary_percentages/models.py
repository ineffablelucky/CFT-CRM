from django.db import models
from apps.ctc.models import CTC_breakdown


class Salary_calculations(models.Model):

    financial_year = models.IntegerField(default=2018, null=False)
    allowances = models.IntegerField(default=6, null=False)
    hra_percentage = models.IntegerField(default=12, null=False)
    ppf_percentage =  models.IntegerField(default=20, null=False)

class Employee_details(models.Model):
    worker=models.ForeignKey(CTC_breakdown,to_field='employee',on_delete=models.PROTECT,null=True)
    ctc = models.IntegerField( default=200000)
    given_bonus = models.IntegerField(default=0)
    percentage_bonus_of_max_bonus=models.IntegerField(default=0)

    def percentage_bonus_amt(self):
        a=CTC_breakdown.objects.filter(employee_id=self.worker_id).values('ctc_max_bonus')
        self.percentage_bonus_of_max_bonus=int((self.given_bonus/a)*100)