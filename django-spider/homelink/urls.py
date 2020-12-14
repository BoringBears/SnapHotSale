from django.urls import path
from . import views

app_name = 'homelink'

urlpatterns = [
    path('', views.house_index, name='house_index'),
    path('fetch/', views.house_fetch, name='house_fetch'),
    path('spider/', views.house_spider, name='house_spider'),
]