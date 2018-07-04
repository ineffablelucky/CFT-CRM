import logging
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from .models import Salary_calculations,CTC_breakdown
from .forms import SalaryForm,CtcForm,SalaryGenerationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.leave.models import Leave
from apps.attendance.models import Attendance

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
    return HttpResponseRedirect(reverse("salary_percentages:upload_csv"))

def monthly_salary(request):
    context=CTC_breakdown.objects.all()
    form=SalaryGenerationForm()
    return render(request,'work/monthly_salary.html',{'context':context,'form':form})

def view_monthly_salary(request,id):
    year = int(request.GET['year'])
    month = int(request.GET['month'])
    ctc_objects = CTC_breakdown.objects.get(employee_id=id)
    leave_objects = Leave.objects.get(user_id=id)
    attendance_objects = Attendance.objects.filter(user_id=id)

    deduction_due_to_leaves = 0
    allowed_leaves = leave_objects.pl + leave_objects.cl
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 31)
    else:
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 30)
    list_of_absent_dates = []
    for a in attendance_objects:
        if a.status == 'absent':
            list_of_absent_dates.append(a.date)
            absent_days = len(list_of_absent_dates)
            if absent_days < allowed_leaves:
                deduction_due_to_leaves = 0
            else:
                deduction_due_to_leaves = (absent_days - allowed_leaves) * fixed_daily_salary
        elif a.status == 'On Leave':
            deduction_due_to_leaves = deduction_due_to_leaves + 0
        #elif a.status=='present':
    print(allowed_leaves)
    print(deduction_due_to_leaves)
    final_salary = ctc_objects.fixed_monthly_salary - deduction_due_to_leaves
    return render(request,'view_final_salary.html',{'ctc_objects':ctc_objects,'deduction_due_to_leaves':deduction_due_to_leaves,'final_salary':final_salary})


