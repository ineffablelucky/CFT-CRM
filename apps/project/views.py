from django.shortcuts import render

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "project_manager_view"

