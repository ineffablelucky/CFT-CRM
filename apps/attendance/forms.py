from django import forms
from .models import Attendance, MyUser
from django.forms.widgets import SelectDateWidget, DateInput
from django.contrib.admin.widgets import AdminDateWidget
import datetime

from django.utils import timezone
class LeaveForm(forms.ModelForm):
    print("Entering LeaveForm model")
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': True}))
    date = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date'}))
    note = forms.CharField(max_length=500, widget=forms.Textarea)

    class Meta:
        model = Attendance
        fields = ('name', 'leave_type', 'date', 'end_date', 'note')

    def __init__(self, *args, **kwargs):
        # print(kwargs, args)
        self.logged_user = kwargs.pop('logged_user')
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.logged_user

    """"
    def clean_date(self):

        data = self.cleaned_data.get('date')
        return data
    
    def clean_from_date(self):
        print("Entering clean_form_data Leaveform")
        data = self.cleaned_data.get('from_date')
        #if data > datetime.datetime():
        return data
        #else:
         #   raise forms.ValidationError('year should be greater than 2000')
    
    def clean_end_date(self):
        print("Entering clean_end_data Leaveform")
        data = self.cleaned_data.get('end_date')
        print(data)
        #if data > datetime.datetime():
        return data
        #else:
        #    raise forms.ValidationError('year should be greater than 2000')
    """
    def clean_leave_type(self):
        data = self.cleaned_data.get('leave_type')
        return data

    def clean_note(self):
        data = self.cleaned_data.get('note')
        return data

    def save(self, commit=True):
        instance = super(LeaveForm, self).save(commit=False)
        instance.user_id = self.logged_user.id

        saved_instance = []
        if commit:
            data = []
            start_date = self.cleaned_data.get('date')
            end_date = self.cleaned_data.get('end_date')
            delta = datetime.timedelta(days=1)
            while start_date <= end_date:
                data.append(start_date)
                start_date += delta
            for date in data:
                if instance.id:
                    instance.id = None
                instance.date = date
                instance.save()
                saved_instance.append(self.instance)
        return saved_instance



