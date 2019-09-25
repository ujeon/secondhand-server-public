from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [path("input/data/", views.input_bungae_data)]
