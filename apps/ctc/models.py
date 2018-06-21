from django.db import models
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone
from apps.users.models import MyUser


class CTC_breakdown(models.Model):

    employee = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True)
    basic = models.IntegerField(default=12)
    hra = models.IntegerField(default=12)
    ppf = models.IntegerField(default=12)
    allowances = models.IntegerField(default=12)
    ctc = models.IntegerField(default=12)
    year = models.IntegerField(max_length=5, default=timezone.now().year)
    ctc_max_bonus = models.IntegerField(default=12)
    #given_Bonus = models.IntegerField()
    #percentage_bonus_of_max_bonus = models.IntegerField()
    #deduction_due_to_leaves
    #final_amount

    #def ctc_amt(self):
        #self.ctc = MyUser.objects.get(user.id = self.employee_id).values('salary')

    def basic_amt(self):
        self.basic = 0.5*self.ctc

    def hra_amt(self):
        a = Salary_calculations.objects.get(financial_year=self.year).values('hra_percentage')
        self.hra = (a*self.basic)/100

    def allowances_amt(self):
        a = Salary_calculations.objects.get(financial_year=self.year).values('allowances')
        self.allowances = (a*self.basic)/100

    def ppf_amt(self):
        a = Salary_calculations.objects.get(financial_year=self.year).values('ppf_percentage')
        self.ppf = (a*self.basic)/100

    def max_bonus_amt(self):
        b = (self.ctc-(self.basic+self.allowances+self.hra+(2*self.ppf)))

