from django.urls import path

from . import views

urlpatterns = [
    path('', views.changehistory, name='change_history'),
]