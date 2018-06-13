from django.http import request
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView,ListView,DetailView
from .models import LEADS
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateForm




# class LeadIndex(ListView):
# 	model=LEADS
#
# 	# def get_context_data(self, **kwargs):
# 	# 	context = super(LeadIndex,self).get_context_data(**kwargs)
# 	# 	context['LEADS_LIST'] =LEADS.objects.all().order_by('contact_person')
# 	template_name='leads/index.html'


class LeadDetails(ListView):
    model = LEADS
    template_name = 'leads/details.html'




class LeadCreate(CreateView):
    form_class = CreateForm
    template_name = 'leads/create.html'




    def form_valid(self, form):
        print('adfsadf')
        obj = form.save()
        return obj

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



