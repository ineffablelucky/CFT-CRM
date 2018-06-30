from django.shortcuts import render,HttpResponse
from django.views.generic import CreateView
from .models import Complaints
from apps.users.models import MyUser
from .forms import createcomplaintsform
from django.http import JsonResponse
from django.core import serializers
from ..users import views
import json

class createComplaints(CreateView):
    form_class = createcomplaintsform
    template_name = 'complaints/createcomplaints.html'



def complaints_ajax(request):
    if request.method =='GET':
        key = request.GET["name"]
        data = serializers.serialize("json", MyUser.objects.filter(department=key))
        context={'data':data}

        # print(type(data))
        # print(type(context))
        # print(context)
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # temp = dict(context['data'])
        # print(type(temp))
        return JsonResponse(data=context)





