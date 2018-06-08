from django.db import models


class USER(models.Model):
    CHOICES = (
        ('F', 'Female')
    )
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)
    created_on = models.DateField(auto_now_add=True, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)