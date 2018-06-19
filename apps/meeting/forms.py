from django import forms
from apps.meeting.models import MEETING
from apps.users.models import MyUser


class CreateMeeting(forms.ModelForm):
    date = forms.CharField(
        label='Meeting Date',
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    extras = forms.ModelMultipleChoiceField(
        label='Extra Personnel',
        queryset=MyUser.objects.filter(department='Marketing'),
    )
    #Opportunity = forms.
    class Meta:
        model = MEETING
        fields = (
            'date',
            'extras',
            'Opportunity',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['Opportunity'].initial =