from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from apps.users.models import MyUser
from apps.client.models import CLIENT
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from apps.client.forms import AddClientForm


class AddClientView(CreateView):
    form_class = AddClientForm
    model = CLIENT
    template_name = 'client/add_client.html'
    print('Hello World')
