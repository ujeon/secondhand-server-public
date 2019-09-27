from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.handle_user_signup),
    path("signin/", views.handle_user_signin),
]