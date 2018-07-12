from .models import Monthly_Salary
from .forms import SalaryGenerationForm,BasicSalaryForm
from django.utils import timezone
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse,redirect
from apps.users.models import MyUser

def edit_salary_list(request):

    context=Monthly_Salary.objects.filter(year=timezone.now().year)
    return render(request,'monthly_salary/edit_salary_list.html',{'context':context})

def edit_salary(request,id):
    if request.method=='POST':
        my_user = MyUser.objects.get(id=id)
        monthly_objects = Monthly_Salary.objects.get(staff__id=id,  year = timezone.now().year, month=timezone.now().month)
        form=BasicSalaryForm(request.POST, initial={'staff': my_user}, instance=monthly_objects)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('monthly_salary:edit_salary_list'))
        else:
            print(form.errors)

    monthly_objects = Monthly_Salary.objects.get(staff__id=id, year=timezone.now().year, month=timezone.now().month)
    data={'basic_monthly_salary':monthly_objects.basic_monthly_salary,'given_bonus':monthly_objects.given_bonus}
    form=BasicSalaryForm(initial=data)
    return render(request,'monthly_salary/edit_salary.html',{'form':form,'id':id})

def monthly_salary_list(request):
    context=Monthly_Salary.objects.all()
    form=SalaryGenerationForm()
    return render(request,'monthly_salary/monthly_salary_list.html',{'context':context,'form':form})


def monthly_salary(request, id):
    month = request.GET['month']
    year = request.GET['year']
    monthly_objects = Monthly_Salary.objects.get(staff_id=id,year=year,month=month)
    if monthly_objects.basic_monthly_salary == None or monthly_objects.basic_monthly_salary == 0:
        return HttpResponse("Monthly salary of user has not been added")
    else:
        monthly_objects.save()
        return render(request, 'monthly_salary/monthly_salary.html',{'monthly_objects':monthly_objects})

# def salary(request):
#     context=get_user_model().objects.all()


