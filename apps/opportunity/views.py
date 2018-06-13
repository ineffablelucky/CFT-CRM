from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin


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


class ChangeStatus(LoginRequiredMixin, UpdateView):
    pass
