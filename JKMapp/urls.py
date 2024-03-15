from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('counter/', views.counter, name="counter"),
    path('test/', views.test, name="test"),
    path('upload_image/', views.upload_image, name="upload_image"),
    
    path('scanner/', views.scanner, name='scanner'),
    #path('success', success, name='success'),


]
