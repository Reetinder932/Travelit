from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
]
