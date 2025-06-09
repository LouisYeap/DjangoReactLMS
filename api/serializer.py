import email
import re
from django.contrib.auth.password_validation import validate_password
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
        

class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    write_only=True: 表示该字段只用于输入（不会出现在响应数据中）。
    required=True: 必填项。
    Django 内置的 validate_password 方法进行密码强度校验（如长度、复杂度等）。
    """
    password = serializers.CharField(write_only=True, required=True,validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    """
    指定此序列化器操作的模型是 User。
    包含的字段有：
    username: 用户名
    email: 邮箱地址
    password: 密码
    password2: 确认密码
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    """
    这是自定义的验证逻辑，在调用 .is_valid() 时触发：
    检查两次密码是否一致：
    如果 password 和 password2 不一致，抛出 ValidationError 错误提示。
    使用 Django 内置密码策略验证密码强度：
    调用 validate_password() 对密码进行标准校验（例如：最小长度、不能太简单等）。
    最后返回清洗后的属性字典 attrs，供后续保存使用。
    """
    def validate(self, attrs):
        """
        验证密码和确认密码是否一致
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("两次输入的密码不一致")
        
        # 验证密码强度
        validate_password(attrs['password'])
        
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            full_name = validated_data["username"],
            email = validated_data["email"],
        )
        email_username = user.email.split('@')[0]
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()
        return user
    

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





