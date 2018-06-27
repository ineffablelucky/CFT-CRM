from django.db import models
from apps.ctc.models import CTC_breakdown
from django.db.models.signals import post_save

class Salary_calculations(models.Model):

    financial_year = models.IntegerField(default=2018, null=False)
    allowances = models.IntegerField(default=6, null=False)
    hra_percentage = models.IntegerField(default=12, null=False)
    ppf_percentage =  models.IntegerField(default=20, null=False)

    def __str__(self):
        return "%d"%(self.financial_year)

class Employee_details(models.Model):
    worker=models.OneToOneField(CTC_breakdown,to_field='employee',on_delete=models.PROTECT,null=True)
    ctc = models.IntegerField( default=200000,null=True)
    given_bonus = models.IntegerField(default=0,null=True)
    percentage_bonus_of_max_bonus=models.IntegerField(default=0,null=True)

    def __str__(self):
        return '%d'%(self.worker_id)

    def percentage_bonus_amt(self):
        a=CTC_breakdown.objects.filter(employee_id=self.worker_id).values('ctc_max_bonus')
        self.percentage_bonus_of_max_bonus=int((self.given_bonus/a)*100)

def create_profile(sender,**kwargs):
    if kwargs['created']:
        Employee_details.objects.create(worker=kwargs['instance'])

post_save.connect(create_profile,sender=CTC_breakdown)
