from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ..users.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

