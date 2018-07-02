from django.db import models
from apps.users.models import MyUser
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone

class Salary_calculations(models.Model):

    financial_year = models.IntegerField(default=2018, null=False)
    allowances = models.IntegerField(default=6, null=False)
    hra_percentage = models.IntegerField(default=12, null=False)
    ppf_percentage =  models.IntegerField(default=20, null=False)

    def __str__(self):
        return "%d" % (self.financial_year)

    class Meta:
        permissions = (
            ('view_Salary_calculations', 'Can view salary calculations'),
        )



class CTC_breakdown(models.Model):

    employee=models.OneToOneField(MyUser,on_delete=models.PROTECT,null=True,related_name='employee')
    ctc = models.IntegerField( default=200000,null=True)
    basic = models.IntegerField(default=18000)
    hra = models.IntegerField(default=40)
    ppf = models.IntegerField(default=13)
    allowances = models.IntegerField(default=10)
    year = models.IntegerField(default=timezone.now().year)
    ctc_max_bonus = models.IntegerField(default=5)
    given_bonus = models.IntegerField(default=0, null=True)
    percentage_bonus_of_max_bonus = models.IntegerField(default=0, null=True)
    fixed_monthly_salary = models.IntegerField(default=20000)
    #deduction_due_to_leaves_monthly=models.FloatField(default=0)
    #final_monthly_salary=models.FloatField(default=20000)

    # def __init__(self):
    #    self.basic=self.basic_amt()
    #    self.hra=self.hra_amt()
    #    self.allowances=self.allowances_amt()

    def save(self, *args, **kwargs):
        a = Salary_calculations.objects.get(financial_year=self.year)

        self.basic = int(self.ctc * 0.5)
        self.hra = int((a.hra_percentage * self.basic) / 100)
        self.ppf = int((a.ppf_percentage * self.basic) / 100)
        self.allowances = int((a.allowances * self.basic) / 100)
        self.ctc_max_bonus = int((self.ctc - (self.basic + self.allowances + self.hra + (2 * self.ppf))))
        self.percentage_bonus_of_max_bonus = int((self.given_bonus / self.ctc_max_bonus) * 100)
        self.fixed_monthly_salary = int((self.basic + self.hra + self.allowances) / 12)
        #self.final_monthly_salary = float(self.fixed_monthly_salary-self.deduction_due_to_leaves_monthly)
        super(CTC_breakdown, self).save(*args, **kwargs)

        # def basic_amt(self):
        #    self.basic = int(self.ctc_amt().get('ctc') * 0.5)
        #    return self.basic

# def create_profile(sender,**kwargs):
#     if kwargs['created'] :
#         print(kwargs.get('instance').designation)
#         if kwargs.get('instance').designation != 'Client':
#             CTC_breakdown.objects.create(employee=kwargs['instance'])
#
# post_save.connect(create_profile,sender=settings.AUTH_USER_MODEL)
