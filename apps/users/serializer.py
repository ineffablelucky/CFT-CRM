from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import Group


class MyUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=MyUser.objects.all())])
    password=serializers.CharField()

    class Meta:
        model = MyUser
        fields = (
            'email',

            'first_name',
            'middle_name',
            'password',
            'last_name',
            'contact',
            'department',
            'designation',
            'gender',
        )

    def create(self,validated_data):
        print('*******************')

        print(validated_data)
        myuser=MyUser(**validated_data)
        myuser.username=myuser.email.split('@')[0]
        myuser.save()
        print(myuser.department)
        print(myuser.designation)

        if myuser.designation == 'Admin':
            group_user = Group.objects.get_by_natural_key('Admin Group')
            group_user.user_set.add(myuser)

        elif myuser.designation == 'Manager' and myuser.department == 'Marketing':
            group_user = Group.objects.get_by_natural_key('Marketing Manager Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Employee Group')
            group_user.user_set.add(myuser)

        elif myuser.designation == 'Manager' and myuser.department == 'HR':
            group_user = Group.objects.get_by_natural_key('HR Manager Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('HR Employee Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Employee Group')
            group_user.user_set.add(myuser)

        elif myuser.designation == 'Manager' and myuser.department == 'IT':
            group_user = Group.objects.get_by_natural_key('IT Manager Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('IT Employee Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Employee Group')
            group_user.user_set.add(myuser)

        elif myuser.department == 'Accounts' and myuser.designation == 'Manager':
            group_user = Group.objects.get_by_natural_key('Account Manager Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Account Employee Group')
            group_user.user_set.add(myuser)
            group_user = Group.objects.get_by_natural_key('Employee Group')
            group_user.user_set.add(myuser)

        elif myuser.designation == 'Employee':
            group_user = Group.objects.get_by_natural_key('Employee Group')
            group_user.user_set.add(myuser)
            if myuser.department == 'HR':
                group_user = Group.objects.get_by_natural_key('HR Employee Group')
                group_user.user_set.add(myuser)
            elif myuser.department == 'IT':
                group_user = Group.objects.get_by_natural_key('IT Employee Group')
                group_user.user_set.add(myuser)
            elif myuser.department == 'Marketing':
                group_user = Group.objects.get_by_natural_key('Marketing Employee Group')
                group_user.user_set.add(myuser)
            elif myuser.department == 'Accounts':
                group_user = Group.objects.get_by_natural_key('Account Employee Group')
                group_user.user_set.add(myuser)

        elif myuser.designation == 'Client':
            group_user = Group.objects.get_by_natural_key('Client Group')
            group_user.user_set.add(myuser)
        elif myuser.designation == myuser.department:
            raise serializers.ValidationError("designation and department both can not be NA")
        elif myuser.designation == 'Client' and myuser.department != 'NA':
            raise serializers.ValidationError('not correct match of designation and department')

        else:
            raise Exception("Not correct designation or department")


        return myuser




    def validate_email(self,email):
        try:
            MyUser.objects.get(email=email)
            raise serializers.ValidationError("Email already exists")
        except MyUser.DoesNotExist:
            return email

    def validate_first_name(self,firstname):
        if re.match('^[a-zA-Z]*$',firstname):
            return firstname
        else:
            raise serializers.ValidationError("Only alphabets are allowed")

    def validate_middle_name(self, middlename):
        if re.match('^[a-zA-Z]*$', middlename):
            return middlename
        else:
            raise serializers.ValidationError("Only alphabets are allowed")

    def validate_last_name(self, lastname):
        if re.match('^[a-zA-Z]*$', lastname):
            return lastname
        else:
            raise serializers.ValidationError("Only alphabets are allowed")

    def validate_contact_number(self,val):
        if val==None:
            pass
        else:
            if re.search('[+-]', val):
                raise serializers.ValidationError("'+', '-' are not allowed")
            elif re.search('^[0-9]+$') & len(val) == 10:
                return val
            else:
                raise serializers.ValidationError("Please enter a 10 digit number")

    def validate_salary(self,salary):
        if salary == None:
            pass
        else:
            salary = str(salary)
            if re.search('[+-]', salary):
                raise serializers.ValidationError("'+', '-' are not allowed")
            else:
                return salary

    def validate_designation(self, design):
        return design
        # if design==dept:
        #     raise serializers.ValidationError("designation and department both can not be NA")
        # elif design=='Client' and dept!='NA':
        #     raise serializers.ValidationError('not correct match of designation and department')
        # else:
        #     return design
    def validate_password(self,passw):
        passw=make_password(passw)
        return passw


# {
#     "email": "gdshg@gmail.com",
#     "first_name": "devesh",
#     "middle_name": "",
#     "last_name": "",
#     "password1": "a1password",
#     "password2": "a1password",
#     "contact": "9632587416",
#     "department": "Marketing",
#     "designation": "Manager",
#     "gender": "M"
#
# }




