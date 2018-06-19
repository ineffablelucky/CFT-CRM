from django.shortcuts import render,redirect
from . import models
from .models import Salary_calculations
from .forms import SalaryForm
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView,TemplateView

def table(request):
    var = Salary_calculations.objects.all()
    return render(request,'work/table.html',{'var':var})

def add(request):
    if request.method=="POST":
        form = SalaryForm(request.POST)
        form.save()
        return redirect('/salary_structure')
    else :
        form = SalaryForm()
        return render(request,'work/fill.html',{'form':form})