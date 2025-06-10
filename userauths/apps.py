from django.apps import AppConfig  # 导入 AppConfig，用于配置当前 Django 应用



# 定义一个配置类，表示 userauths 这个 Django 应用的配置
class UserauthsConfig(AppConfig):
    # 设置模型的默认主键类型为 BigAutoField（64位整型自增ID）
    default_auto_field = 'django.db.models.BigAutoField'

    # 指定这个配置类对应的应用名称，必须与目录名一致
    name = 'userauths'

