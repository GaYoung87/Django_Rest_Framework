from django.urls import path
from . import views

# /utilities/________ 로 표현됨 -> _____ 자리에 index/ 들어감
urlpatterns = [
    path('index/', views.index),
]
