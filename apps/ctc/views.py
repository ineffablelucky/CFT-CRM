from django.shortcuts import render
from .models import CTC_breakdown
from .forms import SalaryGenerationForm
from apps.salary_percentages.models import Salary_calculations
from django.utils import timezone
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class Index(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'get_salary.html'


class CTC(LoginRequiredMixin,ListView):
    model = CTC_breakdown
    template_name = 'gross_sal.html'

    def get_queryset(self):
        details=CTC_breakdown.objects.get(employee_id= self.request.user)
        year = timezone.now().year
        d=Salary_calculations.objects.get(financial_year=year)
        return details