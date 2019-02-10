from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bad-email/', views.repeat_email, name='bad email'),
    path('bad-city/', views.invalid_city, name='bad city'),
    path('error/', views.error, name='error'),
    path('success/', views.success, name='success'),
    path('send/', views.send, name='send'),
]