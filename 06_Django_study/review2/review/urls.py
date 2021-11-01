"""review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

# 사용자가 들어오는 경로를 계속 연결
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
                # urls.py끼리 mapping(urls를 다른 곳으로 넘겨주는 것)
    path('admin/', admin.site.urls),
]
