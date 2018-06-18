import logging

from django.contrib import messages
from django.http import request, HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView,ListView,DetailView,FormView
from .models import LEADS
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateForm,DetailForm




# class LeadIndex(ListView):
# 	model=LEADS
#
# 	# def get_context_data(self, **kwargs):
# 	# 	context = super(LeadIndex,self).get_context_data(**kwargs)
# 	# 	context['LEADS_LIST'] =LEADS.objects.all().order_by('contact_person')
# 	template_name='leads/employee_leads.html'


class LeadDetails(ListView,FormView):
    form_class = DetailForm

    model = LEADS
    fields='__all__'
    template_name = 'leads/details.html'




class LeadCreate(CreateView):
    model=LEADS
    form_class = CreateForm
    template_name = 'leads/create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    success_url = '/leads/details/'






class LeadEdit(UpdateView):

    model = LEADS
    fields = '__all__'
    template_name = 'leads/update.html'


    def get_success_url(self, **kwargs):
        return reverse_lazy('leads:LeadDetails')

	# success_url = reverse_lazy('clients:projectdetails')


	#def get_success_url(self, **kwargs):
		#return reverse_lazy('clients:projectdetails', args=(self.object.id,))


class LeadDelete(DeleteView):
    model = LEADS
    template_name = 'leads/delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('leads:LeadDetails')

	#success_url = reverse_lazy('LeadIndex')


def upload_csv(request):

    data = {}
    if "GET" == request.method:
        return render(request, "leads/upload_csv.html", data)
    # if not GET, then proceed

    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')

            return HttpResponseRedirect(reverse("leads:upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))


            return HttpResponseRedirect(reverse("leads:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display

        for line in lines:
            fields = line.split(",")

            data_dict = {}
            print(fields)
            data_dict["contact_number"] = fields[0]
            data_dict["company_name"] = fields[1]
            data_dict["contact_person"] = fields[2]
            data_dict["source"] = fields[3]
            data_dict["source_type"] = fields[4]
            data_dict["description"] = fields[5]

            data_dict["email"] = fields[6]
            data_dict["website"] = fields[7]
            data_dict["assigned_boolean"] = fields[8]
            print(data_dict)
            lead=LEADS(**data_dict)
            lead.save()






    except Exception as e:

        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        # messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("leads:upload_csv"))

from apps.opportunity.models import Opportunity
def LeadsAssign(request):


    data = (request.POST['ids']).split(',')
    
    if len(data) > 0:
        for item in data:
            tmp = Opportunity()
            tmp.lead_id = int(item)
            tmp.assigned_to_id = request.POST.get('assign')
            tmp.save()
    return HttpResponse("this is devesh")

