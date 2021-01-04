from django.urls import path
from . import views

app_name = 'showdeals'

urlpatterns = [
    path('', views.show_deals, name='show_deals'),
]
