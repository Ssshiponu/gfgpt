from django.urls import path
from django.views.generic import TemplateView
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),

    # API
    path('send/', views.send, name='send'),
    path('clear/', views.clear, name='clear'),
    path('create/', views.create, name='create'),
    path('settings/', views.user_settings, name='settings'),

    # robots.txt and sitemap.xml
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
]