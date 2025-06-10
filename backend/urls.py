"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

from django.conf.urls.static import static
urlpatterns = [
    # 管理后台的 URL 路径，例如访问 http://127.0.0.1:8000/admin/ 会进入后台管理界面
    path('admin/', admin.site.urls),

    # 接口版本 v1 的 URL 路径，包含 api 应用下的所有 URL（api/urls.py 里定义的）
    path('api/v1/', include('api.urls')),
]


# 将媒体文件 URL（用户上传的内容）映射到对应的文件路径，开发环境中使用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 将静态文件 URL（如 CSS/JS）映射到对应的文件路径，开发环境中使用
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
