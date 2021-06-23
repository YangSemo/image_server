from rest_framework import serializers
from .models import UserStatus, CheckLog

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['id','user_id','pwd','email','name','now_inOut','time']

class CheckLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckLog
        fields = ['name','now_inOut','time']
