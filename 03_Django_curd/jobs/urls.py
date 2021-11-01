from django.urls import path
from . import views

app_name = 'jobs'
# /jobs/ ___
urlpatterns = [
    path('', views.name, name='name'),
    path('past_job/', views.past_job, name='past_job'),
]
