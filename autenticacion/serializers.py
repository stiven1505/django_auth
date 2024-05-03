from rest_framework import serializers
from django.contrib.auth.models import User #modelo predeterminado de django para usuarios


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id','username','email','password']