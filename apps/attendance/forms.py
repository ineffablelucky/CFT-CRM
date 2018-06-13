from django import forms
from .models import Attendance, MyUser
from django.forms.widgets import SelectDateWidget, DateInput
from django.contrib.admin.widgets import AdminDateWidget


class LeaveForm(forms.ModelForm):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': True}))
    from_date = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date'}))
    reason = forms.CharField(max_length=500, widget=forms.Textarea)

    class Meta:
        model = Attendance
        fields = ('name', 'leave_type', 'from_date', 'end_date', 'reason')

    def __init__(self, *args, **kwargs):
        print(kwargs, args)
        self.logged_user = kwargs.pop('logged_user')
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.logged_user


