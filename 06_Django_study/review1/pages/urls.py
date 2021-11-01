from django.urls import path
from . import views  # 현재 directory에서 views를 가지고온다.

# 특정 domain.com/pages/_____
urlpatterns = [
    path('greeting/<str:name>/', views.greeting),
    path('', views.index)  # 이미 /는 되어있기 때문에 path('/', views.index)가 아닌 path('', views.index)임
]
