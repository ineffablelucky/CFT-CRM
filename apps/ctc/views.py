from .forms import SalaryGenerationForm
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.salary_percentages.models import Salary_calculations,CTC_breakdown
from django.shortcuts import redirect,render,HttpResponseRedirect,reverse
from apps.attendance.models import Attendance
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
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
    year=int(request.GET['year'])
    month=int(request.GET['month'])
    response = HttpResponse(content_type='application/pdf')
    filename='Salary'+'-%d'%year+'-%d'%month
    print(filename)
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    ctc_objects=CTC_breakdown.objects.get(employee_id=request.user.id)
    leave_objects = Leave.objects.get(user_id=request.user.id)
    attendance_objects = Attendance.objects.filter(user_id=request.user.id)

    deduction_due_to_leaves=0
    allowed_leaves = leave_objects.pl + leave_objects.cl
    if month == 1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 31)
    else:
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 30)
    list_of_absent_dates=[]
    for a in attendance_objects:
        if a.status=='absent':
            list_of_absent_dates.append(a.date)
            absent_days = len(list_of_absent_dates)
            if absent_days < allowed_leaves:
                deduction_due_to_leaves = 0
            else:
                deduction_due_to_leaves = (absent_days - allowed_leaves) * fixed_daily_salary
        elif a.status=='On Leave':
            deduction_due_to_leaves=deduction_due_to_leaves+0
        #elif a.status
    print(allowed_leaves)
    print(deduction_due_to_leaves)
    final_salary=ctc_objects.fixed_monthly_salary-deduction_due_to_leaves
    salary_slip = ' User ID: ' + str(ctc_objects.employee.id) + ' Fixed Monthly Salary: ' + str(ctc_objects.fixed_monthly_salary)+" Deduction Amount: "+ str(deduction_due_to_leaves)+" Net monthly salary"+str(final_salary)+"HRA:"+str(ctc_objects.hra/12)
    p = canvas.Canvas(buffer)
    p.drawString(0,400,salary_slip)
    p.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
































