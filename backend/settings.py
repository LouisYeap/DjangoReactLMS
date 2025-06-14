"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/

常见“约定大于配置”的 settings.py 变量（必须使用这些名字）
这些变量名是 Django 框架规定好的，必须用这些名称，否则不会生效：

变量名	说明
INSTALLED_APPS	注册所有的 Django app，决定哪些模块被加载。
MIDDLEWARE	定义中间件顺序，影响请求处理流程。
DATABASES	配置数据库连接信息。
TEMPLATES	模板系统配置（如引擎、路径、上下文处理器等）。
STATIC_URL	静态文件访问路径前缀（用于开发服务器）。
STATICFILES_DIRS	设置额外的静态文件目录。
STATIC_ROOT	collectstatic 命令收集文件到的目录。
MEDIA_URL	媒体文件访问路径前缀（用户上传内容）。
MEDIA_ROOT	媒体文件实际存储位置。
ROOT_URLCONF	指定 URL 配置模块（如 myproject.urls）。
WSGI_APPLICATION	指定 WSGI 网关应用模块路径。
ASGI_APPLICATION	指定 ASGI 网关应用模块路径（用于异步支持）。
AUTH_PASSWORD_VALIDATORS	密码强度校验器配置。
AUTH_USER_MODEL	自定义用户模型路径，必须写在应用加载之前。
LANGUAGE_CODE	默认语言。
TIME_ZONE	默认时区。
USE_I18N, USE_TZ	是否使用国际化、是否使用时区。
SECRET_KEY	用于加密的密钥，必须设置，且不能泄露。
DEBUG	开发模式设置。
ALLOWED_HOSTS	允许访问的域名/IP 白名单。
LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL	登录系统相关默认跳转地址。
EMAIL_BACKEND, EMAIL_HOST 等	邮件系统配置。
DEFAULT_AUTO_FIELD	新模型的默认主键类型（从 Django 3.2 起）。

