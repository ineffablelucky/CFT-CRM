from django import forms
from apps.opportunity.models import Opportunity
from apps.users.models import MyUser
from django.db.models import Q
from apps.client.models import CLIENT
from django.contrib.auth.forms import UserCreationForm

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


class CreateClientForm(UserCreationForm):
    opportunity = forms.ModelChoiceField(queryset=Opportunity.objects.filter(status='Approved'))

    email = forms.CharField(
        label='Email ',
        widget=forms.TextInput(),
    )

    company_name = forms.CharField(
        max_length=100, label='Company Name'
    )

    class Meta:
        model = MyUser
        fields = (
            'email',
        )

