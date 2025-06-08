from rest_framework import serializers
from userauths.models import User , Profile



class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'otp')




class ProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    """
    class Meta:
        model = Profile
        fields = "__all__"





