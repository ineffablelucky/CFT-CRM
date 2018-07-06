import logging
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from django.utils import timezone
from apps.users.models import MyUser
from .models import Salary_calculations,CTC_breakdown
from .forms import SalaryForm,CtcForm,SalaryGenerationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.leave.models import Leave
from apps.attendance.models import Attendance
import datetime

def salary(request):
    context=CTC_breakdown.objects.all()
    return render(request,'work/salary.html',{'context':context})
# def salary(request):
#     context=get_user_model().objects.all()
#     return render(request,'work/salary.html',{'context':context})

def edit_salary(request,id):
    if request.method == 'POST':
        # form = CtcForm(request.POST)
        # if form.is_valid():
        #     form.save()
        # else:
        #     print(form.errors)
        a=CTC_breakdown.objects.get(employee_id=id)
        if 'ctc' in request.POST:
            a.ctc= int(request.POST['ctc'])
        if 'given_bonus' in request.POST:
            a.given_bonus=int(request.POST['given_bonus'])
        a.save()
        return HttpResponseRedirect(reverse('salary_percentages:edit_salary',kwargs={'id' : id}))
    ctc_objects=CTC_breakdown.objects.get(employee_id=id)
    return render(request,'work/edit_salary.html',{'ctc_objects':ctc_objects})

def edit_ctc(request,id):
    form=CtcForm()
    return render(request,'work/edit_ctc.html',{'form':form,'request_id':id})

def edit_bonus(request,id):
    form=CtcForm()
    return render(request,'work/edit_bonus.html',{'form':form,'request_id':id})

def salary_structure(request):
    context = Salary_calculations.objects.all()
    return render(request,'work/salary_struct_table.html',{'context':context})

def add(request):
    if request.method=="POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("salary_percentages:salary_structure"))
        else:
            return HttpResponse('You have entered an incorrect data')
    else :
        form = SalaryForm()
        return render(request,'work/salary_struct_form.html',{'form':form})

def upload_csv(request):

    data={}
    if request.method=="GET":
        return render(request,'work/upload_csv.html',data)

    try:
        csv_file = request.FILES("csv_file")

        if not csv_file.name.endswith('.csv'):
            messages.error('Sorry!! This file is not csv type')
            return HttpResponseRedirect(reverse("salary_percentages:upload_csv"))

        if csv_file.multiple_chunks():
            messages.error("Uploaded file is too big(%.2f MB) " % (csv_file.size / (1000*1000)))
            return HttpResponseRedirect(reverse("salary_percentages:upload_csv"))

        file_data = csv_file.read().decode('utf-8')
        lines=file_data.split("\n")

        for line in lines:
            fields=line.split(",")

            data_dict = {}
            data_dict["financial_year"] = fields[0]
            data_dict["allowances"] = fields[1]
            data_dict["hra_percentage"] = fields[2]
            data_dict["ppf_percentage"] = fields[3]
            print(data_dict)
            salary_percentages = Salary_calculations(**data_dict)
            salary_percentages.save()


    except Exception as e:

        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
    return HttpResponseRedirect(reverse("salary_percentages:salary_structure"))

def monthly_salary(request):
    context=CTC_breakdown.objects.all()
    form=SalaryGenerationForm()
    return render(request,'work/monthly_salary.html',{'context':context,'form':form})

def procedure(id,year,month):

    start_date = datetime.strptime(year + '-' + month + '-' + '01', '%Y-%m-%d')

    if month == "1" or month == "3" or month == "5" or month == "7" or month == "8" or month == "10" or month == "12":
        end_date = datetime.strptime(year + '-' + month + '-' + '31', '%Y-%m-%d')

    else:
        end_date = datetime.strptime(year + '-' + month + '-' + '30', '%Y-%m-%d')

    if MyUser.objects.filter(id=id,created_on__lte=start_date):
        ctc_objects = CTC_breakdown.objects.get(employee_id=id)
        attendance_objects = Attendance.objects.filter(user_id=id, date__gte = start_date, date__lte= end_date).order_by('date')

        print(ctc_objects)
        print(attendance_objects)

        if month == "1" or month == "3" or month == "5" or month == "7" or month == "8" or month == "10" or month == "12":
            fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 31)
        else:
            fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 30)

        print(fixed_daily_salary)

        final_daily_sal_list=[]
        for a in attendance_objects:
            if a.status=="On Leave":
                daily_deduction=0
            elif a.status=="present":
                if a.note.find("Late")!=-1:
                        daily_deduction=float(fixed_daily_salary/3)
                else:
                    daily_deduction=0
            elif a.status=="absent":
                if a.note=="PL" or a.note=="CL":
                    daily_deduction=0
                else:
                    daily_deduction=fixed_daily_salary
            final_daily_salary=fixed_daily_salary-daily_deduction
            final_daily_sal_list.append(final_daily_salary)

        if month == '1' or month == '3' or month == '5' or month == '7' or month == '8' or month == '10' or month == '12':
            free_sal=(31-len(final_daily_sal_list))*fixed_daily_salary
        else:
            free_sal = (30-len(final_daily_sal_list))*fixed_daily_salary
        working_sal = sum(final_daily_sal_list)
        final_monthly_salary=int(working_sal+free_sal)
        deduction_due_to_leaves=int(ctc_objects.fixed_monthly_salary-final_monthly_salary)
        temp = {'deduction_due_to_leaves':deduction_due_to_leaves,'final_monthly_salary':final_monthly_salary,'ctc_objects':ctc_objects}
        return temp
    else:
        return None


def view_monthly_salary(request,id):

    year = request.GET['year']
    month = request.GET['month']
    temp=procedure(id,year,month)
    if temp==None:
        return HttpResponse("The user is not registered")
    else:
        return render(request,'work/view_final_salary.html',temp)


