from typing import Iterable
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

"""
post_save 是 Django 提供的一个信号机制，用于在模型保存之后执行某些逻辑，常用于自动创建关联对象（如 Profile)、发送通知、记录日志等场景。无论是新建还是更新，只要是通过 Django ORM 的保存机制完成的保存操作，都会触发。
我认为就像是一个监听器
"""

class User(AbstractUser):
    
    """
    自定义用户模型，继承自 Django 的 AbstractUser
    
    Fields:
        username: 用户名(唯一)最大长度100
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
        max_length=100,  # 最大长度100字符
        null=True, 
        blank=True,
    )

    """
    
    解释：
    在 AbstractBaseUser 中，这两个字段定义如下（简化版）：
    class AbstractBaseUser(models.Model):
    USERNAME_FIELD = 'username'  # 默认使用 username 登录
    REQUIRED_FIELDS = ['email']  # 默认创建用户时需要 email
    因为 Django 在处理用户认证和创建时，会动态读取你自定义用户模型上的这些属性：
    当你用 authenticate(email='xxx', password='xxx') 登录时,Django 会去检查你的用户模型里的 USERNAME_FIELD 是什么，然后根据那个字段来查找用户。
    当你运行 createsuperuser 命令时,Django 会自动读取 REQUIRED_FIELDS 来决定还需要哪些额外字段。

    """
    USERNAME_FIELD = "email"  # 用户以后登录的时候，用的是 邮箱
    REQUIRED_FIELDS = ["username"]  # ：在你创建用户的时候（比如通过命令 python manage.py createsuperuser），除了 email 和 password，还必须输入 username。

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
        # 调用 Django 的 AbstractUser 类中的 save() 方法，找到 User 类的父类”（也就是 AbstractUser）并将原始传入的参数原样传递过去。
        super().save(*args, **kwargs)


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
        # 📌 举例：如果你的 app 名是 userauths，用户模型叫 User，那么 AUTH_USER_MODEL = 'userauths.User' 会在 settings.py 中配置。
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 当关联的 User 被删除时，该用户的 Profile 也会一并删除。这是数据库中的“级联删除”行为（Cascade delete）。但是删除 Profile 不会影响对应的 User。
        related_name='profile'     # 允许你从 User 对象反向访问对应的 Profile。my_profile = user.profile 如果不设置 related_name，默认会my_profile = user.profile_set.first() 反之也可以self.user.full_name
    )

    """
    settings.AUTH_USER_MODEL,为什么那么设置？
    无法灵活替换用户模型；
    如果你想换一个用户模型（比如换成 CustomUser),必须修改所有引用的地方；
    容易引起循环导入错误（尤其是在多个 app 都依赖 User 模型时）；
    而通过 settings.AUTH_USER_MODEL,你可以 在 settings 中配置一次，全局生效。
    """
    image = models.FileField(
        upload_to="user_folder",  # 上传的文件保存在 user_folder 路径
        default="default-user.png",  # 默认头像路径
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

# sender：发送信号的模型类（比如 User）！！！
def create_user_porfile(sender,instance,created,**kwargs):
    # “如果这是一个新创建的用户，那就给他创建一个关联的 Profile。”
    """
    创建一个新的 Profile 实例；
    将它的 user 字段设置为传入的 User 对象（即 instance）；
    保存到数据库中。
    """
    if created:
        Profile.objects.create(user =instance)

def save_user_profile(sender,instance,**kwargs):
    """
    你可以把它理解为：
    当你修改并保存用(User)的信息时，
    这个函数会“顺便”也保存用户的个人资料(Profile)。
    """
    instance.profile.save()

# post_save 是 Django 提供的一个 内置信号（built-in signal），它会在模型调用 .save() 方法之后自动触发。第一个参数相当于监听函数
post_save.connect(create_user_porfile,sender=User)
post_save.connect(save_user_profile,sender=User)