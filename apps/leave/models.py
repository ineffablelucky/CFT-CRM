from django.db import models

class Leave:
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
