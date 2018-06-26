from django import forms
from apps.meeting.models import MEETING
from apps.users.models import MyUser
import datetime


class CreateMeeting(forms.ModelForm):
    Opportunity = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True}), label='Opportunity ID'
    )

    date = forms.DateField(
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

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("Please select a future date or current date")
        return self.cleaned_data.get('date')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.Opportunity_id = self.oppo
        if commit:
            instance.save()
        instance.extras.set(self.cleaned_data['extras'])
        return instance


class AddMeetingNotes(forms.ModelForm):

    description = forms.CharField(
        max_length=1000,
        label='Add Notes',
        widget=forms.TextInput,
        required=False
    )

    class Meta:
        model = MEETING
        fields = (
            'description',
        )

    def save(self, commit=True, user1=''):
        self.user1 = str(user1)
        instance = super().save(commit=False)
        print(instance.description)

        # print(self.editing_user)


        # prev.description += '\n' + self.user1 + ': ' + instance.description
        #
        # instance.description = prev.description
        commit = False
        if commit:
            instance.save()
        return instance



