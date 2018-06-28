from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from apps.opportunity.models import Opportunity
from apps.meeting.models import MEETING
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.opportunity.forms import ChangeStatus, AddProjManager, CreateClientForm
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from apps.client.models import CLIENT

class ListOppo(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('opportunity.view_opportunity',)
    model = Opportunity
    template_name = 'opportunity/employee_leads.html'
    context_object_name = 'opportunity'
    #print("Hello!!")

    def get_queryset(self):
        user_id = MyUser.objects.get(username=self.request.user)
        #print(user_id)
        queryset2 = MEETING.objects.filter(extras__in=[self.request.user])
        queryset = Opportunity.objects.filter(Q(assigned_to=self.request.user) | Q(meeting__in=queryset2)).distinct()
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = AddProjManager()
    #     return context


class C_Status(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = (
        'opportunity.change_opportunity',
        'users.view_opportunity',
    )
    model = Opportunity
    template_name = 'opportunity/change_status.html'
    form_class = ChangeStatus
    success_url = reverse_lazy('opportunity:list_oppo')


class A_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        'users.view_opportunity',
        'users.view_meeting',
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


class A_PManager(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        'users.view_meeting',
        'users.view_opportunity',
    )
    model = Opportunity
    form_class = AddProjManager
    #template_name = 'opportunity/assigned_leads.html'
    success_url = reverse_lazy('opportunity:assign_lead')


class C_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        'users.view_meeting',
        'users.view_opportunity',
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


class D_Leads(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'opportunity.change_opportunity',
        'opportunity.add_opportunity',
        'opportunity.delete_opportunity',
        'users.view_meeting',
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
    model = CLIENT
