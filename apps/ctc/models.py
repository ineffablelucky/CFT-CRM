from django.db import models
from django.utils import timezone
from apps.users.models import MyUser
import apps.salary_percentages as s_percent
from django.db.models.signals import post_save
from django.conf import settings

class CTC_breakdown(models.Model):

    employee = models.OneToOneField(MyUser, on_delete=models.PROTECT, null=True)
    basic = models.IntegerField(default=12)
    hra = models.IntegerField(default=12)
    ppf = models.IntegerField(default=12)
    allowances = models.IntegerField(default=12)
    year = models.IntegerField(default=timezone.now().year)
    ctc_max_bonus = models.IntegerField(default=12)
    fixed_monthly_salary = models.IntegerField(default = 20000)
    #deduction_due_to_leaves
    #final_amount

    def ctc_amt(self):
        a = s_percent.models.Employee_details.objects.filter(worker_id = self.employee_id).values('ctc')
        return a

    @property
    def basic_amt(self):
        self.basic = 0.5*self.ctc_amt()

    @property
    def hra_amt(self):
        a = s_percent.models.Salary_calculations.objects.filter(financial_year=self.year).values('hra_percentage')
        self.hra = int((a*self.basic)/100)

    @property
    def allowances_amt(self):
        a = s_percent.models.Salary_calculations.objects.filter(financial_year=self.year).values('allowances')
        self.allowances = int((a*self.basic)/100)

    @property
    def ppf_amt(self):
        a = s_percent.models.Salary_calculations.objects.filter(financial_year=self.year).values('ppf_percentage')
        self.ppf = int((a*self.basic)/100)

    @property
    def max_bonus_amt(self):
        self.ctc_max_bonus = (self.ctc_amt()-(self.basic+self.allowances+self.hra+(2*self.ppf)))

    @property
    def fixed_amt(self):
       self.fixed_monthly_salary = (self.basic + self.hra + self.allowances)/12


def create_profile(sender, **kwargs):
    if kwargs['created']:
        CTC_breakdown.objects.create(employee=kwargs['instance'])

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
