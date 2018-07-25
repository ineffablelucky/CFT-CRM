from django.db import models
from apps.users.models import MyUser
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone
from apps.salary_percentages.models import Salary_Structure
from apps.monthly_salary.models import Monthly_Salary

class CTC_breakdown(models.Model):

    staff=models.ForeignKey(MyUser,on_delete=models.PROTECT,related_name='staff')
    year = models.IntegerField(null=True,default=timezone.now().year)
    basic_yearly = models.IntegerField(null=True,blank=True)
    hra_yearly = models.IntegerField(null=True,blank=True)
    pf_yearly = models.IntegerField(null=True,blank=True)
    conveyance_allowance_yearly=models.IntegerField(null=True,blank=True)
    dearness_allowance_yearly=models.IntegerField(null=True,blank=True)
    medical_allowance_yearly=models.IntegerField(null=True,blank=True)
    washing_allowance_yearly=models.IntegerField(null=True,blank=True)
    other_allowance_yearly = models.IntegerField(null=True,blank=True)
    max_bonus = models.IntegerField(null=True,blank=True)
    fixed_yearly_salary = models.IntegerField(null=True,blank=True)
    ctc = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return "%d%s%s"%(self.staff_id,self.staff.username,self.year)

    def save(self, **kwargs):

        Salary_Structure_data = Salary_Structure.objects.get(financial_year=self.year)
        monthly_data=Monthly_Salary.objects.get(staff_id=self.staff_id,year=self.year)

        self.basic_yearly = (monthly_data.basic_monthly_salary)*12
        self.hra_yearly = (monthly_data.hra)*12
        self.pf_yearly = (monthly_data.pf)*12
        self.conveyance_allowance_yearly = (monthly_data.conveyance_allowance)*12
        self.dearness_allowance_yearly = (monthly_data.dearness_allowance)*12
        self.medical_allowance_yearly = (monthly_data.medical_allowance) * 12
        self.washing_allowance_yearly = (monthly_data.washing_allowance) * 12
        self.other_allowance_yearly = (monthly_data.other_allowance) * 12
        self.max_bonus = Salary_Structure_data.max_bonus_percentage * self.basic_yearly / 100
        self.fixed_yearly_salary = monthly_data.fixed_monthly_salary * 12
        self.ctc = self.fixed_yearly_salary + (2 * self.pf_yearly) + self.max_bonus
        super(CTC_breakdown, self).save(**kwargs)

def create_profile(sender,**kwargs):
    if kwargs['created'] :
        if kwargs.get('instance').designation != 'Client':
            CTC_breakdown.objects.create(staff=kwargs['instance'])

post_save.connect(create_profile,sender=settings.AUTH_USER_MODEL)
