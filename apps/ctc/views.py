from .forms import SalaryGenerationForm
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.salary_percentages.models import Salary_calculations,CTC_breakdown
from django.shortcuts import redirect,render,HttpResponseRedirect,reverse
from apps.attendance.models import Attendance
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from apps.salary_percentages.views import procedure
from apps.leave.models import Leave
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

class Salary(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'ctc/get_salary.html'

    # def get_initial(self):
    #     return {'month': self.kwargs['month'],'year': self.kwargs['year']}

class CTC(LoginRequiredMixin,ListView):
     model = CTC_breakdown
     template_name = 'ctc/ctc_breakdown.html'
     context_object_name = 'context'

     def get_queryset(self):
         queryset= CTC_breakdown.objects.get(employee_id = self.request.user)
         queryset.save()
         return queryset

     def get_context_data(self,**kwargs):
         context = super().get_context_data()
         year = timezone.now().year
         context['struct'] = Salary_calculations.objects.get(financial_year=year)
         return context

@login_required
def Download_Salary(request):
    year=request.GET['year']
    month=request.GET['month']
    response = HttpResponse(content_type='application/pdf')
    filename='Salary-%s-%s'%(year,month)
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    temp=procedure(request.user.id,year,month)
    salary_slip = ' User ID: ' + str((temp['ctc_objects']).employee.id) + ' Fixed Monthly Salary: ' + str((temp['ctc_objects']).fixed_monthly_salary)+" Deduction Amount: "+ str(temp['deduction_due_to_leaves'])+" Net monthly salary"+str(temp['final_monthly_salary'])+"HRA:"+str((temp['ctc_objects']).hra/12)
    p = canvas.Canvas(buffer)
    p.drawString(0,400,salary_slip)
    p.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
































