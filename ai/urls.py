from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('recognize', views.recognize.as_view(), name='recognize'),
    path('form_recognize', views.form_recognize_ajax, name='form_recognize_ajax'),
]