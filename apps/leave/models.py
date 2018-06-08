from django.db import models
#from Crmproject.project.apps.users import User


class Leave(models.Model):

    LEAVE_TYPE_CHOICES = (
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('Half Day', 'Half Day'),
    )

    leave_type = models.CharField(
        max_length= 8,
        choices=LEAVE_TYPE_CHOICES,
        default='PL',
    )



    #user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
