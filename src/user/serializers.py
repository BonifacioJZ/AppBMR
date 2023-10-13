#Python 
#Django
from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
#Local Import

User = get_user_model()

class UserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',)