"""

from pathlib import Path
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0s%$j30-d#oss9a$kqr0s&%3(600t%c^3b-pseo-@8@+s5bx=v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 美化 Django admin 界面的第三方应用
    'jazzmin',
    # Django 自带的管理后台
    'django.contrib.admin',
    # Django 内置的认证系统（用户和权限管理）
    'django.contrib.auth',
    # 支持 Django 内容类型系统（框架内部使用）
    'django.contrib.contenttypes',
    # 会话管理（支持用户登录状态保持）
    'django.contrib.sessions',
    # 消息框架，支持显示临时消息（成功、错误提示等）
    'django.contrib.messages',
    # 管理静态文件（CSS、JS、图片等）
    'django.contrib.staticfiles',

    # ----------------- 自定义应用 -----------------

    # 核心应用，项目自定义的主要逻辑模块
    'core',
    # 用户认证相关功能模块（注册、登录等）
    'userauths',
    # 提供 API 接口的应用（可能用 DRF 实现）
    'api',

    # ----------------- 第三方应用 -----------------

    # Django REST Framework，强大的REST API开发框架
    'rest_framework',
    # 简单 JWT 的 token 黑名单功能，用于管理JWT令牌失效
    'rest_framework_simplejwt.token_blacklist',
    # 处理跨域请求，允许不同域名前端访问后端API
    'corsheaders',
]


MIDDLEWARE = [
    # 安全中间件，增强应用安全性，如强制HTTPS、HSTS等
    'django.middleware.security.SecurityMiddleware',
    # 跨域资源共享中间件，允许指定域名跨域请求（需要安装 django-cors-headers）
    'corsheaders.middleware.CorsMiddleware',
    # 会话中间件，支持使用 session 存储用户数据
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 常用请求处理，自动添加斜杠重定向、处理HTTP头等
    'django.middleware.common.CommonMiddleware',
    # CSRF保护中间件，防止跨站请求伪造攻击，验证POST等请求的CSRF令牌
    'django.middleware.csrf.CsrfViewMiddleware',
    # 认证中间件，根据请求session添加用户认证信息（request.user）
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 消息中间件，用于临时存储提示消息（如成功/错误提示）在不同页面传递
    'django.contrib.messages.middleware.MessageMiddleware',
    # 点击劫持防护中间件，设置X-Frame-Options响应头，防止网页被iframe嵌入
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        # 指定模板引擎，这里使用 Django 自带的模板引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 模板文件搜索路径，告诉 Django 去 BASE_DIR/templates 文件夹找模板
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 是否自动搜索安装的 app 目录下的 templates 文件夹
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 让模板中可以访问 request 对象
                'django.template.context_processors.request',
                # 让模板中可以访问用户认证信息（user、permissions 等）
                'django.contrib.auth.context_processors.auth',
                # 让模板中可以显示消息框内容（如错误提示、成功提示）
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # 验证密码是否和用户的某些属性（用户名、邮箱等）过于相似，防止弱密码
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 验证密码的最小长度，默认最少8个字符，增强密码强度
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # 验证密码是否是常见密码（如123456、password等），防止易被猜测的密码
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # 验证密码是否全是数字，避免简单密码
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = BASE_DIR / 'templates'

MEDIA_URL = '/media/' 
# 127.0.0.1/media/avatar.png

MEDIA_ROOT = BASE_DIR / 'media'

# 用于用户权限验证的模型 规定要写在setting中，继承自AbstractUser类
AUTH_USER_MODEL= 'userauths.User'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    # 窗口标题（浏览器标签页显示的标题）
    # 如果缺省或为 None，则默认使用 admin site 的 site_title
    "site_title": "Library LMS",

    # 登录页面顶部标题（最多19个字符）
    # 如果缺省或为 None，则默认使用 admin site 的 site_header
    "site_header": "Library LMS",

    # 左上角品牌名称（最多19个字符）
    # 如果缺省或为 None，则默认使用 admin site 的 site_header
    "site_brand": "Desphixs LMS",

    # 网站 logo 图片路径，需放在静态文件目录中
    # 用于左上角品牌图标显示
    # "site_logo": "books/img/logo.png",

    # 登录页面的欢迎文字
    "welcome_sign": "Welcome to the library LMS",

    # 页脚版权信息
    "copyright": "Acme Library Ltd",

    # 是否显示侧边栏的界面自定义器（UI Customizer）
    "show_ui_builder": True,
}


# Configuration for the 'djangorestframework-simplejwt' package
SIMPLE_JWT = {
    # Access token 有效期，签发后15分钟内有效
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),

    # Refresh token 有效期，签发后50天内有效
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),

    # 使用refresh token换取新access token时，同时颁发新的refresh token
    'ROTATE_REFRESH_TOKENS': True,

    # 旋转refresh token后，旧的refresh token加入黑名单，防止重复使用
    'BLACKLIST_AFTER_ROTATION': True,

    # 是否在通过JWT认证时更新用户的 last_login 字段，False表示不更新
    'UPDATE_LAST_LOGIN': False,

    # 签名算法，这里使用HS256即HMAC SHA-256
    'ALGORITHM': 'HS256',

    # 对称加密不需要公钥，这里设置为None
    'VERIFYING_KEY': None,

    # 期望的受众，未设置则为None
    'AUDIENCE': None,

    # 发行者，未设置则为None
    'ISSUER': None,

    # JSON Web Key (JWK) 的URL，未设置则为None
    'JWK_URL': None,

    # 容忍时钟偏差时间，单位秒，默认0表示不容忍
    'LEEWAY': 0,

    # HTTP Authorization头中标识token类型的前缀，通常是 'Bearer'
    'AUTH_HEADER_TYPES': ('Bearer',),

    # HTTP头字段名，包含token的字段，默认HTTP_AUTHORIZATION
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    # 用户模型中用作用户唯一标识的字段名称
    'USER_ID_FIELD': 'id',

    # JWT中存储用户唯一标识的claim名称
    'USER_ID_CLAIM': 'user_id',

    # 判断用户是否通过token认证的规则函数路径
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    # 用于认证的token类型类，默认使用AccessToken
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    # JWT中标识token类型的claim名称
    'TOKEN_TYPE_CLAIM': 'token_type',

    # 根据token生成的用户类
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    # JWT唯一标识claim名称（JWT ID）
    'JTI_CLAIM': 'jti',

    # sliding token的刷新过期时间claim名称
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',

    # sliding token有效期，默认5分钟
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),

    # sliding token最大刷新期限，默认1天
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# 允许跨域请求
CORS_ALLOW_ALL_ORIGINS = True