from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from userauths.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义 Token 序列化器继承自TokenObtainPairSerializer
    用于在登录后生成自定义的 JWT 令牌，并附加额外字段（如用户名、邮箱、全名）
    """
    @classmethod
    def get_token(cls, user):
        # 调用父类的方法生成标准 token
        token = super().get_token(user)

        # 添加额外用户信息到 token，有助于前端显示
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册用的序列化器
    用于接收注册信息，并创建新用户。
    """

    # 密码字段，write_only 表示只用于输入不会被返回，validate_password 用于强度校验
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    # 确认密码字段，write_only
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        指定这个序列化器对应的模型是 User
        指定哪些字段需要序列化和反序列化
        """
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        """
        在调用 .is_valid() 时自动执行
        用于校验密码和确认密码是否一致，同时检查密码强度
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("两次输入的密码不一致")

        # 再次使用 Django 提供的密码强度验证
        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data):
        """
        创建并保存用户实例
        注意：这里并没有直接保存 username，而是从 email 自动生成用户名
        """
        user = User.objects.create(
            full_name=validated_data["username"],   # 暂存为 full_name
            email=validated_data["email"],
        )

        # 自动从 email 提取用户名
        email_username = user.email.split('@')[0]
        user.username = email_username

        # 设置密码（会自动哈希）
        user.set_password(validated_data['password'])

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    用于展示当前用户的基础信息，不包含密码
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'otp')


class ProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    用于处理 Profile 模型（用户扩展信息）
    """
    class Meta:
        model = Profile
        fields = "__all__"  # 所有字段都序列化
