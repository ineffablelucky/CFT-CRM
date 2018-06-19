from django.shortcuts import render
from .models import CTC_breakdown,Dropdown
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone

def index(request):
    xyz= Dropdown.objects.all()
    return render(request,'get_salary.html',{'xyz':xyz})


def slip(request,id):
    details=CTC_breakdown.objects.get(employee_id=id)
    year = timezone.now().year
    d=Salary_calculations.objects.filter(financial_year=year)
    return render(request,'gross_sal.html',{'details':details},{'d':d})
