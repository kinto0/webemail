from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bad-email/', views.repeat_email, name='index'),
    path('bad-city/', views.invalid_city, name='index'),
    path('error/', views.error, name='index'),
    path('success/', views.success, name='index'),
]