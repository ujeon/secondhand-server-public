
from django.contrib import admin

from django.urls import path

from . import views

urlpatterns = [
    path("eachModelInfo/<str:brand>/<str:model>/info", views.handle_each_model_info)
]

