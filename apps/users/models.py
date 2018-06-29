from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):

    designation_choices = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Client', 'Client'),
        ('Admin', 'Admin'),
        ('NA', 'NA'),
    )

    department_choices = (
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
        ('Accounts', 'Accounts'),
        ('IT', 'IT'),
        ('NA', 'NA'),
    )

    gender_choice = (
        ('M', 'M'),
        ('F', 'F'),
        ('Other', 'Other'),
    )
    username            = models.CharField(unique=True, blank=False, max_length=50, default=None)
    email               = models.EmailField(unique=False, blank=False, default=None)
    first_name          = models.CharField(blank=False, max_length=35, default=None)
    middle_name         = models.CharField(blank=True, max_length=35, null=True)
    last_name           = models.CharField(blank=True, max_length=35, null=True)
    age                 = models.IntegerField(null=True, blank=True, default=None)
    contact             = models.BigIntegerField(null=True, blank=True, default=None)
    salary              = models.IntegerField(null=True, blank=True, default=None)
    created_on          = models.DateTimeField(auto_now_add=True)
    date_of_joining     = models.DateField(blank=True, null=True)
    department          = models.CharField(default='NA', choices=department_choices, max_length=35)
    designation         = models.CharField(default='NA', choices=designation_choices, max_length=35)
    gender              = models.CharField(default='M', choices=gender_choice, max_length=10)

    class Meta:
        permissions = (
            ('view_users', 'Can view users'),
        )

class user_token(models.Model):
    token = models.CharField(default=None, blank=True, max_length=255)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, blank=True, null=True)




