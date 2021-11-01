# review에서 articles로 보내라했기 때문에 articles에서도 urls.py가 있어야 에러가 안남. 
from django.urls import path
from . import views  # 현재 app에서 view를 가지고오겠다 -> .=현재 앱

app_name = 'articles'

urlpatterns = [
    # index:현재 있는 모든 아티클들을 보여줌
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),  # 여러 앱에서 create라는 함수가 있을 수 있는데, 이름을 지정하면 이름이 나올 때 가라!
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    # 선생님 코드
    # path('<int:article_pk>/comments/', views.comment_create, name='comment_create'),  article_pk번째 article에 comments를 생성하겠다.
    # 삭제 시에는 article_pk가 필요없을 수도 있지만, 상속성을 나타내기 위해서
    # path('<int:article_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:article_pk>/follow/<int:user_pk>/', views.follow, name='follow')
]
