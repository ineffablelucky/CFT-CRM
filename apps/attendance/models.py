from django.db import models
from ..users.models import MyUser
from datetime import date


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('On Leave', 'On Leave')
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
        max_length=10,
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

    class Meta:
        permissions = (
            ('view_attendance', 'Can view attendance'),
        )


class LeaveRequest(models.Model):

    LEAVE_TYPE_CHOICES = (
        ('PL', 'Privilege leave'),
        ('CL', 'Casual leave'),
        ('Half Day', 'Half Day'),
    )
    leave_type = models.CharField(
        max_length=8,
        choices=LEAVE_TYPE_CHOICES,
        null=True,
    )
    date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default='Pending',
    )
    note = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, default=None)

    class Meta:
        permissions = (
            ('view_leaverequest', 'Can view Leave Request'),
        )


