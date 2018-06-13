from django import forms
from apps.opportunity.models import Opportunity


class ChangeStatus(forms.ModelForm):
    status = 
    class Meta:
        model = Opportunity
        fields = ('status',)