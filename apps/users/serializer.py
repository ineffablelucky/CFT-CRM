from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re
from django.contrib.auth.hashers import make_password
from apps.users.models import MyUser



class MyUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=MyUser.objects.all())])
    password=serializers.CharField()

    class Meta:
        model = MyUser
        fields = (
            'email',
            'username',
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
        user=MyUser.objects.create(**validated_data)
        return user

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


