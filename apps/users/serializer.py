from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
import re
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import Group


class MyUserSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=MyUser.objects.all())])
    password1=serializers.CharField()
    password2=serializers.CharField()
    first_name=serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    contact=serializers.IntegerField()

    designation_choices = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
    )

    department_choices = (
        ('HR', 'HR'),
        ('Marketing', 'Marketing'),
        ('Accounts', 'Accounts'),
        ('IT', 'IT'),
    )

    gender_choice = (
        ('M', 'M'),
        ('F', 'F'),
        ('Other', 'Other'),
    )
    department=serializers.ChoiceField(
        label='department',
        choices=department_choices
    )
    gender=serializers.ChoiceField(
        label='gender',
        choices=gender_choice
    )
    designation=serializers.ChoiceField(
        label='designation',
        choices=designation_choices
    )

    def create(self,validated_data):
        print('*******************')

        print(validated_data)
        validated_data.pop('password1')
        validated_data.pop('password2')

        print(validated_data,"filtered")

        myuser=MyUser(**validated_data)
        myuser.username=myuser.email.split('@')[0]
        myuser.save()



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

    def validate(self, data):
        print(type(data))
        print(data)
        passwd1=data.get('password1')
        print(passwd1,'%%%%%%%%%%%%%%%%')
        passwd2=data.get('password2')
        print(passwd2,'$$$$$$$$$$$$$$$')
        if not data.get('password1') or not data.get('password2'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError("Those passwords don't match.")

        passw=data.get('password1')
        data['password']=make_password(passw)

        print(data)
        # data.pop('password1')
        # data.pop('password2')
        print(data,'~!@#$%^&*()')
        return data

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


class UserLogin(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()



    def validate(self,data):
        print(data)
        username1=data.get('username')
        password1=data.get('password')
        password=make_password(password1)
        print(username1,password1)
        user=authenticate(username=username1,password=password1)
        print(user,"@@@@@@@@@@@@@@")
        print(user.id)
        if user:
            # print("Hello World")
            token=Token.objects.create(user_id=user.id)
            print(token)


            data['Token']=token.key
            print(data)
            return data

        return serializers.ValidationError("Wrong credentials for access")





