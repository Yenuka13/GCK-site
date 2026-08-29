from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events_list, name='events'),
    path('about/', views.about_view, name='about'),
]
