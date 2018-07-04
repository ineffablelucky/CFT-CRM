import logging

from django.contrib import messages
from django.http import request, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView,ListView,DetailView,FormView
from .models import LEADS
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateForm,DetailForm,UpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.opportunity.models import Opportunity
from django.contrib.auth.decorators import permission_required, login_required
import json
from django.http import JsonResponse



# class LeadIndex(ListView):
# 	model=LEADS
#
# 	# def get_context_data(self, **kwargs):
# 	# 	context = super(LeadIndex,self).get_context_data(**kwargs)
# 	# 	context['LEADS_LIST'] =LEADS.objects.all().order_by('contact_person')
# 	template_name='leads/employee_leads.html'


class LeadDetails(LoginRequiredMixin, PermissionRequiredMixin, ListView,FormView):
    form_class = DetailForm
    permission_required = (
        'leads.view_leads',
        #'users.view_users',
    )
    model = LEADS
    fields='__all__'
    template_name = 'leads/details.html'
    def get_queryset(self):
        queryset=LEADS.objects.filter(assigned_boolean=False)
        return queryset


class LeadCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('leads.add_leads',)

    model=LEADS
    form_class = CreateForm
    template_name = 'leads/create.html'

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    success_url = '/leads/details/'








class LeadEdit(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('leads.change_leads',)

    form_class =UpdateForm

    template_name = 'leads/update.html'

    model = LEADS
    print("this is not good")
    def get_success_url(self, **kwargs):
        print(kwargs)
        return reverse_lazy('leads:LeadDetails')


def check(request,id):
    instance = get_object_or_404(LEADS, id=id)
    print("instance is:")
    print(instance)
    form = UpdateForm(request.POST, instance=instance)
    
    if request.method=='POST':

        if form.is_valid():
            form.save()

            return JsonResponse(data={'true':'true'})
        else:


            return JsonResponse(data={'error': form.errors})
    return JsonResponse({"details incorrect":"details incorrect"})

	# success_url = reverse_lazy('clients:projectdetails')


	#def get_success_url(self, **kwargs):
		#return reverse_lazy('clients:projectdetails', args=(self.object.id,))


class LeadDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = LEADS
    template_name = 'leads/delete.html'
    permission_required = ('leads.delete_leads',)
    def get_success_url(self, **kwargs):
        return reverse_lazy('leads:LeadDetails')

	#success_url = reverse_lazy('LeadIndex')

@login_required
@permission_required('leads.view_leads', raise_exception=True)
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
        print(len(lines))
        for l in range(1,len(lines)):
            fields = lines[l].split(",")

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
            return HttpResponseRedirect(reverse("leads:LeadDetails"))






    except Exception as e:

        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        # messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("leads:upload_csv"))

@login_required
@permission_required('leads.view_leads', raise_exception=True)
def LeadsAssign(request):
    data = (request.POST['ids']).split(',')
    print(data)
    if len(data) > 0:
        for item in data:
            tmp = Opportunity()
            tmp.lead_id = int(item)
            tmp.assigned_to_id = request.POST.get('assign')
            tmp.save()
            abc=LEADS.objects.get(id=int(item))
            abc.assigned_boolean=True
            abc.save()
    return HttpResponseRedirect(reverse_lazy("leads:LeadDetails"))

