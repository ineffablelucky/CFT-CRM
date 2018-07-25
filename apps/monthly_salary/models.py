from django.db import models
from django.db import models
from apps.users.models import MyUser
from django.conf import settings
from django.db.models.signals import post_save
from apps.salary_percentages.models import Salary_Structure
from django.utils import timezone
from apps.ctc import models as ctc_models
from datetime import datetime
from apps.attendance.models import Attendance

class Monthly_Salary(models.Model):
    staff=models.ForeignKey(MyUser,on_delete=models.PROTECT, null=True)
    month=models.CharField(max_length=2,default=timezone.now().month,null=False)
    year=models.CharField(max_length=4,default=timezone.now().year,null=False)
    basic_monthly_salary=models.IntegerField(default=0,blank=True,null=True)
    hra=models.IntegerField(blank=True,null=True)
    dearness_allowance=models.IntegerField(blank=True,null=True)
    pf = models.IntegerField(blank=True,null=True)
    medical_allowance=models.IntegerField(blank=True,null=True)
    conveyance_allowance=models.IntegerField(blank=True,null=True)
    washing_allowance=models.IntegerField(blank=True,null=True)
    other_allowance=models.IntegerField(blank=True,null=True)
    fixed_monthly_salary=models.IntegerField(blank=True,null=True)
    deduction_due_to_leaves=models.IntegerField(blank=True,default=0,null=True)
    total_deductions=models.IntegerField(blank=True,null=True)
    given_bonus=models.IntegerField(blank=True,default=0,null=True)
    net_salary=models.IntegerField(blank=True,null=True)

    # def procedure(id, year, month):
    #
    #     start_date = datetime.strptime(year + '-' + month + '-' + '01', '%Y-%m-%d')
    #
    #     if month == "1" or month == "3" or month == "5" or month == "7" or month == "8" or month == "10" or month == "12":
    #         end_date = datetime.strptime(year + '-' + month + '-' + '31', '%Y-%m-%d')
    #
    #     else:
    #         end_date = datetime.strptime(year + '-' + month + '-' + '30', '%Y-%m-%d')
    #
    #     if MyUser.objects.filter(id=id, created_on__lte=start_date):
    #         ctc_objects = CTC_breakdown.objects.get(staff_id=id)
    #         attendance_objects = Attendance.objects.filter(user_id=id, date__gte=start_date,
    #                                                        date__lte=end_date).order_by('date')
    #
    #         if month == "1" or month == "3" or month == "5" or month == "7" or month == "8" or month == "10" or month == "12":
    #             fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 31)
    #         else:
    #             fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 30)
    #
    #         print(fixed_daily_salary)
    #
    #         final_daily_sal_list = []
    #         for a in attendance_objects:
    #             if a.status == "On Leave":
    #                 daily_deduction = 0
    #             elif a.status == "present":
    #                 if a.note.find("Late") != -1:
    #                     daily_deduction = float(fixed_daily_salary / 3)
    #                 else:
    #                     daily_deduction = 0
    #             elif a.status == "absent":
    #                 if a.note == "PL" or a.note == "CL":
    #                     daily_deduction = 0
    #                 else:
    #                     daily_deduction = fixed_daily_salary
    #             final_daily_salary = fixed_daily_salary - daily_deduction
    #             final_daily_sal_list.append(final_daily_salary)
    #
    #         if month == '1' or month == '3' or month == '5' or month == '7' or month == '8' or month == '10' or month == '12':
    #             free_sal = (31 - len(final_daily_sal_list)) * fixed_daily_salary
    #         else:
    #             free_sal = (30 - len(final_daily_sal_list)) * fixed_daily_salary
    #         working_sal = sum(final_daily_sal_list)
    #         final_monthly_salary = int(working_sal + free_sal)
    #         deduction_due_to_leaves = int(ctc_objects.fixed_monthly_salary - final_monthly_salary)
    #         temp = {'deduction_due_to_leaves': deduction_due_to_leaves, 'final_monthly_salary': final_monthly_salary,
    #                 'ctc_objects': ctc_objects}
    #         return temp
    #     else:
    #         return None
    def __str__(self):
        return "%d%s%s"%(self.staff_id,self.month,self.year)

    def save(self, **kwargs):

        salary_structure_objects = Salary_Structure.objects.get(financial_year=self.year)

        self.hra = (salary_structure_objects.hra_percentage*self.basic_monthly_salary)/100
        self.dearness_allowance = (salary_structure_objects.dearness_percentage*self.basic_monthly_salary)/100
        self.pf = (salary_structure_objects.pf_percentage*self.basic_monthly_salary)/100
        self.medical_allowance = salary_structure_objects.medical_allowance
        self.conveyance_allowance=salary_structure_objects.conveyance_allowance
        self.washing_allowance=salary_structure_objects.washing_allowance
        self.other_allowance=(salary_structure_objects.other_allowance_percentage*self.basic_monthly_salary)/100
        self.fixed_monthly_salary=self.basic_monthly_salary+self.hra+self.dearness_allowance+self.medical_allowance+self.conveyance_allowance+self.other_allowance+self.washing_allowance
        #self.deduction_due_to_leaves=procedure(self.staff_id,self.year,self.month)
        self.total_deductions=self.pf+self.deduction_due_to_leaves
        self.net_salary=self.fixed_monthly_salary-self.total_deductions
        super(Monthly_Salary, self).save(**kwargs)


    # def __init__(self):
    #     if MyUser.objects.filter(id=staff_id,date_of_joining):

def create_profile(sender,**kwargs):
    if kwargs['created'] :
        if kwargs.get('instance').designation != 'Client':
            Monthly_Salary.objects.create(staff=kwargs['instance'])

post_save.connect(create_profile,sender=settings.AUTH_USER_MODEL)







