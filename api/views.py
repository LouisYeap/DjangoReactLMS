from django.shortcuts import render
from api import serializer as api_serializer  # 导入序列化器模块并重命名为 api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView  # 引入 JWT 登录视图
from rest_framework import generics  # 引入泛型视图（如 CreateAPIView）
from rest_framework.permissions import AllowAny  # 引入权限类，允许所有用户访问

from userauths.models import User  # 导入用户模型

# Create your views here.  # 这是 Django 自动生成的注释，表示你可以在这里写视图逻辑


class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义 JWT 登录视图。
    继承自 SimpleJWT 提供的 TokenObtainPairView。
    """
    # 告诉 DRF 使用自定义的序列化器（MyTokenObtainPairSerializer）
    # 这个序列化器中添加了额外字段（如用户名、邮箱、全名等）
    serializer_class = api_serializer.MyTokenObtainPairSerializer

    # 注释说明：
    # serializer_class 不是 Python 关键字，但在 DRF 中是“约定俗成”的属性名，
    # 视图调用时会自动使用这里指定的序列化器来处理请求数据（如登录验证）。


class RegisterView(generics.CreateAPIView):
    """
    用户注册视图
    使用 DRF 提供的通用类视图 CreateAPIView 来处理 POST 注册请求
    """

    # 该视图操作的查询集（CreateAPIView 不直接使用，但是 DRF 的要求）
    queryset = User.objects.all()

    # 设置权限为允许任意用户访问（即使未登录也能注册）
    permission_classes = (AllowAny,)

    # 指定用于处理请求的序列化器
    serializer_class = api_serializer.RegisterSerializer
