from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.handle_user_signup),
    path("signin/", views.handle_user_signin),
    path("info/", views.handle_userinfo),
    path("favorite/", views.handle_user_favorite),
    path("auth/", views.check_user_auth),
    path("favorite/info/", views.handle_user_favorite_info),
]
