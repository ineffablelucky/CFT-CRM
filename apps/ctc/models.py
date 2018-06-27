from django.db import models
from django.utils import timezone
from apps.users.models import MyUser
import apps.salary_percentages as s_percent
from django.db.models.signals import post_save
from django.conf import settings

class CTC_breakdown(models.Model):

    employee = models.OneToOneField(MyUser, on_delete=models.PROTECT, null=True)
    basic = models.IntegerField(default=18000)
    hra = models.IntegerField(default=40)
    ppf = models.IntegerField(default=13)
    allowances = models.IntegerField(default=10)
    year = models.IntegerField(default=timezone.now().year)
    ctc_max_bonus = models.IntegerField(default=5)
    fixed_monthly_salary = models.IntegerField(default = 20000)
    #deduction_due_to_leaves
    #final_amount

    def __str__(self):
        return "%d"%(self.year)

    #def __init__(self):
    #    self.basic=self.basic_amt()
    #    self.hra=self.hra_amt()
    #    self.allowances=self.allowances_amt()
    #    self.ppf=self.ppf_amt()

    def ctc_amt(self):
        a = s_percent.models.Employee_details.objects.get(worker_id=self.employee_id)
        return a.ctc

    def save(self, *args, **kwargs):
        ctc_value=s_percent.models.Employee_details.objects.get(worker_id=self.employee_id)
        a = s_percent.models.Salary_calculations.objects.get(financial_year=self.year)

        self.basic = int((ctc_value.get('ctc')) * 0.5)
        self.hra = int((a.hra_percentage*self.basic)/100)
        self.allowances=int((a.allowances*self.basic)/100)
        self.ppf=int((a.ppf_percentage*self.basic)/100)
        self.ctc_max_bonus=int((ctc_value.ctc-(self.basic+self.allowances+self.hra+(2*self.ppf))))
        self.fixed_monthly_salary= int((self.basic + self.hra + self.allowances)/12)
        super(CTC_breakdown, self).save(*args, **kwargs)

    #def basic_amt(self):
    #    self.basic = int(self.ctc_amt().get('ctc') * 0.5)
    #    return self.basic
        

def create_profile(sender, **kwargs):
    if kwargs['created']:
        CTC_breakdown.objects.create(employee=kwargs['instance'])

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
