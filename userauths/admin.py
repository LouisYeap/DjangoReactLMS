from django.contrib import admin
from userauths.models import User,Profile
# Register your models here.

# 定义一个自定义的后台管理类，用于美化或增强 Profile 模型在后台的显示方式
class ProfileAdmin(admin.ModelAdmin):
    # 指定在后台“列表页”显示的字段
    list_display = ['user', 'full_name', 'date']  # 显示用户名、全名、创建时间等字段


# 将自定义用户模型 User 注册到后台，使用默认展示方式
admin.site.register(User)

# 将 Profile 模型注册到后台，并使用自定义的 ProfileAdmin 管理类来控制显示样式
admin.site.register(Profile, ProfileAdmin)
