from django.db import models
from ..users.models import MyUser


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

    date = models.DateField()
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    status = models.CharField(
        max_length=7,
        choices = STATUS_CHOICES,
        default = 'Absent',
    )

    leave_type = models.CharField(
        max_length=8,
        choices=LEAVE_TYPE_CHOICES,
        default='CL',
    )
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, default=None)

    note = models.CharField(max_length=500)

