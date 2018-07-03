from .forms import SalaryGenerationForm
from django.views.generic import FormView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.salary_percentages.models import Salary_calculations,CTC_breakdown
from django.shortcuts import redirect,render,HttpResponseRedirect,reverse
from apps.attendance.models import Attendance
from apps.leave.models import Leave
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

class Salary(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'ctc/get_salary.html'

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

# class Download_Salary(LoginRequiredMixin,ListView):
#
#     model = CTC_breakdown
#     context_object_name = 'context'
#
#     def get_queryset(self):
#         queryset = CTC_breakdown.objects.get(employee_id=self.request.user)
#         queryset.save()
#         return queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context=super().get_context_data()
#         if self.kwargs.get('id1')=='1' or '3' or '5' or '7' or '8' or '10' or '12':
#             fixed_daily_salary=float(context.fixed_monthly_salary/31)
#         else :
#             fixed_daily_salary=float(context.fixed_monthly_salary/30)
#        if i<(context.leave.pl+context.leave.cl):
#            deduction_due_to_leaves=0
#         context['attendance']=Attendance.objects.get(user=self.request.user)
#         context['leave']=Leave.objects.all(user=self.request.user)
#         i=0
#         while context.attendance.status=="Absent":
#             i=i+1

def Download_Salary(request, **kwargs):
    # Create the HttpResponse object with the appropriate PDF headers.
    print(kwargs)
    response = HttpResponse(content_type='application/pdf')
    filename=('my_salary/%d/%d',id1,id2)
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    ctc_objects = CTC_breakdown.objects.get(employee_id=request.user_id)
    leave_objects = Leave.objects.all(user=request.user)
    attendance_objects = Attendance.objects.get(user=request.user_id)
    if id1 == '1' or '3' or '5' or '7' or '8' or '10' or '12':
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 31)
    else:
        fixed_daily_salary = float(ctc_objects.fixed_monthly_salary / 30)

    #if attendance_objects.status == "Absent":
    #    if leave_objects.pl + leave_objects.cl < i:

    p = canvas.Canvas(buffer)
    p.drawString(ctc_objects)
    p.showpage()
    p.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
































