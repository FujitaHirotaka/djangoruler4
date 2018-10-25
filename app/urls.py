
from django.contrib import admin
from django.urls import path, include 
from . import views

app_name="app"
urlpatterns = [
    path('', views.main, name='main' ),
    path('ajax_api_projectmake', views.projectmake, name='projectmake'),
    path('ajax_api_projectselect', views.projectselect, name='projectselect'),
    path('ajax_api_projectreturn', views.projectreturn, name='projectreturn'),
    path('ajax_api_projectdelete', views.projectdelete, name='projectdelete'),
    path('ajax_api_appdetermine',  views.appdetermine, name='appdetermine'),
    path('ajax_api_appestablish',  views.app_establish, name='app_establish'),
]
