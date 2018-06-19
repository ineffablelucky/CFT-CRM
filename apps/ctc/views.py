from django.shortcuts import render
from .models import CTC_breakdown


def slip(request,id):
    c=CTC_breakdown.objects.get(id=id)
    return render(request,'gross_sal.html',{'c':c})
