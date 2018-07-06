from django import forms
from .models import Attendance, MyUser, LeaveRequest
from ..leave.models import Leave
import datetime
from django.db.models import Q
from django.utils.timezone import utc
from pytz import timezone


class LeaveForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'readonly': True, 'class': ''}),
        label='Name'
    )

    date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': ''}),
        label='Start Date'
    )

    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': ''}),
        label='End Date'
    )

    note = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'class': ''})
    )

    LEAVE_TYPE_CHOICES = (
        ('PL', 'Privilege leave'),
        ('CL', 'Casual leave'),
        ('Half Day', 'Half Day')
    )

    leave_type = forms.ChoiceField(
        choices=LEAVE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': ''}),
        label='Type of Leave'

    )

    class Meta:
        model = LeaveRequest
        fields = ('name', 'leave_type', 'date', 'end_date', 'note')

    def __init__(self, *args, **kwargs):
        # print(kwargs, args)
        self.logged_user = kwargs.pop('logged_user')
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.logged_user

    """
    
    
    def clean_from_date(self):
        print("Entering clean_form_data Leaveform")
        data = self.cleaned_data.get('from_date')
        #if data > datetime.datetime():
        return data
        #else:
         #   raise forms.ValidationError('year should be greater than 2000')
    """
    """
    def clean_date(self):
        data = self.cleaned_data.get('date')

        if data <= datetime.date.today():
            raise forms.ValidationError('Start Date should be greater than Today\'s date')
        return data
    """
    def clean_end_date(self):
        leave = Leave.objects.get(user_id=self.logged_user.id)
        data3 = self.cleaned_data.get('leave_type')
        data = self.cleaned_data.get('end_date')
        data1 = self.cleaned_data.get('date')

        if LeaveRequest.objects.filter(Q(user_id=self.logged_user.id) & Q(date=data1) & Q(end_date=data)):
            raise forms.ValidationError("Already applied for the leaves on the dates mentioned")

        elif data >= data1:
            if data3 == "PL":
                sdate = data1
                edate = data
                count = 0
                d = datetime.timedelta(days=1)
                while sdate <= edate:
                    if sdate.weekday() == 5:
                        count = count+1
                    elif sdate.weekday() == 6:
                        count = count+1
                    sdate = sdate+d
                delta = datetime.timedelta(days=leave.pl+count)
                if data - data1 <= delta:
                    return data
                else:
                    raise forms.ValidationError("No sufficient PL left")
            elif data3 == "CL":
                sdate = data1
                edate = data
                count = 0
                d = datetime.timedelta(days=1)
                while sdate <= edate:
                    if sdate.weekday() == 5:
                        count = count + 1
                    elif sdate.weekday() == 6:
                        count = count+1
                    sdate = sdate + d
                delta = datetime.timedelta(days=leave.cl+count)
                if data - data1 <= delta:
                    return data
                else:
                    raise forms.ValidationError("No sufficient CL left")
            elif data3 == "Half Day":
                    return data

        else:
            raise forms.ValidationError('End Date should be greater than Start Date')

    def clean_leave_type(self):
        data = self.cleaned_data.get('leave_type')
        return data

    def clean_note(self):
        data = self.cleaned_data.get('note')
        return data

    def save(self, commit=True):
        instance = super(LeaveForm, self).save(commit=False)
        instance.user_id = self.logged_user.id
        if commit:
            data = []
            start_date = self.cleaned_data.get('date')
            end_date = self.cleaned_data.get('end_date')
            if LeaveRequest.objects.filter(Q(user_id=self.logged_user.id) & Q(date__gte=start_date)
                                           & Q(end_date__lte=end_date) & Q(status='Pending')) is not None:
                leave = LeaveRequest.objects.filter(Q(user_id=self.logged_user.id) & Q(date__gte=start_date)
                                                    & Q(end_date__lte=end_date) & Q(status='Pending'))
                for l in leave:
                    l.delete()
            instance.date = start_date
            instance.end_date = end_date
            instance.save()
            """
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
            """
        return instance


class AttendanceForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control has-feedback-left'}),
        label='Select Date'
    )
    to_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control has-feedback-left'}),
        label='To Date'
    )

    class Meta:
        model = Attendance
        fields = ('date',)
    """
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        if datetime.date.today().weekday() == 0:
            self.fields['date'].initial = datetime.date.today()-datetime.timedelta(days=3)
        else:
            self.fields['date'].initial = datetime.date.today() - datetime.timedelta(days=1)
    """


"""
class ClockinForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': True}), label='Name')

    class Meta:
        model = Attendance
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        # print(kwargs, args)
        self.logged_user = kwargs.pop('logged_user', None)
        super(ClockinForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = self.logged_user

    def save(self, commit=True):
        instance = super(ClockinForm, self).save(commit=False)
        instance.user_id = self.logged_user.id
        instance.date = datetime.date.today()
        instance.time_in = datetime.datetime.now()
        print(instance.time_in)
        instance.status = 'present'
        instance.save()
        return instance


class ClockoutForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ()

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        super(ClockoutForm, self.__init__(*args, **kwargs))

    def save(self, commit=True):
        a = Attendance.objects.get(user_id = self.logged_user.id, date=datetime.date.today())
        a.time_out = datetime.datetime.now()
        instance = super(ClockoutForm, self).save(commit=False)
        instance = a
        instance.time_out = datetime.datetime.now()
        instance.save()
        return instance
"""


class GraphForm(forms.ModelForm):
    year=[]
    for i in range(1990,2050):
        a = (str(i),str(i))
        year.append(a)

    Year_Choice=tuple(year)
    year2= forms.ChoiceField(
        choices=Year_Choice,
        widget=forms.Select(attrs={'class': ''}),
        label='Select Year'

    )

    class Meta:
        model=Attendance
        fields=('year2',)

