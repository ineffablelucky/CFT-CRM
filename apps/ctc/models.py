from django.db import models
from django.utils import timezone
from apps.users.models import MyUser
import apps.salary_percentages as s_percent


class CTC_breakdown(models.Model):

    employee = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True,unique=True)
    basic = models.IntegerField(default=12)
    hra = models.IntegerField(default=12)
    ppf = models.IntegerField(default=12)
    allowances = models.IntegerField(default=12)
    ctc = models.IntegerField(default=12)
    year = models.IntegerField(default=timezone.now().year)
    ctc_max_bonus = models.IntegerField(default=12)
    fixed_monthly_salary = models.IntegerField(default = 20000)
    #deduction_due_to_leaves
    #final_amount

    @property
    def ctc_amt(self):
        self.ctc = s_percent.models.Employee_details.objects.filter(worker_id = self.employee_id).values('ctc')

    @property
    def basic_amt(self):
        self.basic = 0.5*self.ctc

    @property
    def hra_amt(self):
        a = s_percent.models.Salary_calculations.objects.filter(financial_year=self.year).values('hra_percentage')
        (self.hra) = int((a*self.basic)/100)

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
        self.ctc_max_bonus = (self.ctc-(self.basic+self.allowances+self.hra+(2*self.ppf)))

    @property
    def fixed_amt(self):
       self.fixed_monthly_salary = (self.basic + self.hra + self.allowances)/12
