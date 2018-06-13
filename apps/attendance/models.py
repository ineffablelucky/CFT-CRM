from django.db import models
from ..users.models import MyUser
from datetime import date


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent')
    )
    LEAVE_TYPE_CHOICES = (
        ('PL', 'Privilege leave'),
        ('CL', 'Casual leave'),
        ('Half Day', 'Half Day'),
    )

    date = models.DateField(null=True)
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=7,
        choices = STATUS_CHOICES,
        default = 'Absent',
    )

    leave_type = models.CharField(
        max_length=8,
        choices=LEAVE_TYPE_CHOICES,
        null=True,
    )
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, default=None)

    note = models.CharField(max_length=500, null=True)

