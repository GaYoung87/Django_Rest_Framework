from django.urls import path
from . import views

app_name = 'accounts'

# urlpatterns가 있어야 error가 안남 -> list 우선적으로 만들자!
urlpatterns = [
    # 회원가입 url 
    path('signup/', views.signup, name='signup'),
    # 로그인 url
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # 회원탈퇴
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
        # 로그인이 되어있기때문에, user의 정보를 id값으로 판별할 필요가 없음 -> pk값 필요없음
    path('password/', views.password, name='password'),
]
