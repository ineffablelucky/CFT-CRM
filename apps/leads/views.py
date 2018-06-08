from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import LEADS
from django.contrib.messages.views import SuccessMessageMixin


class LeadCreate(SuccessMessageMixin,CreateView):
    model = LEADS
    fields = '__all__'
    template_name = 'leads/create.html'
    success_message = "lead was created successfully"


	#success_url = reverse_lazy('clients:p')


class leadedit(UpdateView):
	model=LEADS
	template_name = 'leads/update.html'
	fields = '__all__'
	# success_url = reverse_lazy('clients:projectdetails')


	#def get_success_url(self, **kwargs):
		#return reverse_lazy('clients:projectdetails', args=(self.object.id,))


class leaddelete(DeleteView):
	model = LEADS
	success_url = reverse_lazy('clients:p')
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

