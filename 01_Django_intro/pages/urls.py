from django.urls import path
from . import views   # .은 현재 경로

urlpatterns = [
    path('num/pull/', views.pull),
    path('num/push/', views.push),
    path('static_css_example/', views.static_css_example),
    path('static_example/', views.static_example),
    path('lotto_result/', views.lotto_result),
    path('lotto_pick/', views.lotto_pick),
    path('result/', views.result),
    path('search/', views.search),
    path('lotto/', views.lotto),
    path('isitbirthday/', views.isitbirthday),
    path('template_language/', views.template_language),
    path('times/<int:num1>/<int:num2>/', views.times),
    path('greeting/<str:name>/', views.greeting),
    path('image/', views.image),
    path('dinner/<str:name>/', views.dinner),
    path('introduce/', views.introduce),
    path('index/', views.index),
]
