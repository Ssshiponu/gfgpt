from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('send/', views.send, name='send'),
    path('clear/', views.clear, name='clear'),
    path('create/', views.create, name='create')
]