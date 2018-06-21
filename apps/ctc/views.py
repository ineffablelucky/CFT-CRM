from django.shortcuts import render
from .models import CTC_breakdown
from .forms import SalaryGenerationForm
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class Download_salary(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'ctc/get_salary.html'


class CTC(LoginRequiredMixin,ListView):
    model = CTC_breakdown
    template_name = 'ctc/gross_sal.html'

    #def query_data(self):



