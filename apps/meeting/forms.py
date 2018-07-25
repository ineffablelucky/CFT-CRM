from django import forms
from apps.meeting.models import MEETING
from apps.users.models import MyUser
import datetime
from django.db.models import Q
from apps.opportunity.models import Opportunity as temp_model


class CreateMeeting(forms.ModelForm):
    Opportunity = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control col-md-7 col-xs-12'}),
        label='Opportunity ID'
    )

    date = forms.DateField(
        label='Meeting Date',
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control col-md-7 col-xs-12'}
        )
    )
    extras = forms.ModelMultipleChoiceField(
        label='Extra Personnel',
        queryset=MyUser.objects.filter(
            Q(department='Marketing')
        ),
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
        temp = temp_model.objects.get(id=self.oppo)
        temp = temp.assigned_to
        self.fields['extras'].queryset = MyUser.objects.filter(Q(department='Marketing') & ~Q(user_to__assigned_to=temp))
        # CreateMeeting.temp = self.oppo

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
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        required=False
    )

    class Meta:
        model = MEETING
        fields = (
            'description',
        )

    def __init__(self, *args, **kwargs):
        # print('printing init')
        # print(kwargs)
        initial = kwargs.get('initial', None)
        # print('Printing initial')
        # print(initial)
        self.logged_user = initial.pop('logged_user')
        #print(temp)
        kwargs.update(initial=initial)
        # print(kwargs.pop('logged_user'))
        # self.user = kwargs.pop('logged_user')
        # print(self.user)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        # print(instance)
        #
        # print(self.logged_user)

        prev = MEETING.objects.get(id=instance.id)
        # print('printing prev')
        # print(prev.description)
        prev.description += '<br>' + self.logged_user.username + ': ' + instance.description
        instance.description = prev.description
        if commit:
            instance.save()
        return instance



