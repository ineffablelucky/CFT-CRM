from django.shortcuts import render,redirect
from . import models
from .models import Salary_calculations
from .forms import SalaryForm
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView,TemplateView

def salary_structure(request):
    context = Salary_calculations.objects.all()
    return render(request,'work/salary_struct_table.html',{'context':context})

def add(request):
    if request.method=="POST":
        form = SalaryForm(request.POST)
        form.save()
        return redirect('/salary_structure')
    else :
        form = SalaryForm()
        return render(request,'work/salary_struct_form.html',{'form':form})