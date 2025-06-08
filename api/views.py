from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain a token pair with additional user information.
    """
    # 这句代码 不会在类定义时“执行”或调用序列化器，它只是 告诉 DRF 在调用这个视图时要使用哪个 Serializer 类。serializer_class 这个名字不是 Python 的保留字，
    # 但在 Django REST Framework（DRF）中，它是 “约定俗成” 的属性名，用于告诉视图用哪个序列化器（serializer）。
    serializer_class = api_serializer.MyTokenObtainPairSerializer