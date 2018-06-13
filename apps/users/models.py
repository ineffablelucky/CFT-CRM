from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

    designation_choices = (
        ('emp', 'Employee'),
        ('manager', 'Manager'),
        ('client', 'Client'),
        ('admin', 'Admin'),
    )

    department_choices = (
        ('hr', 'HR'),
        ('marketing', 'Marketing'),
        ('accounts', 'Accounts'),
        ('it', 'IT'),
    )

    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('other', 'Other'),
    )
    username            = models.CharField(unique=True, blank=False, max_length=50, default=None)
    email               = models.EmailField(unique=False, blank=False, default=None)
    first_name          = models.CharField(blank=False, max_length=35, default=None)
    middle_name         = models.CharField(blank=True, max_length=35, default=None)
    last_name           = models.CharField(blank=True, max_length=35, default=None)
    age                 = models.IntegerField(null=True, blank=True, default=None)
    contact             = models.BigIntegerField(null=True, blank=True, default=None)
    salary              = models.IntegerField(null=True, blank=True, default=None)
    created_on          = models.DateTimeField(auto_now_add=True)
    date_of_joining     = models.DateField(blank=True, null=True)
    department          = models.CharField(default=None, choices=department_choices, max_length=35)
    designation         = models.CharField(default=None, choices=designation_choices, max_length=35)
    gender              = models.CharField(default='M', choices=gender_choice, max_length=10, null=True, blank=True)


