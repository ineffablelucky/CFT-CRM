from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from apps.opportunity.models import Opportunity
from apps.meeting.models import MEETING
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.opportunity.forms import ChangeStatus, AddProjManager, CreateClientForm, AddExistingClientOpportunity
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from apps.client.models import CLIENT
import re
from django.core.mail import  send_mail


def sendEmail(subject, message, sender, to):
    send_mail(
        subject,
        message,
        sender,
        [to],
        fail_silently=True
    )


class ListOppo(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('opportunity.view_opportunity',)
    model = Opportunity
    template_name = 'opportunity/employee_leads.html'
    context_object_name = 'opportunity'
    #print("Hello!!")

    def get_queryset(self):
        user_id = MyUser.objects.get(username=self.request.user)
        queryset2 = MEETING.objects.filter(extras__in=[self.request.user])
        queryset = Opportunity.objects.filter(Q(assigned_to=self.request.user) | Q(meeting__in=queryset2)).distinct()
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = AddProjManager()
    #     return context

# change status


class C_Status(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.view_opportunity',
    )
    model = Opportunity
    template_name = 'opportunity/change_status.html'
    form_class = ChangeStatus
    success_url = reverse_lazy('opportunity:list_oppo')

# assigned leads


class A_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        #'users.view_users',
        'opportunity.view_opportunity',
        'meeting.view_meeting',
    )
    model = Opportunity
    template_name = 'opportunity/assigned_leads.html'
    context_object_name = 'assigned_leads'

    def get_queryset(self):
        queryset = Opportunity.objects.filter(~Q(status='Approved'))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddProjManager()
        return context

# assign project manager


class A_PManager(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        #'users.view_users',
        'opportunity.view_opportunity',
    )
    model = Opportunity
    form_class = AddProjManager
    # template_name = 'opportunity/assigned_leads.html'
    success_url = reverse_lazy('opportunity:assign_lead')

# closed leads


class C_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        #'users.view_users',
        'opportunity.view_opportunity',
    )
    model = Opportunity
    template_name = 'opportunity/closed_leads.html'
    context_object_name = 'closed_leads'

    def get_queryset(self):
        queryset = Opportunity.objects.filter(status='Approved')
        return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['oppo_id'] =

# declined leads


class D_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        #'users.view_users',
        'opportunity.view_opportunity',
    )
    model = Opportunity
    template_name = 'opportunity/declined_leads.html'
    context_object_name = 'declined_leads'

    def get_queryset(self):
        queryset = Opportunity.objects.filter(status='Rejected')
        return queryset


class CreateClientView(LoginRequiredMixin, CreateView):
    form_class = CreateClientForm
    template_name = 'opportunity/create_client.html'
    success_url = reverse_lazy('opportunity:client_list')
    # print('Hello world')

    def form_valid(self, form):
        temp = super().form_valid(form)
        email = form.cleaned_data.get('email')
        sender = 'rajeshjha2097@gmail.com'
        subject = 'This is registration confirmation email'
        username = '_'.join(re.findall(r'\S+', form.cleaned_data.get('company_name')))
        key = username + '1234'
        message = "Your Login credentials are : username - " + username + " and password is - " + key + "."
        sendEmail(subject, message, sender, email)
        print(key)
        return temp


class UpdateClientOpportunityView(LoginRequiredMixin, CreateView):
    form_class = AddExistingClientOpportunity
    success_url = reverse_lazy('opportunity:client_list')
    template_name = 'opportunity/add_opportunity_existing_client.html'


class ListClient(LoginRequiredMixin, ListView):
    model = CLIENT
    context_object_name = 'clients'
    template_name = 'opportunity/client_list.html'

    def get_queryset(self):
        queryset = CLIENT.objects.all()
        print(queryset)
        return queryset


class ListClientOpportunity(LoginRequiredMixin, ListView):
    model = Opportunity
    context_object_name = 'client_opportunity'
    template_name = 'opportunity/client_opportunity_details.html'

    def get_queryset(self):
        print(self.kwargs)
        queryset = Opportunity.objects.filter(client__id=self.kwargs.get('pk'))
        print(queryset)
        return queryset
