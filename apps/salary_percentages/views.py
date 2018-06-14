from django.shortcuts import render,redirect
from . import models
from .models import Salary_calculations
from .forms import SalaryForm

def table(request):
    var = Salary_calculations.objects.all()
    return render(request,'work/table.html',{'var':var})

def add(request):
    if request.method=="POST":
        form = SalaryForm(request.POST)
        form.save()
        return redirect('/salary')
    else :
        form = SalaryForm()
        return render(request,'work/fill.html',{'form':form})