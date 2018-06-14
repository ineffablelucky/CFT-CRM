from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.opportunity.forms import ChangeStatus
from django.urls import reverse, reverse_lazy

class ListOppo(LoginRequiredMixin, ListView):
    model = Opportunity
    template_name = 'opportunity/index.html'
    context_object_name = 'opportunity'
    print("Hello!!")

    def get_queryset(self):
        user_id = MyUser.objects.get(username=self.request.user)
        print(user_id)
        queryset = Opportunity.objects.filter(assigned_to=self.request.user)
        print(queryset)
        return queryset


class C_Status(LoginRequiredMixin, UpdateView):
    model = Opportunity
    template_name = 'opportunity/change_status.html'
    form_class = ChangeStatus
    success_url = reverse_lazy('list_oppo')

