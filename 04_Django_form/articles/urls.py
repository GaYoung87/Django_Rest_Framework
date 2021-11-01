from django.urls import path
from . import views

app_name = 'articles'

# www.domain.com/articles/____
urlpatterns = [
    path('', views.index, name='index'),  # articles 앱에있는 index라는 이름으로 접근 가능
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
]
