from .models import CTC_breakdown
from .forms import SalaryGenerationForm
from apps.salary_percentages.models import Salary_calculations
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

class Download_salary(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'ctc/get_salary.html'


class CTC(LoginRequiredMixin,ListView):
    model = CTC_breakdown
    template_name = 'ctc/ctc_breakdown.html'
    context_object_name = 'context'

    def get_queryset(self):
        print(self.request.user.id)
        queryset = CTC_breakdown.objects.get(employee_id = self.request.user)
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        year = timezone.now().year
        context['struct'] = Salary_calculations.objects.get(financial_year=year)
        return context

