from .forms import SalaryGenerationForm
from django.views.generic import FormView,ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.salary_percentages.models import Salary_Structure
from apps.monthly_salary.models import Monthly_Salary
from apps.ctc.models import CTC_breakdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

class Salary(LoginRequiredMixin,FormView):
    form_class = SalaryGenerationForm
    template_name = 'ctc/get_salary.html'

    def get_initial(self):
        initials = {
            "month":'1',
            "year": '2010'
        }
        return initials

class CTC(LoginRequiredMixin,ListView):
     model = CTC_breakdown
     template_name = 'ctc/ctc_breakdown.html'
     context_object_name = 'context'

     def get_queryset(self):
         queryset= CTC_breakdown.objects.get(staff_id = self.request.user,year=self.request.GET['year'])
         return queryset

     def get_context_data(self,**kwargs):
         context = super().get_context_data()
         print(self.request.GET)
         context['struct'] = Salary_Structure.objects.get(financial_year=self.request.GET['year'])
         return context


@login_required
def Download_Salary(request):
    if request.method=='POST':
        year = request.POST['year']
        month = request.POST['month']
    response = HttpResponse(content_type='application/pdf')
    filename='Salary-%s-%s'%(year,month)
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    monthly_data = Monthly_Salary.objects.get(staff_id=request.user.id,
                                                         year=year,
                                                         month=month)
    salary_slip = ' User ID: '+str(monthly_data.staff_id)+'Basic Monthly Salary'+str(monthly_data.basic_monthly_salary)+'Fixed Monthly Salary'+str(monthly_data.fixed_monthly_salary)
    #temp=procedure(request.user.id,year,month)
    #salary_slip = ' User ID: ' + str((temp['ctc_objects']).employee.id) + ' Fixed Monthly Salary: ' + str((temp['ctc_objects']).fixed_monthly_salary)+" Deduction Amount: "+ str(temp['deduction_due_to_leaves'])+" Net monthly salary"+str(temp['final_monthly_salary'])+"HRA:"+str((temp['ctc_objects']).hra/12)
    p = canvas.Canvas(buffer)
    p.drawString(0,400,salary_slip)
    p.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
































