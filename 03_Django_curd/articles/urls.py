from django.urls import path
from . import views


app_name = 'articles'
# /articles/ ___
urlpatterns = [
    path('', views.index, name='index'),  # 비워두면 articles/와 같은 것
    # path('new/', views.new, name='new'),  # articles에 있는 new
    path('create/', views.create, name='create'),

    # /articles/3/
    path('<int:article_pk>/', views.detail, name='detail'),
        # detail 우리는 이름만 보고 갈 것이므로 <int:article_pk>/ 가 <int:article_pk>/detail/ 로 바뀌어도 괜찮
    
    # /articles/4/delete/ -> 삭제를 하겠다
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/update/', views.update, name='update'),

    # /articles/3/comment
    path('<int:article_pk>/comments/', views.comments_create, name='comments_create'),

    # /articles/3/comments/2/delete  
    # url이 길어지면, name이 꼭 필요하게 됨
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]


# 2) 자원에 대한 행위는 HTTP Method(GET, POST, PUT, DELETE 등)로 표현
# get : 정보를 주세요라는 요청(가지고오다)
# post : 작성하라(등록해주세요)
# delete : 삭제
# put : 정보 수정
# html에서는 POST나 GET