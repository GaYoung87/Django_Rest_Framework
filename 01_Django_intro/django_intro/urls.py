"""django_intro URL Configuration

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

# www.ssafy.com/admin/ (이 우리 홈페이지면 path 가 있기 때문에) -> 홈페이지로 들어올 수 있음
# www.ssafy.com/login/  -> path에 없음 -> 보여줄 수 있는 페이지 없음(404m). if 있다면, '로그인 페이지 관련 함수'로 이동해!
urlpatterns = [   # path('사용자가 접속하는 경로')
    # path('login/', 로그인 페이지 관련 함수),
    # 가장 위에 적은 것으로 감  ex. 밑에 index가 있어도 지금 index로 가게함.
    path('utilities/', include('utilities.urls')), 
    path('pages/', include('pages.urls')), 
    path('admin/', admin.site.urls),
]

