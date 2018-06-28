from django import forms
from apps.client.models import CLIENT
from apps.users.models import MyUser
from django.db.models import Q


class AddClientForm(forms.ModelForm):

    class Meta:
        model = CLIENT
        fields = (
            'company_name',
        )