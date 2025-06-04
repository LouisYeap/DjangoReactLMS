from typing import Iterable
from django.db import models
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    自定义用户模型，继承自 Django 的 AbstractUser
    
    Fields:
        username: 用户名（唯一），最大长度100
        email: 电子邮件地址（唯一）
        full_name: 完整姓名（唯一）
        otp: 一次性密码（唯一）
    """
    username = models.CharField(
        unique=True,  # 用户名必须唯一
        max_length=100  # 最大长度100字符
    )
    email = models.EmailField(unique=True)  # 电子邮件地址必须唯一
    full_name = models.CharField(
        unique=True,  # 完整姓名必须唯一
        max_length=100  # 最大长度100字符
    )
    otp = models.CharField(
        unique=True,  # 一次性密码必须唯一
        max_length=100  # 最大长度100字符
    )

    USERNAME_FIELD = "email"  # 使用电子邮件作为登录字段
    REQUIRED_FIELDS = ["username"]  # 注册时需要填写的字段

    def __str__(self):
        """返回用户的电子邮件地址作为字符串表示"""
        return self.email

    def save(self, *args, **kwargs):
        """
        重写保存方法，自动设置用户名和完整姓名
        
        1. 从电子邮件地址中提取用户名（@之前的部分）
        2. 如果完整姓名为空，则使用用户名
        3. 如果用户名为空，则使用电子邮件的用户名部分
        """
        email_username, full_name = self.email.split("@")
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    """
    用户个人资料模型
    
    Fields:
        user: 与用户模型一对一关联
        image: 用户头像图片
        full_name: 用户完整姓名
        country: 用户所在国家
        about: 用户个人简介
        date: 资料创建时间
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # 关联到自定义的用户模型
        on_delete=models.CASCADE,  # 如果用户被删除，则删除个人资料
        related_name='profile'     # 可以通过 user.profile 访问个人资料
    )
    image = models.FileField(
        upload_to="user_folder",  # 上传的文件保存在 user_folder 目录下
        default="default-user.png",  # 默认头像
        null=True, blank=True      # 可以为空
    )
    full_name = models.CharField(max_length=100)  # 用户完整姓名
    country = models.CharField(
        max_length=100,  # 国家名称
        null=True, blank=True  # 可以为空
    )
    about = models.TextField(
        null=True, blank=True  # 个人简介，可以为空
    )
    date = models.DateTimeField(auto_now_add=True)  # 创建时间，自动添加

    def __str__(self) -> str:
        """
        返回个人资料的字符串表示
        如果设置了完整姓名，返回完整姓名
        否则返回关联用户的完整姓名
        """
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)

    def save(self, *args, **kwargs):
        """
        重写保存方法
        如果完整姓名为空，则使用关联用户的完整姓名
        """
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.full_name
        super().save(*args, **kwargs)
