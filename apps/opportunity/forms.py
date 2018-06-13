from django import forms
from apps.opportunity.models import Opportunity


class ChangeStatus(forms.ModelForm):
    Opportunity_status = (
        ('Approved', 'Approved'),
        ('RQ_stage', 'Requirement Stage'),
        ('Negotiation', 'Negotiation Stage'),
        ('Pending', 'Pending')
    )

    status = forms.ChoiceField(choices=Opportunity_status,widget=forms.Select())

    class Meta:
        model = Opportunity
        fields = ('status',)