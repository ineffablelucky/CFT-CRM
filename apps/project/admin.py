from django.contrib import admin
from .models import IT_Project
# Register your models here.

admin.site.register(IT_Project)

class IT_Project(admin.ModelAdmin):
    list_display    = ('get_employees')