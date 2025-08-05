from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),

    # API
    path('send/', views.send, name='send'),
    path('clear/', views.clear, name='clear'),
    path('create/', views.create, name='create'),
    path('settings/', views.user_settings, name='settings'),

    # robots.txt and sitemap.xml
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
]