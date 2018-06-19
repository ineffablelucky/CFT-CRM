from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import CreateleaveForm


class LeaveCreation(CreateView):
    form_class = CreateleaveForm
    template_name = 'assignleave.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return redirect('/')


