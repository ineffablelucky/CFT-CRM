from django import forms
from apps.meeting.models import MEETING
from apps.users.models import MyUser


class CreateMeeting(forms.ModelForm):
    Opportunity = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True}), label='Opportunity ID'
    )

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

    class Meta:
        model = MEETING
        fields = (
            'date',
            'extras',
        )

    def __init__(self, *args, **kwargs):
        self.oppo = kwargs.pop('oppo_id')
        super().__init__(*args, **kwargs)
        self.fields['Opportunity'].initial = self.oppo

    def save(self, commit=True):
        instance = super().save(commit=False)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(instance)
        instance.Opportunity_id = self.oppo
        if commit:
            instance.save()
        instance.extras.set(self.cleaned_data['extras'])
        return instance


class AddMeetingNotes(forms.ModelForm):

    description = forms.CharField(
        max_length=1000,
        label='Add Notes',
        widget=forms.TextInput
    )

    class Meta:
        model = MEETING
        fields = (
            'description',
        )
