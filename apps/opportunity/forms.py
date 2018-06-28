from django import forms
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from django.db.models import Q
from apps.client.models import CLIENT


class ChangeStatus(forms.ModelForm):
    Opportunity_status = (
        ('Approved', 'Approved'),
        ('RQ_stage', 'Requirement Stage'),
        ('Negotiation', 'Negotiation Stage'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )

    status = forms.ChoiceField(choices=Opportunity_status, widget=forms.Select(), label='Change Status')

    class Meta:
        model = Opportunity
        fields = ('status',)


class AddProjManager(forms.ModelForm):
    proj_manager = forms.ModelChoiceField(
        label='Select Project Manager',
        queryset=MyUser.objects.filter(Q(department='IT') & Q(designation='Manager'))
    )

    class Meta:
        model = Opportunity
        fields = ('proj_manager',)


class CreateClientForm(forms.ModelForm):
    opportunity = forms.ModelChoiceField(queryset=Opportunity.objects.filter(status='Approved'))

    class Meta:
        model = CLIENT
        fields = (
            'company_name',
        )