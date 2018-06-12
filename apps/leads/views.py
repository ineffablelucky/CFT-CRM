from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView,ListView,DetailView
from .models import LEADS
from django.contrib.messages.views import SuccessMessageMixin

class LeadIndex(SuccessMessageMixin,ListView):
	model=LEADS

	def get_context_data(self, **kwargs):
		context = super(LeadIndex, self).get_context_data(**kwargs)
		context['LEADS_LIST'] =LEADS.objects.all().order_by('contact_person')
		return HttpResponseRedirect('leads/index.html',context)





class LeadCreate(SuccessMessageMixin,CreateView):
	model = LEADS
	fields = '__all__'
	template_name = 'leads/create.html'
	success_message = "lead was created successfully"


	#success_url = reverse_lazy('clients:p')


class LeadEdit(UpdateView):
	model=LEADS
	template_name = 'leads/update.html'
	fields = '__all__'
	# success_url = reverse_lazy('clients:projectdetails')


	#def get_success_url(self, **kwargs):
		#return reverse_lazy('clients:projectdetails', args=(self.object.id,))


class LeadDelete(DeleteView):
	model = LEADS
	success_url = reverse_lazy('clients:p')
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

