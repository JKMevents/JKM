from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('counter/', views.counter, name="counter"),
    path('test/', views.test, name="test"),
    path('tickets/', views.tickets, name="tickets")
]
