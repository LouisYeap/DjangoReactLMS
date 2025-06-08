from rest_framework import serializers
from userauths.models import User , Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义token序列化器
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token
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





